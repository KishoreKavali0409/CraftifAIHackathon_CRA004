"""Read normalized JSONL metadata from stdin; write incident JSONL to stdout."""
import argparse
import json
import sys
from .controllers.metadata import MetadataController
from .models.zones import ZoneEngine
from .views.jsonl import JsonlView


def main():
    """Composition root: wire MVC components to CLI arguments and streams."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="JSON zone configuration")
    args = parser.parse_args()
    # Create one model/controller per invocation; do not share mutable state.
    view = JsonlView(sys.stdout, sys.stderr)
    try:
        with open(args.config, encoding="utf-8") as source:
            configuration = json.load(source)
        engine = ZoneEngine(configuration["zones"], configuration.get("confirm_frames", 3),
                            configuration.get("min_confidence", 0.5))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        view.error(f"Configuration error: {exc}")
        return 2
    # Runtime orchestration belongs to the controller, not the CLI entry point.
    return MetadataController(engine, view).run(sys.stdin)


if __name__ == "__main__":
    raise SystemExit(main())
