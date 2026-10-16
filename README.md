# GuardianEdge AI

Industrial safety analytics prototype for CraftifAI PipeGen Track A.

## Implemented and verified

The real PipeGen 0.5.1 workflow completed Requirement, Pipeline IR, Model, Compiler and Run. It generated a DeepStream application, compiled a YOLO11s TensorRT engine, benchmarked it, ran a real NVIDIA sample video, and exported the application. The MVC analytics consumes its actual tracked metadata and produces intrusion, observed-exit and track-loss events. A native presentation extension draws the configured demonstration zone in the actual DeepStream output.

This is a working prototype, not a production safety system or a completed submission. Submission form review and confirmation remain pending.

## MVC structure

| Layer | Location | Responsibility |
|---|---|---|
| Model | `guardianedge/models/zones.py` | Geometry, validated state, three-observation confirmation, incident lifecycle |
| Controller | `guardianedge/controllers/metadata.py` | Frame/stream orchestration and errors |
| View | `guardianedge/views/jsonl.py` | Incident JSONL and separate diagnostics |
| Native view installer | `scripts/apply_zone_overlay.py` | Add zone display metadata to exported DeepStream frames |
| Adapter | `guardianedge/adapters/pipegen.py` | Map the inspected, real DeepStream JSON schema |
| Composition | `guardianedge/__main__.py` | CLI arguments, configuration, dependency wiring |
| Generated pipeline | `pipegen-export/` | Actual PipeGen export, with documented overlay and recording changes |

See [architecture](docs/architecture.md) and [runtime evidence](evidence/README.md). Existing `guardianedge.zones` imports remain supported.

## Test the code

Python 3.10+; analytics uses only the standard library:

```bash
python3 -m unittest discover -s tests -v
```

Tests use synthetic fixtures. Actual inference evidence is separately recorded in `evidence/`.

## Run on this configured laptop

Open Ubuntu 22.04, keep Docker Desktop and the PipeGen application running, then:

```bash
cd /home/kishore/craftifai/guardianedge-ai
bash scripts/run_guardianedge.sh
```

The default source is the locally installed NVIDIA sample `media/sample_720p.mp4`. To use another video visible inside the existing container:

```bash
bash scripts/run_guardianedge.sh /home/kishore/path/to/video.mp4
```

Add `--display` as the second argument for live display. Default recording mode writes `output.mp4`, actual `metadata.json`, `pipeline.log`, and the MVC `incidents.jsonl` into a new timestamped `work/run-...` folder. Incidents are processed after the video run completes; continuous streaming alerts are not implemented. The zone configuration is `config/pedestrian-demo.json`.

The full local export includes model assets. Git excludes ONNX/engine/video binaries. For a Git clone, obtain the original model using the vendor catalog download instructions in [reproduction](docs/reproduction.md), or use the full local export. Original exported `run.sh` is also included; its standalone first-run workflow has not been separately verified on a clean machine.

## Analyze already-recorded real metadata

```bash
python3 -m guardianedge.adapters.pipegen \
  --input evidence/pipegen-metadata.json \
  --config config/pedestrian-demo.json > work/replayed-incidents.jsonl
```

Generic normalized JSONL remains supported:

```bash
python3 -m guardianedge --config config/zones.json \
  < normalized-frames.jsonl > incidents.jsonl
```

Neither analysis command runs a detector. The real detector is the PipeGen-generated DeepStream pipeline.

## Time, geometry and identity

Zone polygons use normalized frame coordinates. The model checks a person's bounding-box bottom-center; three consecutive qualifying observations at confidence >=0.5 confirm an intrusion. Continued presence suppresses repeated entry alerts. Observed outside closes the incident; reentry creates a new ID. Lost/low-confidence tracks produce `TRACK_LOST`, not an invented exit.

The adapter uses actual `frame`, `source_id`, `pts_ns`, dimensions, labels, boxes and tracker IDs. Every processed observation is retained, including empty person detections. It rejects unconfirmed person identities and missing/unknown PTS. Events preserve `source_pts_ns` and `timestamp_basis=media_pts_epoch_not_capture_utc`. The 1970 date in `timestamp_utc` is an explicit representation of relative video time, **not the capture date**. Dwell is derived from video PTS, not Python processing speed. Do not infer personal identity from tracker IDs.

## Measured performance and limitations

On this MX550 2 GB laptop, PipeGen's engine benchmark reports 18.539 ms per inference (~54 FPS derived), with 16.925 ms GPU compute. The FP16-requested engine is mixed precision: 208 FP16, 18 FP32 and one unknown layer. The live display screenshot separately shows 17.36 FPS and dropped frames. These measurements are different scopes; neither is an accuracy measurement. Modelled Jetson predictions in the vendor report are not measurements from this machine.

The demonstration uses a public bundled street video and an explicitly labelled demonstration zone. It is not an industrial-site validation. The first complete overlay run yielded 70 intrusion confirmations, 10 observed exits and 60 track-loss events across 1,442 frames. Frequent track loss and threshold crossings fragment incidents; the system is not validated for worker protection. Stable identity across long occlusion/reentry is not guaranteed. No facial recognition is performed by this code.

## Submission status

Actual graph, benchmark report, live-run screenshot, generated sources, zone-overlay frame and real metadata/events are present. Check [acceptance](docs/acceptance-checklist.md) and [verification ledger](docs/verification-ledger.md) for remaining checks. Repo visibility, active wildcard form, user feedback and final submission confirmation must be verified before claiming submission.
