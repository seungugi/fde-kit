"""Repository entrypoint. Installed projects use .agents/skills/fde-kit/scripts/recipes.py."""
from pathlib import Path
import runpy
import sys

scripts = Path(__file__).resolve().parent / 'skills/fde-kit/scripts'
sys.path.insert(0, str(scripts))
runpy.run_path(str(scripts / 'recipes.py'), run_name='__main__')
