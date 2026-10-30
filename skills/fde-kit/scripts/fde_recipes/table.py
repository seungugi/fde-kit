"""Schema-driven cleaning and exact-decimal aggregation."""
from decimal import Decimal, localcontext

from .common import (csv_text, dump, keys, load_json, markdown, publish,
                     read_rows, require, typed_rows)


def run(args):
    config, config_source = load_json(args.config)
    keys(config, ('schema', 'group_by', 'aggregates'), ('schema', 'aggregates'))
    rows, header, source = read_rows(args.input)
    good, bad = typed_rows(rows, header, config['schema'])
    groups = config.get('group_by', [])
    require(isinstance(groups, list) and len(groups) <= 8 and len(set(groups)) == len(groups)
            and all(g in header for g in groups), 'group_by must contain unique declared columns.')
    aggregates = config['aggregates']
    require(isinstance(aggregates, dict) and 0 < len(aggregates) <= 20, 'Declare 1..20 aggregates.')
    for name, spec in aggregates.items():
        require(isinstance(name, str) and name.strip(), 'Aggregate name must be nonempty.')
        keys(spec, ('column', 'op'), ('column', 'op'))
        require(spec['column'] in header and config['schema']['columns'][spec['column']]['type'] == 'number',
                'Aggregate column must be numeric.')
        require(spec['op'] in ('sum', 'mean', 'min', 'max'), 'Unknown aggregate operation.')
    require(good, 'No valid rows; inspect the data/schema. No successful report was published.')
    buckets = {}
    for item in good:
        key = tuple(item['values'][g] for g in groups)
        buckets.setdefault(key, []).append(item['values'])
    require(len(buckets) * len(aggregates) <= 100000, 'Too many group/metric combinations.')
    result = []
    for group, members in sorted(buckets.items(), key=lambda kv: dump(kv[0])):
        entry = {'group': dict(zip(groups, group)), 'row_count': len(members), 'metrics': {}}
        for name, spec in aggregates.items():
            numbers = [r[spec['column']] for r in members if r[spec['column']] is not None]
            value = None
            if numbers:
                with localcontext() as ctx:
                    ctx.prec = 160
                    value = {'sum': lambda: sum(numbers, Decimal(0)),
                             'mean': lambda: sum(numbers, Decimal(0)) / len(numbers),
                             'min': lambda: min(numbers), 'max': lambda: max(numbers)}[spec['op']]()
            entry['metrics'][name] = {'value': value, 'nonmissing_count': len(numbers), 'operation': spec['op']}
        result.append(entry)
    report = {'status': 'complete_with_exclusions' if bad else 'complete',
              'counts': {'input': len(rows), 'accepted': len(good), 'excluded': len(bad)},
              'groups': result, 'accepted': good, 'excluded': bad,
              'semantics': 'Numbers are decimal strings. Missing optional numbers are not zero; denominator is nonmissing_count.'}
    lines = ['# Data report', '', f'Input {len(rows)} = accepted {len(good)} + excluded {len(bad)}.',
             'Aggregates describe accepted records only; exclusions can bias conclusions.', '',
             '| Group | Rows | Metric | Value | Nonmissing denominator |', '|---|---:|---|---|---:|']
    for entry in result[:100]:
        label = ', '.join(f"{g}={entry['group'][g]}" for g in groups) or 'all'
        for name, metric in entry['metrics'].items():
            lines.append(f"| {markdown(label)} | {entry['row_count']} | {markdown(name)} | {markdown(metric['value'])} | {metric['nonmissing_count']} |")
    lines += ['', 'Full groups, row references and exclusion reasons: result.json.',
              'clean.csv is a spreadsheet-safe display export; canonical values remain in result.json.']
    numeric = [k for k, v in config['schema']['columns'].items() if v['type'] == 'number']
    return publish(args.out, {'result.json': dump(report), 'report.md': '\n'.join(lines) + '\n',
                             'clean.csv': csv_text([r['values'] for r in good], header, numeric)},
                   [source, config_source], 'table', [args.input, args.config])
