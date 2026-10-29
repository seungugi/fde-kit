"""Small example with explicit ordering rules; see README.md."""
from datetime import date
import json
from pathlib import Path
import sys


def build_queue(events):
    seen, versions, latest = {}, {}, {}
    for event in events:
        for field in ['event_id', 'request_id', 'status', 'received_at']:
            if not isinstance(event[field], str) or not event[field]:
                raise ValueError(f'Invalid {field}')
        if event['status'] not in ('open', 'done'):
            raise ValueError('Unknown status')
        if type(event['version']) is not int or type(event['priority']) is not int:
            raise ValueError('Version and priority must be integers')
        if date.fromisoformat(event['received_at']).isoformat() != event['received_at']:
            raise ValueError('Expected YYYY-MM-DD')
        event_id, request_id = event['event_id'], event['request_id']
        if event_id in seen:
            if seen[event_id] != event:
                raise ValueError('Conflicting event_id: ' + event_id)
            continue
        seen[event_id] = event
        version_key = request_id, event['version']
        if version_key in versions:
            raise ValueError('Ambiguous request version: ' + request_id)
        versions[version_key] = event
        if request_id not in latest or event['version'] > latest[request_id]['version']:
            latest[request_id] = event
    pending = [dict(event) for event in latest.values() if event['status'] == 'open']
    return sorted(pending, key=lambda event: (event['priority'], event['received_at'], event['request_id']))


if __name__ == '__main__':
    events = json.loads(Path(sys.argv[1]).read_text(encoding='utf-8'))
    result = build_queue(events)
    Path(sys.argv[2]).write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
