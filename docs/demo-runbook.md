# Live demo and evidence runbook

Status: preparation only. None of the runtime evidence below exists yet.

## First working run
1. Sign into the actual PipeGen application; record installed version and platform.
2. Use the requirement in `docs/pipegen-requirement.txt`. Prefer a supported,
   small, single-stream person detector. Keep batch 1 and avoid training.
3. Complete and preserve Requirement, Pipeline IR, Model, Compiler and Run.
4. Capture the real Pipeline IR and actual TensorRT speed report immediately.
5. Inspect exported source/configuration and its actual run command before editing.
6. Run the generated application with a video stored under the Linux home folder.
7. Inspect actual metadata output; verify frame dimensions, timestamps, class IDs,
   boxes and stable tracker IDs before implementing the adapter.
8. Map that schema to the implemented metadata contract, including empty frames.
9. Calibrate the polygon against the actual demo video and display that same polygon.

## Capture a repeatable safety scenario
- Person outside: no incident.
- Brief one/two-frame entry: no confirmed incident.
- Sustained entry: one RESTRICTED_ZONE_INTRUSION with actual source frame/time.
- Continued presence: no repeated intrusion events for the same incident.
- Observed exit: ZONE_EXIT with metadata-derived dwell duration.
- Re-entry: a different incident ID.
- Lost detection: TRACK_LOST, described as uncertainty rather than a certain exit.

Match the JSON events to the source video. Unit fixtures do not establish that the
detector/tracker behaves this way on real frames. If a scenario fails, document
and repair it before claiming acceptance.

## Evidence to retain
- Actual PipeGen project/export and generated configs/source/run script.
- Real requirement and Pipeline IR screenshots.
- Real model/precision/input settings and actual TensorRT speed report.
- Actual GPU live inference screenshot/recording with polygon visible.
- Actual emitted incident JSONL and the video/source provenance.
- Exact tested machine, input, model and run instructions.
- Known runtime limitations and failed scenarios, if any remain.

Keep vendor installers, credentials, raw private logs and unlicensed videos out of
the published source repository. Capture demo screenshots from the actual run;
do not create a simulated dashboard screenshot to fill an evidence gap.

## Suggested short presentation
1. State the problem: a passive camera feed does not provide a usable zone incident.
2. Show the actual PipeGen graph and explain its detector, tracker and metadata path.
3. Play the real outside-entry-exit scenario and show the corresponding incident.
4. Show the actual speed report; distinguish engine benchmark from end-to-end speed.
5. Explain duplicate suppression, metadata-only storage and honest track-loss handling.
6. State tested limits, especially 2 GB VRAM and any tracker/detection weaknesses.

Avoid claims of accident prediction, deployment readiness, accuracy percentages,
INT8 benefits, or closed-loop hardware control unless separately implemented and verified.

## Submission gate
Complete `docs/acceptance-checklist.md`, update the description from draft to
actual results, make the repository judge-accessible, review the active feedback
and project forms, request the user's final submission confirmation, and retain
the receipt. A GitHub push alone is not a hackathon submission.
