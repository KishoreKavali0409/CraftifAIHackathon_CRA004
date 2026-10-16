# Verified versus pending

## 2026-10-16 18:36 IST — takeover
- Read supplied AGENTS.md and CODEX_HANDOFF.md completely.
- `/home/kishore/craftifai/guardianedge-ai` exists and was empty.
- Ubuntu Docker command connects to Docker Engine 29.8.2.
- DISPLAY is :0. PipeGen command absent.
- No PipeGen/prerequisite/.deb files found within Downloads depth 2.
- C: free space: 131,529,170,944 bytes (about 122 GiB).
- Previous GPU-container test is handover evidence; not rerun and not TensorRT proof.
- User asked to download official installer and prerequisite package while preparatory work proceeds.

## Pending mandatory evidence
All five PipeGen stages; installed product/version; actual TensorRT engine;
PipeGen speed report; live DeepStream inference; real actionable event output;
actual export; screenshots; GitHub URL; active deadline/form; submission receipt.

## Implementation decisions
- Keep a reviewable Windows output copy and synchronize source to the existing Linux workspace.
- Build only metadata safety logic before installer access. No substitute detector.
- Require stable upstream object IDs; do not silently combine different people into one incident.
- Track disappearance is an observation gap, not proof that a person exited a zone.

## 2026-10-16 — installer admission progress
- Official downloads supplied by the user: PipeGen_0.5.1_amd64.deb and prerequisite shell script.
- Package SHA256: FDA8E0D45423F14929C291D054EF6E5D01F1E0C1586536C5B2779777EFE6586C.
- Read complete prerequisite script; did not execute it because it configures a Linux Docker runtime/service.
- Inspected package metadata and postinst; APT preview: one new package, no removals/upgrades.
- Installed PipeGen; `pipegen --version` prints `PipeGen version 0.5.1`.
- Initial launch failed solely on missing host NVIDIA Container Toolkit; all other checks including X11 passed.
- Added NVIDIA's signed stable repository using official instructions; installed Toolkit 1.20.1-1 and three library/base packages. No Docker runtime reconfiguration, daemon replacement or restart.
- Retried launch: ALL PipeGen prerequisite checks pass. App is pulling its selected image `craftifaidocker/deepstream:7.1-amd64-v3`.
- Live GUI, account login and pipeline remain pending until pull/startup finishes.
- Original brief's submission URL resolves to the PipeGen feedback form; it explicitly says project submission is linked on the last page and feedback is required for scoring. Did not fill or submit.
- Zone-engine tests written before implementation: initial run failed on missing module; implemented engine then 14/14 passed.
- CLI tests written first: all four failed on missing entry point; implementation added, full-suite verification follows.

## 2026-10-16 19:00–19:05 IST — source and review
- CLI plus zone suite passed 18/18 on Windows and Ubuntu.
- Reverified actual cached CUDA-container GPU passthrough after Toolkit installation; saved timestamped `work/setup-verification.txt` in the Linux workspace.
- GitHub user completed official device authentication; verified account KishoreKavali0409.
- Created PRIVATE repository https://github.com/KishoreKavali0409/guardianedge-ai and pushed initial source commit a570721. It remains private until a judge-ready artifact is available.
- Independent read-only review found one Important issue: derived coordinate overflow could occur after partial state mutation.
- Added three regression tests first; observed two overflow errors and one missing-validation failure.
- Moved coordinate derivation/validation before mutation; rejects unrepresentable integers and nonfinite derived positions as ValueError.
- Full suite passed 21/21 on Windows and Ubuntu after the fix; pushed commit 710c2b5 to the private repository.
- GUI was paused after user pressed Escape; user explicitly authorized resuming PipeGen GUI control.
- Actual image manifest reports 44 layers, 12.61 GiB compressed. Large layers are actively transferring; application GUI and all five pipeline stages are still pending.

## Review scope decisions
- Upstream tracker stability, real inference provenance and exported schema remain pending integration checks, not unit-test claims.
- Frame-number gaps and equal timestamps follow the documented processed-observation/nondecreasing-time contract. The actual adapter must send every processed observation, including empty frames.
- No other concrete code findings or deferred minor findings from the review pass.

## 2026-10-16 19:20 IST — runtime download blocker
- First vendor-image pull failed with `lookup registry-1.docker.io: no such host`; secondary progress client also reported auth.docker.io DNS failure.
- Verified Windows DNS answers and Ubuntu HTTPS connectivity (registry HTTP 401, auth endpoint HTTP 404), indicating DNS/connectivity had recovered.
- Retried the official launcher using `script -e -q -f -c pipegen work/pipegen-retry.log`, keeping a detailed progress log.
- Some previously downloaded but unfinalized layers restarted; finalized layers can be reused. Do not assume partial bytes survived.
- Runtime download remains active. No PipeGen GUI, model compilation, engine, benchmark or live inference verified yet.
- User confirmed no organizer-provided cloud GPU access is available; continue local path.
- User explicitly authorized resuming PipeGen GUI control after the earlier Escape interruption.

## MVC refactor — 16 October 2026
- Separated domain model, metadata controller, and JSONL presentation. Existing CLI and public ZoneEngine imports preserved.
- Added four controller integration tests using the real model and in-memory streams. Observed missing MVC modules fail first, then all 25 tests passed on Windows after implementation.
- The real PipeGen metadata adapter, account authentication and runtime evidence are still pending; no detector or benchmark results claimed.

## 16 October 2026, approximately 21:00 IST — resumed pipeline setup
- Pushed MVC explanatory comments as c63a996; all 25 tests passed on Windows and Ubuntu. No runtime behavior changed.
- Existing PipeGen container had exited normally. Restarted official launcher; all prerequisite checks passed and cached runtime reused.
- Actual PipeGen main screen now shows signed-in user. Account authentication is no longer the current blocker.
- Submitted GuardianEdge requirement in the actual app; it parsed input/output and opened its nine-step requirement configuration wizard. This is not completion of the Requirement stage.
- Inspected real bundled video previews; requested changing the initial fisheye sample_cam5.mp4 to clearer sample_720p.mp4 with pedestrians. Input update is processing; verify final persisted settings in app.
- Actual container GPU check: MX550 2048 MiB, 0 MiB allocated before model compilation. No engine, speed report, inference result or export yet.

- Actual app accepted sample_720p.mp4: H.264 1280x720, 30 fps, 48.067 seconds verified with ffprobe. Selected RestrictedAreaMonitoring catalog source rather than unrelated abandonment example; actual vendor downloader is active. ONNX/OpenCV reference inspected, not executed as replacement inference.

## Final code and runtime verification on 16 October 2026
- Requirement, Pipeline IR, Model, Compiler and Run completed in real PipeGen 0.5.1.
- Actual YOLO11s TensorRT 10.3 engine compiled in 33.7 s, 20,298,204 bytes; requested FP16 with 208 FP16/18 FP32/1 unknown layers. Engine SHA256 recorded in evidence.
- PipeGen measured 18.539 ms inference frame time, 16.925 ms GPU compute and about 54 derived FPS. This is not end-to-end video throughput. Genuine speed/IR screenshots and unmodified report saved.
- Generated DeepStream application ran real NVIDIA sample video. Actual export completed at 2026-10-16T16:06:49Z. Untouched export retained privately; working copy includes native zone view and recording mux fix.
- Actual frame_json.h and emitted metadata inspected. MVC adapter implemented against observed fields; preserves empty frames, real tracking IDs, boxes, dimensions and media PTS. No inference replacement.
- Review found optional provenance inconsistency and submicrosecond PTS regression; two regressions observed failing before fixes. All 32 tests pass in final Windows and Ubuntu runs. Reviewer recheck found no remaining concrete bugs.
- Final one-command runner completed all 1,442 real frames and 13,754 object records; MVC output: 70 intrusion confirmations, 10 observed exits, 60 track-loss events. Same-ID observed exit/reentry examples recorded in verification-summary.json.
- Native zone overlay compiled and was visually confirmed in real recorded output. Initial fragmented MP4 emitted FFmpeg decode warnings; switched recording mux to mp4mux faststart. Final entire video decode exit 0 with no errors.
- Actual deliberately corrupt video rejected by GStreamer with exit 1, not reported as a successful empty run.
- Final run: work/run-20261016T162714Z. Genuine metadata, incidents, runtime logs, final video and both unit test transcripts are in the Windows evidence directory.
- Time limitation disclosed: media-relative PTS is represented against a 1970 epoch and explicitly labelled; it is not capture UTC. Alerts are analyzed after the run, and frequent tracking/threshold losses fragment incidents.
- User will submit personally. Do not submit forms or change account authentication on their behalf.
