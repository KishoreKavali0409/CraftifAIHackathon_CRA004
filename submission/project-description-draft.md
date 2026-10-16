# GuardianEdge AI — Explainable Zone Incident Monitoring

Participant submission draft, updated after local verification on 2026-10-16.
The participant will submit personally; this is not a submission receipt.

## Problem and implemented solution
Passive camera feeds require an operator to notice zone entries. GuardianEdge
converts tracked person observations into explainable incidents, suppresses repeat
confirmations and distinguishes observed exits from disappearing tracks.

The actual PipeGen 0.5.1 workflow completed Requirement, Pipeline IR, Model,
Compiler and Run. Its exported DeepStream pipeline uses YOLO11s, a TensorRT FP16
engine and NVIDIA tracking. A native extension draws the configured demo polygon.
The Python adapter consumes actual generated metadata. The MVC model checks each
person's bounding-box bottom-center, confirms entry over three qualifying processed
observations, records observed exits and reports track loss separately. Controllers
orchestrate validated input; views serialize incident JSONL and diagnostics.
Incident analysis currently runs after video completion.

## Verified results
The final configured-laptop GPU run processed 1,442 frames and 13,754 object records,
producing 140 events: 70 intrusion confirmations, 10 observed exits and 60 track
losses. All 32 software tests passed on Windows and Ubuntu. Corrupt video failed
with a nonzero exit code. The final MP4 decoded completely without errors.

PipeGen reported 18.539 ms/frame for the engine benchmark, approximately 54 FPS
derived. A separate live display screenshot showed 17.36 FPS with dropped frames.
These have different measurement scopes. Hardware: NVIDIA MX550, 2 GB VRAM.
No measured accuracy, INT8 optimization or actual Jetson deployment is claimed.
Jetson predictions in the original report are modelled estimates.

## Evidence and limits
The repository includes actual exported source, Pipeline IR, original speed report,
genuine screenshots, metadata, incidents, test transcripts and a detailed Word
guide. Model, engine and video binaries are excluded from Git and retained locally.
The public street sample has an explicitly labelled demonstration zone, not a real
site restriction. Source media PTS is preserved with an explicit timestamp basis;
it is not a capture date. No facial recognition is implemented. The demo recording
contains visible people and vehicles. Frequent track loss can fragment incidents.
This prototype does not claim validated industrial safety performance.
Clean-machine standalone rebuilding has not been independently verified.

Repository: https://github.com/KishoreKavali0409/guardianedge-ai

The repository remains private. Before submitting, the participant must arrange
judge access, confirm the active form and permitted attachments, and retain the
submission receipt.
