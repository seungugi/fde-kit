"""Run a complete local lifecycle in a NEW directory, using only this Python."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

kit = Path(__file__).resolve().parent
project = Path(sys.argv[1] if len(sys.argv) > 1 else 'fde-practice').resolve()
if project.exists():
    raise SystemExit('Choose a new directory; existing contents were preserved.')
shutil.copytree(kit / 'examples/request-priority', project,
                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))

def fde(*arguments):
    subprocess.run([sys.executable, str(kit / 'fde.py'), *map(str, arguments)], check=True)

fde('init', project, '--profile', 'competition', '--goal', 'Create a verified request queue')
(project / 'fde-notes/BRIEF.md').write_text(
    '# Request queue\n\nSource and acceptance: ../README.md.\n'
    'Expected sample request IDs: R3, R2, R1.\n'
    'Deliver result.json and a reproducible check; use local files only.\n', encoding='utf-8')
fde('add', project, 'T1', 'Generate and verify request queue', '--acceptance',
    'Sample order is R3,R2,R1; duplicate/conflict/reopening behavior follows README.',
    '--files', 'README.md', 'queue_requests.py', 'events.json', 'test_queue.py', 'check_delivery.py', 'result.json')
fde('start', project, 'T1')
subprocess.run([sys.executable, 'queue_requests.py', 'events.json', 'result.json'], cwd=project, check=True)
fde('ready', project, 'T1')
fde('verify', project, 'T1', '--', sys.executable, 'check_delivery.py')
result = json.loads((project / 'result.json').read_text(encoding='utf-8'))
assert [row['request_id'] for row in result] == ['R3', 'R2', 'R1']
# A harmless input-file edit still requires fresh evidence.
with (project / 'events.json').open('a', encoding='utf-8') as target:
    target.write('\n')
snapshot = subprocess.check_output([sys.executable, str(kit / 'fde.py'), 'status', str(project), '--json'], encoding='utf-8')
assert json.loads(snapshot)['tasks']['T1']['effective_status'] == 'needs_verification'
print('Input changed: old evidence correctly became needs_verification.', flush=True)
fde('verify', project, 'T1', '--', sys.executable, 'check_delivery.py')
fde('handoff', project)
fde('status', project)
print(f'\nDemo complete: {project}', flush=True)
