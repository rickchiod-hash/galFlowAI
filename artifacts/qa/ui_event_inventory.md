# UI Event Inventory — GalFlowAI Recovery Mission S30

## Tab: Criar Comercial (new UI — `app/ui/gradio_app.py`)

| Componente | Evento | Callback | Função Destino | Inputs | Outputs | Efeito Esperado | Efeito Real | Status |
|-----------|-------|---------|---------------|-------|--------|----------------|------------|:------:|
| `generate_script_btn` | click | `fn=on_generate_script` | `app/ui/gradio_app.py:92` | briefing, provider, app_state | briefing_output, app_state, flow_status | Gera roteiro, atualiza state e status | ✅ Funciona | OK |
| `.then()` | — | lambda | — | app_state | stage2_group | Mostra stage2 | ✅ Funciona | OK |
| `.then()` | — | lambda | — | app_state | script_textbox | Preenche script | ✅ Funciona | OK |
| `.then()` | — | lambda | — | app_state | script_provider_box, script_quality_box, script_time_box | Mostra metadados | ✅ Funciona | OK |
| `check_providers_btn` | click | lambda | get_provider_status | — | provider_status_md | Mostra status dos providers | ✅ Funciona | OK |
| **Correção S30:** | | | | | | | | |
| `on_generate_script` | — | `save_manual_edit()` | `app/services/script_service.py:303` | pid, script, note | — | Salva script no disco | ✅ Agora salva | FIXED |
| `approve_btn` | click | `on_approve_script` | `app/ui/gradio_app.py:114` | app_state | app_state, flow_status | Aprova roteiro, avança step | ⚠️ Depende do script estar no disco | FIXED |
| `.then()` | — | lambda | — | app_state | stage3_group | Mostra stage3 | ⚠️ Depende do approve funcionar | FIXED |
| `save_edit_btn` | click | `on_save_edit` | `app/ui/gradio_app.py:404` | script_textbox, app_state | stage2_status | Salva edição no disco | ✅ Funciona | OK |
| `improve_btn` | click | `on_improve_script` | `app/ui/gradio_app.py:425` | script_textbox, app_state | script_textbox, stage2_status | Melhora script via LLM | ✅ Funciona | OK |
| `complement_btn` | click | `on_complement_script` | `app/ui/gradio_app.py:437` | script_textbox, app_state | script_textbox, stage2_status | Complementa script | ✅ Funciona | OK |
| `viral_btn` | click | `on_viral_script` | `app/ui/gradio_app.py:449` | script_textbox, app_state | script_textbox, stage2_status | Torna mais viral | ✅ Funciona | OK |
| `premium_btn` | click | `on_premium_script` | `app/ui/gradio_app.py:461` | script_textbox, app_state | script_textbox, stage2_status | Torna mais premium | ✅ Funciona | OK |
| `direct_btn` | click | `on_direct_script` | `app/ui/gradio_app.py:473` | script_textbox, app_state | script_textbox, stage2_status | Torna mais direto | ✅ Funciona | OK |
| `gen_narration_btn` | click | `on_generate_narration_script` | `app/ui/gradio_app.py:128` | app_state | app_state, narration_script_box, stage3_status | Gera script de narração | ✅ Funciona | OK |
| `gen_tts_btn` | click | `on_generate_tts` | `app/ui/gradio_app.py:153` | narration_script_box, tts_engine, tts_voice, allow_no_audio, app_state | app_state, audio_player, srt_output, stage3_status | Gera áudio TTS | ✅ Funciona | OK |
| `gen_srt_btn` | click | `on_generate_srt` | `app/ui/gradio_app.py:185` | app_state | app_state, srt_output, stage3_status | Gera legendas SRT | ✅ Funciona | OK |
| `gen_scenes_btn` | click | `on_generate_scenes` | `app/ui/gradio_app.py:316` | app_state | app_state, scenes_output, stage4_status | Gera cenas | ✅ Funciona | OK |
| `.then()` | — | lambda | — | app_state | stage5_group | Mostra stage5 | ✅ Funciona | OK |
| **Missing:** | — | — | — | — | stage4_group | **stage4 nunca mostrado** | ❌ Nunca visível | BUG |
| `gen_prompts_btn` | click | `on_generate_scene_prompts` | `app/ui/gradio_app.py:366` | app_state | stage4_status | Gera prompts visuais | ✅ Funciona | OK |
| `validate_scenes_btn` | click | `on_validate_scenes` | `app/ui/gradio_app.py:380` | app_state | stage4_status | Valida cenas | ✅ Funciona | OK |
| `render_btn` | click | `on_render_scenes` | `app/ui/gradio_app.py:336` | app_state | app_state, render_progress, render_logs, preview_video | Renderiza cenas | ✅ Funciona | OK |
| `.then()` | — | lambda | — | app_state | stage6_group | Mostra stage6 | ✅ Funciona | OK |
| `sync_btn` | click | lambda | — | app_state | sync_status_md | Sincroniza áudio+video | ✅ Funciona | OK |
| `export_btn` | click | `on_export_final` | `app/ui/gradio_app.py:205` | app_state, audio_player, srt_output, allow_no_audio | app_state, preview_video, stage6_status | Exporta MP4 | ✅ Funciona | OK |
| `quick_btn` | click | `on_quick_generate` | `app/ui/gradio_app.py:391` | quick_product, quick_audience, quick_duration, quick_style | quick_video, quick_error | Modo rápido | ✅ Funciona | OK |

## Tab: Criar Comercial (legacy — `app/main.py`)

| Componente | Evento | Callback | Status |
|-----------|-------|---------|:------:|
| `btn` (Criar comercial) | click | `on_create` | ✅ OK |
| `btn_save` | click | `on_save` | **FIXED** — output incorreto (gr.Textbox novo) |
| `btn_improve` | click | `_improve_wrapper` | **FIXED** — usava `result.get("status", "Erro")` (chave errada) |
| `btn_complement` | click | `_complement_wrapper` | **FIXED** |
| `btn_viral` | click | `_viral_wrapper` | **FIXED** |
| `btn_premium` | click | `_premium_wrapper` | **FIXED** |
| `btn_direct` | click | `_direct_wrapper` | **FIXED** |
| `btn_new_version` | click | `_new_version_wrapper` | **FIXED** — não tinha handler |
| `btn_restore` | click | `_restore_wrapper` | **FIXED** — não tinha handler |
| `btn_approve` | click | `_approve_wrapper` | **FIXED** — não tinha handler |
| `vid_generate_btn` | click | `generate_video_wrapper` | ✅ OK |

## Tab: Logs e Diagnóstico

| Componente | Evento | Status |
|-----------|-------|:------:|
| `refresh_logs_btn` | click | ✅ OK |
| `refresh_errors_btn` | click | ✅ OK |
| `refresh_diagnostic_btn` | click | ✅ OK |
| `refresh_providers_diag_btn` | click | ✅ OK |
| Log tab (new UI) `refresh_logs_btn` | click | ✅ OK |
| Log tab (new UI) `refresh_errors_btn` | click | ✅ OK |

## Tab: Dashboard de Projetos

| Componente | Evento | Status |
|-----------|-------|:------:|
| `refresh_dashboard_btn` (new UI) | click | ✅ OK |
| `create_project_btn` (new UI) | click | ✅ OK |
| `btn_refresh` (legacy) | click | ✅ OK |
| `demo.load` (legacy) | load | ✅ OK |
