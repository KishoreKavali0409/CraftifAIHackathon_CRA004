"""Read normalized JSONL metadata from stdin; write incident JSONL to stdout."""
import argparse
import json
import sys
from .controllers.metadata import MetadataController
from .models.zones import ZoneEngine
from .views.jsonl import JsonlView


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="JSON zone configuration")
    args = parser.parse_args()
    view = JsonlView(sys.stdout, sys.stderr)
    try:
        with open(args.config, encoding="utf-8") as source:
            configuration = json.load(source)
        engine = ZoneEngine(configuration["zones"], configuration.get("confirm_frames", 3),
                            configuration.get("min_confidence", 0.5))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        view.error(f"Configuration error: {exc}")
        return 2
    return MetadataController(engine, view).run(sys.stdin)


if __name__ == "__main__":
    raise SystemExit(main())
