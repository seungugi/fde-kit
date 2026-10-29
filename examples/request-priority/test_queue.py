import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from queue_requests import build_queue


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.events = json.loads(Path(__file__).with_name('events.json').read_text(encoding='utf-8'))

    def test_example_order_and_reopened_request(self):
        self.assertEqual([row['request_id'] for row in build_queue(self.events)], ['R3', 'R2', 'R1'])

    def test_empty(self):
        self.assertEqual(build_queue([]), [])

    def test_conflicting_event_is_rejected(self):
        self.events.append({**self.events[0], 'status': 'done'})
        with self.assertRaises(ValueError):
            build_queue(self.events)

    def test_ambiguous_version_is_rejected(self):
        self.events.append({**self.events[0], 'event_id': 'different'})
        with self.assertRaises(ValueError):
            build_queue(self.events)

    def test_input_order_does_not_change_latest_version(self):
        self.assertEqual(build_queue(self.events), build_queue(list(reversed(self.events))))

    def test_command_line_writes_expected_output(self):
        folder = Path(__file__).resolve().parent
        with tempfile.TemporaryDirectory(prefix='queue-check-', dir=folder) as temp:
            Path(temp).resolve().relative_to(folder)
            output = Path(temp) / 'result.json'
            subprocess.run([sys.executable, str(folder / 'queue_requests.py'),
                            str(folder / 'events.json'), str(output)], check=True)
            result = json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual([row['request_id'] for row in result], ['R3', 'R2', 'R1'])


if __name__ == '__main__':
    unittest.main()
