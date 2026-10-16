# MVC architecture

GuardianEdge uses Python 3.10+ and the standard library. MVC applies to the implemented metadata analytics application. Actual PipeGen generation, inference, and its metadata adapter are still pending.

## Responsibilities

- **Model — `guardianedge/models/zones.py`:** validates normalized observations, owns per-camera/person/zone state, applies polygon and persistence rules, and creates incident dictionaries. No file, console, GUI, or transport I/O.
- **Controller — `guardianedge/controllers/metadata.py`:** accepts a normalized frame or a JSONL stream, invokes the model, forwards events to the view, and stops malformed streams with a nonzero status. It does not implement zone geometry or tracking.
- **View — `guardianedge/views/jsonl.py`:** renders machine-readable incident JSONL to an injected output stream and human-readable errors/status to a separate diagnostics stream. It does not change incident state. The current view is a CLI presentation, not a web dashboard.
- **Composition root — `guardianedge/__main__.py`:** parses arguments, loads configuration, creates the model/view/controller, and connects stdin/stdout/stderr.
- **Compatibility — `guardianedge/zones.py`:** preserves existing public imports of ZoneEngine and point_in_polygon.

## Runtime flow

```text
Real PipeGen detector + tracker (pending)
    -> verified schema adapter (pending)
    -> MetadataController.process_frame(normalized_frame)
    -> ZoneEngine.process(frame)
    -> JsonlView.events(events)
    -> incident JSONL
```

The existing command also supports normalized JSONL input:

```sh
python3 -m guardianedge --config config/zones.json < normalized-frames.jsonl > incidents.jsonl
```

For a future in-process adapter, create one controller per processing session:

```python
import sys
from guardianedge.models.zones import ZoneEngine
from guardianedge.controllers.metadata import MetadataController
from guardianedge.views.jsonl import JsonlView

controller = MetadataController(
    ZoneEngine(zones=zone_configuration),
    JsonlView(sys.stdout, sys.stderr),
)
# Call for every real processed frame, including empty detections:
# controller.process_frame(normalized_frame)
```

Input must follow the README contract. Track IDs must come from a verified upstream tracker. Invalid direct frames raise validation errors; the JSONL controller reports a line number and exits with status 2. Output failures propagate; adapters must not retry already processed frames blindly. Processing is synchronous; controllers/models are not shared across threads.

## Verification

Run `python3 -m unittest discover -s tests -v`. Model tests cover safety transitions and atomic validation; CLI tests cover command behavior; controller tests use real models and in-memory streams to verify event presentation, direct frame ingestion, malformed-stream termination, and rejection of empty evidence. Synthetic inputs are not proof of PipeGen inference.
