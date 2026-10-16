# GuardianEdge AI implementation plan

Goal: a genuine PipeGen Track A submission, then competitive safety analytics.
Spec: supplied CODEX_HANDOFF.md, read completely on 2026-10-16.
Execution: inline and autonomous, as explicitly requested by the user.

## Constraints
- Preserve working Docker Desktop, WSL, NVIDIA drivers and GPU passthrough.
- PipeGen 0.5.1 must generate the actual DeepStream/TensorRT pipeline.
- One video stream, batch 1, lightweight supported person detector, 2 GB VRAM.
- Do not claim generated code, runtime results, evidence or submission before verification.
- Credentials and final submission require user action/confirmation.

## Tasks
- [x] Admission: official installer, reviewed prerequisites, package metadata, installation, GUI and login.
- [x] PipeGen: Requirement, IR, Model, Compiler, Run; retain export and real speed report.
- [x] Zone engine: dependency-free Python metadata consumer; test outside, short entry, confirmed entry, suppression, exit, re-entry and malformed input before implementing.
- [x] Integration: inspect the real generated metadata schema and supported extension points; map to the zone engine, retain source frame/timestamp provenance.
- [x] Verification: actual video with outside/inside/exit behavior, GPU runtime, genuine JSON events, screenshots and reports.
- [x] Packaging: accurate README, architecture, project description, GitHub repo; exclude vendor binaries, secrets and unlicensed video.
- [ ] Submission: participant will submit personally, arrange judge access and retain the receipt.

## Review focus
- Missing detections must reset unconfirmed frame persistence, and must not be falsely reported as observed exits.
- Per-object and per-camera state must be isolated.
- Bad input must fail before partially changing state.
- Timestamp/frame ordering must prevent duplicate frames counting as three observations.
- Unit fixtures are never live inference evidence; integration is verified against the retained actual PipeGen output.

## Interface
`ZoneEngine.process(frame: dict) -> list[dict]` consumes normalized frame metadata:
camera_id, frame_id (strictly increasing per camera), timestamp_utc, width, height,
and objects containing track_id, class_name, confidence, bbox [left, top, width, height].
Zones use normalized polygon coordinates. `track_id` requires stable upstream IDs.
Missing IDs are rejected; any future fallback must be explicit and documented.
