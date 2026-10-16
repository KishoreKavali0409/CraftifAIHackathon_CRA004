# GuardianEdge AI — Proactive Industrial Safety Intelligence

Status: DRAFT. Runtime integration and mandatory evidence are still pending.
Do not submit as a completed build until the verification checklist is satisfied.

## Problem
Industrial restricted areas are often watched through passive camera feeds.
A useful safety monitor must turn an observed zone entry into a clear incident,
without repeatedly alerting throughout the same continuous event.

## Proposed solution and actual work so far
GuardianEdge is designed around a CraftifAI PipeGen-generated DeepStream
person-detection pipeline with a TensorRT engine. The implemented downstream
analytics module checks each person's bounding-box bottom-center against a
configurable polygon, confirms entry over three processed observations, suppresses
duplicate alerts, records observed exits, and reports lost tracks as uncertain.
Its JSONL consumer and state machine currently pass 18 software tests.

## Track and integration
Track A: PipeGen. The five-stage pipeline, supported model, precision, actual
input, generated application export and speed report must be recorded after
the real application finishes setup and generation. The custom module performs
metadata analysis and does not replace PipeGen, TensorRT or DeepStream inference.

## Privacy and explainability
No facial recognition. Analytics store metadata rather than raw identifiable
frames. Each event includes a source frame, timestamp, camera, zone, tracking ID,
confidence and bounding box. Observed exits and missing detections have distinct
event types so the timeline does not imply certainty the camera did not provide.

## Before finalizing this description
- Replace planned integration with the actual generated pipeline and run command.
- Identify actual model, engine precision, input and tested hardware.
- Include measured speed/latency only from actual reports; benchmark latency is
  not automatically end-to-end application latency.
- Link real Pipeline IR and speed-report screenshots, live demo and emitted events.
- Confirm generated-export redistribution permissions and video provenance.
- Include a verified GitHub URL and accurate limitations.
- Do not claim INT8/Jetson bonus for FP16 alone.
