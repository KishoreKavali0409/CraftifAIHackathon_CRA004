import io
import unittest
from guardianedge.adapters.pipegen import normalize_frame
from guardianedge.controllers.metadata import MetadataController
from guardianedge.models.zones import ZoneEngine
from guardianedge.views.jsonl import JsonlView
from test_zones import ZONE


def packet(index=0, objects=None):
    return {'frame': index, 'source_id': 0, 'pts_ns': index * 100000000,
            'width': 640, 'height': 480, 'objects': [] if objects is None else objects}


def person(identifier=7):
    return {'id': identifier, 'class_id': 0, 'label': 'person', 'confidence': .9,
            'bbox': {'left': 300, 'top': 200, 'width': 50, 'height': 150}}


class PipeGenAdapterTests(unittest.TestCase):
    def test_real_schema_preserves_box_tracking_and_media_time(self):
        row = normalize_frame(packet(2, [person()]), 'demo')
        self.assertEqual(row['camera_id'], 'demo:0')
        self.assertEqual(row['frame_id'], 2)
        self.assertEqual(row['source_pts_ns'], 200000000)
        self.assertEqual(row['timestamp_utc'], '1970-01-01T00:00:00.200000+00:00')
        self.assertEqual(row['objects'][0]['bbox'], [300, 200, 50, 150])
        self.assertEqual(row['objects'][0]['track_id'], 7)
        self.assertEqual(row['timestamp_basis'], 'media_pts_epoch_not_capture_utc')

    def test_empty_frame_and_nonperson_remain_an_observation(self):
        car = person()
        car.update(class_id=2, label='car')
        row = normalize_frame(packet(3, [car]), 'demo')
        self.assertEqual(row['objects'], [])
        self.assertEqual(row['frame_id'], 3)

    def test_unknown_identity_and_missing_pts_are_rejected(self):
        with self.assertRaises(ValueError):
            normalize_frame(packet(0, [person(None)]), 'demo')
        for value in [None, -1, True, 18446744073709551615]:
            row = packet()
            row['pts_ns'] = value
            with self.assertRaises(ValueError):
                normalize_frame(row, 'demo')

    def test_incident_preserves_source_pts_and_explicit_time_basis(self):
        import json
        output = io.StringIO()
        controller = MetadataController(ZoneEngine([ZONE]), JsonlView(output, io.StringIO()))
        for index in range(3):
            controller.process_frame(normalize_frame(packet(index, [person()]), 'demo'))
        event = json.loads(output.getvalue())
        self.assertEqual(event['event_type'], 'RESTRICTED_ZONE_INTRUSION')
        self.assertEqual(event['source_pts_ns'], 200000000)
        self.assertEqual(event['timestamp_basis'], 'media_pts_epoch_not_capture_utc')

class ProvenanceValidationTests(unittest.TestCase):
    def test_invalid_provenance_is_rejected_before_incident_state_changes(self):
        from test_zones import frame
        engine = ZoneEngine([ZONE])
        engine.process(frame(1))
        bad = frame(2)
        bad['source_pts_ns'] = float('nan')
        bad['timestamp_basis'] = 'media_pts_epoch_not_capture_utc'
        with self.assertRaises(ValueError):
            engine.process(bad)
        self.assertEqual(engine.process(frame(2)), [])

    def test_timestamp_cannot_contradict_media_pts(self):
        row = normalize_frame(packet(1, [person()]), 'demo')
        row['timestamp_utc'] = '2026-10-16T14:00:00+00:00'
        with self.assertRaises(ValueError):
            ZoneEngine([ZONE]).process(row)

    def test_submicrosecond_pts_regression_does_not_advance_state(self):
        engine = ZoneEngine([ZONE])
        first = packet(1, [person()])
        first['pts_ns'] = 999
        engine.process(normalize_frame(first, 'demo'))
        second = packet(2, [person()])
        second['pts_ns'] = 1
        with self.assertRaises(ValueError):
            engine.process(normalize_frame(second, 'demo'))
        second['pts_ns'] = 1000
        self.assertEqual(engine.process(normalize_frame(second, 'demo')), [])
