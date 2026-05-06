# CHECKPOINT: FLOWFORGEAI - H10 PLANNING & CONTEXT

**Date:** May 5, 2026
**Session Target:** H10 - H17 Implementation
**Status:** 58 Tests Passing / Planning Complete / Build Mode Active

---

## 1. Session Summary (What was done)

### Completed in Previous Sessions
1.  **H4a-H8 Stories**: Downloaded GPT4All model, installed PyTorch, configured LLM providers.
2.  **WanGP Adapter Fix**: Fixed path typo (`COMERCIAL` vs `COMMERCIAL`).
3.  **VideoService**: Created `app/services/video_service.py` with 8 unit tests.
4.  **Test Suite Expansion**: Added `test_prompt_builder.py`, `test_scene_splitter.py`, `test_script_generator.py`, `test_complete_system.py`, `test_video_service.py`.
5.  **Documentation**: Updated `README.md`, created `docs/VIDEO_SERVICE.md`, `docs/PROVIDERS_SETUP.md`.
6.  **TemplateProvider**: Created `app/adapters/llm/template_provider.py` as fallback.
7.  **Test Runner**: Created `run_all_tests.py`.

### Current State
-   **Branch**: `master`
-   **Last Commit**: `b78c3e5` (fix: atualiza teste README para FlowForgeAI)
-   **Working Tree**: Clean (`nothing to commit`)
-   **Tests**: 58 passed in `pytest` (H4a-H8 cycle complete).

---

## 2. Technical Context (Environment)

### Paths
-   **Workspace**: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\`
-   **Python (Studio)**: `K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe`
-   **Models**: `K:\AI_VIDEO_COMERCIAL_STUDIO\models\`
-   **Assets**: `K:\AI_VIDEO_COMERCIAL_STUDIO\assets\reference\`

### Environment Variables (Set in every script run)
```powershell
$env:PIP_CACHE_DIR="K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"
$env:HF_HOME="K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface"
$env:TORCH_HOME="K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch"
$env:XDG_CACHE_HOME="K:\AI_VIDEO_COMERCIAL_STUDIO\cache"
$env:TEMP="K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
$env:TMP="K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
$env:OLLAMA_MODELS="K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama"
```

### Hardware Constraints
-   **GPU**: NVIDIA GTX 1660 Super (6GB VRAM)
-   **Preset**: 1.3B Model, 480p Resolution, Single Scene Render.

---

## 3. Refined Backlog (H10 - H17)

*Planning Poker: 3 Points per Story*

### **H10 — Application Layer Consolidation (Use Cases)**
-   **Objective**: Isolate business logic from `app/api.py` and `app/pipeline/` into `app/application/use_cases/`.
-   **Tasks**:
    1.  Create `app/application/use_cases/generate_commercial_use_case.py`.
    2.  Migrate orchestration from `VideoGenerationPipeline` to this use case.
    3.  Migrate script logic from `app/api.py` to `generate_script_use_case.py`.
-   **Acceptance Criteria**:
    - [ ] `app/api.py` is a "thin controller" (no business logic).
    - [ ] Pipeline remains functional (WanGP -> FFmpeg fallback preserved).
    - [ ] Success in `pytest -q`.

### **H11 — Job Queue and State Machine**
-   **Objective**: Implement persistence and status for video rendering (critical for 6GB VRAM).
-   **Tasks**:
    1.  Implement State Enum: `QUEUED`, `RUNNING`, `SUCCEEDED`, `FAILED`.
    2.  Evolve `app/jobs/queue.py` with SQLite or JSON persistence.
    3.  Create endpoint `GET /api/projects/{project_id}/status`.
-   **Acceptance Criteria**:
    - [ ] Only 1 render happens at a time (mutex).
    - [ ] Status reflected in `project.json`.
    - [ ] Structured logs include `project_id` and `status`.

### **H12 — Contract Standardization & Error Handling**
-   **Objective**: Standardize error envelopes and API contracts (per `BACKLOG.md` P0-03).
-   **Tasks**:
    1.  Create standard `Result` object (`ok`, `code`, `message`, `details`).
    2.  Apply to `app/adapters/llm/provider_router.py`.
    3.  Add contract tests for `/api/health` and `/api/llm/*`.
-   **Acceptance Criteria**:
    - [ ] No generic 500 errors in API.
    - [ ] Coverage >= 70% in `app/api.py`.

### **H13 — Hardware-Awareness Integration**
-   **Objective**: Connect `wangp_adapter.py` to `hardware.py` for dynamic VRAM detection.
-   **Tasks**:
    1.  Remove hardcoded 1.3B presets in `wangp_adapter`.
    2.  Call `HardwareManager` to decide model/resolution.
    3.  Add structured logging for VRAM availability.
-   **Acceptance Criteria**:
    - [ ] `wangp_adapter` logs detected VRAM at init.
    - [ ] 3 unit tests simulating different VRAM scenarios.

### **H14 — Observability & Structured Logs**
-   **Objective**: Implement JSON structured logs (per `BACKLOG.md` P2-02).
-   **Tasks**:
    1.  Integrate `LogService` into all adapters.
    2.  Format: `project_id`, `provider`, `latency_ms`, `fallback_used`.
    3.  Create endpoint `GET /api/logs/recent`.
-   **Acceptance Criteria**:
    - [ ] Logs viewable via UI Central de Logs.
    - [ ] Log errors do not break the app.

---

## 4. Pending TODOs found in Code (for reference)

| File | Line | TODO |
| :--- | :--- | :--- |
| `app/pipeline/video_generation_pipeline.py` | 21 | Break steps into independent use cases |
| `app/pipeline/video_generation_pipeline.py` | 22 | Standardize job state |
| `app/adapters/wangp_adapter.py` | 197 | Integrate with `hardware.py` |
| `app/api.py` | 20 | Technical debt: Modularization |
| `app/adapters/llm/provider_router.py` | 9 | Technical debt review |

---

## 5. QA Commands (Run at end of session)

```powershell
# 1. Run all tests
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest -q

# 2. Check coverage (Target >= 70% for critical modules)
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest --cov=app --cov-report=term-missing

# 3. Syntax check main files
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m py_compile app/api.py

# 4. Run QA Plan
# Read qa/QA_TEST_PLAN.md and verify Fase T1, T2, T3 items.
```

---

## 6. Next Session Startup Instructions

1.  **Read this file**: `CHECKPOINT_H10.md`.
2.  **Read Backlog**: `BACKLOG.md` and `qa/QA_TEST_PLAN.md`.
3.  **Verify Environment**: Run `pytest -q` to ensure 58 tests still pass.
4.  **Execute H10**: Start by creating the `app/application/use_cases/` directory.
5.  **Commit Often**: Use descriptive commit messages (e.g., `feat(H10): create use cases layer`).

**First Command for new session:**
```powershell
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest test_all_stories.py test_video_service.py -v
```

---
*End of Checkpoint*
