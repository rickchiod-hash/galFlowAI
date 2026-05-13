"""Interface Web Gradio para GalFlowAI - Fluxo por Etapas"""

import sys
import os
import tempfile
import logging
import json
import time as _time
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import gradio as gr

from app.logging_config import setup_logger
logger = setup_logger("galflowai", "info")

from app.services.script_service import (
    generate_script_with_provider,
    get_provider_status,
    get_provider_diagnostics,
)
from app.services.log_service import get_recent_logs, get_log_summary, copy_diagnostic_bundle, get_structured_errors
from app.services.metrics_service import get_metrics_service
from app.services.config_service import get_config_service
from app.services.tts_service import TTSService
from app.services.srt_service import SRTService
from app.domain.audio_plan import AudioPlan, NarrationEntry, AudioPlanService, AudioPlanStatus
from app.project_manager import create_project, load_project
from app.config import PROJECTS_DIR


PROVIDER_CHOICES = ["auto", "template", "lmstudio", "koboldcpp", "llamacpp", "gpt4all"]
TTS_ENGINE_CHOICES = ["auto", "pyttsx3", "kokoro", "silence"]
VOICE_CHOICES = ["default", "pt-BR", "en-US", "es-ES"]

_STATE_DEFAULT = {
    "project_id": "",
    "script": "",
    "script_provider": "",
    "script_time": 0,
    "script_approved": False,
    "narration_plan_id": "",
    "narration_script": "",
    "audio_path": "",
    "srt_path": "",
    "scenes": [],
    "scenes_file": "",
    "render_done": False,
    "export_path": "",
    "export_without_audio": False,
    "current_step": 1,
}


def _step_status(app_state_val: dict) -> str:
    steps = [
        ("1. Briefing", app_state_val.get("current_step", 1) >= 1),
        ("2. Roteiro", app_state_val.get("script", "") != ""),
        ("3. Narracao/Legendas", app_state_val.get("script_approved", False)),
        ("4. Cenas/Prompts", app_state_val.get("scenes_file", "") != ""),
        ("5. Render", app_state_val.get("render_done", False)),
        ("6. Export", app_state_val.get("export_path", "") != ""),
    ]
    parts = []
    current_step = app_state_val.get("current_step", 1)
    next_step = "Concluido"
    for i, (label, done) in enumerate(steps, 1):
        if done:
            parts.append(f"✅ {label}")
        elif i == current_step:
            parts.append(f"▶ **{label}**")
            next_step = label
        else:
            parts.append(f"⬜ {label}")
    nav = " | ".join(parts)
    return nav, next_step


# ---- UI Callbacks ----

def on_generate_script(briefing, provider, app_state_val):
    if not briefing or len(briefing.strip()) < 5:
        return None, app_state_val, "Briefing muito curto (minimo 5 caracteres)."
    result = generate_script_with_provider(briefing, provider)
    if result.get("ok"):
        app_state_val["script"] = result.get("script", "")
        app_state_val["script_provider"] = result.get("provider", "-")
        app_state_val["script_time"] = result.get("time", 0)
        app_state_val["current_step"] = max(app_state_val.get("current_step", 1), 2)
    else:
        return None, app_state_val, "Erro: %s" % result.get("error", "Falha desconhecida")
    nav, next_s = _step_status(app_state_val)
    status_md = "**Etapa atual:** %s  \n**Proximo passo:** %s" % (next_s, next_s)
    return result.get("script", ""), app_state_val, status_md


def on_approve_script(app_state_val):
    if not app_state_val.get("script"):
        return app_state_val, "Nao ha roteiro para aprovar."
    app_state_val["script_approved"] = True
    app_state_val["current_step"] = max(app_state_val.get("current_step", 1), 3)
    nav, next_s = _step_status(app_state_val)
    status_md = "**Etapa atual:** %s  \n**Proximo passo:** %s" % (next_s, next_s)
    return app_state_val, status_md


def on_generate_narration_script(app_state_val):
    if not app_state_val.get("script_approved"):
        return app_state_val, "", "Aprove o roteiro primeiro."
    plan_id = app_state_val.get("narration_plan_id", "")
    if not plan_id:
        plan_svc = AudioPlanService()
        plan = AudioPlan(
            project_id=app_state_val.get("project_id", "web_ui"),
            narrations=[],
            status=AudioPlanStatus.DRAFT,
        )
        plan_id = plan_svc.create(plan)
        app_state_val["narration_plan_id"] = plan_id
    script_text = app_state_val.get("script", "")
    lines = [l.strip() for l in script_text.split("\n") if l.strip()]
    narration_lines = []
    for i, line in enumerate(lines, 1):
        narration_lines.append(
            "### Cena %d\n**Texto:** %s\n**Duracao estimada:** 3s\n**Voz:** default\n" % (i, line)
        )
    narration_md = "\n".join(narration_lines)
    app_state_val["narration_script"] = narration_md
    return app_state_val, narration_md, "Script de narracao gerado com base no roteiro."


def on_generate_tts(narration_script, engine, voice, allow_no_audio, app_state_val):
    if not narration_script:
        return app_state_val, None, "", "Nenhum script de narracao disponivel."
    tts = TTSService()
    output_path = str(PROJECT_ROOT / ".." / "output" / "narration.wav")
    os.makedirs(str(Path(output_path).parent), exist_ok=True)
    try:
        audio_result = tts.generate_audio(
            text=narration_script, output_path=output_path, voice=voice if voice != "default" else None
        )
        if audio_result.get("success"):
            app_state_val["audio_path"] = audio_result.get("audio_path", output_path)
            app_state_val["export_without_audio"] = False
            status = "Audio gerado em: %s" % audio_result.get("audio_path", output_path)
            return app_state_val, audio_result.get("audio_path", output_path), "", status
        else:
            if allow_no_audio:
                app_state_val["export_without_audio"] = True
                return app_state_val, None, "TTS falhou, mas export sem audio esta liberado por fallback.", (
                    "AVISO: TTS falhou. Export sem audio permitido."
                )
            else:
                return app_state_val, None, "TTS falhou: %s" % audio_result.get("error", "erro"), "ERRO: TTS indisponivel."
    except Exception as e:
        if allow_no_audio:
            app_state_val["export_without_audio"] = True
            return app_state_val, None, "TTS falhou, mas export sem audio esta liberado por fallback.", (
                "AVISO: TTS falhou (%s). Export sem audio permitido." % e
            )
        return app_state_val, None, "", "ERRO: %s" % e


def on_generate_srt(app_state_val):
    srv = SRTService()
    script_text = app_state_val.get("narration_script", app_state_val.get("script", ""))
    lines = [l.strip() for l in script_text.split("\n") if l.strip() and not l.startswith("#")]
    srt_lines = []
    t = 0.0
    for i, line in enumerate(lines, 1):
        dur = max(2.0, len(line) / 15.0)
        start_s = srv._format_srt_timestamp(t) if hasattr(srv, '_format_srt_timestamp') else "00:00:00,000"
        end_s = srv._format_srt_timestamp(t + dur) if hasattr(srv, '_format_srt_timestamp') else "00:00:05,000"
        srt_lines.append("%d\n%s --> %s\n%s\n" % (i, start_s, end_s, line))
        t += dur
    srt_content = "\n".join(srt_lines)
    output_path = str(PROJECT_ROOT / ".." / "output" / "commercial.srt")
    os.makedirs(str(Path(output_path).parent), exist_ok=True)
    Path(output_path).write_text(srt_content, encoding="utf-8")
    app_state_val["srt_path"] = output_path
    return app_state_val, srt_content, "SRT gerado: %s" % output_path


def on_export_final(app_state_val, audio_path, srt_path, allow_no_audio):
    from app.services.video_service import VideoService
    vs = VideoService()
    if not vs.ffmpeg_available:
        return app_state_val, None, "FFmpeg nao disponivel para export."
    video_path = app_state_val.get("video_path", "")
    final_dir = Path(PROJECT_ROOT) / ".." / "output" / "final"
    final_dir.mkdir(parents=True, exist_ok=True)
    export_path = str(final_dir / "commercial.mp4")
    manifest = {"audio": bool(audio_path), "srt": bool(srt_path), "fallback_sem_audio": not bool(audio_path)}
    try:
        if video_path and Path(video_path).exists():
            result = vs.export_final_video(
                video_path=video_path, audio_path=audio_path if audio_path else None,
                srt_path=srt_path if srt_path else None, output_path=export_path,
            )
            if result.get("success"):
                app_state_val["export_path"] = result.get("video_path", export_path)
                if srt_path and Path(srt_path).exists():
                    import shutil
                    shutil.copy2(srt_path, str(final_dir / "commercial.srt"))
                Path(final_dir / "export_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
                status = "Export concluido"
                if app_state_val.get("export_without_audio"):
                    status += " (sem audio por fallback)"
                return app_state_val, result.get("video_path", export_path), status
            return app_state_val, None, result.get("error", "Falha no export")
        return app_state_val, None, "Video de origem nao encontrado para export."
    except Exception as e:
        return app_state_val, None, "Export falhou: %s" % e


def on_create_project(project_name):
    proj = create_project(project_name)
    return proj.get("id", "")


def on_refresh_logs(level, search, limit):
    logs_data = get_recent_logs(level=level, search=search if search else None, limit=int(limit))
    summary = get_log_summary()
    summary_md = (
        "**%s** INFO | **%s** WARN | **%s** ERROR | **%s** ESTRUTURADOS"
        % (summary.get("total_info", 0), summary.get("total_warn", 0), summary.get("total_error", 0), summary.get("total_structured_errors", 0))
    )
    rows = []
    for log in logs_data.get("logs", []):
        rows.append([
            log.get("horario", ""),
            log.get("nivel", ""),
            log.get("modulo", ""),
            log.get("mensagem", ""),
            log.get("sugestao", ""),
            log.get("code", ""),
            log.get("stage", ""),
            "Sim" if log.get("retryable") else "Nao",
            "Sim" if log.get("fallback_used") else "Nao",
        ])
    return rows, summary_md


def on_refresh_structured_errors(severity, limit):
    errors = get_structured_errors(limit=int(limit))
    rows = []
    for err in errors:
        sev = err.get("severity", "")
        if severity != "TODOS" and sev != severity:
            continue
        rows.append([
            err.get("code", ""),
            sev,
            err.get("message", "")[:100],
            err.get("stage", ""),
            "Sim" if err.get("retryable") else "Nao",
            "Sim" if err.get("fallback_used") else "Nao",
            err.get("provider", ""),
            err.get("timestamp", ""),
        ])
    return rows


def on_refresh_metrics():
    svc = get_metrics_service()
    summary = svc.get_summary()
    ops = svc.get_recent_operations(limit=10)
    summary_md = (
        "**Scripts:** %s | **Videos:** %s | **Sucesso:** %s%% | **Tempo Medio:** %.2fs | **Fallback:** %s | **Erros:** %s"
        % (
            summary["generated_scripts"],
            summary["generated_videos"],
            summary["success_rate_percent"],
            summary["average_generation_time"],
            summary.get("fallback_used", 0),
            summary["errors"],
        )
    )
    ops_rows = []
    for op in ops:
        provider = op.get("provider", op.get("engine", ""))
        ops_rows.append([
            op.get("timestamp", "")[-19:],
            op.get("type", ""),
            "Sim" if op.get("success") else "Nao",
            "%.1fs" % op.get("duration", 0),
            provider,
            "Sim" if op.get("used_fallback") else "Nao",
        ])
    if not ops_rows:
        ops_rows.append(["-", "-", "-", "-", "-", "-"])
    return summary_md, ops_rows


def on_generate_scenes(app_state_val):
    """Generate scenes from approved script text."""
    script = app_state_val.get("script", "")
    if not script or not app_state_val.get("script_approved"):
        return app_state_val, [], "Aprove o roteiro antes de gerar cenas."
    from app.pipeline.scene_splitter import split_script_into_scenes
    project_id = app_state_val.get("project_id", "web_ui")
    scenes = split_script_into_scenes(script, project_id)
    app_state_val["scenes"] = scenes
    app_state_val["current_step"] = 5
    rows = []
    for sc in scenes:
        sc_id = sc.get("scene_number", sc.get("id", ""))
        desc = sc.get("description", sc.get("prompt", ""))[:60]
        prompt = sc.get("prompt_positive", "")
        dur = str(sc.get("duration_estimate", 5)) + "s"
        rows.append([str(sc_id), desc, prompt, dur])
    return app_state_val, rows, "Cenas geradas: %d" % len(scenes)


def on_render_scenes(app_state_val):
    """Attempt real render via pipeline, fallback to FFmpeg placeholder."""
    scenes = app_state_val.get("scenes", [])
    if not scenes:
        return app_state_val, 0, "Nenhuma cena para renderizar.", ""
    project_id = app_state_val.get("project_id", "web_ui")
    from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
    pipeline = VideoGenerationPipeline()
    from app.pipeline.scene_splitter import save_scenes
    save_scenes(project_id, scenes)
    from app.config import PROJECTS_DIR
    script_path = PROJECTS_DIR / project_id / "script"
    script_path.mkdir(parents=True, exist_ok=True)
    (script_path / "script_approved.md").write_text(
        app_state_val.get("script", ""), encoding="utf-8"
    )
    try:
        result = pipeline.generate_commercial(
            project_id=project_id,
            product=app_state_val.get("script", "")[:50],
            target_audience="",
            progress_callback=None,
        )
        if result.get("success"):
            final_video = result.get("final_video", result.get("video_path", ""))
            app_state_val["video_path"] = final_video
            return app_state_val, 100, "Render concluido via pipeline.", final_video
        app_state_val["video_path"] = ""
        return app_state_val, 0, "Pipeline retornou erro: %s" % result.get("error", "desconhecido"), ""
    except Exception as e:
        app_state_val["video_path"] = ""
        return app_state_val, 0, "Render falhou: %s" % e, ""


def on_generate_scene_prompts(app_state_val):
    """Generate prompts for each scene."""
    scenes = app_state_val.get("scenes", [])
    if not scenes:
        return "Nenhuma cena disponivel."
    from app.pipeline.prompt_builder import build_prompts_for_scenes
    try:
        scenes = build_prompts_for_scenes(scenes)
        app_state_val["scenes"] = scenes
        return "Prompts gerados para %d cenas." % len(scenes)
    except Exception as e:
        return "Falha ao gerar prompts: %s" % e


def on_validate_scenes(app_state_val):
    scenes = app_state_val.get("scenes", [])
    if not scenes:
        return "Nenhuma cena para validar."
    missing = [s.get("id") for s in scenes if not s.get("prompt_positive") and not s.get("prompt")]
    if missing:
        return "Cenas sem prompt: %s. Use 'Gerar Prompts' primeiro." % missing
    app_state_val["current_step"] = max(app_state_val.get("current_step", 1), 5)
    return "Cenas validadas: %d cenas, todas com prompt." % len(scenes)


def on_quick_generate(product, audience, duration, style):
    from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
    p = VideoGenerationPipeline()
    pid = "quick_%d" % int(_time.time())
    result = p.generate_commercial(
        project_id=pid, product=product, target_audience=audience,
        duration_seconds=duration, style=style,
    )
    if result.get("success"):
        return result.get("final_video", ""), ""
    return "", result.get("error", "Falha desconhecida")


def on_save_edit(script_text):
    if not script_text or script_text.startswith("Erro"):
        return "Nada para salvar."
    result = generate_script_with_provider("Edicao manual salva", "template")
    return "Edicao registrada. Provedor: %s" % result.get("provider", "-")


# ---- UI Build ----

def create_gradio_app():
    web_interface = None
    metrics_service = get_metrics_service()

    custom_css = """
    .gradio-container { max-width: 1280px !important; }
    .status-box { background-color: #f0f0f0; padding: 20px; border-radius: 10px; margin: 10px 0; }
    .step-done { color: #2e7d32; font-weight: bold; }
    .step-active { color: #1565c0; font-weight: bold; }
    .step-pending { color: #9e9e9e; }
    .stage-group { border: 1px solid #e0e0e0; border-radius: 8px; padding: 16px; margin: 8px 0; }
    .gate-badge { background-color: #fff3e0; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; }
    .error-text { color: #c62828; }
    .warning-text { color: #e65100; }
    """

    with gr.Blocks(css=custom_css, title="GalFlowAI - Gerador de Comerciais") as demo:
        app_state = gr.State(value=dict(_STATE_DEFAULT))

        gr.Markdown(
            "# GalFlowAI - Criacao de Comerciais em Video\n"
            "Fluxo guiado: **Briefing → Roteiro → Aprovacao → Narracao/Legendas → Cenas → Render → Export**"
        )

        # ─────────── Tab 1: Criar Comercial ───────────
        with gr.Tab("Criar Comercial"):
            flow_status = gr.Markdown("**Etapa atual:** 1. Briefing  \n**Proximo passo:** Preencha o briefing e gere o roteiro.")

            # Stage 1: Briefing
            with gr.Group(elem_classes="stage-group"):
                gr.Markdown("### Etapa 1 — Briefing")
                with gr.Row():
                    with gr.Column(scale=2):
                        briefing_input = gr.Textbox(
                            label="Briefing do Produto",
                            placeholder="Descreva o produto, publico-alvo, estilo, dor, promessa e CTA...",
                            lines=4,
                        )
                    with gr.Column(scale=1):
                        provider_dropdown = gr.Dropdown(
                            choices=PROVIDER_CHOICES, value="auto", label="Motor de Roteiro"
                        )
                        provider_status_md = gr.Markdown("Clique em 'Status' para ver provedores")
                        check_providers_btn = gr.Button("Status dos Provedores", size="sm")
                generate_script_btn = gr.Button("Gerar Roteiro", variant="primary")
                stage1_status = gr.Markdown("")
                briefing_output = gr.Textbox(
                    label="Roteiro Gerado", lines=10,
                    placeholder="O roteiro aparecera aqui apos gerar...",
                )

            # Stage 2: Roteiro Editavel
            with gr.Group(elem_classes="stage-group", visible=False) as stage2_group:
                gr.Markdown("### Etapa 2 — Roteiro Editavel")
                script_textbox = gr.Textbox(label="Roteiro", lines=12)
                with gr.Row():
                    script_provider_box = gr.Textbox(label="Motor Utilizado", interactive=False, scale=1)
                    script_quality_box = gr.Textbox(label="Qualidade", interactive=False, scale=1)
                    script_time_box = gr.Textbox(label="Tempo (s)", interactive=False, scale=1)
                with gr.Row():
                    save_edit_btn = gr.Button("Salvar Edicao Manual", size="sm")
                    improve_btn = gr.Button("Melhorar", size="sm")
                    complement_btn = gr.Button("Complementar", size="sm")
                    viral_btn = gr.Button("Mais Viral", size="sm")
                    premium_btn = gr.Button("Mais Premium", size="sm")
                    direct_btn = gr.Button("Mais Direto", size="sm")
                with gr.Row():
                    approve_btn = gr.Button("Aprovar Roteiro e Liberar Proximas Etapas", variant="primary", scale=2)
                    stage2_status = gr.Markdown("")
                script_versions_md = gr.Markdown("**Veroes:** Nenhuma versao salva ainda.")

            # Stage 3: Narracao e Legendas
            with gr.Group(elem_classes="stage-group", visible=False) as stage3_group:
                gr.Markdown("### Etapa 3 — Narracao e Legendas")
                with gr.Row():
                    with gr.Column(scale=1):
                        tts_engine = gr.Dropdown(choices=TTS_ENGINE_CHOICES, value="auto", label="Motor de TTS")
                        tts_voice = gr.Dropdown(choices=VOICE_CHOICES, value="default", label="Voz/Idioma")
                        tts_speed = gr.Slider(minimum=0.5, maximum=2.0, value=1.0, step=0.1, label="Velocidade")
                        allow_no_audio = gr.Checkbox(value=True, label="Permitir export sem audio se TTS falhar")
                    with gr.Column(scale=2):
                        narration_script_box = gr.Textbox(label="Script de Narracao", lines=6)
                with gr.Row():
                    gen_narration_btn = gr.Button("Gerar Script de Narracao", variant="secondary", size="sm")
                    gen_tts_btn = gr.Button("Gerar Narracao/TTS", variant="primary", size="sm")
                    gen_srt_btn = gr.Button("Gerar Legenda/SRT", variant="secondary", size="sm")
                with gr.Row():
                    audio_player = gr.Audio(label="Audio Gerado", type="filepath")
                    srt_output = gr.Textbox(label="SRT Gerado", lines=4, interactive=False)
                stage3_status = gr.Markdown("")

            # Stage 4: Cenas e Prompts
            with gr.Group(elem_classes="stage-group", visible=False) as stage4_group:
                gr.Markdown("### Etapa 4 — Cenas e Prompts")
                scenes_output = gr.Dataframe(
                    headers=["Cena", "Descricao", "Prompt Visual", "Duracao"],
                    label="Cenas",
                    datatype=["str", "str", "str", "str"],
                )
                with gr.Row():
                    gen_scenes_btn = gr.Button("Gerar Cenas", variant="primary", size="sm")
                    gen_prompts_btn = gr.Button("Gerar Prompts", variant="secondary", size="sm")
                    validate_scenes_btn = gr.Button("Validar Cenas", variant="secondary", size="sm")
                stage4_status = gr.Markdown("")

            # Stage 5: Render Visual
            with gr.Group(elem_classes="stage-group", visible=False) as stage5_group:
                gr.Markdown("### Etapa 5 — Render Visual")
                with gr.Row():
                    with gr.Column(scale=1):
                        render_model = gr.Dropdown(
                            choices=["wan-gp", "ffmpeg-fallback"], value="wan-gp", label="Modelo de Video"
                        )
                        render_resolution = gr.Dropdown(
                            choices=["640x480 (GTX 1660)", "832x512", "1280x720"], value="640x480 (GTX 1660)",
                            label="Resolucao",
                        )
                        use_ffmpeg_fallback = gr.Checkbox(value=True, label="Usar fallback FFmpeg")
                    with gr.Column(scale=2):
                        render_progress = gr.Slider(minimum=0, maximum=100, value=0, label="Progresso", interactive=False)
                        render_logs = gr.Textbox(label="Logs do Render", lines=4, interactive=False)
                with gr.Row():
                    render_btn = gr.Button("Renderizar Cenas", variant="primary", scale=2)
                    ffmpeg_fallback_btn = gr.Button("Usar Fallback FFmpeg", variant="secondary", size="sm")
                stage5_status = gr.Markdown("")

            # Stage 6: Sincronizacao e Export
            with gr.Group(elem_classes="stage-group", visible=False) as stage6_group:
                gr.Markdown("### Etapa 6 — Sincronizacao e Export")
                with gr.Row():
                    with gr.Column(scale=2):
                        sync_status_md = gr.Markdown(
                            "- **Video:** Pendente\n- **Audio:** Pendente\n- **SRT:** Pendente\n- **Sincronizacao:** Pendente"
                        )
                    with gr.Column(scale=1):
                        gr.Markdown("**Fallback ativo:** Nao\n**Export sem audio:** Nao")
                preview_video = gr.Video(label="Preview Final")
                with gr.Row():
                    sync_btn = gr.Button("Sincronizar Audio + Video", variant="secondary", size="sm")
                    export_btn = gr.Button("Exportar MP4", variant="primary", scale=2)
                stage6_status = gr.Markdown("")

            # Modo Rapido (antigo Gerar Comercial Completo — rebaixado)
            with gr.Accordion("Modo Rapido (apenas para testes)", open=False):
                gr.Markdown(
                    "**ATENCAO:** Este modo ignora aprovacao humana e validacoes por etapa. "
                    "Use apenas para testes rapidos. O fluxo principal esta nas etapas acima."
                )
                with gr.Row():
                    with gr.Column(scale=2):
                        quick_product = gr.Textbox(label="Produto", value="Produto Teste")
                        quick_audience = gr.Textbox(label="Publico", value="Teste")
                    with gr.Column(scale=1):
                        quick_duration = gr.Slider(minimum=10, maximum=60, value=15, step=5, label="Duracao (s)")
                        quick_style = gr.Dropdown(choices=["viral", "premium", "direct"], value="viral", label="Estilo")
                quick_btn = gr.Button("Executar Modo Rapido", variant="secondary")
                quick_video = gr.Video(label="Resultado")
                quick_error = gr.Markdown("", visible=True)

            # ─── Event Wiring ───

            # Stage 1: Gerar Roteiro
            generate_script_btn.click(
                fn=on_generate_script,
                inputs=[briefing_input, provider_dropdown, app_state],
                outputs=[briefing_output, app_state, flow_status],
            ).then(
                fn=lambda s: (gr.update(visible=s.get("script", "") != ""),),
                inputs=[app_state],
                outputs=[stage2_group],
            ).then(
                fn=lambda s: (gr.update(value=s.get("script", "")),) if s.get("script") else (gr.update(),),
                inputs=[app_state],
                outputs=[script_textbox],
            ).then(
                fn=lambda s: (
                    s.get("script_provider", "-"),
                    "template",
                    "%.2f" % s.get("script_time", 0),
                ),
                inputs=[app_state],
                outputs=[script_provider_box, script_quality_box, script_time_box],
            )

            check_providers_btn.click(
                fn=lambda: "\n".join(
                    "- **%s:** %s" % (n, "Disponivel" if a else "Indisponivel")
                    for n, a in get_provider_status().items()
                ),
                outputs=[provider_status_md],
            )

            # Stage 2: Approve
            approve_btn.click(
                fn=on_approve_script,
                inputs=[app_state],
                outputs=[app_state, flow_status],
            ).then(
                fn=lambda s: (gr.update(visible=s.get("script_approved", False)),),
                inputs=[app_state],
                outputs=[stage3_group],
            )

            save_edit_btn.click(fn=on_save_edit, inputs=[script_textbox], outputs=[stage2_status])
            improve_btn.click(
                fn=lambda t: t if t else "Nada para melhorar.",
                inputs=[script_textbox],
                outputs=[script_textbox],
            )
            complement_btn.click(
                fn=lambda t: (t + "\n\n[Complemento - 10s]\nTexto: 'Informacoes adicionais.'" if t else t),
                inputs=[script_textbox],
                outputs=[script_textbox],
            )
            viral_btn.click(
                fn=lambda t: ("[Hook - 3s]\nTexto: 'Voce nao pode perder isso!'\n\n" + t if "[Hook" not in t else t),
                inputs=[script_textbox],
                outputs=[script_textbox],
            )
            premium_btn.click(
                fn=lambda t: t.replace("Texto:", "Texto premium:").replace("Narracao:", "Narracao premium:") if t else t,
                inputs=[script_textbox],
                outputs=[script_textbox],
            )
            direct_btn.click(
                fn=lambda t: (t + "\n\n[Cena CTA - 3s]\nTexto: 'Compre agora!'" if "CTA" not in t else t),
                inputs=[script_textbox],
                outputs=[script_textbox],
            )

            # Stage 3: Narracao
            gen_narration_btn.click(
                fn=on_generate_narration_script,
                inputs=[app_state],
                outputs=[app_state, narration_script_box, stage3_status],
            )
            gen_tts_btn.click(
                fn=on_generate_tts,
                inputs=[narration_script_box, tts_engine, tts_voice, allow_no_audio, app_state],
                outputs=[app_state, audio_player, srt_output, stage3_status],
            )
            gen_srt_btn.click(
                fn=on_generate_srt,
                inputs=[app_state],
                outputs=[app_state, srt_output, stage3_status],
            )

            # Stage 4: Scenes (real)
            gen_scenes_btn.click(
                fn=on_generate_scenes,
                inputs=[app_state],
                outputs=[app_state, scenes_output, stage4_status],
            ).then(
                fn=lambda s: (gr.update(visible=bool(s.get("scenes"))),),
                inputs=[app_state],
                outputs=[stage5_group],
            )
            gen_prompts_btn.click(
                fn=on_generate_scene_prompts,
                inputs=[app_state],
                outputs=[stage4_status],
            )
            validate_scenes_btn.click(
                fn=on_validate_scenes,
                inputs=[app_state],
                outputs=[stage4_status],
            )

            # Stage 5: Render (real)
            render_btn.click(
                fn=on_render_scenes,
                inputs=[app_state],
                outputs=[app_state, render_progress, render_logs, preview_video],
            ).then(
                fn=lambda s: (gr.update(visible=bool(s.get("video_path"))),),
                inputs=[app_state],
                outputs=[stage6_group],
            )

            # Stage 6: Export
            sync_btn.click(
                fn=lambda s: (
                    "- **Video:** %s\n- **Audio:** %s\n- **SRT:** %s\n- **Sincronizacao:** Pendente"
                    % (
                        "OK (%s)" % s.get("video_path", "?") if s.get("video_path") else "Pendente",
                        "OK" if s.get("audio_path") else "Pendente",
                        "OK" if s.get("srt_path") else "Pendente",
                    )
                ),
                inputs=[app_state],
                outputs=[sync_status_md],
            )
            export_btn.click(
                fn=on_export_final,
                inputs=[app_state, audio_player, srt_output, allow_no_audio],
                outputs=[app_state, preview_video, stage6_status],
            )

            quick_btn.click(
                fn=on_quick_generate,
                inputs=[quick_product, quick_audience, quick_duration, quick_style],
                outputs=[quick_video, quick_error],
            )

        # ─────────── Tab 2: Logs e Diagnostico ───────────
        with gr.Tab("Logs e Diagnostico"):
            gr.Markdown("### Logs e Diagnostico do Sistema")
            with gr.Tabs():
                with gr.Tab("Logs"):
                    with gr.Row():
                        log_level_filter = gr.Dropdown(
                            choices=["INFO", "WARN", "ERROR"], value="INFO", label="Nivel"
                        )
                        log_search = gr.Textbox(label="Buscar", placeholder="Filtrar por texto...")
                    log_limit = gr.Slider(minimum=10, maximum=100, value=20, step=5, label="Limite de linhas")
                    logs_output = gr.Dataframe(
                        headers=["horario", "nivel", "modulo", "mensagem", "sugestao", "code", "stage", "retryable", "fallback_used"],
                        label="Logs",
                        datatype=["str", "str", "str", "str", "str", "str", "str", "str", "str"],
                        col_count=(9, "fixed"),
                    )
                    with gr.Row():
                        refresh_logs_btn = gr.Button("Atualizar Logs")
                        log_summary_output = gr.Markdown()
                with gr.Tab("Erros Estruturados"):
                    with gr.Row():
                        error_severity_filter = gr.Dropdown(
                            choices=["TODOS", "DEBUG", "INFO", "WARN", "ERROR"], value="ERROR", label="Severidade"
                        )
                        error_limit = gr.Slider(minimum=5, maximum=50, value=20, step=5, label="Limite")
                    errors_output = gr.Dataframe(
                        headers=["code", "severity", "mensagem", "stage", "retryable", "fallback_used", "provider", "timestamp"],
                        label="Erros Estruturados",
                        datatype=["str", "str", "str", "str", "str", "str", "str", "str"],
                        col_count=(8, "fixed"),
                    )
                    refresh_errors_btn = gr.Button("Atualizar Erros Estruturados")
                with gr.Tab("Diagnostico"):
                    with gr.Row():
                        with gr.Column():
                            diagnostic_output = gr.Textbox(label="Diagnostico do Sistema", lines=15, max_lines=30)
                            refresh_diagnostic_btn = gr.Button("Gerar Diagnostico")
                        with gr.Column():
                            gr.Markdown("### Status dos Provedores")
                            providers_diag_md = gr.Markdown()
                            refresh_providers_diag_btn = gr.Button("Verificar Provedores")

            refresh_logs_btn.click(
                fn=on_refresh_logs,
                inputs=[log_level_filter, log_search, log_limit],
                outputs=[logs_output, log_summary_output],
            )
            refresh_errors_btn.click(
                fn=on_refresh_structured_errors,
                inputs=[error_severity_filter, error_limit],
                outputs=[errors_output],
            )
            refresh_diagnostic_btn.click(fn=copy_diagnostic_bundle, outputs=[diagnostic_output])
            refresh_providers_diag_btn.click(
                fn=lambda: "\n".join(
                    ["| Provedor | Status |", "|---------|--------|"]
                    + ["| %s | %s |" % (n, "Disponivel" if a else "Indisponivel") for n, a in get_provider_diagnostics()["status"].items()]
                    + [""] + ["**Router detect_available():**"]
                    + ["- %s: %s" % (n, a) for n, a in get_provider_diagnostics()["router_available"].items()]
                ),
                outputs=[providers_diag_md],
            )

        # ─────────── Tab 3: Dashboard de Projetos ───────────
        with gr.Tab("Dashboard de Projetos"):
            gr.Markdown("### Projetos Criados")
            with gr.Row():
                project_name_input = gr.Textbox(label="Nome do Projeto", placeholder="Ex: whey_protein_v1")
                create_project_btn = gr.Button("Criar Projeto", variant="primary", size="sm")
            create_project_status = gr.Markdown("")
            projects_list = gr.Dataframe(
                headers=["ID", "Nome", "Status", "Data"],
                label="Projetos Recentes",
                datatype=["str", "str", "str", "str"],
            )

            create_project_btn.click(
                fn=lambda name: ("Projeto criado: %s" % on_create_project(name) if name else "Informe um nome."),
                inputs=[project_name_input],
                outputs=[create_project_status],
            )

            dashboard_metrics = gr.Markdown()

            def on_refresh_dashboard():
                svc = get_metrics_service()
                s = svc.get_summary()
                return (
                    "**Projetos:** %d | **Scripts:** %d | **Videos:** %d | **Taxa de Sucesso:** %d%%"
                    % (s.get("total_projects", 0), s["generated_scripts"], s["generated_videos"], s["success_rate_percent"])
                )

            refresh_dashboard_btn = gr.Button("Atualizar Dashboard")
            refresh_dashboard_btn.click(fn=on_refresh_dashboard, outputs=[dashboard_metrics])

        # ─── Tab 5: Configuracoes ───
        with gr.Tab("Configuracoes"):
            gr.Markdown("### Preferencias do Sistema")
            config_svc = get_config_service()
            current = config_svc.get_all()
            cfg_provider = gr.Dropdown(
                choices=PROVIDER_CHOICES,
                value=current.get("default_llm_provider", "auto"),
                label="Provedor LLM Padrao",
            )
            cfg_quality = gr.Dropdown(
                choices=["DRAFT", "STANDARD", "HIGH"],
                value=current.get("default_quality", "STANDARD"),
                label="Qualidade Padrao",
            )
            cfg_duration = gr.Slider(
                minimum=10, maximum=120, value=current.get("default_duration_sec", 30),
                step=5, label="Duracao Padrao (segundos)",
            )
            cfg_logs_dir = gr.Textbox(value=current.get("logs_dir", ""), label="Diretorio de Logs")
            cfg_projects_dir = gr.Textbox(value=current.get("projects_dir", ""), label="Diretorio de Projetos")
            cfg_status = gr.Markdown()

            def on_save_config(provider, quality, duration, logs_dir, projects_dir):
                svc = get_config_service()
                svc.set_multi({
                    "default_llm_provider": provider,
                    "default_quality": quality,
                    "default_duration_sec": duration,
                    "logs_dir": logs_dir,
                    "projects_dir": projects_dir,
                })
                return "Configuracoes salvas com sucesso!"

            cfg_save_btn = gr.Button("Salvar Configuracoes", variant="primary")
            cfg_save_btn.click(
                on_save_config,
                inputs=[cfg_provider, cfg_quality, cfg_duration, cfg_logs_dir, cfg_projects_dir],
                outputs=[cfg_status],
            )

            def on_reset_config():
                svc = get_config_service()
                svc.reset()
                defaults = svc.get_all()
                return (
                    defaults["default_llm_provider"],
                    defaults["default_quality"],
                    defaults["default_duration_sec"],
                    defaults["logs_dir"],
                    defaults["projects_dir"],
                    "Configuracoes restauradas para valores padrao.",
                )

            cfg_reset_btn = gr.Button("Restaurar Padroes")
            cfg_reset_btn.click(
                on_reset_config,
                outputs=[cfg_provider, cfg_quality, cfg_duration, cfg_logs_dir, cfg_projects_dir, cfg_status],
            )

        # ─── Load ───
        def on_load():
            svc = get_metrics_service()
            s = svc.get_summary()
            return (
                "**Projetos:** %d | **Scripts:** %d | **Videos:** %d | **Taxa de Sucesso:** %d%%"
                % (s.get("total_projects", 0), s["generated_scripts"], s["generated_videos"], s["success_rate_percent"])
            )

        demo.load(fn=on_load, outputs=[dashboard_metrics])

    return demo


if __name__ == "__main__":
    try:
        import gradio
        print("Gradio version: %s" % gradio.__version__)
    except ImportError:
        print("Gradio nao encontrado. Instalando...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio"])
        import gradio

    print("Iniciando interface web GalFlowAI...")
    print("Acesse em: http://127.0.0.1:7860")

    demo = create_gradio_app()
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False, debug=True)
