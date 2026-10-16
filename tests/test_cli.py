import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from test_zones import frame, ZONE


class CommandTests(unittest.TestCase):
    def run_cli(self, rows, configuration=None):
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "zones.json"
            config.write_text(json.dumps(configuration or {"zones": [ZONE], "confirm_frames": 3}), encoding="utf-8")
            return subprocess.run([sys.executable, "-m", "guardianedge", "--config", str(config)],
                                  input=rows, capture_output=True, text=True)

    def test_jsonl_stream_produces_one_incident_from_three_inside_frames(self):
        result = self.run_cli("\n".join(json.dumps(frame(n)) for n in range(1, 4)))
        self.assertEqual(result.returncode, 0, result.stderr)
        events = [json.loads(line) for line in result.stdout.splitlines()]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["event_type"], "RESTRICTED_ZONE_INTRUSION")
        self.assertEqual(events[0]["frame_id"], 3)

    def test_corrupt_json_fails_without_inventing_events(self):
        result = self.run_cli('{broken\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")
        self.assertIn("line 1", result.stderr)

    def test_invalid_metadata_fails_with_line_number(self):
        result = self.run_cli('{}\n')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("line 1", result.stderr)

    def test_empty_input_fails_to_prevent_empty_evidence_claim(self):
        result = self.run_cli('')
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("no frames", result.stderr.lower())


if __name__ == "__main__":
    unittest.main()
