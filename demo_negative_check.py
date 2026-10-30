"""Show that a plausible wrong result fails; only temporary copies are changed."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

kit = Path(__file__).resolve().parent
example = kit / 'skills/fde-kit/assets/verification-example'
temp_root = kit / '.test-tmp'
temp_root.mkdir(exist_ok=True)
original = (example / 'result.json').read_bytes()
with tempfile.TemporaryDirectory(prefix='negative-', dir=temp_root) as directory:
    folder = Path(directory).resolve()
    folder.relative_to(temp_root.resolve())
    good = folder / 'good.json'
    bad = folder / 'wrong.json'
    good.write_bytes(original)
    wrong = json.loads(original)
    wrong[0]['status'] = 'complete'
    wrong[0]['remaining'] = ''
    bad.write_text(json.dumps(wrong), encoding='utf-8')
    for path, expected_exit in [(good, 0), (bad, 1)]:
        result = subprocess.run([sys.executable, str(example / 'check_result.py'), str(path)],
                                capture_output=True, text=True, encoding='utf-8')
        if result.returncode != expected_exit:
            raise SystemExit(f'Unexpected checker outcome: {path.name}: {result.returncode}\n{result.stdout}{result.stderr}')
        print(f'{path.name}: checker exit {result.returncode}, expected {expected_exit}')
if (example / 'result.json').read_bytes() != original:
    raise SystemExit('Original example unexpectedly changed.')
print('PASS: same row count and IDs, but wrong business outcome rejected. Original preserved.')
