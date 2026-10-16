# Acceptance and submission checklist

## Verified software behavior
- [x] Outside person produces no incident.
- [x] One/two inside observations do not confirm an incident.
- [x] Third inside observation confirms an incident with actual input metadata.
- [x] Continued presence produces no duplicate intrusion.
- [x] Observed exit closes the incident with a measured metadata dwell duration.
- [x] Re-entry creates a new incident ID.
- [x] Missing detections reset pending confirmation.
- [x] Lost active tracks create TRACK_LOST, without an invented observed exit.
- [x] Camera and person IDs isolate state.
- [x] Invalid/duplicate/out-of-order metadata is rejected.
- [x] JSONL CLI rejects corrupt input and empty input.

These checks used synthetic test fixtures. They are not live vision evidence.

## Mandatory runtime acceptance — pending
- [ ] PipeGen account authenticated in the actual app.
- [ ] Requirement, Pipeline IR, Model, Compiler, Run all completed.
- [ ] Pipeline IR screenshot captured from the actual project.
- [ ] Actual TensorRT engine compiled and model/precision/input recorded.
- [ ] PipeGen speed report saved and screenshot captured.
- [ ] Generated DeepStream app runs on the NVIDIA GPU with a real video source.
- [ ] Generated metadata schema inspected; real adapter integrated and tested.
- [ ] Video demonstrates outside, entry, sustained entry, exit, re-entry.
- [ ] Zone polygon appears in the actual visual output.
- [ ] Actual incidents saved from that run and matched to source video frames.
- [ ] Actual PipeGen export and permitted code included.
- [ ] Corrupt video input behavior documented from actual runtime.

## Submission — pending
- [ ] Active wildcard deadline and correct form confirmed.
- [ ] GitHub source pushed, repository URL accessible to judges.
- [ ] README/description reflect actual implemented and tested behavior.
- [ ] Video/report/screenshots contain genuine evidence, with no invented metrics.
- [ ] Participant details and subjective tool feedback provided by the user.
- [ ] Required feedback form completed; linked project form reviewed.
- [ ] User gives final submission confirmation.
- [ ] Submission receipt captured.
