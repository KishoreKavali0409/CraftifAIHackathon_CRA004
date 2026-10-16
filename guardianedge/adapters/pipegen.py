"""Adapt inspected PipeGen frame_json.h output to the MVC frame contract.

Media PTS is a relative timeline. Its epoch representation is explicitly marked
and must never be presented as a recording/capture UTC date.
"""
import argparse
from datetime import datetime, timedelta, timezone
import json
import sys

from ..controllers.metadata import MetadataController
from ..models.zones import ZoneEngine
from ..views.jsonl import JsonlView


def normalize_frame(packet, camera_prefix):
    """Map actual DeepStream JSON fields, preserving empty observations and IDs."""
    try:
        if not isinstance(packet, dict) or not isinstance(camera_prefix, str) or not camera_prefix:
            raise ValueError('frame object and nonempty camera prefix required')
        pts, source, index = packet['pts_ns'], packet['source_id'], packet['frame']
        for name, value in [('pts_ns', pts), ('source_id', source), ('frame', index)]:
            if not isinstance(value, int) or isinstance(value, bool) or value < 0:
                raise ValueError(f'{name} must be a nonnegative integer')
        if pts == 18446744073709551615:
            raise ValueError('unknown GStreamer timestamp')
        timestamp = datetime(1970, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=pts // 1000)
        if not isinstance(packet['objects'], list):
            raise ValueError('objects must be a list')
        people = []
        for obj in packet['objects']:
            if not isinstance(obj, dict):
                raise ValueError('object record required')
            if obj.get('label') != 'person':
                if obj.get('class_id') == 0:
                    raise ValueError('COCO person class and label disagree')
                continue
            if obj.get('class_id') != 0 or obj.get('id') in (None, 18446744073709551615):
                raise ValueError('confirmed person tracker identity required')
            box = obj['bbox']
            people.append({'track_id': obj['id'], 'class_name': 'person',
                           'confidence': obj['confidence'],
                           'bbox': [box['left'], box['top'], box['width'], box['height']]})
        return {'camera_id': f'{camera_prefix}:{source}', 'frame_id': index,
                'timestamp_utc': timestamp.isoformat(), 'source_pts_ns': pts,
                'timestamp_basis': 'media_pts_epoch_not_capture_utc',
                'width': packet['width'], 'height': packet['height'], 'objects': people}
    except (KeyError, TypeError, OverflowError) as exc:
        raise ValueError(f'invalid PipeGen frame: {exc}') from exc


def main():
    """Compose the actual exported metadata adapter with the existing MVC app."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, help='Completed PipeGen metadata.json')
    parser.add_argument('--config', required=True, help='GuardianEdge zone JSON')
    parser.add_argument('--camera-id', default='pipegen-demo')
    args = parser.parse_args()
    view = JsonlView(sys.stdout, sys.stderr)
    try:
        with open(args.config, encoding='utf-8') as source:
            config = json.load(source)
        model = ZoneEngine(config['zones'], config.get('confirm_frames', 3), config.get('min_confidence', .5))
        controller = MetadataController(model, view)
        with open(args.input, encoding='utf-8') as source:
            document = json.load(source)
        frames = document['frames']
        if not isinstance(frames, list) or not frames:
            raise ValueError('nonempty PipeGen frames list required')
        for number, packet in enumerate(frames, 1):
            try:
                controller.process_frame(normalize_frame(packet, args.camera_id))
            except ValueError as exc:
                raise ValueError(f'PipeGen observation {number}: {exc}') from exc
        view.completed(len(frames))
        return 0
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        view.error(f'PipeGen input error: {exc}')
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
