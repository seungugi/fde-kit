"""Independent expectations from README.md; does not import product logic."""
import argparse
import json
from pathlib import Path
import sys

# These values come from the example's agreed cases, not a generator's output.
EXPECTED = [
    {'id': 'R1', 'status': 'pending', 'remaining': 'Attach labels'},
    {'id': 'R2', 'status': 'complete', 'remaining': ''},
    {'id': 'R3', 'status': 'review', 'remaining': 'Confirm changed quantity'},
]


def main():
    parser = argparse.ArgumentParser(description='Check this example only; adapt expectations to your actual requirement.')
    parser.add_argument('result', type=Path)
    args = parser.parse_args()
    try:
        actual = json.loads(args.result.read_text(encoding='utf-8'))
    except (OSError, UnicodeError, ValueError) as error:
        print(f'Cannot read result: {error}', file=sys.stderr)
        return 2
    if actual != EXPECTED:
        print('Business expectation mismatch: compare IDs, order, status and remaining actions with README.md.', file=sys.stderr)
        return 1
    print('Agreed example outcomes match.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
