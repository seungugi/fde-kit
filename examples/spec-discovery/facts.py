"""Reproduce observations from the synthetic sample, without inferring policy."""
import csv
from datetime import date
import json
from pathlib import Path


def main():
    source = Path(__file__).parent / 'task' / 'arrivals.csv'
    with source.open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream))
    days = sorted({row['date'] for row in rows})
    gaps = [max(int(row['arrivals']) - int(row['capacity']), 0) for row in rows]
    result = {
        'rows': len(rows),
        'dates': days,
        'weekday_numbers_monday_0': sorted({date.fromisoformat(day).weekday() for day in days}),
        'observed_hours': sorted({int(row['hour']) for row in rows}),
        'total_observed_arrivals': sum(int(row['arrivals']) for row in rows),
        'observed_gap_by_input_row': gaps,
        'total_observed_gap': sum(gaps),
        'over_capacity_rows': sum(gap > 0 for gap in gaps),
        'duplicate_date_hour_keys': len(rows) - len({(r['date'], r['hour']) for r in rows}),
        'blank_cells': sum(value == '' for row in rows for value in row.values()),
        'limit': 'Unobserved dates/hours and unrecorded visitors are unknown, not zero.',
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
