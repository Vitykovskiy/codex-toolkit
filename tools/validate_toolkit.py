"""Offline, read-only structural checks (Python 3.11+, PyYAML).

Markdown support is deliberately bounded: inline links/images and reference-style
links, relative destinations, optional titles and percent escapes. Fenced/indented
code, inline code examples, URLs, anchors and destinations with <parameters>,
{parameters} or $VARIABLES are excluded. Backticked references/... are checked
only in a skill's instructions. Profiles use explicit relative Markdown links. Nested
parentheses/labels, HTML links and anchor existence need manual review. This is
not a full Markdown parser, nor a proof of dependency semantics or acyclicity.
Explicit skill checks recognize $codex-name outside inline code and explicitly
marked skill/скилл/навык `codex-name` mentions, not arbitrary codex-* words.
Executable metadata prompts are checked including their inline tokens. Empty legacy directories are not skills.
Historical docs/refactoring-map.md, evals/README.md and evals/cases.jsonl are excluded from mandatory active content checks.
Report YAML examples are checked structurally; prose consistency needs review.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess
import sys
import tomllib
from urllib.parse import unquote, urlsplit

import yaml

SKILLS = frozenset('codex-' + name for name in (
    'communication-pact', 'development-pact', 'documentation-pact',
    'orchestration-pact', 'ui-analysis-pact', 'web-implementation',
    'debugging', 'web-verification', 'security-review',
    'long-orchestration', 'product-quality'))
ROLES = frozenset(('scout', 'analyst', 'analyst_standard', 'architect', 'decomposer', 'developer',
                   'mechanical', 'reviewer', 'integration_reviewer', 'quality_owner'))
PROFILE_FILES = {
    **{role.replace('_', '-') + '.toml': role for role in ROLES},
    'architect-astra.toml': 'architect_astra',
    'quality-owner-astra.toml': 'quality_owner_astra',
    'analyst-standard.toml': 'analyst_standard',
}
RUNTIME_DIRS = frozenset(('runtime', 'traces', 'cache', '.cache', '__pycache__',
                          '.venv', 'venv', 'env', '.pytest_cache', 'screenshots'))
RUNTIME_PROBES = [name + '/probe.txt' for name in sorted(RUNTIME_DIRS)] + [
    '.codex/tmp/probe.txt', 'evals/runtime/probe.txt', 'evals/traces/probe.txt',
    'evals/screenshots/probe.txt', 'tests/__pycache__/probe.pyc', '.env']
REPORT_KEYS = {'status', 'changed_files', 'checks', 'result', 'risks', 'next_action'}
STATUSES = {'completed', 'approved', 'blocked', 'split_required', 'baseline_failure', 'paused'}
ENVELOPE_KEYS = {'status', 'artifact', 'assignment_id', 'attempt', 'profile', 'accepts',
                 'finding_id', 'progress', 'no_progress', 'next_transition'}


class UniqueLoader(yaml.SafeLoader):
    """Reject duplicate mapping keys before SafeLoader can overwrite them."""


def unique_mapping(loader, node, deep=False):
    loader.flatten_mapping(node)
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in result
        except TypeError as error:
            raise yaml.constructor.ConstructorError(None, None, 'unhashable key', key_node.start_mark) from error
        if duplicate:
            raise yaml.constructor.ConstructorError(None, None, f'duplicate key: {key}', key_node.start_mark)
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def canonical_accepts(accepts):
    """Render report accepts in the canonical compact envelope representation."""
    if accepts is None:
        return None
    if not isinstance(accepts, dict) or type(accepts.get('assignment_id')) is not str or not accepts['assignment_id'].strip() or type(accepts.get('attempt')) is not int or accepts['attempt'] < 1 or type(accepts.get('goal_version')) is not int:
        raise ValueError('invalid report accepts')
    snapshot = accepts.get('snapshot')
    if snapshot is not None and (type(snapshot) is not str or not snapshot.strip()):
        raise ValueError('invalid accepts snapshot')
    return f"{accepts['assignment_id']}/{accepts['attempt']}" + (f"@{snapshot}" if snapshot else '')


def prose_lines(text):
    """Keep original line numbers while excluding fenced and indented examples."""
    fence = None
    for number, line in enumerate(text.splitlines(), 1):
        marker = re.match(r'^\s{0,3}(`{3,}|~{3,})', line)
        if marker:
            token = marker[1]
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None and not line.startswith(('    ', '\t')):
            yield number, line


class Validator:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.errors = []
        self.warnings = []

    def error(self, path, reason, line=1):
        if isinstance(path, tuple):
            path, line = path
        self.errors.append(f'{path}:{line}: {reason}')

    def read(self, path):
        try:
            return path.read_text(encoding='utf-8')
        except (OSError, UnicodeError) as error:
            self.error(path, str(error))
            return ''

    def parse_yaml(self, path, text, offset=0):
        try:
            return yaml.load(text, Loader=UniqueLoader)
        except (yaml.YAMLError, RecursionError) as error:
            mark = getattr(error, 'problem_mark', None)
            self.error(path, getattr(error, 'problem', None) or str(error).splitlines()[0], offset + (mark.line + 1 if mark else 1))
            return None

    def fields(self, path, value, schema, label=''):
        if not isinstance(value, dict):
            self.error(path, f'{label or "document"} must be a mapping')
            return False
        valid = True
        for name, kind in schema.items():
            item = value.get(name)
            if type(item) is not kind or (kind is str and not item.strip()):
                self.error(path, f'{label}{name} must be {kind.__name__}' + (' (nonempty)' if kind is str else ''))
                valid = False
        return valid

    def budget(self, path, text, limit):
        count = len(text.split())
        if count > limit:
            self.warnings.append(f'{path}:1: {count} words exceeds advisory budget {limit}; explain responsibility in review')

    def local_link(self, path, target, line=1, base=None):
        target = target.strip()
        if target.startswith('<') and target.endswith('>'):
            target = target[1:-1]
        if not target or re.search(r'[{}<>$]', target) or target.startswith(('#', '//')):
            return
        try:
            parsed = urlsplit(target)
        except ValueError as error:
            self.error(path, f'invalid link target: {error}', line)
            return
        if parsed.scheme:
            return
        relative = unquote(parsed.path)
        if relative and not ((base or path.parent) / relative).exists():
            self.error(path, f'local target does not exist: {target}', line)

    def skill_references(self, path, text, line=1):
        for skill in re.findall(r'\$(codex-[\w-]+)', text):
            if skill not in SKILLS:
                self.error(path, f'unknown explicit skill: {skill}', line)

    def links(self, path, text, owner=None):
        lines = list(prose_lines(text))
        definitions = {}
        for number, line in lines:
            match = re.match(r'^\s{0,3}\[([^]]+)\]:\s*(<[^>]+>|\S+)', line)
            if match:
                definitions[match[1].casefold()] = match[2]
                self.local_link(path, match[2], number)
        for number, line in lines:
            if owner:
                for match in re.finditer(r'`(references/[^`]+)`', line):
                    self.local_link(path, match[1], number, owner)
            plain = re.sub(r'`+[^`]*`+', '', line)
            self.skill_references(path, plain, number)
            explicit_skills = re.findall(r'(?:skill|скилл|навык)\s+`\$?(codex-[\w-]+)`', line, re.I)
            for skill in explicit_skills:
                if skill not in SKILLS:
                    self.error(path, f'unknown explicit skill: {skill}', number)
            for role in re.findall(r'(?:role|роль|роли)\s*[:=]?\s*`([^`\s]+)`', line, re.I):
                if role not in ROLES:
                    self.error(path, f'unknown explicit role: {role}', number)
            for match in re.finditer(r'!?\[[^]\n]*\]\(\s*(<[^>]+>|[^\s)]+)(?:\s+["\'][^\n]*?["\'])?\s*\)', plain):
                self.local_link(path, match[1], number)
            for match in re.finditer(r'\[([^]\n]+)\]\[([^]\n]*)\]', plain):
                label = (match[2] or match[1]).casefold()
                if label not in definitions:
                    self.error(path, f'undefined reference link: {label}', number)

    def skill(self, directory):
        path = directory / 'SKILL.md'
        text = self.read(path)
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', text, re.S)
        if not match:
            self.error(path, 'missing YAML front matter')
            return None
        data = self.parse_yaml(path, match[1], 1)
        name = None
        if self.fields(path, data, {'name': str, 'description': str}):
            name = data['name']
            if name != directory.name:
                self.error(path, 'skill name must match directory')
        limit = 250 if directory.name == 'codex-communication-pact' else 1100 if directory.name == 'codex-orchestration-pact' else 700
        self.budget(path, text[match.end():], limit)
        metadata = directory / 'agents/openai.yaml'
        data = self.parse_yaml(metadata, self.read(metadata))
        if not self.fields(metadata, data, {'interface': dict, 'policy': dict}):
            return name
        interface = data['interface']
        if self.fields(metadata, interface, {'display_name': str, 'short_description': str, 'default_prompt': str}, 'interface.'):
            if not re.search(r'\$' + re.escape(directory.name) + r'(?![\w-])', interface['default_prompt']):
                self.error(metadata, 'default_prompt must contain its own $skill-name')
            self.skill_references(metadata, interface['default_prompt'])
        policy = data['policy']
        if self.fields(metadata, policy, {'allow_implicit_invocation': bool}, 'policy.'):
            if policy['allow_implicit_invocation'] != (directory.name != 'codex-communication-pact'):
                self.error(metadata, 'incorrect implicit invocation policy for skill')
        for key in ('icon_small', 'icon_large', 'brand_logo'):
            if key in interface:
                if type(interface[key]) is not str:
                    self.error(metadata, f'interface.{key} must be str')
                else:
                    self.local_link(metadata, interface[key])
        return name

    def profile(self, path):
        text = self.read(path)
        try:
            data = tomllib.loads(text)
        except tomllib.TOMLDecodeError as error:
            self.error(path, str(error), getattr(error, 'lineno', 1))
            return None
        if not self.fields(path, data, {'name': str, 'description': str, 'developer_instructions': str,
                                        'model': str, 'model_reasoning_effort': str}):
            return None
        if data['name'] != PROFILE_FILES.get(path.name):
            self.error(path, 'profile name must match role (integration_reviewer uses underscore)')
        self.budget(path, data['developer_instructions'], 250)
        if data.get('sandbox_mode') != 'workspace-write':
            self.error(path, 'sandbox_mode must be workspace-write')
        self.links(path, text)
        return data['name']

    def report(self, path, text):
        count = 0
        for match in re.finditer(r'^```ya?ml\s*\n(.*?)^```\s*$', text, re.M | re.S):
            if not re.search(r'^changed_files:', match[1], re.M):
                continue
            count += 1
            data = self.parse_yaml(path, match[1], text[:match.start()].count('\n') + 1)
            if not self.fields(path, data, {'status': str, 'changed_files': list, 'checks': list, 'result': dict, 'risks': list}):
                continue
            if set(data) != REPORT_KEYS or data['status'] not in STATUSES:
                self.error(path, 'report must have six canonical keys and valid status')
            if data.get('next_action') is not None and type(data['next_action']) is not str:
                self.error(path, 'report next_action must be str or null')
            if not all(type(item) is str for item in data['changed_files']):
                self.error(path, 'changed_files items must be str')
            if type(data['result'].get('evidence')) is not list:
                self.error(path, 'result.evidence must be list')
            if type(data['result'].get('findings')) is not list:
                self.error(path, 'result.findings must be list')
            for check in data['checks']:
                if not isinstance(check, dict) or type(check.get('command')) is not str or not check['command'].strip():
                    self.error(path, 'check requires string command')
                    continue
                if 'result' not in check:
                    self.error(path, 'check requires result key (explicit null when unexecuted)')
                execution = check.get('execution_status')
                if type(execution) is not str or execution not in {'checked', 'not_run', 'unable_to_verify'}:
                    self.error(path, 'invalid execution_status')
                    continue
                if execution == 'checked' and check.get('result') not in ('passed', 'failed'):
                    self.error(path, 'checked result must be passed or failed')
                if execution in {'not_run', 'unable_to_verify'} and (check.get('result') is not None or not isinstance(check.get('reason'), str) or not check['reason'].strip()):
                    self.error(path, 'unexecuted check requires null result and reason')
        return count

    def strings(self, path, value, label):
        if type(value) is not list or any(type(x) is not str or not x.strip() for x in value):
            self.error(path, f'{label} must be a list of nonblank strings')
            return False
        return True

    def choice(self, path, value, choices, label):
        if type(value) is not str or value not in choices:
            self.error(path, f'invalid {label}')

    def integer(self, path, value, label, minimum=0):
        if type(value) is not int or value < minimum:
            self.error(path, f'{label} must be an integer >= {minimum}')

    def task_path(self, path, value, task_root=None, nullable=False, directory=False, future=False):
        """Templates check syntax; concrete instances additionally resolve containment."""
        if value is None and nullable:
            return None
        if type(value) is not str or not value.strip():
            self.error(path, 'task path must be a nonblank relative string')
            return None
        relative = Path(value)
        if relative.is_absolute() or '..' in relative.parts or '\\' in value:
            self.error(path, f'unsafe task path: {value}')
            return None
        if task_root is None:
            return None
        try:
            root = Path(task_root).resolve(strict=True)
            target = (root / relative).resolve(strict=not future)
            target.relative_to(root)
            if future:
                if not target.parent.is_dir():
                    raise ValueError('missing parent')
            elif not (target.is_dir() if directory else target.is_file()):
                raise ValueError('expected directory' if directory else 'expected file')
            return target
        except (OSError, RuntimeError, ValueError) as error:
            self.error(path, f'unsafe or missing task path {value}: {error}')
            return None

    def task_artifacts(self, task_root, manifest_name):
        """Validate explicit task artifact correlations; never infer Markdown workflow."""
        root = Path(task_root).resolve()
        manifest_path = self.task_path(root / manifest_name, manifest_name, root)
        if manifest_path is None:
            return {'status': 'not_verified', 'errors': self.errors}
        manifest = self.parse_yaml(manifest_path, self.read(manifest_path))
        if not self.fields(manifest_path, manifest, {'version': int, 'reports': list}):
            return {'status': 'not_verified', 'errors': self.errors}
        if manifest['version'] != 1:
            self.error(manifest_path, 'unsupported task manifest version')
        owners = manifest.get('owners')
        if owners is not None and (not isinstance(owners, dict) or any(type(key) is not str or type(value) is not str for key, value in owners.items())):
            self.error(manifest_path, 'owners must map assignment IDs to owner IDs')
            owners = None
        not_verified = owners is None
        for item in manifest['reports']:
            if not self.fields(manifest_path, item, {'path': str, 'assignment_id': str, 'attempt': int, 'goal_version': int, 'next_transition': str}):
                continue
            report_path = self.task_path(manifest_path, item['path'], root)
            transition = self.task_path(manifest_path, item['next_transition'], root)
            if report_path is None or transition is None:
                continue
            report = self.parse_yaml(report_path, self.read(report_path))
            if not self.fields(report_path, report, {'status': str, 'changed_files': list, 'checks': list, 'result': dict, 'risks': list}):
                continue
            if set(report) != REPORT_KEYS or report['status'] not in STATUSES:
                self.error(report_path, 'report must have six canonical keys and valid status')
                continue
            assignment = report['result'].get('assignment')
            if not isinstance(assignment, dict) or any(assignment.get(name) != item[key] for name, key in (('id', 'assignment_id'), ('attempt', 'attempt'), ('goal_version', 'goal_version'))):
                self.error(report_path, 'report assignment does not match explicit expectation')
            if report.get('next_action') != item['next_transition']:
                self.error(report_path, 'report next_action is stale or differs from explicit transition')
            accepts = report['result'].get('accepts')
            if report['status'] == 'approved':
                if not isinstance(accepts, dict) or not all(name in accepts for name in ('assignment_id', 'attempt', 'goal_version')):
                    self.error(report_path, 'approved report requires accepts correlation')
                else:
                    expected_accepts = item.get('accepts')
                    if expected_accepts is None:
                        not_verified = True
                    elif not isinstance(expected_accepts, dict) or any(expected_accepts.get(name) != accepts.get(name) for name in ('assignment_id', 'attempt', 'goal_version')):
                        self.error(report_path, 'accepts does not match explicit accepted-result expectation')
                    if owners is not None:
                        current = owners.get(item['assignment_id'])
                        accepted = owners.get(accepts['assignment_id'])
                        if current is None or accepted is None:
                            not_verified = True
                        elif current == accepted:
                            self.error(report_path, 'self-approval in supplied owner map')
            elif accepts is not None:
                self.error(report_path, 'non-approved report must have null accepts')
            envelope_name = item.get('envelope')
            if envelope_name is None:
                continue
            envelope_path = self.task_path(manifest_path, envelope_name, root)
            if envelope_path is None:
                continue
            envelope = self.parse_yaml(envelope_path, self.read(envelope_path))
            if not isinstance(envelope, dict) or set(envelope) != ENVELOPE_KEYS:
                self.error(envelope_path, 'invalid envelope keys')
                continue
            if envelope.get('status') not in STATUSES or type(envelope.get('artifact')) is not str or type(envelope.get('assignment_id')) is not str or type(envelope.get('attempt')) is not int or envelope['attempt'] < 1 or type(envelope.get('profile')) is not str or (envelope.get('next_transition') is not None and type(envelope.get('next_transition')) is not str):
                self.error(envelope_path, 'invalid envelope field types')
            finding_id = envelope.get('finding_id')
            progress = envelope.get('progress')
            no_progress = envelope.get('no_progress')
            if finding_id is None:
                if progress is not None or no_progress is not None:
                    self.error(envelope_path, 'non-blocker envelope must use null progress and no_progress')
            elif type(finding_id) is not str or not finding_id.strip() or progress not in {'confirmed', 'none', 'unknown'}:
                self.error(envelope_path, 'blocker envelope requires finding_id and valid progress')
            elif progress in {'none', 'unknown'}:
                if not isinstance(no_progress, dict) or any(type(no_progress.get(key)) is not str or not no_progress[key].strip() for key in ('missing_input', 'next_check')):
                    self.error(envelope_path, 'none or unknown progress requires nonblank no_progress fields')
            elif no_progress is not None:
                self.error(envelope_path, 'confirmed progress must use null no_progress')
            if envelope.get('artifact') != item['path'] or envelope.get('assignment_id') != item['assignment_id'] or envelope.get('attempt') != item['attempt'] or envelope.get('next_transition') != item['next_transition']:
                self.error(envelope_path, 'envelope is stale or does not correlate with report expectation')
            try:
                expected_envelope_accepts = canonical_accepts(accepts)
            except ValueError as error:
                self.error(report_path, str(error))
                expected_envelope_accepts = None
            if envelope.get('status') != report.get('status') or envelope.get('accepts') != expected_envelope_accepts:
                self.error(envelope_path, 'envelope does not correlate with report')
        return {'status': 'not_verified' if not_verified else 'checked', 'errors': self.errors}

    def quality(self, path, data, task_root=None):
        schema = {'version': int, 'campaign_id': str, 'iteration': int, 'permission': str, 'unresolved_questions': list, 'next_step': str}
        if not self.fields(path, data, schema):
            return
        self.integer(path, data['iteration'], 'iteration')
        if data['version'] != 1:
            self.error(path, 'unsupported quality version')
        self.choice(path, data['permission'], {'observe_only', 'improve'}, 'quality permission')
        if 'expected' not in data or (data['expected'] is not None and (type(data['expected']) is not str or not data['expected'].strip())):
            self.error(path, 'expected must be nonblank string or null')
        self.strings(path, data['unresolved_questions'], 'unresolved_questions')
        for key in ('inventory_path', 'findings_path', 'current_batch_path', 'decisions_path', 'evidence_path'):
            self.task_path(path, data.get(key), task_root, directory=key == 'evidence_path')

    def finding(self, path, data, concrete=False):
        if not self.fields(path, data, {'id': str, 'surface': str, 'scenario': str, 'state': str, 'observed': str, 'evidence': list, 'classification': str, 'confidence': str, 'decision_required': bool, 'recommended_next_role': str}):
            return
        self.choice(path, data['classification'], {'defect', 'stale_design', 'missing_decision', 'unknown'}, 'classification')
        self.choice(path, data['confidence'], {'high', 'medium', 'low'}, 'confidence')
        self.choice(path, data['recommended_next_role'], ROLES, 'recommended_next_role')
        if 'severity' not in data or data['severity'] is not None and (type(data['severity']) is not str or data['severity'] not in {'blocker', 'major', 'minor'}):
            self.error(path, 'invalid severity')
        for key in ('expected', 'expected_source'):
            if key not in data or data[key] is not None and (type(data[key]) is not str or not data[key].strip()):
                self.error(path, f'{key} must be nonblank string or null')
        if data['classification'] == 'defect' and (not data.get('expected') or not data.get('expected_source') or not data['evidence']):
            self.error(path, 'defect requires expected/source/evidence')
        if concrete and not data['evidence']:
            self.error(path, 'concrete finding requires evidence')
        if any(not ((type(item) is str and item.strip()) or (type(item) is dict and item)) for item in data['evidence']):
            self.error(path, 'finding evidence entries must describe provenance')
        viewport = data.get('viewport')
        if 'viewport' not in data:
            self.error(path, 'missing viewport')
        if viewport is not None:
            if self.fields(path, viewport, {'width': int, 'height': int}):
                for key in ('width', 'height'):
                    self.integer(path, viewport[key], key, 1)
                if 'dpr' not in viewport or viewport['dpr'] is not None and (type(viewport['dpr']) not in (int, float) or viewport['dpr'] <= 0):
                    self.error(path, 'dpr must be positive number or null')

    def findings(self, path, data, concrete=False):
        if type(data) is not list:
            self.error(path, 'findings registry must be a list')
            return
        seen = set()
        for finding in data:
            self.finding(path, finding, concrete)
            if isinstance(finding, dict) and type(finding.get('id')) is str:
                if finding['id'] in seen:
                    self.error(path, 'duplicate finding ID')
                seen.add(finding['id'])

    def templates(self):
        for name, method in (
            ('codex-product-quality/references/templates/quality-state.yaml', self.quality),
        ):
            path = self.root / 'skills' / name
            method(path, self.parse_yaml(path, self.read(path)))
        for name, methods in (
            ('codex-product-quality/references/finding-schema.md', (self.finding,)),
        ):
            path = self.root / 'skills' / name
            blocks = re.findall(r'^```yaml\s*\n(.*?)^```', self.read(path), re.M | re.S)
            if len(blocks) != len(methods):
                self.error(path, 'missing or extra canonical YAML schema blocks')
            for block, method in zip(blocks, methods):
                method(path, self.parse_yaml(path, block))

    def runtime(self):
        # Git is queried only; no files, index entries or configuration are changed.
        try:
            inside = subprocess.run(['git', '-C', str(self.root), 'rev-parse', '--show-toplevel'], capture_output=True, text=True)
            if inside.returncode or Path(inside.stdout.strip()).resolve() != self.root:
                self.error(self.root, 'runtime tracking checks require root of a Git repository')
                return
            ignored = subprocess.run(['git', '-C', str(self.root), 'check-ignore', '--no-index', '--stdin'], input='\n'.join(RUNTIME_PROBES) + '\n', capture_output=True, text=True)
            if ignored.returncode not in (0, 1):
                self.error(self.root / '.gitignore', ignored.stderr.strip())
            for probe in sorted(set(RUNTIME_PROBES) - set(ignored.stdout.splitlines())):
                self.error(self.root / '.gitignore', f'runtime path is not ignored: {probe}')
            tracked = subprocess.run(['git', '-C', str(self.root), 'ls-files', '-z'], capture_output=True, text=True, check=True)
            for name in filter(None, tracked.stdout.split('\0')):
                parts = Path(name).parts
                if RUNTIME_DIRS.intersection(parts[:-1]) or name.startswith('.codex/tmp/') or (Path(name).name.startswith('.env') and Path(name).name != '.env.example') or name.endswith(('.pyc', '.tmp')):
                    self.error(self.root / name, 'runtime artifact is tracked')
        except (OSError, subprocess.CalledProcessError) as error:
            self.error(self.root, f'cannot verify runtime tracking: {error}')

    def run(self):
        directories = sorted(
            path for path in (self.root / 'skills').glob('*')
            if path.is_dir() and (path.name in SKILLS or any(item.is_file() for item in path.rglob('*')))
        )
        actual = {path.name for path in directories}
        if actual != SKILLS:
            self.error(self.root / 'skills', f'skill set mismatch; missing={sorted(SKILLS - actual)}, extra={sorted(actual - SKILLS)}')
        names = [self.skill(path) for path in directories]
        profiles = sorted((self.root / 'agents').glob('*.toml'))
        roles = [self.profile(path) for path in profiles]
        for values, path in ((names, self.root / 'skills'), (roles, self.root / 'agents')):
            known = [value for value in values if value is not None]
            if len(known) != len(set(known)):
                self.error(path, 'duplicate name')
        markdown = list((self.root / 'skills').rglob('*.md')) + list((self.root / 'docs').rglob('*.md')) + list((self.root / 'evals').glob('*.md'))
        markdown += [path for path in (self.root / 'README.md', self.root / 'AGENTS.md') if path.exists()]
        report_path = self.root / 'skills/codex-orchestration-pact/references/templates/report.md'
        if not report_path.is_file():
            self.error(report_path, 'missing canonical report template')
        for path in sorted(markdown):
            if path in {self.root / 'docs/refactoring-map.md', self.root / 'evals/README.md'}:
                continue
            text = self.read(path)
            relative = path.relative_to(self.root)
            owner = self.root / 'skills' / relative.parts[1] if relative.parts[0] == 'skills' else None
            self.links(path, text, owner)
            reports = self.report(path, text)
            if path == report_path and not reports:
                self.error(path, 'missing canonical YAML report example')
        self.templates()
        self.runtime()
        return not self.errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    parser.add_argument('--task-root', type=Path)
    parser.add_argument('--manifest')
    args = parser.parse_args(argv)
    if (args.task_root is None) != (args.manifest is None):
        parser.error('--task-root and --manifest must be supplied together')
    if args.task_root is not None:
        validator = Validator(args.task_root)
        result = validator.task_artifacts(args.task_root, args.manifest)
        for message in validator.errors:
            print(message, file=sys.stderr)
        print(f"Task artifact validation: {result['status']}; {len(validator.errors)} errors. Semantic approval and runtime sender remain unverified.")
        return 0 if not validator.errors else 1
    validator = Validator(args.root)
    passed = validator.run()
    for message in validator.errors:
        print(message, file=sys.stderr)
    for message in validator.warnings:
        print('warning: ' + message, file=sys.stderr)
    print(f'Structural validation: {len(validator.errors)} errors, {len(validator.warnings)} warnings. Semantic consistency and Codex behavior require separate verification.')
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
