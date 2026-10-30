"""Independent sample acceptance checks; no imports from the recipe implementation."""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check(kind):
    require(kind in ('table', 'decide', 'search'), 'Choose a concrete acceptance check.')
    directory = ROOT / 'outputs' / kind
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    require(manifest['recipe'] == kind, 'Wrong recipe manifest.')
    input_root = ROOT / 'docs' if kind == 'search' else ROOT
    expected_inputs = {'operations.md'} if kind == 'search' else {'requests.csv', 'table.json' if kind == 'table' else 'decision.json'}
    require({s['path'] for s in manifest['inputs']} == expected_inputs, 'Input inventory changed.')
    if kind == 'search':
        require({p.relative_to(input_root).as_posix() for p in input_root.rglob('*') if p.is_file()} == expected_inputs,
                'Document inventory changed; regenerate and review expectations.')
    for source in manifest['inputs']:
        path = input_root / source['path']
        require(hashlib.sha256(path.read_bytes()).hexdigest() == source['sha256'], 'Source changed since generation.')
    package = ROOT / '.agents/skills/fde-kit/scripts/fde_recipes'
    require(set(manifest['implementation']) == {p.name for p in package.glob('*.py')}, 'Implementation inventory changed.')
    for name, expected in manifest['implementation'].items():
        require(hashlib.sha256((package / name).read_bytes()).hexdigest() == expected, 'Implementation changed since generation.')
    require(bool(manifest['artifacts']), 'Empty manifest is not evidence.')
    for name, expected in manifest['artifacts'].items():
        path = directory / name
        require(path.resolve().is_relative_to(directory.resolve()), 'Artifact escaped output directory.')
        require(hashlib.sha256(path.read_bytes()).hexdigest() == expected, 'Changed artifact: ' + name)
    result = json.loads((directory / 'result.json').read_text(encoding='utf-8'))
    if kind == 'table':
        require(result['counts'] == {'input': 9, 'accepted': 6, 'excluded': 3}, 'Row accounting mismatch.')
        groups = {g['team']: g for g in result['groups']}
        require(groups['ops']['metrics']['total_amount']['value'] == '20.4', 'Ops total must be 20.40.')
        require(groups['sales']['metrics']['total_amount']['value'] == '20.2', 'Sales total must be 20.20.')
        require(groups['sales']['metrics']['mean_amount']['nonmissing_count'] == 1, 'Missing amount became zero.')
        require([r['source_row'] for r in result['excluded']] == [4, 7, 8], 'Wrong excluded records.')
    elif kind == 'decide':
        queue = result['queue']
        require([r['id'] for r in queue] == ['003', '001', '002', '005', '006', '009', '004', '007', '008'], 'Wrong queue order.')
        require([r['outcome'] for r in queue[:3]] == ['critical', 'urgent', 'due'], 'Wrong rule result.')
        require(all(r['review_required'] and r['outcome'] == 'INVALID_INPUT' for r in queue[-3:]), 'Invalid row became normal.')
        require(queue[2]['trace'][-1]['checks'][0]['actual'] == '24', 'Exact boundary was not checked.')
    else:
        require(result['query'] == '긴급 요청 처리 기준', 'Wrong search question.')
        require(result['status'] == 'evidence_found' and result['hits'], 'Expected evidence was not retrieved.')
        require('24시간' in result['hits'][0]['excerpt'], 'Top evidence does not contain the required threshold.')
        for hit in result['hits']:
            path = ROOT / 'docs' / hit['path']
            require(path.resolve().is_relative_to((ROOT / 'docs').resolve()), 'Citation escaped document root.')
            raw = path.read_bytes()
            require(hashlib.sha256(raw).hexdigest() == hit['sha256'], 'Citation source changed.')
            expected = '\n'.join(raw.decode('utf-8-sig').splitlines()[hit['start_line'] - 1:hit['end_line']])
            require(expected == hit['excerpt'], 'Citation does not match source lines.')
    print(kind + ': independently checked sample acceptance and artifact hashes')


if __name__ == '__main__':
    try:
        require(len(sys.argv) == 2, 'Usage: check_delivery.py table|decide|search')
        check(sys.argv[1])
    except (ValueError, OSError, KeyError, TypeError, IndexError) as exc:
        raise SystemExit(str(exc))
