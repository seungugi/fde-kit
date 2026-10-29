"""Verify both behavior and the actual delivered sample file."""
import json
from pathlib import Path
import subprocess
import sys

folder = Path(__file__).resolve().parent
subprocess.run([sys.executable, '-m', 'unittest', '-v', 'test_queue'], cwd=folder, check=True)
actual = json.loads((folder / 'result.json').read_text(encoding='utf-8'))
# Derived from the example's explicit input and rules, not from the implementation.
expected = [
    {'event_id': 'e4', 'request_id': 'R3', 'version': 2, 'status': 'open', 'priority': 1, 'received_at': '2026-01-02'},
    {'event_id': 'e2', 'request_id': 'R2', 'version': 1, 'status': 'open', 'priority': 1, 'received_at': '2026-01-03'},
    {'event_id': 'e1', 'request_id': 'R1', 'version': 1, 'status': 'open', 'priority': 2, 'received_at': '2026-01-01'},
]
if actual != expected:
    raise SystemExit('Delivered result.json differs from the independently specified expected result.')
print('Delivered result.json: exact expected sample verified.')
