# GuardianEdge AI — Antigravity continuation context

Updated: 16 October 2026, approximately 21:12 IST. Read this file before resuming. This is an engineering handoff, not evidence that the hackathon project is complete.

## Mission and priorities

User wants a real CraftifAI PipeGen Track A hackathon submission before **16 October 2026 at 11 PM IST** according to their latest announcement. Original SF brief has a different time/event; verify the active wildcard submission form. Prioritize mandatory working submission, then competitive improvements. Work autonomously on routine engineering. Ask only for required downloads, authentication/OTP, permissions, essential GUI interactions and final submission confirmation. Never ask for passwords or tokens in chat.

Read `AGENTS.md` and `CODEX_HANDOFF.md` fully. They are the original handoff and contain useful requirements, but their installation status is OLD. This context supersedes their earlier status claims. Preserve working Docker Desktop, WSL and GPU integration. Do not install a competing Linux Docker daemon, podman-docker or replace NVIDIA drivers. Never fake benchmarks, graphs, exports, screenshots or inference events.

## Current blocker and immediate next action

**PipeGen 0.5.1 is installed and SIGNED IN as of the latest actual GUI observation. Its full DeepStream runtime is cached and container craftifai-amd64-v3 is running. The real Requirement wizard is active, clearer sample_720p.mp4 input was accepted, and the selected RestrictedAreaMonitoring catalog source is downloading its YOLO11s ONNX model. No TensorRT compile, live inference, speed report or export yet.**

The user asked where the credentials are. Explained: use their CraftifAI Developer email/password used for downloads; Sign up or Forgot Password if needed. Agent does not possess account credentials. User must enter secrets in official app/site themselves.

Latest attempt to inspect the window via Codex Computer Use immediately returned: “Computer Use was stopped by the user with the physical Escape key.” No further GUI actions occurred. Codex instructed user to click PipeGen title bar and try Tab; effectiveness is UNKNOWN. Respect the stop and obtain renewed authorization before resuming this agent's GUI control. Do not infer that PipeGen is frozen from this alone. Diagnose focus/input versus process hang. Do not reinstall the runtime or repeat its huge download.

## Locations and machine

- Windows user: `C:\Users\kisho`; WSL distro: `Ubuntu-22.04`; Linux user: `kishore`.
- **Canonical Git repository and runtime workspace:** `/home/kishore/craftifai/guardianedge-ai`.
- Windows review/output mirror: `C:\Users\kisho\Documents\Codex\2026-10-16\ls-lh-mnt-c-users-kisho\outputs\guardianedge-ai`.
- Private scratch/download backup: `C:\Users\kisho\Documents\Codex\2026-10-16\ls-lh-mnt-c-users-kisho\work`.
- Original handoff/PDF files: `C:\Users\kisho\Downloads\guardianedge_codex_handoff` and Downloads.
- GPU: NVIDIA GeForce MX550, **2048 MiB VRAM**, Windows driver 610.60. Ubuntu and actual PipeGen container GPU passthrough verified.
- Docker Desktop 4.95; Engine 29.8.2; Ubuntu Docker command uses Desktop integration.
- WSL display `:0`; actual GUI opened, so X11 startup works. Current input problem unresolved.
- No MCU/ESP32 board and **no cloud GPU access**. User switched to faster internet and confirmed connected.
- Windows bundled Python: `C:\Users\kisho\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
- In Codex sandbox, WSL access returned `Wsl/Service/E_ACCESSDENIED`; rerunning the same command with approved elevated tool access succeeded. This is not proof of a broken WSL install.

## Installation and runtime — completed

Official user downloads:

- `C:\Users\kisho\Downloads\PipeGen_0.5.1_amd64.deb` (88,214,664 bytes).
- SHA256: `FDA8E0D45423F14929C291D054EF6E5D01F1E0C1586536C5B2779777EFE6586C`.
- `pipegen_prerequisites_ubuntu_x86.sh` (11,194 bytes), fully read, deliberately NOT run: it configures/restarts a separate Linux Docker runtime.

Inspected package/postinst and installed via APT. `pipegen --version` prints `PipeGen version 0.5.1`. Launcher `/usr/local/bin/pipegen`, application `/opt/PipeGen/run` / `/opt/PipeGen/PipeGenApp`. Installed official signed NVIDIA Container Toolkit 1.20.1-1 plus dependencies to satisfy launcher prerequisite; did NOT change Docker runtime configuration or restart/replace daemon. All official preflight checks passed.

Exact runtime image **fully downloaded**:

```text
craftifaidocker/deepstream:7.1-amd64-v3
sha256:87b0bd90d18b92e24b539348ae93c58c42c636b3e379109b073ad0a7466dfd30
```

Actual app container **`craftifai-amd64-v3`** was running at last check. Inside it verified GPU MX550 2048 MiB, `/usr/bin/deepstream-app`, `/usr/bin/trtexec`, `/usr/src/tensorrt/bin/trtexec`, ffmpeg and ffprobe. This proves runtime availability, NOT successful model compilation/inference.

Launcher was left running in a terminal session using:

```bash
cd /home/kishore/craftifai/guardianedge-ai
script -e -q -f -c pipegen work/pipegen-retry.log
```

Codex session ID 58175 may not be transferable. Do not kill the app blindly. Inspect `docker ps` and processes first. Earlier logs `work/pipegen-startup.log` (missing toolkit), `work/pipegen-startup-2.log` (DNS failure) are historical; retry log records successful pull. Avoid exposing auth debug logs after sign-in.

Private Windows `work/deepstream-layer-backup/` contains 41 official manifest/config/layer blobs, 13.54 GB, all SHA256 verified; `manifest.json` and `verified.json`. Complete recovery backup, NOT repository content. Skopeo 1.4.1 installed as CLI only, no daemon changes. Never modify Docker Desktop content-store internals.

## Existing implementation

Python standard-library package `guardianedge/`, config `config/zones.json`, tests, JSONL CLI, README, implementation plan, demo runbook, verification ledger, acceptance checklist and draft project description.

**21 tests passed on Windows and Ubuntu**, including regression tests after independent review. Synthetic fixtures verify only custom logic; they are NOT live inference evidence.

Normalized frame input contract:

```json
{"camera_id":"cam1","frame_id":1,"timestamp_utc":"2026-10-16T14:00:00+00:00","width":640,"height":480,"objects":[{"track_id":7,"class_name":"person","confidence":0.9,"bbox":[280,200,60,200]}]}
```

- Stable real upstream track ID required; no fabricated tracking.
- Per-camera strictly increasing integer frame ID; nondecreasing timezone-aware timestamp.
- Finite valid dimensions, confidence, bbox; full frame validated before state mutation (including overflow/duplicate IDs).
- Bottom-center bbox vs normalized polygon, inclusive boundary. Default zone polygon `[[0.4,0.4],[0.8,0.4],[0.8,0.9],[0.4,0.9]]`.
- Three consecutive processed observations inside at confidence >=0.5 opens one `RESTRICTED_ZONE_INTRUSION`.
- Continued inside suppresses duplicates; observed outside yields `ZONE_EXIT` on same incident, metadata-derived dwell duration. Reentry creates a new incident.
- Missing observations reset pending confirmation; missing active track yields `TRACK_LOST` with stale bbox flagged, never an invented observed exit/dwell.
- CLI rejects empty/corrupt input, events on stdout, counters/errors on stderr.

```bash
python3 -m unittest discover -s tests -v
python3 -m guardianedge --config config/zones.json < normalized-frames.jsonl > incidents.jsonl
```

**No actual PipeGen metadata adapter exists yet.** Inspect the generated export/schema first. Adapter must preserve real identities/timestamps and send every processed frame including empty frames. Document video PTS versus wall-clock duration carefully. Do not invent native GUI features.

## Real demo video preparation

Copied bundled NVIDIA sample clips from running container into ignored Linux `media/`:

- `sample_cam5.mp4`
- `sample_office.mp4`
- `sample_720p.mp4`

Original source: `/opt/nvidia/deepstream/deepstream-7.1/samples/streams/` inside container. Respect licensing; do not commit/rehost vendor videos without permission.

Unmodified preview frames successfully extracted to Linux `work/cam5-preview.png` and `work/office-preview.png`, **not yet visually inspected**. Copy to a visible local path and inspect before choosing source/zone. Command known to work:

```bash
docker exec craftifai-amd64-v3 ffmpeg -hide_banner -loglevel error -ss 2 -i /home/kishore/craftifai/guardianedge-ai/media/sample_cam5.mp4 -vframes 1 -y /home/kishore/craftifai/guardianedge-ai/work/cam5-preview.png
```

PowerShell nesting split `-frames:v` incorrectly; use `-vframes 1` or a shell script. Prefer simple commands/scripts over nested PowerShell/bash quoting.

## Mandatory work STILL pending

1. Continue the active Requirement wizard after catalog model download; authentication is now completed.
2. Complete real PipeGen **Requirement → Pipeline IR → Model → Compiler → Run**.
3. Supported lightweight person detector, single stream, batch 1, low memory; FP16 only if supported. 2 GB GPU is a real feasibility constraint.
4. Actual TensorRT engine compiled through PipeGen, **PipeGen speed report** saved. FP16 alone does not qualify INT8 bonus.
5. Real GPU DeepStream run on actual video (video-file input is allowed).
6. Inspect actual export, implement supported metadata adapter/custom zone extension, render zone and save real actionable incident JSON.
7. Match incidents to actual video entries/exits/reentry and verify behavior; capture genuine Pipeline IR, speed report and live-run screenshots, actual export and report. No placeholder evidence.
8. Update README, verification ledger and draft description to measured reality. Existing ledger entries before this context still describe the download as pending: those are historical.
9. Review exported code for secrets/licenses, push permitted source/config/evidence, make repository judge accessible.
10. Verify correct active form, get user profile/subjective feedback answers, prepare final submission, ask final confirmation, submit and capture receipt.

Suggested requirement prompt is already in `docs/pipegen-requirement.txt`. Preserve the genuine generated pipeline. A Python-only detector substitute fails mandatory integration.

## GitHub and commits

Repository: **https://github.com/KishoreKavali0409/guardianedge-ai** — **PRIVATE** at last verification, not yet accessible to unauthenticated judges. GitHub CLI device authentication completed by user; do not repeat unless expired. Ubuntu `gh` 2.4.0. Never print auth tokens.

Canonical repo branch `main`. Before this handoff, pushed head was `b54f69e` (ledger/status/permissions); previous commits `710c2b5` (overflow atomicity fix) and `a570721` (initial tested source). Use `git log` to obtain handoff commit after this file is committed. No PR exists.

Working push command if credential helper is needed:

```bash
git -c credential.helper= -c 'credential.helper=!/usr/bin/gh auth git-credential' push origin main
```

Ignore credentials, `.env`, work/, installers, videos, engines/plans/ONNX, large backups. Retain real generated artifacts privately as needed; publish only permitted files. User requested commit/push all project work plus this context, not secret or downloaded runtime data.

## Submission links and source material

- Official product/setup: https://developer.craftifai.com/products/pipegen
- Track brief: https://docs.google.com/document/d/1nxSV7QiLeO3DvOLIdt2AOiZQtMqIYqt5m2tSAqqwmAY/edit
- Event reference: https://luma.com/5z8w42mq
- PDF-provided form: https://forms.gle/eJyeCKCG2UH757QZ8
- Resolved form: https://docs.google.com/forms/d/e/1FAIpQLSc3OkTWFA58URYmLmHSNjunO2yJLEEq8aMuaxrT7ROyPHarzA/viewform
- Form title: **Feedback Form: PipeGen Hackathon**. First page explicitly says feedback is required for scoring, judges do not see feedback, and project submission link is on LAST page. No fields filled or submitted yet. User announcement may provide a newer wildcard form; confirm.
- Form asks experience/platform/model/input/stage/time/manual fixes/tool ratings/failures/improvements/use again; user must provide subjective answers, do not fabricate satisfaction.
- Source PDFs in Downloads: `Embedded SF_ CraftifAI Physical AI Hackathon — Official Problem Statement.pdf`, `ESP32_BLE_FirmGen_Simple_PRD.pdf`, `FirmGen Hands On Lab.pdf`. Last two are Track B, not required for this project.
- PipeGen lab Google doc https://docs.google.com/document/d/15HpN0QEd8UMjtQVhQ_OdcJoq09JsuSZIBh-VntsnfB4/edit required Google login; not accessed.

## Recommended continuation order

Refresh time and remaining deadline. Inspect existing container/app without disrupting it. Fix actual input problem and let user authenticate. While awaiting login inspect preview clips and choose a credible demo zone. Capture a working base pipeline/export/benchmark FIRST. Add real adapter/zone logic and evidence. Publish honest results and finalize form with confirmation. Do not claim completion on the basis of the passing unit tests alone.

## MVC implementation update — 16 October 2026

The metadata analytics now uses `guardianedge/models/zones.py`, `controllers/metadata.py`, and `views/jsonl.py`. The CLI is a composition root and the old `guardianedge.zones` imports remain compatible. `MetadataController.process_frame` is the integration entry point for a future verified PipeGen adapter. See `docs/architecture.md`. The 25-test suite includes controller coverage; these remain synthetic logic tests, not inference evidence. PipeGen authentication/input and all mandatory generation/runtime evidence remain pending.


## Latest runtime continuation

Actual PipeGen project directory: `/home/kishore/.pipegen/kishorekishore0409/96ced244-f937-4552-bf25-e1d5425b5efb`. Selected catalog source: `/home/kishore/.pipegen/kishorekishore0409/cache/catalog/backup-19-repos/RestrictedAreaMonitoring/RestrictedAreaMonitoring`. Read its application.py; it is the original ONNX/OpenCV reference, not the generated DeepStream export. Do not run it as a substitute. Actual GUI must generate the DeepStream pipeline. Model downloader uses gdown to fetch a ready ONNX from its vendor-specified Google Drive URL; a 26 MB partial file was observed around 21:12 IST. Do not execute duplicate downloads while the app works. Restart launcher session 40455 is active; keep it running. Code comments pushed as c63a996; all25 tests verified again.
