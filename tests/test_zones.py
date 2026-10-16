import copy
import math
import unittest

from guardianedge.zones import ZoneEngine, point_in_polygon


ZONE = {"id": "hazard", "polygon": [[0.4, 0.4], [0.8, 0.4], [0.8, 0.9], [0.4, 0.9]]}


def frame(n, x=50, camera="cam-1", track="person-1", objects=None):
    return {"camera_id": camera, "frame_id": n,
            "timestamp_utc": f"2026-10-16T13:00:{n:02d}Z", "width": 100, "height": 100,
            "objects": objects if objects is not None else [
                {"track_id": track, "class_name": "person", "confidence": 0.9,
                 "bbox": [x - 5, 30, 10, 40]}]}


class ZoneTests(unittest.TestCase):
    def setUp(self):
        self.engine = ZoneEngine([ZONE], confirm_frames=3)

    def test_polygon_includes_boundary_and_excludes_outside(self):
        self.assertTrue(point_in_polygon((0.5, 0.7), ZONE["polygon"]))
        self.assertTrue(point_in_polygon((0.4, 0.7), ZONE["polygon"]))
        self.assertFalse(point_in_polygon((0.2, 0.7), ZONE["polygon"]))

    def test_outside_never_alerts(self):
        self.assertEqual([self.engine.process(frame(n, x=20)) for n in range(1, 5)], [[], [], [], []])

    def test_three_observations_create_one_real_metadata_event(self):
        self.assertEqual(self.engine.process(frame(1)), [])
        self.assertEqual(self.engine.process(frame(2)), [])
        events = self.engine.process(frame(3))
        self.assertEqual(len(events), 1)
        event = events[0]
        self.assertEqual(event["event_type"], "RESTRICTED_ZONE_INTRUSION")
        self.assertEqual(event["frame_id"], 3)
        self.assertEqual(event["timestamp_utc"], "2026-10-16T13:00:03Z")
        self.assertEqual(event["camera_id"], "cam-1")
        self.assertEqual(event["zone_id"], "hazard")
        self.assertEqual(event["bbox"], [45, 30, 10, 40])
        self.assertEqual(event["confidence"], 0.9)

    def test_sustained_intrusion_is_suppressed(self):
        events = [e for n in range(1, 7) for e in self.engine.process(frame(n))]
        self.assertEqual(len(events), 1)

    def test_exit_closes_incident_and_reentry_gets_new_id(self):
        opened = [e for n in range(1, 4) for e in self.engine.process(frame(n))][0]
        closed = self.engine.process(frame(4, x=20))[0]
        self.assertEqual(closed["event_type"], "ZONE_EXIT")
        self.assertEqual(closed["incident_id"], opened["incident_id"])
        self.assertEqual(closed["dwell_seconds"], 3.0)
        again = [e for n in range(5, 8) for e in self.engine.process(frame(n))][0]
        self.assertNotEqual(again["incident_id"], opened["incident_id"])

    def test_short_entry_then_outside_resets_confirmation(self):
        for f in [frame(1), frame(2), frame(3, x=20), frame(4), frame(5)]:
            self.assertEqual(self.engine.process(f), [])
        self.assertEqual(len(self.engine.process(frame(6))), 1)

    def test_missing_detection_resets_pending_confirmation(self):
        for f in [frame(1), frame(2), frame(3, objects=[]), frame(4), frame(5)]:
            self.assertEqual(self.engine.process(f), [])
        self.assertEqual(len(self.engine.process(frame(6))), 1)

    def test_disappearance_is_not_an_observed_zone_exit(self):
        for n in range(1, 4):
            self.engine.process(frame(n))
        events = self.engine.process(frame(4, objects=[]))
        self.assertEqual(events[0]["event_type"], "TRACK_LOST")
        self.assertNotIn("dwell_seconds", events[0])

    def test_cameras_do_not_share_confirmation(self):
        self.engine.process(frame(1))
        self.engine.process(frame(2))
        self.assertEqual(self.engine.process(frame(1, camera="cam-2")), [])
        self.assertEqual(len(self.engine.process(frame(3))), 1)

    def test_different_people_do_not_share_confirmation(self):
        self.engine.process(frame(1, track="a"))
        self.engine.process(frame(2, track="b"))
        self.assertEqual(self.engine.process(frame(3, track="c")), [])

    def test_duplicate_and_out_of_order_frames_are_rejected(self):
        self.engine.process(frame(2))
        for n in [2, 1]:
            with self.assertRaises(ValueError):
                self.engine.process(frame(n))

    def test_bad_frame_does_not_partially_advance_state(self):
        self.engine.process(frame(1))
        invalid = frame(2)
        invalid["objects"].append({"track_id": "bad"})
        with self.assertRaises(ValueError):
            self.engine.process(invalid)
        self.assertEqual(self.engine.process(frame(2)), [])
        self.assertEqual(len(self.engine.process(frame(3))), 1)

    def test_nonperson_and_low_confidence_do_not_alert(self):
        for n in range(1, 5):
            f = frame(n)
            f["objects"][0]["class_name"] = "car"
            self.assertEqual(self.engine.process(f), [])
        for n in range(5, 9):
            f = frame(n)
            f["objects"][0]["confidence"] = 0.1
            self.assertEqual(self.engine.process(f), [])

    def test_invalid_geometry_and_metadata_are_rejected(self):
        for key, value in [("width", 0), ("height", -1), ("timestamp_utc", "invalid")]:
            f = frame(1)
            f[key] = value
            with self.assertRaises(ValueError):
                self.engine.process(f)
        for bbox in [[0, 0, -1, 10], [0, 0, math.nan, 10]]:
            f = frame(1)
            f["objects"][0]["bbox"] = bbox
            with self.assertRaises(ValueError):
                self.engine.process(f)
        for polygon in [[], [[0, 0], [1, 1]], [[0, 0], [1, 1], [2, 2]]]:
            with self.assertRaises(ValueError):
                ZoneEngine([{"id": "bad", "polygon": polygon}])

    def test_coordinate_overflow_rejects_entire_frame_before_advancing_any_person(self):
        first = frame(1)
        first.update(width=1, height=1)
        first["objects"][0]["bbox"] = [0.4, 0.1, 0.2, 0.5]
        self.engine.process(first)
        second = copy.deepcopy(first)
        second.update(frame_id=2, timestamp_utc="2026-10-16T13:00:02Z")
        invalid = copy.deepcopy(second)
        invalid["objects"].append({"track_id": "overflow", "class_name": "person",
                                   "confidence": 0.9, "bbox": [0, 10**308, 1, 10**308]})
        with self.assertRaises(ValueError):
            self.engine.process(invalid)
        self.assertEqual(self.engine.process(second), [])
        third = copy.deepcopy(second)
        third.update(frame_id=3, timestamp_utc="2026-10-16T13:00:03Z")
        self.assertEqual(len(self.engine.process(third)), 1)

    def test_unrepresentable_integer_is_rejected_as_invalid_metadata(self):
        invalid = frame(1)
        invalid["objects"][0]["bbox"][0] = 10**400
        with self.assertRaises(ValueError):
            self.engine.process(invalid)

    def test_nonfinite_derived_position_is_rejected(self):
        invalid = frame(1)
        invalid["width"] = 5e-324
        with self.assertRaises(ValueError):
            self.engine.process(invalid)


if __name__ == "__main__":
    unittest.main()
