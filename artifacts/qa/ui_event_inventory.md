# UI Event Inventory — GalFlowAI gradio_app.py

Todos os callbacks registrados via `.click()` e `.then()` no `create_gradio_app()`.

## Stage 1 — Briefing

| Botão/Ação | Callback | Inputs | Outputs | Status |
|------------|----------|--------|---------|--------|
| Gerar Roteiro | `on_generate_script` | briefing, provider, app_state | briefing_output, app_state, flow_status | ✅ Fixed (PROV-304 fallback visible) |
| → .then() | show stage2 | app_state | stage2_group (visible) | ✅ |
| → .then() | fill script_textbox | app_state | script_textbox | ✅ |
| → .then() | show provider/quality/time | app_state | script_provider_box, script_quality_box, script_time_box | ✅ Fixed (quality from result) |
| Status dos Provedores | `get_provider_status` | — | provider_status_md | ✅ |

## Stage 2 — Roteiro Editável

| Botão/Ação | Callback | Inputs | Outputs | Status |
|------------|----------|--------|---------|--------|
| Aprovar Roteiro | `on_approve_script` | app_state | app_state, flow_status | ✅ Fixed (UI-210) |
| → .then() | show stage3 | app_state | stage3_group (visible) | ✅ |
| Salvar Edição Manual | `on_save_edit` | script_textbox, app_state | stage2_status | ✅ Fixed (UI-209) |
| Melhorar | `on_improve_script` | script_textbox, app_state | script_textbox, stage2_status | ✅ (UI-205) |
| Complementar | `on_complement_script` | script_textbox, app_state | script_textbox, stage2_status | ✅ (UI-205) |
| Mais Viral | `on_viral_script` | script_textbox, app_state | script_textbox, stage2_status | ✅ (UI-205) |
| Mais Premium | `on_premium_script` | script_textbox, app_state | script_textbox, stage2_status | ✅ (UI-205) |
| Mais Direto | `on_direct_script` | script_textbox, app_state | script_textbox, stage2_status | ✅ (UI-205) |

## Stage 3 — Narração e Legendas

| Botão/Ação | Callback | Inputs | Outputs | Status |
|------------|----------|--------|---------|--------|
| Gerar Script de Narração | `on_generate_narration_script` | app_state | app_state, narration_script_box, stage3_status | ✅ |
| Gerar Narração/TTS | `on_generate_tts` | narration_script_box, tts_engine, tts_voice, allow_no_audio, app_state | app_state, audio_player, srt_output, stage3_status | ✅ |
| Gerar Legenda/SRT | `on_generate_srt` | app_state | app_state, srt_output, stage3_status | ✅ |

## Stage 4 — Cenas e Prompts

| Botão/Ação | Callback | Inputs | Outputs | Status |
|------------|----------|--------|---------|--------|
| Gerar Cenas | `on_generate_scenes` | app_state | app_state, scenes_output, stage4_status | ✅ |
| → .then() | show stage5 | app_state | stage5_group (visible) | ✅ |
| Gerar Prompts | `on_generate_scene_prompts` | app_state | stage4_status | ✅ |
| Validar Cenas | `on_validate_scenes` | app_state | stage4_status | ✅ |

## Stage 5 — Render Visual

| Botão/Ação | Callback | Inputs | Outputs | Status |
|------------|----------|--------|---------|--------|
| Renderizar Cenas | `on_render_scenes` | app_state | app_state, render_progress, render_logs, preview_video | ✅ Fixed (gate bypass) |
| → .then() | show stage6 | app_state | stage6_group (visible) | ✅ |

## Stage 6 — Sincronização e Export

| Botão/Ação | Callback | Inputs | Outputs | Status |
|------------|----------|--------|---------|--------|
| Sincronizar Audio + Video | lambda | app_state | sync_status_md | ✅ |
| Exportar MP4 | `on_export_final` | app_state, audio_player, srt_output, allow_no_audio | app_state, preview_video, stage6_status | ✅ |

## Modo Rápido

| Botão/Ação | Callback | Inputs | Outputs | Status |
|------------|----------|--------|---------|--------|
| Executar Modo Rápido | `on_quick_generate` | quick_product, quick_audience, quick_duration, quick_style | quick_video, quick_error | ✅ |

## Abas auxiliares

| Aba | Botão/Ação | Callback | Status |
|-----|-----------|----------|--------|
| Logs | Atualizar Logs | `on_refresh_logs` | ✅ |
| Erros Estruturados | Atualizar Erros | `on_refresh_structured_errors` | ✅ |
| Diagnóstico | Gerar Diagnóstico | `copy_diagnostic_bundle` | ✅ |
| Diagnóstico | Verificar Provedores | lambda com `get_provider_diagnostics` | ✅ |
| Dashboard | Atualizar Dashboard | `on_refresh_dashboard` | ✅ |
| Configurações | Salvar Configurações | `on_save_config` | ✅ |
| Configurações | Restaurar Padrões | `on_reset_config` | ✅ |

## Summary

- Total callbacks: **25** (excluindo lambdas simples)
- P0 bugs corrigidos: **4** (UI-210 ✅, UI-209 ✅, gate bypass ✅, PROV-304 ✅)
- Total de eventos `.click()`: **28**
- Total de eventos `.then()`: **5**
- Total de eventos `.load()`: **1**
