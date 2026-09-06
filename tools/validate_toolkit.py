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
Historical docs/refactoring-map.md is excluded from active-instruction checks.
Report YAML examples are checked structurally; prose consistency needs review.
"""
from __future__ import annotations

import argparse
import json
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
ROLES = frozenset(('scout', 'analyst', 'architect', 'decomposer', 'developer',
                   'mechanical', 'reviewer', 'integration_reviewer', 'quality_owner'))
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
        if not self.fields(path, data, {'name': str, 'description': str, 'developer_instructions': str}):
            return None
        if data['name'] != PROFILE_FILES.get(path.name):
            self.error(path, 'profile name must match role (integration_reviewer uses underscore)')
        if any(key == 'model' or 'reasoning' in key or key.startswith('model_') for key in data):
            self.error(path, 'canonical profile must inherit model/reasoning settings')
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

    def transition(self, path, data, task_root=None, route=None, status=None, *, route_edge=False):
        # Describing a future route edge does not authorize executing it.
        if route is not None and type(route) is not dict:
            self.error(path, 'route context must be a mapping')
            return
        if data is None:
            if status != 'blocked':
                self.error(path, 'null transition requires blocked status')
            return
        if not self.fields(path, data, {'action': str}, 'transition.'):
            return
        action = data['action']
        self.choice(path, action, {'dispatch', 'review', 'fix', 'integrate', 'revalidate', 'await_user', 'finish'}, 'transition action')
        if action == 'await_user':
            if status != 'blocked':
                self.error(path, 'await_user requires blocked status')
            self.task_path(path, data.get('question_path'), task_root)
        elif action == 'finish':
            if not route_edge and route is not None and not self.accepted(route):
                self.error(path, 'finish requires independent route acceptance')
        elif action in {'dispatch', 'review', 'fix', 'integrate', 'revalidate'}:
            if not self.fields(path, data, {'role': str, 'assignment_id': str, 'assignment_path': str, 'input_paths': list}, 'transition.'):
                return
            self.choice(path, data['role'], ROLES, 'transition role')
            self.task_path(path, data['assignment_path'], task_root)
            for item in data['input_paths']:
                self.task_path(path, item, task_root)
            if not route_edge and task_root is not None and route is not None and data['role'] in {'developer', 'mechanical', 'quality_owner'} and not self.accepted(route):
                self.error(path, 'productive transition requires route acceptance')
            if route is not None:
                entry = self.route_entries(route).get(data['assignment_id'])
                if entry is None or any(entry.get(key) != data[key] for key in ('role', 'assignment_path')):
                    self.error(path, 'transition unknown assignment ID or mismatched role/path')

    @staticmethod
    def route_entries(route):
        assignments = route.get('assignments', [])
        if type(assignments) is not list:
            return {}
        return {x['id']: x for x in assignments
                if isinstance(x, dict) and type(x.get('id')) is str}

    @staticmethod
    def accepted(route):
        acceptance = route.get('acceptance')
        if not isinstance(acceptance, dict):
            return False
        entry = Validator.route_entries(route).get(acceptance.get('reviewer_assignment_id')) if type(acceptance.get('reviewer_assignment_id')) is str else None
        return bool(entry and type(entry.get('role')) is str and entry.get('role') in {'reviewer', 'integration_reviewer'}
                    and type(acceptance.get('report_path')) is str
                    and type(acceptance.get('route_revision')) is int
                    and acceptance['route_revision'] == route.get('route_revision'))

    def assignment(self, path, data, task_root=None):
        schema = {'assignment_id': str, 'role': str, 'dispatcher_mode': bool, 'task_root': str, 'route_revision': int, 'goal_path': str, 'input_paths': list, 'write_set': list, 'artifact_path': str, 'criteria': list, 'checks': list, 'allowed_next_assignments': list}
        if not self.fields(path, data, schema):
            return
        self.choice(path, data['role'], ROLES, 'assignment role')
        self.integer(path, data['route_revision'], 'route_revision')
        if data['dispatcher_mode'] is not True:
            self.error(path, 'dispatcher assignment requires dispatcher_mode true')
        if task_root is not None:
            try:
                if Path(data['task_root']).resolve(strict=True) != Path(task_root).resolve(strict=True):
                    self.error(path, 'assignment task_root mismatch')
            except (OSError, RuntimeError, ValueError) as error:
                self.error(path, f'invalid assignment task_root: {error}')
        self.task_path(path, data['goal_path'], task_root)
        self.task_path(path, data['artifact_path'], task_root, future=True)
        for key in ('input_paths', 'allowed_next_assignments'):
            for item in data[key]:
                self.task_path(path, item, task_root)
        for key in ('write_set', 'criteria'):
            self.strings(path, data[key], key)
        if not data['criteria']:
            self.error(path, 'executable assignment requires criteria')

    def route(self, path, data, task_root=None):
        if not self.fields(path, data, {'version': int, 'route_revision': int, 'assignments': list, 'acceptance': dict}):
            return
        self.integer(path, data['route_revision'], 'route_revision')
        if data['version'] != 1:
            self.error(path, 'unsupported version')
        entries = self.route_entries(data)
        if len(entries) != len(data['assignments']):
            self.error(path, 'invalid or duplicate assignment ID')
        for entry in data['assignments']:
            if not self.fields(path, entry, {'id': str, 'role': str, 'assignment_path': str, 'dependencies': list, 'allowed_transitions': list, 'write_set': list, 'shared_resources': list}, 'assignment.'):
                continue
            self.choice(path, entry['role'], ROLES, 'assignment role')
            target = self.task_path(path, entry['assignment_path'], task_root)
            if target:
                assignment = self.parse_yaml(target, self.read(target))
                self.assignment(target, assignment, task_root)
                if not isinstance(assignment, dict) or assignment.get('assignment_id') != entry['id'] or assignment.get('role') != entry['role'] or type(assignment.get('route_revision')) is not int or assignment['route_revision'] != data['route_revision']:
                    self.error(path, 'assignment file ID/role/revision mismatch')
            for key in ('dependencies', 'write_set', 'shared_resources'):
                self.strings(path, entry[key], key)
            if any(type(x) is not str or x not in entries for x in entry['dependencies']):
                self.error(path, 'unknown dependency ID')
            for transition in entry['allowed_transitions']:
                self.transition(path, transition, task_root, data, status='blocked' if isinstance(transition, dict) and transition.get('action') == 'await_user' else None, route_edge=True)
        acceptance = data['acceptance']
        if set(acceptance) != {'reviewer_assignment_id', 'report_path', 'route_revision'}:
            self.error(path, 'invalid acceptance fields')
        if any(value is not None for value in acceptance.values()):
            if not self.accepted(data):
                self.error(path, 'invalid independent route acceptance')
            self.task_path(path, acceptance.get('report_path'), task_root)

    def envelope(self, path, data, task_root=None, route=None, sender=None):
        if route is not None and type(route) is not dict:
            self.error(path, 'route context must be a mapping')
            return
        if sender is not None and not self.fields(path, sender, {'id': str, 'role': str, 'route_revision': int}, 'sender.'):
            return
        required = {'status', 'artifact', 'assignment_id', 'route_revision', 'next_transition', 'decision_question'}
        if not self.fields(path, data, {'status': str, 'artifact': str, 'assignment_id': str, 'route_revision': int}):
            return
        if set(data) != required:
            self.error(path, 'envelope must contain only six envelope fields, never full report')
        self.choice(path, data['status'], STATUSES, 'envelope status')
        self.integer(path, data['route_revision'], 'route_revision')
        artifact = self.task_path(path, data['artifact'], task_root)
        transition = data.get('next_transition')
        self.transition(path, transition, task_root, route, data['status'])
        question = data.get('decision_question')
        if isinstance(transition, dict) and transition.get('action') == 'await_user':
            if question != transition.get('question_path'):
                self.error(path, 'decision_question must match question_path')
        elif question is not None:
            self.error(path, 'decision_question must be null for ordinary transition')
        if route is not None and type(route) is not dict:
            self.error(path, 'route context must be a mapping')
            return
        if task_root is not None and route is None:
            self.error(path, 'concrete envelope requires route context')
        if route is not None:
            before = len(self.errors)
            self.route(path, route, task_root)
            if len(self.errors) != before:
                return
        if sender is not None and (data['assignment_id'] != sender.get('id') or data['route_revision'] != sender.get('route_revision')):
            self.error(path, 'unknown sender or stale revision')
        if route is not None:
            entry = self.route_entries(route).get(data['assignment_id'])
            if entry is None or data['route_revision'] != route.get('route_revision'):
                self.error(path, 'unknown sender or stale revision')
            elif transition is not None and transition not in entry.get('allowed_transitions', []):
                self.error(path, 'transition is not an accepted route edge')
            if task_root is not None and entry is not None:
                assignment_path = self.task_path(path, entry.get('assignment_path'), task_root)
                if assignment_path:
                    assignment = self.parse_yaml(assignment_path, self.read(assignment_path))
                    if isinstance(assignment, dict):
                        allowed_artifact = self.task_path(path, assignment.get('artifact_path'), task_root)
                        if artifact is not None and allowed_artifact is not None and artifact != allowed_artifact:
                            self.error(path, 'artifact differs from sender assignment artifact_path')
            if sender is not None and entry is not None and sender.get('role') != entry.get('role'):
                self.error(path, 'sender role mismatch')

    def state(self, path, data, task_root=None, route=None):
        required = {'version', 'task_id', 'mode', 'goal_path', 'constraints_path', 'phase', 'route_path', 'route_revision', 'active_assignments', 'accepted_index_path', 'next_transition', 'decision', 'budget_path', 'checkpoint_path', 'last_checkpoint'}
        if not self.fields(path, data, {'version': int, 'task_id': str, 'mode': str, 'phase': str, 'route_revision': int, 'active_assignments': list, 'decision': dict}):
            return
        if set(data) != required or data['version'] != 1 or data['mode'] != 'dispatcher_only':
            self.error(path, 'invalid state fields/version/mode')
        self.integer(path, data['route_revision'], 'route_revision')
        for key in ('goal_path', 'constraints_path', 'budget_path'):
            self.task_path(path, data.get(key), task_root)
        for key in ('route_path', 'accepted_index_path', 'checkpoint_path'):
            self.task_path(path, data.get(key), task_root, nullable=True)
        if data.get('last_checkpoint') is not None and (type(data['last_checkpoint']) is not str or not data['last_checkpoint'].strip()):
            self.error(path, 'last_checkpoint must be nonblank string or null')
        if task_root is not None and data.get('route_path') is not None:
            target = self.task_path(path, data['route_path'], task_root)
            if target:
                stored_route = self.parse_yaml(target, self.read(target))
                if type(stored_route) is not dict:
                    self.error(path, 'stored route must be a mapping')
                elif route is None:
                    route = stored_route
                elif route != stored_route:
                    self.error(path, 'route context differs from route_path content')
        if route is not None and type(route) is not dict:
            self.error(path, 'route context must be a mapping')
            return
        bootstrap = data['phase'] == 'bootstrap' and data.get('route_path') is None
        if data.get('route_path') is None and (not bootstrap or data['route_revision'] != 0 or route is not None or data['active_assignments']):
            self.error(path, 'incomplete bootstrap only before accepted route')
        if task_root is not None and not bootstrap and route is None:
            self.error(path, 'concrete state requires route context')
        if route is not None:
            before = len(self.errors)
            self.route(path, route, task_root)
            if len(self.errors) != before:
                return
        if route is not None and data['route_revision'] != route.get('route_revision'):
            self.error(path, 'stale state revision')
        decision = data['decision']
        self.choice(path, decision.get('status'), {'none', 'await_user'}, 'decision status')
        self.task_path(path, decision.get('question_path'), task_root, nullable=decision.get('status') == 'none')
        if decision.get('status') == 'none' and decision.get('question_path') is not None:
            self.error(path, 'none decision requires null question')
        if data.get('next_transition') is not None:
            self.transition(path, data['next_transition'], task_root, route, 'blocked' if decision.get('status') == 'await_user' else None)
        seen = set()
        for entry in data['active_assignments']:
            if not self.fields(path, entry, {'id': str, 'role': str, 'status': str, 'assignment_path': str, 'route_revision': int}, 'active.'):
                continue
            if not {'artifact', 'envelope', 'runtime_handle'} <= set(entry):
                self.error(path, 'missing active assignment fields')
            if entry['id'] in seen:
                self.error(path, 'duplicate active assignment ID')
            seen.add(entry['id'])
            self.choice(path, entry['role'], ROLES, 'active role')
            self.choice(path, entry['status'], {'pending', 'ready', 'running', 'completed', 'approved', 'blocked', 'needs_revalidation', 'cancelled'}, 'active status')
            self.task_path(path, entry['assignment_path'], task_root)
            for key in ('artifact', 'envelope'):
                self.task_path(path, entry.get(key), task_root, nullable=True)
            handle = entry.get('runtime_handle')
            if handle is not None and (type(handle) is not str or not handle.strip()):
                self.error(path, 'runtime_handle must be nonblank string or null')
            if entry['status'] == 'running' and handle is None:
                self.error(path, 'running assignment requires runtime_handle')
            if entry['route_revision'] != data['route_revision']:
                self.error(path, 'stale active revision')
            if route is not None:
                actual = self.route_entries(route).get(entry['id'])
                if actual is None or any(actual.get(k) != entry[k] for k in ('role', 'assignment_path')):
                    self.error(path, 'unknown active assignment or role/path mismatch')
                if entry['status'] in {'ready', 'running'} and not self.accepted(route):
                    self.error(path, 'ready/running requires accepted executable assignment')
                if entry['status'] == 'ready' and actual:
                    statuses = {x.get('id'): x.get('status') for x in data['active_assignments'] if isinstance(x, dict) and type(x.get('id')) is str}
                    # An index path alone supplies no addressed dependency evidence.
                    # Without a declared index schema, missing active evidence stays unconfirmed.
                    if any(type(dep) is not str or statuses.get(dep) not in ('approved', 'completed') for dep in actual.get('dependencies', [])):
                        self.error(path, 'ready assignment has unsatisfied or unconfirmed dependencies')

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
        for key in ('inventory_path', 'findings_path', 'current_batch_path', 'decisions_path', 'evidence_path', 'budget_path'):
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
            ('codex-long-orchestration/references/templates/state.yaml', self.state),
            ('codex-long-orchestration/references/templates/envelope.yaml', self.envelope),
            ('codex-product-quality/references/templates/quality-state.yaml', self.quality),
        ):
            path = self.root / 'skills' / name
            method(path, self.parse_yaml(path, self.read(path)))
        for name, methods in (
            ('codex-long-orchestration/references/dispatcher-mode.md', (self.route, self.budget_data)),
            ('codex-product-quality/references/finding-schema.md', (self.finding,)),
            ('codex-orchestration-pact/references/templates/task.md', (self.assignment,)),
        ):
            path = self.root / 'skills' / name
            blocks = re.findall(r'^```yaml\s*\n(.*?)^```', self.read(path), re.M | re.S)
            if len(blocks) != len(methods):
                self.error(path, 'missing or extra canonical YAML schema blocks')
            for block, method in zip(blocks, methods):
                method(path, self.parse_yaml(path, block))

    def budget_data(self, path, data):
        if not self.fields(path, data, {'await_user': list, 'blocked': list, 'handoff': list, 'permission_source': str}):
            return
        for key in ('max_batches', 'time', 'resources'):
            if key not in data:
                self.error(path, f'missing budget {key}')
        if data.get('max_batches') is not None:
            self.integer(path, data['max_batches'], 'max_batches', 1)
        for key in ('await_user', 'blocked', 'handoff'):
            self.strings(path, data[key], key)
        for key in ('time', 'resources'):
            if data.get(key) is not None and (type(data[key]) is not str or not data[key].strip()):
                self.error(path, f'{key} must be nonblank string or null')
        self.task_path(path, data['permission_source'])

    def cases(self):
        path = self.root / 'evals/cases.jsonl'
        expected = {f'R{i:02}{suffix}' for i in range(1, 12) for suffix in 'PN'} | {f'W{i:02}' for i in range(1, 17)}
        seen = set()
        def unique(pairs):
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f'duplicate JSON key: {key}')
                result[key] = value
            return result
        for line, text in enumerate(self.read(path).splitlines(), 1):
            try:
                data = json.loads(text, object_pairs_hook=unique, parse_constant=lambda value: (_ for _ in ()).throw(ValueError(f'invalid constant {value}')))
            except (ValueError, RecursionError) as error:
                self.error(path, f'invalid JSONL: {error}', line)
                continue
            label = (path, line)
            schema = {'id': str, 'kind': str, 'prompt': str, 'expected_skills': list, 'forbidden_skills': list, 'expected_outcomes': list, 'forbidden_actions': list, 'required_capabilities': list}
            if not self.fields(label, data, schema):
                continue
            if data['id'] in seen:
                self.error(path, 'duplicate case ID', line)
            seen.add(data['id'])
            self.choice(label, data['kind'], {'routing', 'workflow'}, 'case kind')
            if data['id'] in expected and data['kind'] != ('routing' if data['id'].startswith('R') else 'workflow'):
                self.error(path, 'case ID/kind mismatch', line)
            for key in ('expected_skills', 'forbidden_skills', 'expected_outcomes', 'forbidden_actions', 'required_capabilities'):
                self.strings(label, data[key], key)
            skills = data['expected_skills'] + data['forbidden_skills']
            if any(type(x) is not str or x not in SKILLS for x in skills):
                self.error(path, 'unknown case skill', line)
            if any(x in data['forbidden_skills'] for x in data['expected_skills']):
                self.error(path, 'expected/forbidden skills overlap', line)
            if 'fixture' not in data:
                self.error(path, 'missing fixture', line)
            elif data['fixture'] is not None:
                fixture = data['fixture']
                if type(fixture) is not str or not fixture.startswith('fixtures/'):
                    self.error(path, 'fixture must be relative to evals inside fixtures/', line)
                else:
                    self.task_path(label, fixture[len('fixtures/'):], self.root / 'evals/fixtures', directory=True)
        if seen != expected:
            self.error(path, f'case ID set mismatch; missing={sorted(expected-seen)}, extra={sorted(seen-expected)}')

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
            self.error(self.root / 'agents', 'expected exactly nine canonical profile files')
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
        self.templates()
        self.cases()
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
