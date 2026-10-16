# CODEX HANDOFF — GuardianEdge AI / CraftifAI Physical AI Hackathon

> **Read this entire handoff, then begin executing the verified next actions.**
> **Date:** 16 October 2026 (India Standard Time). Updated invitation says **11:00 PM IST deadline**, but the original problem-statement PDF lists **4:00 PM**. Confirm the active submission deadline and link with organizers, and aim to submit as early as possible.
>
> **User priorities:** (1) a **valid Track A submission**, (2) a **competitive, innovative, working product**. Do not sacrifice validity for polish.

## 0. Mission and operating rules

You are the on-machine engineering agent responsible for taking this project from current setup to a demonstrable PipeGen Track A submission. Work autonomously for routine checks and coding; ask the user to act for proprietary downloads, CraftifAI sign-in/OTP, GUI interactions you cannot control, privileged commands, irreversible changes, credentials, and final form submission.

**Do not claim any tool, build, benchmark, screenshot, model, pipeline stage, or submission is complete until you verify it.** Never forge evidence. Do not replace PipeGen with a Python-only OpenCV or YOLO demo; that would fail the mandatory integration requirement. Use the real CraftifAI product and its full workflow.

Use small, reversible changes. Don't alter Windows drivers, replace Docker Desktop, run broad `apt autoremove`, delete Docker contexts, reinstall WSL, or install an arbitrary CUDA/DeepStream/TensorRT stack unless official PipeGen WSL2 instructions explicitly require it and the user approves. Preserve existing data and all working configuration. Keep a timestamped log of stages, commands, problems, actual outputs, and evidence paths.

If an external tool or required GUI is not available to Codex, explicitly tell the user the exact action to perform. Do not pretend to operate unavailable software.

## 1. Ground truth: what is ALREADY VERIFIED

Host / Linux:
- Windows host account folder: `C:\Users\kisho`.
- Ubuntu 22.04.5 LTS under WSL2; Linux user `kishore`.
- `nvidia-smi` runs in Ubuntu and shows NVIDIA GeForce **MX550**, **2,048 MiB VRAM**.
- WSL display `DISPLAY=:0` was observed, but full PipeGen GUI/X11 compatibility is **not yet proven**.
- Workspace: `/home/kishore/craftifai/guardianedge-ai`.
- Downloads: `/mnt/c/Users/kisho/Downloads`.
- Git, Python, pip, curl, wget, unzip, compiler tools installed.

Docker:
- Docker Desktop **4.95.0**, Linux Docker Engine **29.8.2** working both from Windows and from Ubuntu WSL integration.
- Ubuntu `docker --version` returns `29.8.2`, and `docker info` connects to the `docker-desktop` Linux engine.
- Previous `podman-docker` wrapper conflict was resolved; **do not install `docker.io`, `podman-docker`, or a competing Docker daemon**.
- Most important: Docker GPU passthrough **PASSED** using:

  ```bash
  docker run --rm --gpus all nvidia/cuda:12.4.1-base-ubuntu22.04 nvidia-smi
  ```

  The command pulled the image and printed NVIDIA GeForce MX550 (2048 MiB) from **inside the container**. This is a verified GPU container test, **not** a verification of TensorRT/DeepStream/PipeGen operation.

Outstanding:
- **PipeGen v0.5.1 has NOT been installed or launched.**
- The official `.deb` and `pipegen_prerequisites_ubuntu_x86.sh` have NOT been observed in Downloads.
- The prior `sudo apt install ./PipeGen_0.5.1_amd64.deb` failed because the file was absent from the current directory.
- Earlier `find` attempts failed because the shell command was mistyped. Avoid escaped-parenthesis syntax if possible.
- No PipeGen PIR graph, compiled TensorRT engine, speed report, live run, or actionable event feed yet.
- GPU VRAM is limited to 2 GB; actual model + DeepStream memory feasibility unknown.
- Windows physical free disk space (not just Linux `df -h`) has not been confirmed.

## 2. Immediate next actions (DO THESE FIRST)

Work from the Ubuntu shell:

```bash
cd ~/craftifai/guardianedge-ai
pwd
command -v docker
docker info --format '{{.ServerVersion}}'
nvidia-smi
echo "$DISPLAY"
```

Locate downloaded PipeGen files, using **simple one-line commands** (do not concatenate `-type f` directly with a parenthesis):

```bash
find /mnt/c/Users/kisho/Downloads -maxdepth 2 -type f -iname '*pipegen*'
find /mnt/c/Users/kisho/Downloads -maxdepth 2 -type f -iname '*.deb'
find /mnt/c/Users/kisho/Downloads -maxdepth 2 -type f -iname '*prerequisite*'
```

If none are found, **stop trying to install the missing file**. Ask user to sign into CraftifAI and download the **official PipeGen v0.5.1 Linux x86-64 `.deb`** and the **official WSL2 prerequisites package/script**. Direct user to:

- https://developer.craftifai.com/dashboard?tab=downloads
- https://developer.craftifai.com/products/pipegen (read the WSL2 tab, not just Linux x86-64)

Once files exist, inspect actual filenames and the official WSL2 guide. Don't guess filenames. Check package/source provenance and avoid arbitrary unofficial downloads.

Official PipeGen site (checked 16 Oct 2026) states: PipeGen v0.5.1; NVIDIA host driver 560.76+ for WSL2; graphical X11 display; WSL2 minimum 30 GB of free space; its first launch can pull a DeepStream image ~12 GB compressed, ~35 GB unpacked. Since Docker Desktop is working, avoid blindly running a generic prerequisite script that would replace/install Linux Docker or a Linux NVIDIA driver. **Review official WSL2 procedure before executing scripts.**

Check physical Windows drive space in PowerShell when needed, e.g. `Get-PSDrive -PSProvider FileSystem`. A large apparent `df -h ~` virtual filesystem does not prove that Windows has sufficient physical storage.

When installation prerequisites are met and the real `.deb` file is present, install with APT using the exact existing path. Example only (do not run unless file exists and is correct):

```bash
sudo apt install /mnt/c/Users/kisho/Downloads/PipeGen_0.5.1_amd64.deb
```

Confirm `pipegen --version` where supported, launch the actual PipeGen GUI, complete user-mediated sign-in, and test initial model/pipeline support. `DISPLAY=:0` alone does not guarantee the required X11 session works.

### Key go/no-go checkpoint

Set a time-box: if PipeGen cannot launch, compile TensorRT, and run a supported single-stream detector on this MX550 after reasonable targeted effort, **surface the hard blocker immediately**. Ask user/organizers for access to an appropriate supported Linux/NVIDIA GPU machine (or official cloud GPU resources). Do not falsely present CUDA container GPU access as successful PipeGen execution. No ESP32/STM32 board is available, so FirmGen-only Track B is *not* a valid fallback without obtaining real hardware.

## 3. Official mandatory challenge constraints — Track A

A valid project must include all of these, not just a proof-of-concept notebook:

1. Use **CraftifAI PipeGen** through **Requirement → Pipeline IR → Model → Compiler → Run**.
2. Compile at least one **real TensorRT engine** with **PipeGen speed report**.
3. Run live on **video file, USB/CSI camera, or RTSP** using NVIDIA GPU/Jetson and PipeGen-generated DeepStream pipeline.
4. Emit **actionable results beyond boxes**, such as actual JSON or MQTT feed, alerts, analytics, or RTSP.
5. Submit actual **PipeGen export folder** and repository, screenshot of Pipeline IR graph, screenshot of speed report, project description and tested demonstration evidence.
6. Deep integration: PipeGen must be *load-bearing*, not an afterthought.

**Optional:** Edge Optimization bonus only if INT8 quantization or Jetson deployment is real and reported, including truthful speed/power/accuracy trade-offs. Do not claim bonus based only on FP16.

Track A does **not** require a FirmGen PRD, microcontroller, FirmGen traceability report, or physical ESP32. Do not waste time preparing Track B-specific artifacts.

Hackathon docs provided to the user earlier: *Embedded SF: CraftifAI Physical AI Hackathon — Official Problem Statement.pdf*. A separate *FirmGen Hands On Lab.pdf* and BLE PRD were provided but are Track B references, not a replacement for Track A requirements.

## 4. Product to deliver

**Name:** GuardianEdge AI — Proactive Industrial Safety Intelligence

**Core problem:** Passive warehouse/factory camera feeds may miss people entering hazard/restricted zones. Build a privacy-conscious real-time edge vision system that detects person-zone violations and creates actionable events.

### Mandatory-first scope (MVP)

- One MP4 input (chosen because official Track A accepts video files) or USB camera, run through PipeGen-generated DeepStream.
- One supported, low-memory pretrained **person-detection** model selected from PipeGen catalog; TensorRT engine built through PipeGen.
- Live detections and clearly displayed polygonal **restricted zone**.
- Deterministic intrusion: check bottom-center of person bounding box against zone polygon (or clearly document an alternative).
- Trigger violation only after >=3 consecutive processed frames inside zone (adjust to supported pipeline capabilities).
- Publish/produce a **real JSON incident event**, containing timestamp, camera ID, zone ID, event type, confidence, bounding box; use actual values from the pipeline.
- Reset event state after person exits; suppress redundant repeated alerts during one continuous incident.
- Prove: test clip with person outside, entering, leaving zone; output changes accordingly.

If a requested logic feature isn't natively implemented by PipeGen, add a small post-processing extension to the actual PipeGen-generated app. Do not invent unsupported PipeGen GUI buttons or CLI commands.

### Competitive enhancements — ONLY AFTER MVP WORKS

- **Early-warning proximity ring:** use additional outer polygon / geometric distance with WARNING vs VIOLATION; no overconfident claims of intent prediction.
- **Incident timeline:** structured JSONL history, risk counts / dwell-time statistics.
- **False-alert protection:** frame persistence, state machine and cooldown; if stable object IDs available, tie state to tracking ID. If not, document single-person limitation and avoid assuming tracking works.
- **Privacy:** default to no saved identifiable frames; show only metadata/screenshots needed for evidence; no facial identification.
- **Lightweight dashboard:** optional if enough time, but don't let UI polish delay evidence.
- **FP16 vs INT8:** real measurement only after first working TensorRT engine.

### Resource constraints

MX550 has **2GB VRAM**: single stream, batch 1, small detector, lightweight resolution, no model ensemble, keep parallel GPU processes closed. FP16 only if supported. If memory errors occur, gather logs and move to supported GPU if necessary rather than spending all remaining hours tuning.

## 5. Suggested PipeGen requirement prompt

> Create a real-time, single-stream NVIDIA DeepStream person-detection pipeline using CraftifAI PipeGen. Select a supported lightweight pretrained ONNX object detection model that detects the `person` class and compile it into a TensorRT engine, targeting FP16 if supported. The input is a short local MP4 file containing a person approaching, entering, and leaving a configurable restricted area. Render bounding boxes and show an actionable metadata output in JSON or MQTT. Complete and preserve all five PipeGen stages: Requirement, Pipeline IR, Model, Compiler and Run. Save the actual speed report and export generated application and `run.sh`. After a successful base live run, add polygonal zone analysis and stable incident reporting in a supported generated pipeline or downstream extension. Use only real observed performance results.

Set video path inside `/home/kishore/...` if required, rather than using `/mnt/c/` paths for video input.

## 6. Development and validation plan

**Phase A — Admission:** Confirm PipeGen GUI start, login, model catalog, DeepStream image, working Docker/GPU integration. Verify supported X11 environment.

**Phase B — The mandatory pipeline:** Finish five PipeGen stages. Save exported application and real TensorRT speed report. Run one sample MP4 to output display and JSON/MQTT. Capture evidence as soon as available.

**Phase C — Differentiator:** Add restricted-zone intrusion logic, debounce, incident-state transitions and privacy-sensitive analytics. Keep genuine PipeGen pipeline intact.

**Phase D — Tests:** Test outside-zone, entry for 1–2 frames, confirmed entry >=3 frames, sustained entry (one incident), exit, re-entry (new incident), corrupt input handling. Tests of custom logic do not replace real DeepStream run verification.

**Phase E — Packaging:** Code; PipeGen export; YAML/JSON config; sample output; test evidence; project description; README; video/screenshot if available; reports. Only real files.

**Phase F — Submit:** Verify current official deadline and final form; push repo with authentication approval, fill form or prepare form answers and ask user to click submit. Confirm receipt if visible. Submit before deadline.

## 7. Recommended repository

```text
guardianedge-ai/
├── AGENTS.md
├── CODEX_HANDOFF.md
├── README.md
├── pipegen-export/          # actual export, not placeholders
├── config/
│   └── zones.json
├── src/                     # only custom supported extensions
├── tests/
├── evidence/
│   ├── pipeline-ir.png      # real screenshot
│   ├── tensorrt-speed.png   # real report
│   ├── live-run.png         # real proof
│   └── incident.jsonl      # real emitted events
├── docs/
│   └── architecture.md
└── submission/
    └── project-description.md
```

Do not create empty fake evidence files. Do not add large unlicensed videos or vendor proprietary binaries that cannot be redistributed. Respect PipeGen export license and publish permitted source/configs/artifacts.

## 8. Submission inventory & links

Official CraftifAI project/downloads: https://developer.craftifai.com/dashboard?tab=downloads

Official PipeGen product/setup: https://developer.craftifai.com/products/pipegen

Hackathon Luma event: https://luma.com/5z8w42mq

**PipeGen submission form supplied in the challenge PDF:** https://forms.gle/eJyeCKCG2UH757QZ8

**Note:** User's more recent announcement says a new submission link may be shared and 11:00 PM IST deadline. Confirm the active form; don't assume the original form is still accepting entries.

Final truthful checklist:
- [ ] Version / app verified and account signed in
- [ ] Requirement stage captured
- [ ] Pipeline IR reviewed and screenshot saved
- [ ] Model selected / input identified
- [ ] Real TensorRT engine compiled, speed report saved
- [ ] Live DeepStream run on NVIDIA GPU verified
- [ ] Real actionable JSON/MQTT output verified
- [ ] Actual export folder included in repository
- [ ] README and project description accurate
- [ ] Screenshots/logs/videos match working system
- [ ] GitHub push complete, URL verified
- [ ] Correct official form submitted, receipt captured

## 9. Reporting and collaboration protocol

Start with a 2–3 sentence status update, then execute immediate next actions. Provide compact updates at each meaningful checkpoint. When blocked, quote the **first meaningful error**, explain the smallest fix, and ask for one exact user action. Don't keep asking the user to manually execute commands that Codex can run in its Ubuntu shell.

When proposing privileged commands, read/preview effects first and request approval. Never ask for or store passwords, OTPs, access tokens, or authentication secrets. Request the user to enter them in the official app.

**Final instruction: Start now in `/home/kishore/craftifai/guardianedge-ai`. Determine whether the official PipeGen installer is actually present. If not, immediately ask the user to download the official `.deb` and WSL2 prerequisite package while you prepare the project plan, README outline, zone-event logic and tests. After the files appear, continue with setup, full PipeGen execution, evidence, GitHub and submission.**
