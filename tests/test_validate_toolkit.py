"""Structural validator regression tests, using disposable Git repositories."""
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest

import yaml

from tools.validate_toolkit import PROFILE_FILES, RUNTIME_PROBES, SKILLS, Validator, main


REPORT = '''```yaml
status: completed
changed_files: []
checks: []
result:
  evidence: []
  findings: []
risks: []
next_action: null
```
'''


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        self.write('.gitignore', '\n'.join(RUNTIME_PROBES) + '\n')
        for name in SKILLS:
            self.write(f'skills/{name}/SKILL.md', f'---\nname: {name}\ndescription: Test procedure\n---\n# Procedure\n')
            metadata = {'interface': {'display_name': name, 'short_description': 'Test skill', 'default_prompt': f'Use ${name}.'}, 'policy': {'allow_implicit_invocation': name != 'codex-communication-pact'}}
            self.write(f'skills/{name}/agents/openai.yaml', yaml.safe_dump(metadata))
        for filename, role in PROFILE_FILES.items():
            self.write(f'agents/{filename}', f'name = "{role}"\ndescription = "Test role"\nsandbox_mode = "workspace-write"\nmodel = "test-model"\nmodel_reasoning_effort = "medium"\ndeveloper_instructions = "Read assigned input"\n')
        self.write('skills/codex-orchestration-pact/references/templates/report.md', REPORT)
        self.quality_data = dict(version=1, campaign_id='test', iteration=0, permission='observe_only', inventory_path='quality/inventory.yaml', findings_path='quality/findings.yaml', current_batch_path='quality/current-batch.md', decisions_path='quality/decisions.md', evidence_path='quality/evidence', expected=None, unresolved_questions=[], next_step='observe')
        self.finding_data = dict(id='F01', surface='test', scenario='test', state='error', viewport=None, expected=None, expected_source=None, observed='test', evidence=[], classification='unknown', severity=None, confidence='low', decision_required=True, recommended_next_role='analyst')
        self.write('skills/codex-product-quality/references/templates/quality-state.yaml', yaml.safe_dump(self.quality_data))
        self.write('skills/codex-product-quality/references/finding-schema.md', self.block(self.finding_data))

    @staticmethod
    def block(data):
        return '```yaml\n' + yaml.safe_dump(data) + '```\n'

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding='utf-8')
        return path

    def append(self, name, text):
        path = self.root / name
        path.write_text(path.read_text() + text)

    def validate(self):
        result = Validator(self.root)
        result.run()
        return result

    def assert_error(self, fragment):
        result = self.validate()
        self.assertTrue(any(fragment in error for error in result.errors), result.errors)

    def test_minimal_valid_set_and_read_only(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        result = self.validate()
        self.assertEqual([], result.errors)
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_invalid_yaml(self):
        self.write('skills/codex-debugging/agents/openai.yaml', 'interface: [\n')
        self.assert_error('expected')

    def test_unsafe_yaml_tag_is_rejected(self):
        self.write('skills/codex-debugging/agents/openai.yaml', '!!python/object/apply:os.system ["false"]')
        self.assert_error('could not determine a constructor')

    def test_invalid_toml(self):
        self.write('agents/scout.toml', 'name = [')
        self.assert_error('Invalid value')

    def test_duplicate_yaml_key_nested(self):
        self.append('skills/codex-debugging/agents/openai.yaml', 'policy:\n  allow_implicit_invocation: true\n')
        self.assert_error('duplicate key: policy')

    def test_duplicate_frontmatter_key(self):
        self.write('skills/codex-debugging/SKILL.md', '---\nname: codex-debugging\nname: codex-debugging\ndescription: test\n---\n')
        self.assert_error('duplicate key: name')

    def test_name_mismatch_and_duplicate(self):
        self.write('skills/codex-debugging/SKILL.md', '---\nname: codex-development-pact\ndescription: test\n---\n')
        self.assert_error('name must match directory')
        self.assert_error('duplicate name')

    def test_historical_eval_material_is_excluded(self):
        self.write('evals/README.md', '[Cases](missing.jsonl)\n')
        self.write('evals/cases.jsonl', '{broken}\n')
        self.assertEqual([], self.validate().errors)
        self.write('evals/active.md', '[Missing](missing.md)\n')
        self.assert_error('local target does not exist: missing.md')

    def test_broken_markdown_link(self):
        self.append('skills/codex-debugging/SKILL.md', '[Guide](references/missing.md)\n')
        self.assert_error('local target does not exist')

    def test_reference_links_and_percent_escaped_paths(self):
        self.write('docs/guide with space.md', '# Guide\n')
        self.write('README.md', '[Guide][guide]\n[guide]: docs/guide%20with%20space.md "Title"\n')
        self.assertEqual([], self.validate().errors)
        self.append('README.md', '[Missing][missing]\n')
        self.assert_error('undefined reference link')

    def test_example_paths_are_not_file_requirements(self):
        self.write('README.md', '''```md
[Sample](missing.md)
$codex-not-a-real-skill
```
    [Example](missing.md)
`[Inline](missing.md)`
[Parameter](<project/{name}/file.md>)
[Variable]($PROJECT/file.md)
[Web](https://example.invalid/missing)
[Anchor](#heading)
`examples/missing.md`
''')
        self.assertEqual([], self.validate().errors)

    def test_policy_requires_boolean(self):
        path = self.root / 'skills/codex-debugging/agents/openai.yaml'
        data = yaml.safe_load(path.read_text())
        for value in ('true', 1, None, []):
            with self.subTest(value=value):
                data['policy']['allow_implicit_invocation'] = value
                path.write_text(yaml.safe_dump(data))
                self.assert_error('must be bool')

    def test_integration_reviewer_underscore_is_required(self):
        self.assertEqual([], self.validate().errors)
        path = self.root / 'agents/integration-reviewer.toml'
        path.write_text(path.read_text().replace('integration_reviewer', 'integration-reviewer'))
        self.assert_error('integration_reviewer uses underscore')

    def test_metadata_own_prompt_and_resource(self):
        path = self.root / 'skills/codex-debugging/agents/openai.yaml'
        data = yaml.safe_load(path.read_text())
        data['interface']['default_prompt'] = '$codex-debugging-extra'
        data['interface']['icon_small'] = '../missing.svg'
        path.write_text(yaml.safe_dump(data))
        self.assert_error('own $skill-name')
        self.assert_error('local target does not exist')

    def test_metadata_rejects_additional_unknown_skill(self):
        path = self.root / 'skills/codex-debugging/agents/openai.yaml'
        data = yaml.safe_load(path.read_text())
        data['interface']['default_prompt'] = 'Use $codex-debugging and $codex-development-pact.'
        path.write_text(yaml.safe_dump(data))
        self.assertEqual([], self.validate().errors)
        for unknown in ('$codex-unknown', '`$codex-unknown`'):
            with self.subTest(unknown=unknown):
                data['interface']['default_prompt'] = 'Use $codex-debugging. Then use ' + unknown
                path.write_text(yaml.safe_dump(data))
                self.assert_error('unknown explicit skill: codex-unknown')

    def test_explicit_role_uses_identifier_not_profile_filename(self):
        self.write('README.md', 'Delegate role: `integration_reviewer`.\n')
        self.assertEqual([], self.validate().errors)
        self.write('README.md', 'Delegate role: `integration-reviewer`.\n')
        self.assert_error('unknown explicit role: integration-reviewer')

    def test_inline_skill_example_is_not_an_active_reference(self):
        self.write('README.md', 'Example syntax: `$codex-nonexistent`.\n')
        self.assertEqual([], self.validate().errors)
        self.append('README.md', 'Apply skill `$codex-nonexistent`.\n')
        self.assert_error('unknown explicit skill: codex-nonexistent')

    def test_report_unexecuted_result_must_be_explicit(self):
        path = 'skills/codex-orchestration-pact/references/templates/report.md'
        for status in ('not_run', 'unable_to_verify'):
            with self.subTest(status=status):
                check = f'checks:\n  - command: test\n    execution_status: {status}\n    reason: unavailable'
                self.write(path, REPORT.replace('checks: []', check))
                self.assert_error('check requires result key')
                self.write(path, REPORT.replace('checks: []', check + '\n    result: null'))
                self.assertEqual([], self.validate().errors)

    def test_report_findings_type(self):
        self.write('skills/codex-orchestration-pact/references/templates/report.md', REPORT.replace('findings: []', 'findings: No issues.'))
        self.assert_error('result.findings must be list')

    def test_report_check_status_consistency(self):
        self.write('skills/codex-orchestration-pact/references/templates/report.md', REPORT.replace('checks: []', 'checks:\n  - command: test\n    execution_status: not_run\n    result: passed'))
        self.assert_error('unexecuted check requires null result and reason')

    def test_report_malformed_check_types_are_errors(self):
        self.write('skills/codex-orchestration-pact/references/templates/report.md', REPORT.replace('checks: []', 'checks:\n  - command: test\n    execution_status: []\n    result: []'))
        self.assert_error('invalid execution_status')

    def test_skill_set_and_required_types(self):
        self.write('skills/codex-extra/SKILL.md', '---\nname: codex-extra\ndescription: 123\n---\n')
        self.write('agents/extra.toml', 'name = "extra"\n')
        self.assert_error('skill set mismatch')
        self.assert_error('description must be str')

    def test_runtime_ignore_and_tracking(self):
        self.write('.gitignore', '')
        self.assert_error('runtime path is not ignored')
        self.write('.gitignore', '\n'.join(RUNTIME_PROBES) + '\n')
        self.write('traces/probe.txt', 'trace')
        subprocess.run(['git', '-C', str(self.root), 'add', '-f', 'traces/probe.txt'], check=True)
        self.assert_error('runtime artifact is tracked')

    def test_missing_skill(self):
        (self.root / 'skills/codex-debugging/SKILL.md').unlink()
        self.assert_error('missing YAML front matter')

    def test_profile_count_and_model_policy_are_not_enforced(self):
        (self.root / 'agents/scout.toml').unlink()
        path = self.root / 'agents/developer.toml'
        self.write('agents/developer.toml', path.read_text().replace('test-model', 'another-model'))
        self.assertEqual([], self.validate().errors)

    def test_profile_inventory_includes_standard_analyst(self):
        self.assertEqual(13, len(PROFILE_FILES))
        self.assertEqual('analyst_standard', PROFILE_FILES['analyst-standard.toml'])

    def test_explicit_unknown_skill_and_role(self):
        self.write('README.md', 'Apply $codex-unknown.\nrole: `unknown`\n')
        self.assert_error('unknown explicit skill')
        self.assert_error('unknown explicit role')

    def test_client_name_and_empty_legacy_directory_are_not_skills(self):
        self.write('README.md', 'Version: codex-cli 0.152.0; `codex-cli 0.152.0`.\n')
        (self.root / 'skills/codex-pacts/agents').mkdir(parents=True)
        self.assertEqual([], self.validate().errors)
        self.append('README.md', 'Apply skill `codex-unknown`.\n')
        self.assert_error('unknown explicit skill')

    def test_nonempty_unknown_skill_directory_is_rejected(self):
        self.write('skills/codex-pacts/agents/openai.yaml', 'interface: {}\n')
        self.assert_error('skill set mismatch')

    def test_historical_map_excluded(self):
        self.write('docs/refactoring-map.md', '$codex-historical\n[Old](gone.md)\n')
        self.assertEqual([], self.validate().errors)

    def test_budget_warning_does_not_fail(self):
        self.append('skills/codex-communication-pact/SKILL.md', 'word ' * 251)
        result = self.validate()
        self.assertEqual([], result.errors)
        self.assertEqual(1, len(result.warnings))

    def test_cli_exit_code(self):
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(0, main(['--root', str(self.root)]))
            self.write('agents/scout.toml', 'broken [')
            self.assertEqual(1, main(['--root', str(self.root)]))

    def structure(self, method, data, **context):
        validator = Validator(self.root)
        getattr(validator, method)(self.root / 'sample.yaml', data, **context)
        return validator.errors

    def test_quality_state_and_findings(self):
        for patch in (dict(iteration=-1), dict(permission='write'), dict(inventory_path=None), dict(expected=' '), dict(unresolved_questions=[None]), dict(next_step=' ')):
            self.assertTrue(self.structure('quality', dict(self.quality_data, **patch)))
        for patch in (dict(classification='defect'), dict(severity='critical'), dict(confidence=[]), dict(decision_required='true'), dict(recommended_next_role='other'), dict(viewport=dict(width=True, height=2, dpr=None)), dict(expected_source=' ')):
            self.assertTrue(self.structure('finding', dict(self.finding_data, **patch)))
        self.assertTrue(self.structure('finding', self.finding_data, concrete=True))
        self.assertTrue(self.structure('finding', dict(self.finding_data, evidence=[None]), concrete=True))
        self.assertTrue(self.structure('findings', [self.finding_data, self.finding_data]))
        self.assertEqual([], self.structure('finding', dict(self.finding_data, classification='defect', expected='requirement', expected_source='goal.md', evidence=['observed source']), concrete=True))

    def test_source_templates_are_not_runtime(self):
        subprocess.run(['git', '-C', str(self.root), 'add', 'skills'], check=True)
        before = (self.root / '.git/index').read_bytes()
        self.assertEqual([], self.validate().errors)
        self.assertEqual(before, (self.root / '.git/index').read_bytes())

    def test_profile_multiple_explicit_links(self):
        self.append('agents/scout.toml', '# [Report](../skills/codex-orchestration-pact/references/templates/report.md)\n# [Long](../skills/codex-long-orchestration/SKILL.md)\n')
        self.assertEqual([], self.validate().errors)
        self.append('agents/scout.toml', '# [Missing](../skills/codex-product-quality/missing.md)\n')
        self.assert_error('local target does not exist')

    def artifact_report(self, assignment_id='P01', attempt=1, goal_version=1, status='completed', accepts=None):
        return dict(status=status, changed_files=[], checks=[], result=dict(
            assignment=dict(id=assignment_id, attempt=attempt, goal_version=goal_version, snapshot=None),
            accepts=accepts, evidence=[], findings=[]), risks=[], next_action='assignments/R01.yaml')

    def artifact_manifest(self, report='reports/P01.yaml', envelope=None, owners=None, accepts=None):
        entry = dict(path=report, assignment_id='P01', attempt=1, goal_version=1, next_transition='assignments/R01.yaml')
        if envelope is not None:
            entry['envelope'] = envelope
        if accepts is not None:
            entry['accepts'] = accepts
        entries = [entry]
        accepted_items = accepts if isinstance(accepts, list) else [accepts] if accepts is not None else []
        for accepted in accepted_items:
            if not isinstance(accepted, dict):
                continue
            accepted_path = f"reports/{accepted['assignment_id']}.yaml"
            if not (self.root / accepted_path).exists():
                completed = self.artifact_report(accepted['assignment_id'], accepted['attempt'], accepted['goal_version'])
                completed['result']['assignment']['snapshot'] = accepted.get('snapshot')
                completed['result']['evidence'] = ['accepted evidence']
                self.write(accepted_path, yaml.safe_dump(completed))
            entries.append(dict(path=accepted_path, assignment_id=accepted['assignment_id'], attempt=accepted['attempt'], goal_version=accepted['goal_version'], next_transition='assignments/R01.yaml'))
        data = dict(version=1, reports=entries)
        if owners is not None:
            data['owners'] = owners
        self.write('manifest.yaml', yaml.safe_dump(data))
        self.write('assignments/R01.yaml', '{}\n')

    def artifact_validate(self):
        validator = Validator(self.root)
        result = validator.task_artifacts(self.root, 'manifest.yaml')
        return result, validator.errors

    def test_task_artifacts_valid_and_missing_trust(self):
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report()))
        self.artifact_manifest()
        result, errors = self.artifact_validate()
        self.assertEqual('not_verified', result['status'])
        self.assertEqual([], errors)

    def test_task_artifacts_rejects_malformed_stale_and_self_approval(self):
        self.write('reports/P01.yaml', '[\n')
        self.artifact_manifest()
        _, errors = self.artifact_validate()
        self.assertTrue(errors)

        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(status='approved', accepts=dict(assignment_id='P02', attempt=1, goal_version=1))))
        self.artifact_manifest(owners={'P01': 'developer', 'P02': 'developer'}, accepts=dict(assignment_id='P02', attempt=1, goal_version=1))
        _, errors = self.artifact_validate()
        self.assertTrue(any('self-approval' in error for error in errors), errors)

        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(goal_version=2)))
        self.artifact_manifest()
        _, errors = self.artifact_validate()
        self.assertTrue(any('does not match explicit expectation' in error for error in errors), errors)

    def test_task_artifacts_correlates_accepted_result_triple(self):
        accepts = dict(assignment_id='P02', attempt=1, goal_version=1)
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(status='approved', accepts=accepts)))
        self.artifact_manifest(owners={'P01': 'reviewer', 'P02': 'developer'}, accepts=accepts)
        result, errors = self.artifact_validate()
        self.assertEqual('checked', result['status'])
        self.assertEqual([], errors)
        self.artifact_manifest(owners={'P01': 'reviewer', 'P02': 'developer'}, accepts=dict(assignment_id='P02', attempt=2, goal_version=1))
        _, errors = self.artifact_validate()
        self.assertTrue(any('accepted-result expectation' in error for error in errors), errors)
        self.artifact_manifest(owners={'P01': 'reviewer', 'P02': 'developer'}, accepts=dict(assignment_id='P02', attempt=1, goal_version=2))
        _, errors = self.artifact_validate()
        self.assertTrue(any('accepted-result expectation' in error for error in errors), errors)

    def test_task_artifacts_rejects_envelope_path_and_symlink_escape(self):
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report()))
        self.artifact_manifest(report='../outside.yaml')
        _, errors = self.artifact_validate()
        self.assertTrue(any('unsafe task path' in error for error in errors), errors)

        outside = Path(self.temp.name).parent / 'outside-report.yaml'
        outside.write_text(yaml.safe_dump(self.artifact_report()), encoding='utf-8')
        (self.root / 'reports').mkdir(exist_ok=True)
        (self.root / 'reports/P01.yaml').unlink()
        (self.root / 'reports/P01.yaml').symlink_to(outside)
        self.artifact_manifest()
        _, errors = self.artifact_validate()
        self.assertTrue(any('unsafe or missing task path' in error for error in errors), errors)

    def test_task_artifacts_rejects_stale_envelope_and_missing_report(self):
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report()))
        envelope = dict(status='completed', artifact='reports/P01.yaml', assignment_id='P01', attempt=2,
                        profile='developer', accepts=None, finding_id=None, progress=None, no_progress=None,
                        next_transition='assignments/R01.yaml')
        self.write('envelopes/P01.yaml', yaml.safe_dump(envelope))
        self.artifact_manifest(envelope='envelopes/P01.yaml')
        _, errors = self.artifact_validate()
        self.assertTrue(any('envelope is stale' in error for error in errors), errors)

        self.artifact_manifest(report='reports/missing.yaml')
        _, errors = self.artifact_validate()
        self.assertTrue(any('unsafe or missing task path' in error for error in errors), errors)

    def test_task_artifacts_validates_canonical_envelope_accepts_and_progress(self):
        accepts = dict(assignment_id='P02', attempt=1, goal_version=1, snapshot='sha256:abc')
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(status='approved', accepts=accepts)))
        envelope = dict(status='approved', artifact='reports/P01.yaml', assignment_id='P01', attempt=1,
                        profile='reviewer', accepts='P02/1@sha256:abc', finding_id=None, progress=None,
                        no_progress=None, next_transition='assignments/R01.yaml')
        self.write('envelopes/P01.yaml', yaml.safe_dump(envelope))
        self.artifact_manifest(envelope='envelopes/P01.yaml', owners={'P01': 'reviewer', 'P02': 'developer'}, accepts=accepts)
        result, errors = self.artifact_validate()
        self.assertEqual('checked', result['status'])
        self.assertEqual([], errors)
        for value in ('P99/1@sha256:abc', 'P02/2@sha256:abc', 'P02/1@sha256:wrong'):
            with self.subTest(value=value):
                envelope['accepts'] = value
                self.write('envelopes/P01.yaml', yaml.safe_dump(envelope))
                _, errors = self.artifact_validate()
                self.assertTrue(any('does not correlate' in error for error in errors), errors)

    def test_task_artifacts_accepts_packet_with_snapshots(self):
        accepts = [
            dict(assignment_id='P02', attempt=1, goal_version=1, snapshot='sha256:first'),
            dict(assignment_id='P03', attempt=2, goal_version=1, snapshot='sha256:second'),
        ]
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(status='approved', accepts=accepts)))
        envelope = dict(status='approved', artifact='reports/P01.yaml', assignment_id='P01', attempt=1,
                        profile='reviewer', accepts=['P02/1@sha256:first', 'P03/2@sha256:second'],
                        finding_id=None, progress=None, no_progress=None, next_transition='assignments/R01.yaml')
        self.write('envelopes/P01.yaml', yaml.safe_dump(envelope))
        self.artifact_manifest(envelope='envelopes/P01.yaml', owners={'P01': 'reviewer', 'P02': 'developer', 'P03': 'mechanical'}, accepts=accepts)
        result, errors = self.artifact_validate()
        self.assertEqual('checked', result['status'])
        self.assertEqual([], errors)

    def test_task_artifacts_rejects_packet_without_snapshot_or_duplicate(self):
        accepts = [dict(assignment_id='P02', attempt=1, goal_version=1), dict(assignment_id='P02', attempt=1, goal_version=1, snapshot='sha256:x')]
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(status='approved', accepts=accepts)))
        self.artifact_manifest(owners={'P01': 'reviewer', 'P02': 'developer'}, accepts=accepts)
        _, errors = self.artifact_validate()
        self.assertTrue(any('packet accepts requires snapshot' in error for error in errors), errors)

    def test_task_artifacts_resolves_every_accepted_report(self):
        accepted = dict(assignment_id='P02', attempt=1, goal_version=1)
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(status='approved', accepts=accepted)))
        completed = self.artifact_report(assignment_id='P02')
        completed['result']['evidence'] = ['tests/test_feature.py']
        self.write('reports/P02.yaml', yaml.safe_dump(completed))
        manifest = dict(version=1, owners={'P01': 'reviewer', 'P02': 'developer'}, reports=[
            dict(path='reports/P01.yaml', assignment_id='P01', attempt=1, goal_version=1, next_transition='assignments/R01.yaml', accepts=accepted),
            dict(path='reports/P02.yaml', assignment_id='P02', attempt=1, goal_version=1, next_transition='assignments/R01.yaml'),
        ])
        self.write('manifest.yaml', yaml.safe_dump(manifest))
        self.write('assignments/R01.yaml', '{}\n')
        result, errors = self.artifact_validate()
        self.assertEqual('checked', result['status'])
        self.assertEqual([], errors)
        completed['status'] = 'paused'
        completed['result']['evidence'] = []
        self.write('reports/P02.yaml', yaml.safe_dump(completed))
        _, errors = self.artifact_validate()
        self.assertTrue(any('accepted result must be completed' in error for error in errors), errors)
        self.assertTrue(any('accepted result requires evidence' in error for error in errors), errors)
        completed['status'] = 'completed'
        completed['result']['assignment']['attempt'] = 2
        completed['result']['evidence'] = ['tests/test_feature.py']
        self.write('reports/P02.yaml', yaml.safe_dump(completed))
        _, errors = self.artifact_validate()
        self.assertTrue(any('accepted result is stale' in error for error in errors), errors)

    def test_task_artifacts_rejects_packet_snapshot_mismatch_or_null(self):
        accepted = [dict(assignment_id='P02', attempt=1, goal_version=1, snapshot='sha256:good')]
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report(status='approved', accepts=accepted)))
        completed = self.artifact_report(assignment_id='P02')
        completed['result']['assignment']['snapshot'] = 'sha256:other'
        completed['result']['evidence'] = ['tests/test_feature.py']
        self.write('reports/P02.yaml', yaml.safe_dump(completed))
        manifest = dict(version=1, owners={'P01': 'reviewer', 'P02': 'developer'}, reports=[
            dict(path='reports/P01.yaml', assignment_id='P01', attempt=1, goal_version=1, next_transition='assignments/R01.yaml', accepts=accepted),
            dict(path='reports/P02.yaml', assignment_id='P02', attempt=1, goal_version=1, next_transition='assignments/R01.yaml'),
        ])
        self.write('manifest.yaml', yaml.safe_dump(manifest))
        self.write('assignments/R01.yaml', '{}\n')
        _, errors = self.artifact_validate()
        self.assertTrue(any('accepted result is stale' in error for error in errors), errors)
        completed['result']['assignment']['snapshot'] = None
        self.write('reports/P02.yaml', yaml.safe_dump(completed))
        _, errors = self.artifact_validate()
        self.assertTrue(any('accepted result is stale' in error for error in errors), errors)

    def test_task_artifacts_validates_blocker_progress_shape(self):
        self.write('reports/P01.yaml', yaml.safe_dump(self.artifact_report()))
        envelope = dict(status='completed', artifact='reports/P01.yaml', assignment_id='P01', attempt=1,
                        profile='developer', accepts=None, finding_id='F01', progress='none', no_progress=None,
                        next_transition='assignments/R01.yaml')
        self.write('envelopes/P01.yaml', yaml.safe_dump(envelope))
        self.artifact_manifest(envelope='envelopes/P01.yaml')
        _, errors = self.artifact_validate()
        self.assertTrue(any('requires nonblank no_progress' in error for error in errors), errors)
        envelope.update(finding_id=None, progress='none', no_progress=dict(missing_input='x', next_check='y'))
        self.write('envelopes/P01.yaml', yaml.safe_dump(envelope))
        _, errors = self.artifact_validate()
        self.assertTrue(any('non-blocker envelope' in error for error in errors), errors)
        envelope.update(progress=None, no_progress=None)
        self.write('envelopes/P01.yaml', yaml.safe_dump(envelope))
        result, errors = self.artifact_validate()
        self.assertEqual('not_verified', result['status'])
        self.assertEqual([], errors)


if __name__ == '__main__':
    unittest.main()
