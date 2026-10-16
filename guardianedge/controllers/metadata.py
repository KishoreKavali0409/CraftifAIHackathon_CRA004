"""Coordinate normalized input, domain processing and presentation."""
import json
from ..models.zones import ZoneEngine
from ..views.jsonl import JsonlView

class MetadataController:
    """MVC controller: connect observations to the model and event view.

    Geometry and incident decisions stay in the model; serialization stays
    in the view. One instance handles a single synchronous session.
    """

    def __init__(self, model: ZoneEngine, view: JsonlView):
        self.model = model
        self.view = view

    def process_frame(self, frame):
        """Process a normalized observation; validation errors propagate.

        Upstream adapters must provide real track IDs and timestamps and send
        every processed frame, including observations containing no objects.
        """
        # Validation occurs in the model before events reach presentation.
        # Do not retry a processed frame after an output failure blindly.
        self.view.events(self.model.process(frame))

    def run(self, source):
        """Read JSONL, stopping at the first invalid observation."""
        count = 0
        for line_number, line in enumerate(source, 1):
            # Ignore blank transport lines; they are not processed frames.
            if not line.strip():
                continue
            try:
                self.process_frame(json.loads(line))
            except (ValueError, TypeError, KeyError) as exc:
                self.view.error(f"Metadata error at line {line_number}: {exc}")
                return 2
            count += 1
        # An empty feed must never look like a successful inference run.
        if not count:
            self.view.error("No frames received; no inference or incident evidence produced.")
            return 2
        self.view.completed(count)
        return 0
