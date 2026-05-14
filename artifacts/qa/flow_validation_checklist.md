# Flow Validation Checklist — GalFlowAI

Data: 2026-05-14
Session: S30 Phase E (QA-1007, QA-1008, QA-1009, RND-613)

## Scope: Full Pipeline E2E (Gradio UI 6-Stage Flow)

Use this checklist to validate the complete flow. Each item must pass before Phase E is complete.

---

### Pre-Flight

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 1 | App starts without errors (`scripts/start_GalFlowAI_standard.bat`) | ⬜ | Logs: `logs/app_stdout.txt`, `logs/app_stderr.txt` |
| 2 | Gradio UI accessible at `http://127.0.0.1:7860` | ⬜ | Screenshot or curl output |
| 3 | API health check: `GET /api/v1/health` returns 200 | ⬜ | Status + JSON body |
| 4 | Provider list: `GET /api/v1/llm/providers` returns valid JSON | ⬜ | template=true, rest depend on local setup |
| 5 | Config: `GET /api/v1/config` returns 200 | ⬜ | Status + JSON body |

---

### Stage 1: Briefing & Script Generation

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 6 | Briefing field accepts text input (min 5 chars) | ⬜ | UI observation |
| 7 | Provider dropdown shows available providers | ⬜ | UI observation |
| 8 | "Gerar Roteiro" button generates script with TemplateProvider | ⬜ | Script text appears in textbox |
| 9 | Script is persisted to disk after generation | ⬜ | Check `projects/*/scripts/script_latest.md` |
| 10 | Stage 2 group becomes visible after generation | ⬜ | UI observation |
| 11 | Status message shows completion/time taken | ⬜ | UI observation |
| 12 | Provider metadata box shows used provider + quality + time | ⬜ | UI observation |

---

### Stage 2: Script Editing & Approval

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 13 | Script textbox is editable | ⬜ | Type in textbox |
| 14 | "Salvar Edição" persists changes to disk | ⬜ | Read `projects/*/scripts/script_latest.md` after save |
| 15 | "Melhorar" button improves script via LLM | ⬜ | Script text changes; status says "Melhorado" |
| 16 | "Complementar" button extends script | ⬜ | Script text changes; status says "Complementado" |
| 17 | "Mais Viral" button adds viral hooks | ⬜ | Script text changes |
| 18 | "Mais Premium" button upgrades language | ⬜ | Script text changes |
| 19 | "Mais Direto" button adds CTA | ⬜ | Script text changes |
| 20 | "Nova Versão" creates empty version | ⬜ | Script textbox clears |
| 21 | "Restaurar Anterior" restores previous version | ⬜ | Previous script text reappears |
| 22 | **"Aprovar Roteiro" approves script** | ⬜ | `script_approved.md` exists on disk |
| 23 | Stage 3 and Stage 4 groups become visible after approval | ⬜ | UI observation |
| 24 | Q.A-1007: Scenes API returns 400 ("not approved") before approval | ⬜ | `GET /api/v1/scenes/{id}/list` → 400 |
| 25 | Q.A-1007: Scenes API returns 200 after approval | ⬜ | `GET /api/v1/scenes/{id}/list` → 200 |

---

### Stage 3: Narration & Subtitles

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 26 | "Gerar Narração" creates AudioPlan and narration script | ⬜ | `narration_script.md` on disk |
| 27 | "Gerar Áudio (TTS)" generates WAV files per scene | ⬜ | WAV files in `projects/*/audio/` |
| 28 | TTS failure with "allow_no_audio" unchecked blocks pipeline | ⬜ | Error message shown |
| 29 | TTS failure with "allow_no_audio" checked continues | ⬜ | export_without_audio flag set |
| 30 | "Gerar Legendas (SRT)" generates .srt file | ⬜ | SRT file in `projects/*/subtitles/` |

---

### Stage 4: Scene Split & Prompts

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 31 | "Gerar Cenas" splits script into individual scenes | ⬜ | Scenes displayed in UI |
| 32 | Stage 5 group becomes visible after scene generation | ⬜ | UI observation |
| 33 | "Gerar Prompts" builds visual prompts per scene | ⬜ | `prompts.json` on disk |
| 34 | "Validar Cenas" checks prompt completeness | ⬜ | Status message |

---

### Stage 5: Video Render

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 35 | "Renderizar" button triggers render pipeline | ⬜ | Progress bar appears |
| 36 | Render progress updates (0-100%) | ⬜ | Progress bar fills |
| 37 | Render logs show per-scene status | ⬜ | Log entries in render_logs |
| 38 | Preview video loads after render | ⬜ | Video player shows MP4 |
| 39 | Stage 6 group becomes visible after render | ⬜ | UI observation |
| 40 | **RND-613: Video MP4 file exists on disk** | ⬜ | `projects/*/videos/commercial.mp4` |
| 41 | Scenes that fail WanGP fall back to FFmpeg | ⬜ | Logs show `fallback_used=True` or WANGP_UNAVAILABLE |

---

### Stage 6: Sync & Export

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 42 | "Sincronizar" button syncs audio+video | ⬜ | Status message |
| 43 | "Exportar Final" exports final MP4 with audio+SRT | ⬜ | Export MP4 on disk |
| 44 | Export manifest is written | ⬜ | `export_manifest.json` exists |
| 45 | Q.A-1009: Dashboard metrics reflect the job | ⬜ | Dashboard shows script count, scenes, metrics |
| 46 | Q.A-1009: Logs contain structured error entries | ⬜ | `GET /api/v1/logs/structured` returns entries |

---

### Post-Flow Validation

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 47 | Q.A-1008: Provider used matches provider selected | ⬜ | UI metadata box shows selected provider |
| 48 | Q.A-1008: Fallback quality is "fallback" when TemplateProvider used | ⬜ | UI metadata box shows quality="fallback" |
| 49 | No unhandled exceptions in app logs | ⬜ | `logs/app_stderr.txt` is empty or has no tracebacks |
| 50 | API endpoints return correct types (JSONResponse) | ⬜ | All endpoints return JSON with Content-Type: application/json |

---

### API-Only Smoke Tests (separate run)

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 51 | `POST /api/v1/script/generate` returns valid script | ⬜ | JSON with script_markdown, provider_used |
| 52 | `POST /api/v1/script/{id}/save` persists script | ⬜ | Loaded via GET current |
| 53 | `POST /api/v1/script/{id}/approve` approves script | ⬜ | `script_approved.md` on disk |
| 54 | `GET /api/v1/script/{id}/current` loads approved script | ⬜ | Script text returned |
| 55 | `GET /api/v1/metrics` returns summary | ⬜ | JSON with totals |
| 56 | `GET /api/v1/logs/recent` returns log entries | ⬜ | JSON array |
| 57 | `GET /api/v1/pipeline/status` returns component health | ⬜ | JSON with booleans |

---

### Regression Checks

| # | Check | Pass/Fail | Evidence |
|---|-------|-----------|----------|
| 58 | No legacy product name in code or docs | ⬜ | grep test (QA-1000) |
| 59 | All 5 LLM providers exist + TemplateProvider as fallback | ⬜ | test_provider_presence (QA-1001) |
| 60 | Script approval still gates scene split | ⬜ | Pipeline returns error if not approved |
| 61 | TTS failure does not break final export | ⬜ | Export succeeds with fallback_sem_audio=true |
| 62 | "Salvar Edição" still works after all fixes | ⬜ | Edit + save + reload matches |
| 63 | Stage 4 (Cenas) still visible after approval | ⬜ | UI observation (OBS-904 regression) |
