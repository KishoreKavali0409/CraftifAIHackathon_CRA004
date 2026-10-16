#!/usr/bin/env bash
# Composition script: real PipeGen GPU pipeline -> schema adapter -> MVC events.
# Uses the verified existing PipeGen container; does not replace Docker setup.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
INPUT="${1:-$ROOT/media/sample_720p.mp4}"
HEADLESS=1
if [[ "${2:-}" == "--display" ]]; then HEADLESS=0; fi
if [[ ! -f "$INPUT" ]]; then
  echo "Video not found. Pass an absolute Linux path under /home/kishore." >&2
  exit 2
fi
INPUT="$(realpath "$INPUT")"
if [[ "$(docker inspect -f '{{.State.Running}}' craftifai-amd64-v3 2>/dev/null || true)" != "true" ]]; then
  echo "Start Docker Desktop and launch pipegen first; its verified container must be running." >&2
  exit 2
fi
if [[ ! -f pipegen-export/models/yolo11s.fp16.plan ]]; then
  echo "The full local PipeGen export with model assets is required. Model binaries are excluded from Git." >&2
  exit 2
fi
RUN_DIR="$ROOT/work/run-$(date -u +%Y%m%dT%H%M%SZ)"
mkdir -p "$RUN_DIR"
python3 -m scripts.apply_zone_overlay --export pipegen-export --config config/pedestrian-demo.json
# JSON metadata and the video are from the real GPU pipeline. Incident time is
# media PTS; the adapter explicitly marks it as not a capture UTC date.
docker exec \
  -e PG_ROOT="$ROOT/pipegen-export" \
  -e PG_OUT="$RUN_DIR" \
  -e PG_INPUT_KIND=file \
  -e PG_INPUT_URI="file://$INPUT" \
  -e PG_HEADLESS="$HEADLESS" \
  craftifai-amd64-v3 bash "$ROOT/pipegen-export/pipeline/pipeline.sh" \
  > "$RUN_DIR/pipeline.log" 2>&1
python3 -m guardianedge.adapters.pipegen \
  --input "$RUN_DIR/metadata.json" --config config/pedestrian-demo.json \
  > "$RUN_DIR/incidents.jsonl"
echo "Completed real GPU run. Results: $RUN_DIR"
echo "Metadata: metadata.json; incidents: incidents.jsonl; runtime: pipeline.log"
if [[ "$HEADLESS" == "1" ]]; then echo "Annotated video: output.mp4"; fi
