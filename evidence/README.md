# Genuine evidence inventory

- `pipeline-ir.png`: screenshot of the actual PipeGen interactive Pipeline IR graph.
- `PipelineIR.json`: actual generated IR copied before the model node was updated to its TensorRT plan. Preserve as generation evidence; do not treat it as the final exported application.
- `tensorrt-speed.png`: screenshot of PipeGen's actual engine benchmark summary.
- `PipeGen-ModelStage.json`: unmodified PipeGen model-stage report including build warnings and measured engine results.

The MX550 model benchmark reports 18.539 ms per inference (16.925 ms GPU compute), approximately 54 FPS derived, and 27.08 W from nvidia-smi telemetry. These are engine-only measurements, not decoded-video or complete application throughput. Power telemetry under WSL is retained as vendor-reported data, not an independently calibrated measurement. Accuracy has not been measured.

The FP16-requested TensorRT 10.3 engine contains 208 FP16 layers, 18 FP32 layers and one UNKNOWN layer. It is mixed precision; it is not INT8. Engine size reported by PipeGen is 20.3 MB; build time 33.7 seconds is not inference latency.

The vendor report also includes a **modelled Jetson Orin NX comparison**. No Jetson was used. Do not present those predictions as this laptop's measurements or claim a Jetson bonus. Coverage and layer-prediction warnings remain in the original report.

Actual DeepStream inference, exported source and native zone overlay have now been verified. The final recording decoded fully without errors. `pipegen-metadata.json` is the actual 1442-frame output, `incidents.jsonl` contains its 140 derived events, and `verification-summary.json` records counts and exit/reentry examples. `zone-demo-frame.png` is an unmodified frame extracted from genuine output, not a mocked interface. `zone-demo.mp4` is a local deliverable and is excluded from Git. Synthetic unit tests are kept separate from inference evidence.
