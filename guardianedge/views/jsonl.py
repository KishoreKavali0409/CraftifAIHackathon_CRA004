"""Present incidents separately from human-readable diagnostics."""
import json
from typing import TextIO

class JsonlView:
    """MVC view: render events and diagnostics without changing model state."""

    def __init__(self, output: TextIO, diagnostics: TextIO):
        # Inject streams so CLI files, pipes and in-memory tests share the view.
        self.output = output
        self.diagnostics = diagnostics

    def events(self, events):
        # Keep stdout pure JSONL; flushing makes alerts available immediately.
        for event in events:
            print(json.dumps(event, allow_nan=False), file=self.output, flush=True)

    def error(self, message):
        # Diagnostics must not corrupt the machine-readable incident feed.
        print(message, file=self.diagnostics)

    def completed(self, count):
        print(f"Processed {count} metadata frames. Upstream inference provenance requires separate verification.", file=self.diagnostics)
