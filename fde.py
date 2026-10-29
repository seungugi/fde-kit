"""Portable launcher; the installed skill includes the same CLI."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).parent / 'skills/fde-kit/scripts/fde.py'), run_name='__main__')
