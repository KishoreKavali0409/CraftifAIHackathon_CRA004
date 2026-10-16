"""Read normalized JSONL frame metadata from stdin; write incident JSONL to stdout."""

import argparse
import json
import sys

from .zones import ZoneEngine


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", required=True, help="JSON zone configuration")
    args = parser.parse_args()
    try:
        with open(args.config, encoding="utf-8") as source:
            configuration = json.load(source)
        engine = ZoneEngine(configuration["zones"], configuration.get("confirm_frames", 3),
                            configuration.get("min_confidence", 0.5))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2
    count = 0
    for line_number, line in enumerate(sys.stdin, 1):
        if not line.strip():
            continue
        try:
            events = engine.process(json.loads(line))
        except (ValueError, TypeError, KeyError) as exc:
            print(f"Metadata error at line {line_number}: {exc}", file=sys.stderr)
            return 2
        count += 1
        for event in events:
            print(json.dumps(event, allow_nan=False), flush=True)
    if not count:
        print("No frames received; no inference or incident evidence produced.", file=sys.stderr)
        return 2
    print(f"Processed {count} metadata frames. Upstream inference provenance requires separate verification.",
          file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
