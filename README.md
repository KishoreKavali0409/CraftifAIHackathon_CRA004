# GuardianEdge AI

Proactive Industrial Safety Intelligence — CraftifAI PipeGen Track A.

## Current status
**In development; not yet a verified hackathon submission.** The custom zone
analytics and JSONL consumer pass 18 tests. PipeGen 0.5.1 is installed. Pipeline generation,
TensorRT compilation, live inference, actual metadata integration and evidence
are pending. See `docs/verification-ledger.md` for the precise status.

## Purpose
Turn person detections from a real PipeGen-generated DeepStream pipeline into
restricted-zone incidents. A person's bounding-box bottom-center is checked
against normalized polygons. Three consecutive processed observations confirm
an incident; sustained presence produces one alert, observed exit closes it,
and re-entry creates a new incident. Missing tracks create an observation-gap
event, not an invented exit. No facial recognition or raw-frame storage is
performed by the analytics module.

## Architecture
Intended integration: MP4 → PipeGen-generated DeepStream detector and tracker →
verified metadata adapter → GuardianEdge zone state machine → JSON incident feed.
The actual adapter must be based on the generated export, which is not available
yet. This repository does not contain a replacement detector.

## Test the implemented analytics
Python 3.10+; standard library only:

```sh
python3 -m unittest discover -s tests -v
```

Fixtures in tests are synthetic and are never submitted as live inference evidence.

After the real PipeGen metadata adapter is integrated, pipe normalized frame
JSONL into the analytics consumer:

```sh
python3 -m guardianedge --config config/zones.json < normalized-frames.jsonl > incidents.jsonl
```

This command performs metadata analysis only. It does not establish that its
input came from PipeGen. Empty or malformed input returns a nonzero status.

## Metadata contract
`ZoneEngine.process(frame)` accepts a dictionary containing `camera_id`, increasing
integer `frame_id`, timezone-aware `timestamp_utc`, positive `width` and `height`,
and `objects`. Each object has stable `track_id`, `class_name`, `confidence` in
[0,1], and pixel-space `bbox` as [left, top, width, height]. Send every processed
frame, including an empty objects list when no person is detected. Timestamps
must not go backwards within one camera. Stable tracking IDs must come from a
verified upstream tracker; multi-person tracking is not inferred here.

The module emits `RESTRICTED_ZONE_INTRUSION`, `ZONE_EXIT` and `TRACK_LOST` events.
Each incident carries source frame, camera, track, polygon and timestamp metadata.
`dwell_seconds` on an observed exit is measured from the first qualifying inside
observation. A lost-track event includes the last known bounding box and explicitly
marks it stale. It has no asserted dwell time or observed exit.

## Hardware and limitations
Windows + Ubuntu 22.04 WSL2, NVIDIA MX550 with 2 GB VRAM, existing Docker Desktop
integration. Use one stream and batch 1. PipeGen/DeepStream memory feasibility is
still unverified. No measured FPS, accuracy, latency, INT8 bonus or live hardware
success is claimed until actual runtime reports exist.

## Evidence required before submission
All five PipeGen stages; actual engine and speed report; live run screenshot;
real emitted events; generated export and permitted source; accurate tested
configuration; GitHub URL; confirmed current form and submission receipt.

The official form linked in the original brief currently opens a PipeGen feedback
form. It says the project submission link is on the last page, and feedback must
be submitted for scoring. Deadline/extension applicability still needs organizer
confirmation. User credentials and final submission remain user-controlled.
