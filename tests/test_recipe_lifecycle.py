"""Installed-skill lifecycle, stale provenance and broken-output acceptance checks."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]


class RecipeLifecycle(unittest.TestCase):
    def test_installed_recipes_handoff_and_adversarial_acceptance(self):
        parent = KIT / '.test-tmp'
        parent.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=parent) as temporary:
            project = Path(temporary) / '공백 있는 연습'
            run = subprocess.run([sys.executable, str(KIT / 'demo_recipes.py'), str(project)],
                                 capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=40)
            self.assertEqual(run.returncode, 0, run.stdout + run.stderr)
            handoff = (project / 'fde-notes/HANDOFF.md').read_text(encoding='utf-8')
            self.assertIn('All registered tasks have current evidence', handoff)

            def check(kind, ok):
                run = subprocess.run([sys.executable, 'check_delivery.py', kind], cwd=project,
                                     capture_output=True, timeout=10)
                self.assertEqual(run.returncode == 0, ok, run.stdout + run.stderr)

            def status():
                run = subprocess.run([sys.executable, str(KIT / 'fde.py'), 'status', str(project), '--json'],
                                     capture_output=True, check=True, text=True, encoding='utf-8', timeout=10)
                return json.loads(run.stdout)

            data = project / 'requests.csv'
            original = data.read_bytes()
            data.write_bytes(original.replace(b'10.10', b'11.10'))
            check('table', False)  # Old aggregates cannot become evidence for the new input.
            self.assertEqual(status()['tasks']['T1']['effective_status'], 'needs_verification')
            self.assertEqual(status()['tasks']['T2']['effective_status'], 'needs_verification')
            data.write_bytes(original)

            extra = project / 'docs/new-policy.md'
            extra.write_text('New policy', encoding='utf-8')
            check('search', False)  # Independent checker reconciles the entire example inventory.
            extra.unlink()

            output = project / 'outputs/table/result.json'
            original = output.read_bytes()
            output.write_bytes(original + b'\n')
            check('table', False)
            output.write_bytes(original)

            implementation = project / '.agents/skills/fde-kit/scripts/fde_recipes/table.py'
            original = implementation.read_bytes()
            implementation.write_bytes(original + b'\n# changed after generation\n')
            check('table', False)
            implementation.write_bytes(original)
            for kind in ('table', 'decide', 'search'):
                check(kind, True)


if __name__ == '__main__':
    unittest.main()
