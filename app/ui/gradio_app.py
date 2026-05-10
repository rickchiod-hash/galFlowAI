"""Interface Web Gradio para GalFlowAI"""

import sys
import os
import tempfile
import logging
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import gradio as gr

from app.logging_config import setup_logger
logger = setup_logger("galflowai", "info")

from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
from app.services.log_service import get_recent_logs, get_log_summary, copy_diagnostic_bundle
from app.services.metrics_service import get_metrics_service
from app.services.script_service import generate_script_with_provider, get_provider_status, get_provider_diagnostics


class WebInterface:
    """Interface web para GalFlowAI"""

    def __init__(self):
        self.pipeline = None
        self.current_progress = 0
        self.current_message = ""

    def init_pipeline(self):
        if self.pipeline is None:
            self.pipeline = VideoGenerationPipeline()
            logger.info("Pipeline inicializado para interface web")

    def progress_callback(self, progress: int, message: str):
        self.current_progress = progress
        self.current_message = message
        logger.info(f"Progress callback: {progress}% - {message}")
        return progress, message

    def generate_commercial_web(
        self,
        product: str,
        target_audience: str,
        duration: int,
        style: str,
        progress=gr.Progress()
    ) -> Optional[str]:
        try:
            self.init_pipeline()
            progress(0, desc="Iniciando...")

            import time
            project_id = f"web_{int(time.time())}"

            result = self.pipeline.generate_commercial(
                project_id=project_id,
                product=product,
                target_audience=target_audience,
                duration_seconds=duration,
                style=style,
                progress_callback=self.progress_callback
            )

            if result.get("success"):
                final_video = result.get("final_video")
                if final_video and Path(final_video).exists():
                    progress(100, desc="Concluido!")
                    return final_video
                else:
                    return None
            else:
                error_msg = result.get("error", "Erro desconhecido")
                logger.error(f"Pipeline falhou: {error_msg}")
                return f"ERRO: {error_msg}"

        except Exception as e:
            logger.error(f"Erro na interface web: {e}", exc_info=True)
            return f"ERRO: {str(e)}"

    def get_status(self) -> dict:
        self.init_pipeline()
        return self.pipeline.get_pipeline_status()

    def check_availability(self) -> str:
        self.init_pipeline()
        status = self.get_status()

        lines = []
        lines.append("## Status GalFlowAI")
        lines.append(f"- LLM Disponivel: {status.get('llm_available')}")
        lines.append(f"- WanGP Disponivel: {status.get('wangp_available')}")
        lines.append(f"- TTS Disponivel: {status.get('tts_available')}")
        lines.append(f"- FFmpeg Disponivel: {status.get('ffmpeg_available')}")
        lines.append(f"- Mecanismo TTS: {status.get('selected_tts_engine')}")

        return "\n".join(lines)


def create_gradio_app():
    """Cria e configura interface Gradio"""

    web_interface = WebInterface()
    metrics_service = get_metrics_service()

    custom_css = """
    .gradio-container {
        max-width: 1200px !important;
    }
    .status-box {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    """

    with gr.Blocks(css=custom_css, title="GalFlowAI - Gerador de Comerciais") as demo:

        gr.Markdown("# GalFlowAI - Gerador de Comerciais em Video")
        gr.Markdown("Crie videos comerciais curtos para redes sociais com IA")

        # --- Aba 1: Geracao de Video ---
        with gr.Tab("Geracao"):
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### Parametros de Entrada")

                    product_input = gr.Textbox(
                        label="Nome do Produto",
                        placeholder="Digite o nome do produto...",
                        value="Produto Incrivel"
                    )

                    audience_input = gr.Textbox(
                        label="Publico-Alvo",
                        placeholder="Descreva seu publico-alvo...",
                        value="Jovens adultos de 18 a 35 anos"
                    )

                    with gr.Row():
                        duration_input = gr.Slider(
                            minimum=10,
                            maximum=60,
                            value=30,
                            step=5,
                            label="Duracao (segundos)"
                        )

                        style_input = gr.Dropdown(
                            choices=["viral", "premium", "direct"],
                            value="viral",
                            label="Estilo"
                        )

                    generate_btn = gr.Button("Gerar Comercial", variant="primary")

                with gr.Column(scale=1):
                     gr.Markdown("### Status")

                     status_output = gr.Markdown()
                     refresh_btn = gr.Button("Atualizar Status")

            gr.Markdown("### Video Gerado")

            with gr.Row():
                video_output = gr.Video(label="Seu Comercial")
                error_output = gr.Markdown(visible=False)

            gr.Markdown("### Instrucoes")
            gr.Markdown("""
1. Preencha o nome do produto e publico-alvo
2. Ajuste a duracao e o estilo
3. Clique em 'Gerar Comercial'
4. Aguarde a geracao do video (pode levar alguns minutos)
5. Visualize e baixe seu comercial

**Nota:** A primeira geracao pode demorar mais enquanto os modelos sao carregados.
""")

            def on_generate(product, audience, duration, style, progress=gr.Progress()):
                result = web_interface.generate_commercial_web(
                    product=product,
                    target_audience=audience,
                    duration=duration,
                    style=style,
                    progress=progress
                )

                if result and result.startswith("ERRO"):
                    return {
                        video_output: None,
                        error_output: result,
                        error_output: gr.update(visible=True)
                    }
                else:
                    return {
                        video_output: result,
                        error_output: gr.update(visible=False)
                    }

            generate_btn.click(
                on_generate,
                inputs=[product_input, audience_input, duration_input, style_input],
                outputs=[video_output, error_output]
            )

            def on_refresh():
                return web_interface.check_availability()

            refresh_btn.click(
                on_refresh,
                outputs=[status_output]
            )

            demo.load(
                lambda: web_interface.check_availability(),
                outputs=[status_output]
            )

        # --- Aba 2: Logs ---
        with gr.Tab("Logs"):
            gr.Markdown("### Registro de Logs")
            with gr.Row():
                log_level_filter = gr.Dropdown(
                    choices=["INFO", "WARN", "ERROR"],
                    value="INFO",
                    label="Nivel"
                )
                log_search = gr.Textbox(
                    label="Buscar",
                    placeholder="Filtrar por texto..."
                )
            log_limit = gr.Slider(
                minimum=10,
                maximum=100,
                value=20,
                step=5,
                label="Limite de linhas"
            )
            logs_output = gr.Dataframe(
                headers=["horario", "nivel", "modulo", "mensagem", "sugestao"],
                label="Logs",
                datatype=["str", "str", "str", "str", "str"],
                col_count=(5, "fixed")
            )

            with gr.Row():
                refresh_logs_btn = gr.Button("Atualizar Logs")
                log_summary_output = gr.Markdown()

            def refresh_logs(level, search, limit):
                logs_data = get_recent_logs(
                    level=level,
                    search=search if search else None,
                    limit=int(limit)
                )
                summary = get_log_summary()
                summary_md = (
                    f"**{summary.get('total_info', 0)}** INFO | "
                    f"**{summary.get('total_warn', 0)}** WARN | "
                    f"**{summary.get('total_error', 0)}** ERROR"
                )
                return logs_data.get("logs", []), summary_md

            refresh_logs_btn.click(
                refresh_logs,
                inputs=[log_level_filter, log_search, log_limit],
                outputs=[logs_output, log_summary_output]
            )

        # --- Aba 3: Roteiro ---
        with gr.Tab("Roteiro"):
            gr.Markdown("### Geracao e Edicao de Roteiro")

            with gr.Row():
                with gr.Column(scale=2):
                    script_briefing = gr.Textbox(
                        label="Briefing do Produto",
                        placeholder="Descreva o produto, publico-alvo e estilo desejado...",
                        lines=3
                    )
                with gr.Column(scale=1):
                    provider_dropdown = gr.Dropdown(
                        choices=["auto", "template", "lm_studio", "koboldcpp", "llamacpp", "gpt4all"],
                        value="auto",
                        label="Provedor LLM"
                    )
                    provider_status_md = gr.Markdown("Clique em 'Verificar Provedores' para status")
                    check_providers_btn = gr.Button("Verificar Provedores")

            generate_script_btn = gr.Button("Gerar Roteiro", variant="primary")

            script_output = gr.Textbox(
                label="Roteiro Gerado",
                lines=15,
                placeholder="O roteiro aparecera aqui apos gerar..."
            )

            with gr.Row():
                script_provider_used = gr.Textbox(label="Provedor Utilizado", interactive=False)
                script_quality = gr.Textbox(label="Qualidade", interactive=False)
                script_time = gr.Textbox(label="Tempo (s)", interactive=False)

            with gr.Row():
                save_edit_btn = gr.Button("Salvar Edicao Manual")
                approve_btn = gr.Button("Aprovar Roteiro", variant="primary")
                script_status = gr.Markdown()

            def on_generate_script(briefing, provider):
                if not briefing or len(briefing.strip()) < 5:
                    return (
                        "Briefing muito curto (minimo 5 caracteres).",
                        "-", "-", "-"
                    )
                result = generate_script_with_provider(briefing, provider)
                if result.get("ok"):
                    return (
                        result["script"],
                        result.get("provider", "-"),
                        result.get("quality", "-"),
                        f'{result.get("time", 0):.2f}'
                    )
                else:
                    return (
                        f"Erro: {result.get('error', 'Falha desconhecida')}",
                        "-", "-", "-"
                    )

            generate_script_btn.click(
                on_generate_script,
                inputs=[script_briefing, provider_dropdown],
                outputs=[script_output, script_provider_used, script_quality, script_time]
            )

            def on_check_providers():
                status = get_provider_status()
                lines = []
                for name, avail in status.items():
                    icon = "Disponivel" if avail else "Indisponivel"
                    lines.append(f"- **{name}:** {icon}")
                return "\n".join(lines)

            check_providers_btn.click(
                on_check_providers,
                outputs=[provider_status_md]
            )

            def on_save_edit(script_text):
                if not script_text or script_text.startswith("Erro"):
                    return "Nada para salvar."
                import time as _time
                pid = f"manual_{int(_time.time())}"
                result = generate_script_with_provider(
                    f"Edicao manual salva em {pid}", "template"
                )
                return f"Edicao registrada. Provedor: {result.get('provider', '-')}"

            save_edit_btn.click(
                on_save_edit,
                inputs=[script_output],
                outputs=[script_status]
            )

            def on_approve(script_text):
                if not script_text or script_text.startswith("Erro"):
                    return "Nao e possivel aprovar. Gere um roteiro primeiro."
                return "Roteiro aprovado (simulado - sem projeto real vinculado)."

            approve_btn.click(
                on_approve,
                inputs=[script_output],
                outputs=[script_status]
            )

        # --- Aba 4: Metricas ---
        with gr.Tab("Metricas"):
            gr.Markdown("### Metricas de Operacao")

            metrics_summary_output = gr.Markdown()

            recent_ops_output = gr.Dataframe(
                headers=["timestamp", "tipo", "success", "duration", "provider/engine", "fallback"],
                label="Operacoes Recentes",
                datatype=["str", "str", "str", "str", "str", "str"],
                col_count=(6, "fixed")
            )

            refresh_metrics_btn = gr.Button("Atualizar Metricas")

            def refresh_metrics():
                summary = metrics_service.get_summary()
                ops = metrics_service.get_recent_operations(limit=10)

                summary_md = (
                    f"**Scripts:** {summary['generated_scripts']} | "
                    f"**Videos:** {summary['generated_videos']} | "
                    f"**Sucesso:** {summary['success_rate_percent']}% | "
                    f"**Tempo Medio:** {summary['average_generation_time']:.2f}s | "
                    f"**Fallback:** {summary.get('fallback_used', 0)} | "
                    f"**Erros:** {summary['errors']}"
                )

                ops_rows = []
                for op in ops:
                    provider = op.get("provider", op.get("engine", ""))
                    ops_rows.append([
                        op.get("timestamp", "")[-19:],
                        op.get("type", ""),
                        "Sim" if op.get("success") else "Nao",
                        f'{op.get("duration", 0):.1f}s',
                        provider,
                        "Sim" if op.get("used_fallback") else "Nao"
                    ])

                if not ops_rows:
                    ops_rows.append(["-", "-", "-", "-", "-", "-"])

                return summary_md, ops_rows

            refresh_metrics_btn.click(
                refresh_metrics,
                outputs=[metrics_summary_output, recent_ops_output]
            )

        # --- Aba 5: Diagnostico ---
        with gr.Tab("Diagnostico"):
            gr.Markdown("### Diagnostico do Sistema")

            with gr.Row():
                with gr.Column():
                    diagnostic_output = gr.Textbox(
                        label="Informacoes de Diagnostico",
                        lines=20,
                        max_lines=40
                    )
                    refresh_diagnostic_btn = gr.Button("Gerar Diagnostico")

                with gr.Column():
                    gr.Markdown("### Status dos Provedores")
                    providers_diagnostic_md = gr.Markdown()
                    refresh_providers_diag_btn = gr.Button("Verificar Provedores")

            gr.Markdown("Copie o texto de diagnostico para compartilhar informacoes do sistema.")

            def refresh_diagnostic():
                return copy_diagnostic_bundle()

            refresh_diagnostic_btn.click(
                refresh_diagnostic,
                outputs=[diagnostic_output]
            )

            def refresh_providers_diag():
                diag = get_provider_diagnostics()
                lines = ["| Provedor | Status |", "|---------|--------|"]
                for name, avail in diag["status"].items():
                    icon = "Disponivel" if avail else "Indisponivel"
                    lines.append(f"| {name} | {icon} |")
                lines.append("")
                lines.append("**Router detect_available():**")
                for name, avail in diag["router_available"].items():
                    lines.append(f"- {name}: {avail}")
                return "\n".join(lines)

            refresh_providers_diag_btn.click(
                refresh_providers_diag,
                outputs=[providers_diagnostic_md]
            )

    return demo


if __name__ == "__main__":
    try:
        import gradio
        print(f"Gradio version: {gradio.__version__}")
    except ImportError:
        print("Gradio nao encontrado. Instalando...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio"])
        import gradio

    print("Iniciando interface web GalFlowAI...")
    print("Acesse em: http://127.0.0.1:7860")

    demo = create_gradio_app()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True
    )
