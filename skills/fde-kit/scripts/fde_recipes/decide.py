"""Ordered, declarative rules: no eval, arbitrary functions or actions."""
from collections import Counter

from .common import (dump, keys, load_json, markdown, number, publish,
                     read_rows, require, typed_rows)


def outcome(spec, allowed):
    keys(spec, allowed, ('outcome', 'priority', 'review'))
    require(isinstance(spec['outcome'], str) and spec['outcome'].strip(), 'outcome must be a nonempty label.')
    require(type(spec['priority']) is int and 0 <= spec['priority'] <= 999999, 'priority must be integer 0..999999 (smaller first).')
    require(type(spec['review']) is bool, 'review must be boolean.')


def prepare(config, columns):
    require(isinstance(config['rules'], list) and 0 < len(config['rules']) <= 100, 'Declare 1..100 rules.')
    seen, prepared = set(), []
    for rule in config['rules']:
        outcome(rule, ('id', 'all', 'outcome', 'priority', 'review', 'source'))
        require(isinstance(rule.get('id'), str) and rule['id'].strip() and rule['id'] not in seen,
                'Rule IDs must be nonempty and unique.')
        require(isinstance(rule.get('source'), str) and rule['source'].strip(), 'Each rule needs a source/decision reference.')
        seen.add(rule['id'])
        conditions = rule.get('all')
        require(isinstance(conditions, list) and 0 < len(conditions) <= 30, 'Each rule needs 1..30 conditions (no vacuous match).')
        tests = []
        for test in conditions:
            keys(test, ('column', 'op', 'value'), ('column', 'op', 'value'))
            col, op, value = test['column'], test['op'], test['value']
            require(isinstance(col, str) and col in columns, 'Condition names an undeclared column.')
            require(isinstance(op, str) and op in ('eq', 'ne', 'lt', 'le', 'gt', 'ge', 'in', 'not_in'), 'Unknown condition operator.')
            values = value if op in ('in', 'not_in') else [value]
            require(isinstance(values, list) and 0 < len(values) <= 100, 'Membership requires a nonempty bounded list.')
            if columns[col]['type'] == 'number':
                values = [number(v) for v in values]
            else:
                require(op in ('eq', 'ne', 'in', 'not_in') and all(isinstance(v, str) for v in values),
                        'String conditions support eq/ne/in/not_in and string values only.')
            tests.append((col, op, values))
        prepared.append((rule, tests))
    outcome(config['default'], ('outcome', 'priority', 'review', 'source'))
    require(isinstance(config['default'].get('source'), str) and config['default']['source'].strip(), 'Default needs a source.')
    return prepared


def matches(value, op, limits):
    if value is None:
        return None  # Unknown is not false, "not equal" or "not in".
    bound = limits[0]
    return {'eq': lambda: value == bound, 'ne': lambda: value != bound,
            'lt': lambda: value < bound, 'le': lambda: value <= bound,
            'gt': lambda: value > bound, 'ge': lambda: value >= bound,
            'in': lambda: value in limits, 'not_in': lambda: value not in limits}[op]()


def run(args):
    config, config_source = load_json(args.config)
    keys(config, ('schema', 'rules', 'default'), ('schema', 'rules', 'default'))
    rows, header, source = read_rows(args.input)
    good, bad = typed_rows(rows, header, config['schema'])
    prepared = prepare(config, config['schema']['columns'])
    require(len(good) * sum(len(tests) for _, tests in prepared) <= 100000,
            'Rule evaluation budget exceeds 100000 checks; reduce rows or rules.')
    results = []
    id_col = config['schema'].get('id_column')
    for row in good:
        trace, selected = [], None
        for rule, tests in prepared:
            checks = [{'column': col, 'actual': row['values'][col], 'operator': op,
                       'expected': values, 'matched': matches(row['values'][col], op, values)}
                      for col, op, values in tests]
            passed = (False if any(t['matched'] is False for t in checks) else
                      None if any(t['matched'] is None for t in checks) else True)
            trace.append({'rule_id': rule['id'], 'matched': passed, 'checks': checks})
            if passed is None:
                selected = {'id': rule['id'], 'outcome': 'INDETERMINATE_RULE', 'priority': None,
                            'review': True, 'source': rule['source']}
                break
            if passed:
                selected = rule
                break
        selected = selected or config['default']
        results.append({'source_row': row['source_row'],
                        'id': row['values'][id_col] if id_col else str(row['source_row']),
                        'values': row['values'], 'outcome': selected['outcome'],
                        'priority': selected['priority'], 'review_required': selected['review'],
                        'rule_id': selected.get('id', 'DEFAULT'), 'source': selected['source'], 'trace': trace})
    for row in bad:
        results.append({'source_row': row['source_row'], 'id': row['raw'].get(id_col) if id_col else str(row['source_row']),
                        'outcome': 'INVALID_INPUT', 'priority': None, 'review_required': True,
                        'rule_id': None, 'errors': row['errors'], 'raw': row['raw']})
    results.sort(key=lambda r: (r['review_required'], r['priority'] if r['priority'] is not None else 1000000,
                                str(r['id']), r['source_row']))
    report = {'status': 'review_required' if any(r['review_required'] for r in results) else 'complete',
              'counts': {'input': len(rows), 'valid': len(good), 'invalid': len(bad),
                         'outcomes': dict(sorted(Counter(r['outcome'] for r in results).items()))},
              'policy': 'First matching rule wins; review rows last, then ascending priority, ID, source_row. No external actions.',
              'queue': results}
    lines = ['# Decision queue', '', 'Classification only. A matched rule is not authorization to act.',
             'Review-required and invalid rows are separated by the review_required flag.', '',
             '| ID | Outcome | Priority | Review | Rule | Data record |', '|---|---|---:|---|---|---:|']
    for row in results[:100]:
        lines.append('| ' + ' | '.join(markdown(row[k]) for k in ('id', 'outcome', 'priority', 'review_required', 'rule_id', 'source_row')) + ' |')
    lines += ['', 'Full queue, evaluated conditions, original values and sources: result.json.']
    return publish(args.out, {'result.json': dump(report), 'report.md': '\n'.join(lines) + '\n'},
                   [source, config_source], 'decide', [args.input, args.config])
