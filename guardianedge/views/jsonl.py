"""Present incidents separately from human-readable diagnostics."""
import json
from typing import TextIO

class JsonlView:
    def __init__(self, output: TextIO, diagnostics: TextIO):
        self.output = output
        self.diagnostics = diagnostics

    def events(self, events):
        for event in events:
            print(json.dumps(event, allow_nan=False), file=self.output, flush=True)

    def error(self, message):
        print(message, file=self.diagnostics)

    def completed(self, count):
        print(f"Processed {count} metadata frames. Upstream inference provenance requires separate verification.", file=self.diagnostics)
