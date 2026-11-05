"""Create a new web project from optional local assets; never overwrite a project."""
import argparse
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

SKILL = Path(__file__).resolve().parents[1]
ASSETS = SKILL/'assets/web'
IGNORED = {'__pycache__', '.pytest_cache', '.test-tmp', '.git', '.venv'}


def copy_assets(source, target):
    for path in sorted(source.rglob('*')):
        relative=path.relative_to(source)
        if any(part in IGNORED for part in relative.parts):
            continue
        if path.is_symlink() or (hasattr(path,'is_junction') and path.is_junction()):
            raise ValueError('Asset links are not supported')
        if path.is_file():
            if (path.suffix in {'.pyc','.sqlite3','.db'}
                    or re.search(r'\.(sqlite3|db)-(wal|shm|journal)$',path.name)
                    or path.name == '.env' or path.name.startswith('.env.')):
                continue
            destination=target/relative
            destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(path,destination)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    commands=parser.add_subparsers(dest='command',required=True)
    init=commands.add_parser('init')
    init.add_argument('target',type=Path)
    init.add_argument('--example',choices=['meal-planner'])
    init.add_argument('--profile',choices=['standard','competition'],default='standard')
    args=parser.parse_args()
    target=args.target.expanduser().absolute()
    # lexists also rejects a dangling symlink, which must never be replaced.
    if os.path.lexists(target):
        parser.error('Target already exists. Choose a new directory; existing files are never overwritten.')
    source=ASSETS/'starter'
    if not (source/'app/main.py').is_file():
        parser.error('Web assets are missing in this core installation. Use web.py from the full kit repository, or install that same version with init --full.')
    overlay=ASSETS/'examples'/args.example if args.example else None
    if overlay and not (overlay/'app/features.py').is_file():
        parser.error('Requested example is unavailable in this installation.')
    target.parent.mkdir(parents=True,exist_ok=True)
    try:
        with tempfile.TemporaryDirectory(prefix='.fde-web-',dir=target.parent) as temporary:
            stage=Path(temporary)/'project'
            stage.mkdir()
            copy_assets(source,stage)
            if overlay:
                copy_assets(overlay,stage)
            manifest={'schema':1,'stack':['FastAPI','Jinja2','HTMX','SQLite','pytest'],
                      'example':args.example,'profile':args.profile,'source':'FDE Kit optional local web assets'}
            (stage/'scaffold.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            result=subprocess.run([sys.executable,'-X','utf8',str(SKILL/'scripts/fde.py'),'init',str(stage),
                                   '--profile',args.profile,'--goal','Implement and explain the web service using confirmed requirements'],
                                  capture_output=True,text=True,encoding='utf-8',timeout=60)
            if result.returncode:
                raise ValueError('FDE initialization failed: '+(result.stderr or result.stdout).strip())
            # Refuse a target created concurrently. All setup happens in our owned stage.
            if os.path.lexists(target):
                raise ValueError('Target was created during setup; left unchanged.')
            stage.rename(target)
    except (OSError,ValueError,subprocess.SubprocessError) as exc:
        print('Web scaffold failed: '+str(exc),file=sys.stderr)
        return 2
    print('Created: '+str(target))
    print('Example: '+(args.example or 'generic item board'))
    print('FDE Kit: project-local workflow installed; dependencies and server are not started automatically.')
    print('Next: open README.md in the generated project.')
    return 0


if __name__=='__main__':
    raise SystemExit(main())
