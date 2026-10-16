"""Deterministic zone incidents. This module performs no vision inference."""

from datetime import datetime, timezone
import math
from uuid import uuid4


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def point_in_polygon(point, polygon):
    """Ray casting with boundary inclusion; coordinates share the same units."""
    x, y = point
    inside = False
    for i, (ax, ay) in enumerate(polygon):
        bx, by = polygon[(i + 1) % len(polygon)]
        cross = (x - ax) * (by - ay) - (y - ay) * (bx - ax)
        if abs(cross) < 1e-10 and min(ax, bx) <= x <= max(ax, bx) and min(ay, by) <= y <= max(ay, by):
            return True
        if (ay > y) != (by > y) and x < (bx - ax) * (y - ay) / (by - ay) + ax:
            inside = not inside
    return inside


def _timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if result.utcoffset() is None:
            raise ValueError("timezone required")
        return result.astimezone(timezone.utc)
    except (AttributeError, TypeError, ValueError) as exc:
        raise ValueError("timestamp_utc must be an ISO-8601 timestamp with a timezone") from exc


class ZoneEngine:
    def __init__(self, zones, confirm_frames=3, min_confidence=0.5):
        if not isinstance(confirm_frames, int) or isinstance(confirm_frames, bool) or confirm_frames < 1:
            raise ValueError("confirm_frames must be a positive integer")
        if not _number(min_confidence) or not 0 <= min_confidence <= 1:
            raise ValueError("min_confidence must be between 0 and 1")
        self.zones = []
        ids = set()
        for zone in zones:
            polygon = zone.get("polygon", [])
            zid = zone.get("id")
            if not isinstance(zid, str) or not zid or zid in ids or len(polygon) < 3:
                raise ValueError("zones need unique nonempty IDs and at least three vertices")
            if any(not isinstance(p, (list, tuple)) or len(p) != 2 or
                   any(not _number(v) or not 0 <= v <= 1 for v in p) for p in polygon):
                raise ValueError("polygon coordinates must be finite normalized pairs")
            polygon = tuple(tuple(p) for p in polygon)
            area = sum(ax * polygon[(i + 1) % len(polygon)][1] -
                       ay * polygon[(i + 1) % len(polygon)][0] for i, (ax, ay) in enumerate(polygon))
            if abs(area) < 1e-10:
                raise ValueError("polygon must have nonzero area")
            self.zones.append((zid, polygon))
            ids.add(zid)
        if not self.zones:
            raise ValueError("at least one zone is required")
        self.confirm_frames = confirm_frames
        self.min_confidence = min_confidence
        self._states = {}
        self._last = {}

    def _validate(self, frame):
        if not isinstance(frame, dict):
            raise ValueError("frame must be an object")
        camera = frame.get("camera_id")
        index = frame.get("frame_id")
        if not isinstance(camera, str) or not camera:
            raise ValueError("camera_id must be nonempty")
        if not isinstance(index, int) or isinstance(index, bool) or index < 0:
            raise ValueError("frame_id must be a nonnegative integer")
        timestamp = _timestamp(frame.get("timestamp_utc"))
        previous = self._last.get(camera)
        if previous and (index <= previous[0] or timestamp < previous[1]):
            raise ValueError("frame_id must increase and timestamps cannot go backwards per camera")
        for name in ("width", "height"):
            if not _number(frame.get(name)) or frame[name] <= 0:
                raise ValueError(f"{name} must be positive")
        if not isinstance(frame.get("objects"), list):
            raise ValueError("objects must be a list, including on frames with no detections")
        objects, ids = [], set()
        for obj in frame["objects"]:
            if not isinstance(obj, dict):
                raise ValueError("each object must be a dictionary")
            tid = obj.get("track_id")
            if isinstance(tid, bool) or not isinstance(tid, (str, int)) or str(tid) == "":
                raise ValueError("stable track_id required")
            tid = str(tid)
            if tid in ids:
                raise ValueError("duplicate track_id in frame")
            ids.add(tid)
            confidence, bbox, label = obj.get("confidence"), obj.get("bbox"), obj.get("class_name")
            if not _number(confidence) or not 0 <= confidence <= 1 or not isinstance(label, str):
                raise ValueError("class_name and confidence in [0,1] required")
            if not isinstance(bbox, (list, tuple)) or len(bbox) != 4 or any(not _number(v) for v in bbox):
                raise ValueError("bbox must contain four finite numbers")
            if bbox[2] <= 0 or bbox[3] <= 0:
                raise ValueError("bbox width and height must be positive")
            if label == "person" and confidence >= self.min_confidence:
                objects.append({"track_id": tid, "confidence": confidence, "bbox": list(bbox)})
        return camera, index, timestamp, objects

    def _event(self, kind, frame, obj, zid, state):
        return {"event_id": str(uuid4()), "incident_id": state["incident_id"],
                "event_type": kind, "timestamp_utc": frame["timestamp_utc"],
                "camera_id": frame["camera_id"], "frame_id": frame["frame_id"],
                "zone_id": zid, "track_id": obj["track_id"],
                "confidence": obj["confidence"], "bbox": list(obj["bbox"]),
                "first_seen_utc": state["first_seen_utc"],
                "evidence_source": "upstream_metadata"}

    def process(self, frame):
        """Process every inference frame, including empty frames. Reject invalid input atomically."""
        camera, index, timestamp, objects = self._validate(frame)
        events, seen = [], set()
        for obj in objects:
            left, top, width, height = obj["bbox"]
            foot = ((left + width / 2) / frame["width"], (top + height) / frame["height"])
            for zid, polygon in self.zones:
                key = (camera, obj["track_id"], zid)
                seen.add(key)
                state = self._states.get(key)
                if point_in_polygon(foot, polygon):
                    if state is None:
                        state = {"count": 0, "active": False, "first_time": timestamp,
                                 "first_seen_utc": frame["timestamp_utc"], "incident_id": str(uuid4())}
                        self._states[key] = state
                    state["count"] += 1
                    state["last_object"] = obj
                    if not state["active"] and state["count"] >= self.confirm_frames:
                        state["active"] = True
                        events.append(self._event("RESTRICTED_ZONE_INTRUSION", frame, obj, zid, state))
                elif state is not None:
                    if state["active"]:
                        event = self._event("ZONE_EXIT", frame, obj, zid, state)
                        event["dwell_seconds"] = (timestamp - state["first_time"]).total_seconds()
                        events.append(event)
                    del self._states[key]
        for key in list(self._states):
            if key[0] == camera and key not in seen:
                state = self._states.pop(key)
                if state["active"]:
                    event = self._event("TRACK_LOST", frame, state["last_object"], key[2], state)
                    event["bbox_is_last_observation"] = True
                    events.append(event)
        self._last[camera] = (index, timestamp)
        return events
