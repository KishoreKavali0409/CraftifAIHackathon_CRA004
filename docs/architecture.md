# Runtime architecture

The implemented system uses a real PipeGen-generated DeepStream pipeline for detection and tracking. Python MVC owns downstream incident analytics. The configured runner completes a real video run, then analyzes its saved metadata; it does not claim continuous streaming incident delivery.

## Flow

Video -> NVIDIA DeepStream decoder and TensorRT detector -> upstream tracker -> actual per-frame metadata -> PipeGen schema adapter -> MetadataController -> ZoneEngine -> JsonlView -> incident JSONL.

The native view extension adds NvDsDisplayMeta before nvdsosd and draws the same demonstration polygon used by the model. It does not implement a second incident state machine.

## Responsibilities

- `models/zones.py` validates the whole observation before changing per-camera, track and zone state. It owns geometry, persistence and incident lifecycle. Optional media PTS must agree with the epoch timestamp and cannot regress, even within one microsecond.
- `controllers/metadata.py` orchestrates direct normalized observations or JSONL input. It never performs geometry or detection.
- `views/jsonl.py` serializes events and separates diagnostics from machine-readable output.
- `adapters/pipegen.py` maps the inspected generated frame_json.h fields, filters person metadata, requires confirmed IDs, and preserves actual PTS.
- `__main__.py` wires the generic CLI. The adapter module is a separate composition entry point for completed PipeGen metadata.
- `scripts/apply_zone_overlay.py` installs the native presentation extension into a working copy of the actual export. Invoke as `python3 -m scripts.apply_zone_overlay` from the repo root.
- `scripts/run_guardianedge.sh` runs the real exported pipeline in the existing verified container, then invokes the adapter and MVC controller.

Controllers and models are synchronous session objects and are not thread safe. Output failure must not cause a caller to blindly replay an already processed frame. Empty observations are required to detect missing tracks. UUIDs are generated per replay, while event type/frame/track/zone semantics remain reproducible for the same metadata.

## Status and limits

32 tests pass; real video and actual metadata have been verified. The runner depends on the configured laptop's running PipeGen container and locally retained model assets. Clean-machine standalone export rebuilding and production worker-safety performance have not been verified. See README and reproduction guide.
