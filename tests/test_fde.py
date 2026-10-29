import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import runpy

KIT = Path(__file__).resolve().parents[1]
CLI = KIT / 'fde.py'


class KitBehavior(unittest.TestCase):
    def setUp(self):
        self.temp_root = KIT / '.test-tmp'
        self.temp_root.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='run-', dir=self.temp_root)
        self.project = Path(self.temp.name) / 'project'
        self.project.mkdir()

    def tearDown(self):
        Path(self.temp.name).resolve().relative_to(self.temp_root.resolve())
        self.temp.cleanup()

    def call(self, *args, ok=0):
        result = subprocess.run([sys.executable, str(CLI), *map(str, args)],
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertEqual(result.returncode, ok, result.stdout + result.stderr)
        return result

    def init(self):
        self.call('init', self.project, '--profile', 'competition', '--goal', 'Check orders')

    def add(self, name='T1', dependencies=()):
        (self.project / (name + '.txt')).write_text('ready', encoding='utf-8')
        args = ['add', self.project, name, 'Validate ' + name,
                '--acceptance', 'Declared artifact contains ready', '--files', name + '.txt']
        if dependencies:
            args += ['--depends', *dependencies]
        self.call(*args)

    def verify(self, name='T1', code=None, ok=0):
        code = code or f"from pathlib import Path; assert Path('{name}.txt').read_text() == 'ready'"
        return self.call('verify', self.project, name, '--', sys.executable, '-c', code, ok=ok)

    def state(self):
        return json.loads(self.call('status', self.project, '--json').stdout)

    def status(self, name='T1'):
        return self.state()['tasks'][name]['effective_status']

    def test_init_is_local_preserves_user_files_and_is_repeatable(self):
        agents = self.project / 'AGENTS.md'
        original = b'# Project rules\r\nKeep existing behavior.\r\n'
        agents.write_bytes(original)
        self.init()
        self.assertTrue(agents.read_bytes().startswith(original))
        first = agents.read_bytes()
        brief = self.project / 'fde-notes' / 'BRIEF.md'
        brief.write_text('User-edited requirements', encoding='utf-8')
        self.init()
        self.assertEqual(agents.read_bytes(), first)
        self.assertEqual(brief.read_text(), 'User-edited requirements')
        self.assertTrue((self.project / '.agents/skills/fde-kit/SKILL.md').is_file())
        self.assertFalse((self.project / '.codex/config.toml').exists())

    def test_modified_installed_skill_is_not_overwritten(self):
        self.init()
        skill = self.project / '.agents/skills/fde-kit/SKILL.md'
        skill.write_text('custom skill', encoding='utf-8')
        self.call('init', self.project, ok=2)
        self.assertEqual(skill.read_text(), 'custom skill')

    def test_launch_preview_is_read_only_and_uses_project_goal(self):
        self.init()
        state = self.project / 'fde-notes/state.json'
        before = state.read_bytes()
        result = self.call('launch', self.project, '--print-prompt')
        self.assertIn('Check orders', result.stdout)
        self.assertIn('competition', result.stdout)
        self.assertEqual(state.read_bytes(), before)

    def test_launch_uses_provided_codex_in_task_directory(self):
        self.init()
        module = runpy.run_path(str(KIT / 'skills/fde-kit/scripts/fde.py'))
        with patch('shutil.which', return_value='provided-codex') as lookup, \
                patch('subprocess.run') as run:
            run.return_value.returncode = 7
            self.assertEqual(module['main'](['launch', str(self.project)]), 7)
        lookup.assert_called_once_with('codex')
        command = run.call_args.args[0]
        self.assertEqual(len(command), 2)
        self.assertEqual(command[0], 'provided-codex')
        self.assertIn('Check orders', command[1])
        self.assertEqual(run.call_args.kwargs, {'cwd': self.project.resolve()})

    def test_ready_is_not_verified_and_success_requires_actual_run(self):
        self.init()
        self.add()
        self.call('start', self.project, 'T1')
        self.call('ready', self.project, 'T1')
        self.assertEqual(self.status(), 'implemented')
        self.verify()
        self.assertEqual(self.status(), 'verified')
        attempt = self.state()['tasks']['T1']['attempts'][-1]
        self.assertEqual(attempt['exit_code'], 0)
        self.assertTrue((self.project / attempt['log']).is_file())

    def test_source_brief_and_goal_changes_invalidate_evidence(self):
        self.init()
        self.add()
        self.verify()
        watched = self.project / 'T1.txt'
        watched.write_text('changed')
        self.assertEqual(self.status(), 'needs_verification')
        watched.write_text('ready')
        self.verify()
        (self.project / 'fde-notes/BRIEF.md').write_text('Revised boundary condition')
        self.assertEqual(self.status(), 'needs_verification')
        self.verify()
        self.call('intent', self.project, '--goal', 'New scope', '--reason', 'User changed requirements')
        self.assertEqual(self.status(), 'needs_verification')
        self.assertEqual(self.state()['intent']['revision'], 2)

    def test_dependencies_block_execution_and_invalidate_transitively(self):
        self.init()
        self.add('T1')
        self.add('T2', ['T1'])
        self.add('T3', ['T2'])
        self.call('start', self.project, 'T2', ok=2)
        self.verify('T1')
        self.verify('T2')
        self.verify('T3')
        (self.project / 'T1.txt').write_text('changed')
        self.assertEqual(self.status('T3'), 'needs_verification')
        (self.project / 'T1.txt').write_text('ready')
        self.verify('T1')
        self.assertEqual(self.status('T2'), 'needs_verification')

    def test_failure_is_recorded_and_cannot_reuse_old_success(self):
        self.init()
        self.add()
        self.verify()
        self.verify(code="print('actual failure'); raise SystemExit(7)", ok=1)
        self.assertEqual(self.status(), 'failed')
        attempt = self.state()['tasks']['T1']['attempts'][-1]
        self.assertEqual(attempt['exit_code'], 7)
        self.assertIn('actual failure', (self.project / attempt['log']).read_text())

    def test_running_verification_does_not_display_previous_success(self):
        self.init()
        self.add()
        self.verify()
        self.verify(code="import json; from pathlib import Path; s=json.loads(Path('fde-notes/state.json').read_text()); assert s['tasks']['T1']['status'] == 'verifying'")
        self.assertEqual(self.status(), 'verified')

    def test_changed_evidence_log_requires_reverification(self):
        self.init()
        self.add()
        self.verify()
        attempt = self.state()['tasks']['T1']['attempts'][-1]
        (self.project / attempt['log']).write_text('edited evidence')
        self.assertEqual(self.status(), 'needs_verification')

    def test_timeout_is_recorded_as_failure(self):
        self.init()
        self.add()
        self.call('verify', '--timeout', '0.2', self.project, 'T1', '--',
                  sys.executable, '-c', 'import time; time.sleep(5)', ok=1)
        self.assertEqual(self.status(), 'failed')
        self.assertTrue(self.state()['tasks']['T1']['attempts'][-1]['timed_out'])

    def test_verify_cannot_mutate_its_inputs_and_claim_success(self):
        self.init()
        self.add()
        self.verify(code="from pathlib import Path; Path('T1.txt').write_text('mutated')", ok=1)
        self.assertEqual(self.status(), 'failed')

    def test_dependency_changed_during_verification_is_not_accepted(self):
        self.init()
        self.add('T1')
        self.add('T2', ['T1'])
        self.verify('T1')
        self.verify('T2', code="from pathlib import Path; Path('T1.txt').write_text('changed')", ok=1)
        self.assertNotEqual(self.status('T2'), 'verified')

    def test_declared_file_must_exist_for_verification(self):
        self.init()
        self.add()
        (self.project / 'T1.txt').unlink()
        self.verify(ok=2)
        self.assertNotEqual(self.status(), 'verified')

    def test_path_escape_and_unknown_dependency_rejected(self):
        self.init()
        self.call('add', self.project, 'bad', 'Bad', '--acceptance', 'Do work',
                  '--files', '../outside.txt', ok=2)
        self.call('add', self.project, 'bad', 'Bad', '--acceptance', 'Do work',
                  '--files', 'a.txt', '--depends', 'unknown', ok=2)

    def test_parallel_file_ownership_and_state_lock(self):
        self.init()
        self.add()
        self.call('add', self.project, 'T2', 'Other writer', '--acceptance', 'Correct', '--files', 'T1.txt')
        self.call('start', self.project, 'T1')
        self.call('start', self.project, 'T2', ok=2)
        (self.project / 'fde-notes/.lock').write_text('another writer')
        self.call('ready', self.project, 'T1', ok=2)
        self.assertEqual(self.status(), 'doing')

    def test_handoff_reports_current_state_and_preserves_user_notes(self):
        self.init()
        self.add()
        self.verify()
        (self.project / 'T1.txt').write_text('changed')
        self.call('handoff', self.project)
        handoff = (self.project / 'fde-notes/HANDOFF.md').read_text(encoding='utf-8')
        self.assertIn('needs_verification', handoff)
        self.assertIn('T1.txt', handoff)
        self.assertIn('T1', handoff)
        self.assertIn('Check orders', handoff)

    def test_demo_verification_rechecks_the_delivered_file(self):
        demo = self.project / 'delivery-demo'
        result = subprocess.run([sys.executable, str(KIT / 'demo.py'), str(demo)],
                                capture_output=True, text=True, encoding='utf-8', timeout=25)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        saved = json.loads((demo / 'fde-notes/state.json').read_text(encoding='utf-8'))
        command = saved['tasks']['T1']['attempts'][-1]['command']
        self.call('verify', demo, 'T1', '--', *command)
        (demo / 'result.json').write_text('this is not valid JSON')
        self.call('verify', demo, 'T1', '--', *command, ok=1)

    def test_new_project_has_user_led_control_and_no_invented_rubric(self):
        self.init()
        state = self.state()
        self.assertEqual(state['control'], 'user-led')
        self.assertEqual(state['criteria'], {})
        coverage = json.loads(self.call('coverage', self.project, '--json').stdout)
        self.assertEqual(coverage['official_criteria'], 0)
        self.assertNotIn('estimated_score', coverage)

    def test_rubric_coverage_requires_linked_current_evidence(self):
        self.init()
        self.call('criterion', self.project, 'R1', 'Correct orders', '--source', 'README section 2', '--basis', 'official', '--points', '20')
        self.call('criterion', self.project, 'R2', 'Explain tradeoffs', '--source', 'Practice hypothesis', '--basis', 'assumed')
        (self.project / 'T1.txt').write_text('ready')
        self.call('add', self.project, 'T1', 'Validate orders', '--acceptance', 'Correct sample',
                  '--files', 'T1.txt', '--criteria', 'R1')
        self.verify()
        coverage = json.loads(self.call('coverage', self.project, '--json').stdout)
        self.assertEqual(coverage['criteria']['R1']['coverage'], 'evidence_available')
        self.assertEqual(coverage['criteria']['R2']['coverage'], 'unmapped')
        self.call('criterion', self.project, 'R1', 'Correct orders including cancelled',
                  '--source', 'README section 2 updated', '--basis', 'official', '--points', '20')
        self.assertEqual(self.status(), 'needs_verification')
        coverage = json.loads(self.call('coverage', self.project, '--json').stdout)
        self.assertEqual(coverage['criteria']['R1']['coverage'], 'needs_evidence')

    def test_assumed_criteria_cannot_claim_official_points(self):
        self.init()
        self.call('criterion', self.project, 'R1', 'Nice UI', '--source', 'My guess',
                  '--basis', 'assumed', '--points', '30', ok=2)
        self.call('criterion', self.project, 'R1', 'Nice UI', '--source', '', '--basis', 'official', ok=2)
        self.call('criterion', self.project, 'R1', 'Nice UI', '--source', 'Rubric',
                  '--basis', 'official', '--points', 'nan', ok=2)
        self.call('add', self.project, 'T1', 'Work', '--acceptance', 'Works', '--files', 'a.py', '--criteria', 'missing', ok=2)

    def test_reregistering_same_criterion_invalidates_previous_evidence(self):
        self.init()
        criterion = ['criterion', self.project, 'R1', 'Correct orders',
                     '--source', 'README section 2', '--basis', 'official']
        self.call(*criterion)
        (self.project / 'T1.txt').write_text('ready')
        self.call('add', self.project, 'T1', 'Validate orders', '--acceptance', 'Correct sample',
                  '--files', 'T1.txt', '--criteria', 'R1')
        self.verify()
        self.assertEqual(self.status(), 'verified')
        self.call(*criterion)
        self.assertEqual(self.status(), 'needs_verification')
        coverage = json.loads(self.call('coverage', self.project, '--json').stdout)
        self.assertEqual(coverage['criteria']['R1']['coverage'], 'needs_evidence')
        self.verify()
        self.assertEqual(self.status(), 'verified')

    def test_coverage_appears_in_handoff(self):
        self.init()
        self.call('criterion', self.project, 'R1', 'Explain decision', '--source', 'Official guide p4', '--basis', 'official')
        self.call('handoff', self.project)
        handoff = (self.project / 'fde-notes/HANDOFF.md').read_text(encoding='utf-8')
        self.assertIn('R1', handoff)
        self.assertIn('unmapped', handoff)
        self.assertIn('Official guide p4', handoff)


if __name__ == '__main__':
    unittest.main()
