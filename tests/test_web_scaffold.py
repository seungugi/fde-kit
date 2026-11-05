"""Portable opt-in web scaffold contract; no web packages needed for these tests."""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT / '.test-tmp'
TMP.mkdir(exist_ok=True)


class WebScaffold(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TMP)
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name) / 'new project'

    def run_cli(self, *args, script=None):
        return subprocess.run([sys.executable, '-X', 'utf8', str(script or ROOT/'web.py'), *map(str,args)],
                              capture_output=True, text=True, encoding='utf-8')

    def test_new_generic_project_is_runnable_structure_with_local_assets_and_kit(self):
        result = self.run_cli('init', self.target)
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        for name in ['app/main.py','app/features.py','templates/base.html','static/htmx.min.js',
                     'requirements.txt','README.md','.agents/skills/fde-kit/SKILL.md','fde-notes/state.json']:
            self.assertTrue((self.target/name).is_file(), name)
        state = json.loads((self.target/'fde-notes/state.json').read_text(encoding='utf-8'))
        self.assertEqual(state['profile'], 'standard')
        self.assertFalse(list(self.target.rglob('*.sqlite3')))

    def test_existing_target_never_overwritten_even_if_empty(self):
        self.target.mkdir()
        marker=self.target/'my-file.txt'
        marker.write_text('user-owned',encoding='utf-8')
        before=hashlib.sha256(marker.read_bytes()).hexdigest()
        result=self.run_cli('init',self.target)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(hashlib.sha256(marker.read_bytes()).hexdigest(),before)
        self.assertEqual(list(self.target.iterdir()),[marker])

    def test_meal_overlay_is_explicit_and_retains_generic_infrastructure(self):
        result=self.run_cli('init',self.target,'--example','meal-planner')
        self.assertEqual(result.returncode,0,result.stderr+result.stdout)
        self.assertTrue((self.target/'app/planner.py').is_file())
        self.assertTrue((self.target/'templates/index.html').is_file())
        self.assertTrue((self.target/'data/menus.json').is_file())
        self.assertTrue((self.target/'app/security.py').is_file())
        self.assertIn('meal-planner', (self.target/'scaffold.json').read_text(encoding='utf-8'))

    def test_core_only_install_explains_missing_optional_assets_without_writing_target(self):
        core=Path(self.temp.name)/'core'
        initialized=subprocess.run([sys.executable,str(ROOT/'fde.py'),'init',str(core)],capture_output=True,text=True)
        self.assertEqual(initialized.returncode,0,initialized.stderr)
        result=self.run_cli('init',self.target,script=core/'.agents/skills/fde-kit/scripts/web.py')
        self.assertNotEqual(result.returncode,0)
        self.assertFalse(self.target.exists())
        self.assertIn('full', (result.stdout+result.stderr).lower())

    def test_invalid_example_cannot_escape_asset_root(self):
        result=self.run_cli('init',self.target,'--example','../../elsewhere')
        self.assertNotEqual(result.returncode,0)
        self.assertFalse(self.target.exists())

    def test_runtime_data_and_secrets_are_not_distributed_as_web_assets(self):
        source=Path(self.temp.name)/'skill'
        web=source/'assets/web/starter'
        for name in ['app/main.py', '.env', '.env.local', 'data/app.sqlite3',
                     'data/app.sqlite3-wal', 'data/cache.db-shm',
                     '.venv/pyvenv.cfg', '.pytest_cache/README.md']:
            path=web/name
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_text('fixture',encoding='utf-8')
        modules={}
        for name in ['fde','web']:
            spec=importlib.util.spec_from_file_location('test_'+name,ROOT/f'skills/fde-kit/scripts/{name}.py')
            module=importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            modules[name]=module
        self.assertEqual(set(modules['fde'].tree_hashes(source)),{'assets/web/starter/app/main.py'})
        copied=Path(self.temp.name)/'copied'
        modules['web'].copy_assets(web,copied)
        self.assertEqual({p.relative_to(copied).as_posix() for p in copied.rglob('*') if p.is_file()},
                         {'app/main.py'})


if __name__=='__main__':
    unittest.main()
