# Reproduction and export provenance

## Full local package

The actual PipeGen export was created by the app on 2026-10-16T16:06:49Z, with manifest project ID `96ced244-f937-4552-bf25-e1d5425b5efb`. The untouched export remains in the Linux project's ignored `work/vendor-export/` directory. `pipegen-export/` is a working copy of that genuine export.

Custom changes to the working copy:

1. `meta_json.cpp` calls the presentation-only `guardianedge_zone` helper before serializing metadata.
2. `guardianedge_zone.h` is generated from `config/pedestrian-demo.json` by the overlay installer; its Makefile dependency triggers a rebuild.
3. The recording sink uses `mp4mux faststart=true` instead of fragmented qtmux after the first recording caused FFmpeg NAL-unit decode warnings. The initial still image was visually verified; final recording validation is recorded in `evidence/verification-summary.json` and the runtime evidence.

Run the installer as a module from the repository root:

```bash
python3 -m scripts.apply_zone_overlay --export pipegen-export --config config/pedestrian-demo.json
```

The installed-machine runner invokes this command automatically, then runs the generated pipeline in the existing PipeGen container and analyzes its actual metadata through the MVC controller. It does not replace the detector, model parser, TensorRT inference or upstream tracker.

## Model assets

The original catalog's inspected `model/download.sh` fetches ready YOLO11s ONNX using:

```bash
gdown --fuzzy https://drive.google.com/file/d/1OQIrwowlFJ65QMT12yL1OmDMLM1NKZm-/view
```

This command was supplied by the official catalog; downloads are governed by their original model terms. Place the downloaded model at `pipegen-export/models/yolo11s.onnx`. Expected SHA256:

```text
f8d06a921024c1a46091d48a59a8e377ba189f14250df167fe82f408ca37814b
```

The real local prebuilt engine has SHA256:

```text
5c49b9100087df47324b89249553ca79a11a6349a1e85aeb242ee74dddbaeac8
```

The engine is GPU/TensorRT-specific. The original export launcher can rebuild it; inspect its own README and requirements. A clean-machine standalone rebuild has not been tested here. Model binaries and NVIDIA sample media are deliberately excluded from Git, while the full local output package retains the actual model assets for the user.

## Demonstration inputs and output

The source was copied from the vendor container's `/opt/nvidia/deepstream/deepstream-7.1/samples/streams/sample_720p.mp4`, H.264 1280x720 at 30 FPS, 48.067 seconds. Use your own licensed video or the locally installed sample. The native overlay labels the polygon as a DEMO zone. Original and generated vendor notices are retained; no new blanket license for vendor assets is asserted.

Metadata is genuine DeepStream output; the custom adapter filters the person class for analytics. Event UUIDs differ when replaying the same metadata; compare event type, source frame, track and zone instead of UUIDs. Source PTS is recorded to avoid pretending video-relative time is a capture UTC timestamp.
