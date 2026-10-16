"""Exercise MVC boundaries through real models and in-memory streams."""

import io
import json
import unittest

from guardianedge.controllers.metadata import MetadataController
from guardianedge.models.zones import ZoneEngine
from guardianedge.views.jsonl import JsonlView
from test_zones import frame, ZONE


class ControllerTests(unittest.TestCase):
    def setUp(self):
        self.output = io.StringIO()
        self.errors = io.StringIO()
        self.controller = MetadataController(
            ZoneEngine([ZONE]), JsonlView(self.output, self.errors))

    def test_confirmed_entry_and_exit_are_rendered_with_shared_incident(self):
        frames = [frame(n) for n in range(1, 5)]
        frames[-1]["objects"][0]["bbox"] = [0, 0, 10, 10]
        result = self.controller.run(io.StringIO(
            "\n".join(json.dumps(row) for row in frames)))
        self.assertEqual(result, 0)
        events = [json.loads(row) for row in self.output.getvalue().splitlines()]
        self.assertEqual([e["event_type"] for e in events],
                         ["RESTRICTED_ZONE_INTRUSION", "ZONE_EXIT"])
        self.assertEqual(events[0]["incident_id"], events[1]["incident_id"])
        self.assertIn("Processed 4 metadata frames", self.errors.getvalue())

    def test_invalid_row_stops_stream_before_later_frames(self):
        rows = [json.dumps(frame(1)), "{}", json.dumps(frame(2)), json.dumps(frame(3))]
        self.assertEqual(self.controller.run(io.StringIO("\n".join(rows))), 2)
        self.assertEqual(self.output.getvalue(), "")
        self.assertIn("line 2", self.errors.getvalue())

    def test_whitespace_is_not_inference_evidence(self):
        self.assertEqual(self.controller.run(io.StringIO(" \n\n")), 2)
        self.assertEqual(self.output.getvalue(), "")
        self.assertIn("No frames received", self.errors.getvalue())

    def test_direct_frame_input_supports_future_runtime_adapter(self):
        for index in range(1, 4):
            self.controller.process_frame(frame(index))
        events = [json.loads(row) for row in self.output.getvalue().splitlines()]
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["frame_id"], 3)
        self.assertEqual(self.errors.getvalue(), "")


if __name__ == "__main__":
    unittest.main()
