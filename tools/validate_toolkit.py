"""Offline, read-only structural checks (Python 3.11+, PyYAML).

Markdown support is deliberately bounded: inline links/images and reference-style
links, relative destinations, optional titles and percent escapes. Fenced/indented
code, inline code examples, URLs, anchors and destinations with <parameters>,
{parameters} or $VARIABLES are excluded. Backticked references/... are checked
only in a skill's instructions (or a profile naming the owning skill). Nested
parentheses/labels, HTML links and anchor existence need manual review. This is
not a full Markdown parser, nor a proof of dependency semantics or acyclicity.
Explicit skill checks recognize $codex-name outside inline code and explicitly
marked skill/скилл/навык `codex-name` mentions, not arbitrary codex-* words.
Executable metadata prompts are checked including their inline tokens. Empty legacy directories are not skills.
Historical docs/refactoring-map.md is excluded from active-instruction checks.
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
    'debugging', 'web-verification', 'security-review'))
ROLES = frozenset(('scout', 'analyst', 'architect', 'decomposer', 'developer',
                   'mechanical', 'reviewer', 'integration_reviewer'))
PROFILE_FILES = {role.replace('_', '-') + '.toml': role for role in ROLES}
RUNTIME_DIRS = frozenset(('runtime', 'traces', 'cache', '.cache', '__pycache__',
                          '.venv', 'venv', 'env', '.pytest_cache', 'screenshots'))
RUNTIME_PROBES = [name + '/probe.txt' for name in sorted(RUNTIME_DIRS)] + [
    '.codex/tmp/probe.txt', 'evals/runtime/probe.txt', 'evals/traces/probe.txt',
    'evals/screenshots/probe.txt', 'tests/__pycache__/probe.pyc', '.env']
REPORT_KEYS = {'status', 'changed_files', 'checks', 'result', 'risks', 'next_action'}
STATUSES = {'completed', 'approved', 'blocked', 'split_required', 'baseline_failure'}


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
        except yaml.YAMLError as error:
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
        if not self.fields(path, data, {'name': str, 'description': str, 'developer_instructions': str}):
            return None
        if data['name'] != PROFILE_FILES.get(path.name):
            self.error(path, 'profile name must match role (integration_reviewer uses underscore)')
        if any(key == 'model' or 'reasoning' in key or key.startswith('model_') for key in data):
            self.error(path, 'canonical profile must inherit model/reasoning settings')
        self.budget(path, data['developer_instructions'], 250)
        owners = re.findall(r'skill\s+`(codex-[a-z-]+)`', text)
        owner = self.root / 'skills' / owners[0] if len(set(owners)) == 1 else None
        self.links(path, text, owner)
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
            if type(data['result'].get('findings')) is not list:
                self.error(path, 'result.findings must be list')
            for check in data['checks']:
                if not isinstance(check, dict) or type(check.get('command')) is not str:
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
        if {path.name for path in profiles} != set(PROFILE_FILES):
            self.error(self.root / 'agents', 'expected exactly eight canonical profile files')
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
            if path == self.root / 'docs/refactoring-map.md':
                continue
            text = self.read(path)
            relative = path.relative_to(self.root)
            owner = self.root / 'skills' / relative.parts[1] if relative.parts[0] == 'skills' else None
            self.links(path, text, owner)
            reports = self.report(path, text)
            if path == report_path and not reports:
                self.error(path, 'missing canonical YAML report example')
        self.runtime()
        return not self.errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('.'))
    args = parser.parse_args(argv)
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
