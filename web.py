"""Portable entry point for the optional FDE web starter."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).parent/'skills/fde-kit/scripts/web.py'), run_name='__main__')
