"""Gradio Web Interface for GalFlowAI"""

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


class WebInterface:
    """Web interface for GalFlowAI"""

    def __init__(self):
        self.pipeline = None
        self.current_progress = 0
        self.current_message = ""

    def init_pipeline(self):
        if self.pipeline is None:
            self.pipeline = VideoGenerationPipeline()
            logger.info("Pipeline initialized for web interface")

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
            progress(0, desc="Starting...")

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
                    progress(100, desc="Completed!")
                    return final_video
                else:
                    return None
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f"Pipeline failed: {error_msg}")
                return f"ERROR: {error_msg}"

        except Exception as e:
            logger.error(f"Error in web interface: {e}", exc_info=True)
            return f"ERROR: {str(e)}"

    def get_status(self) -> dict:
        self.init_pipeline()
        return self.pipeline.get_pipeline_status()

    def check_availability(self) -> str:
        self.init_pipeline()
        status = self.get_status()

        lines = []
        lines.append("## GalFlowAI Status")
        lines.append(f"- LLM Available: {status.get('llm_available')}")
        lines.append(f"- WanGP Available: {status.get('wangp_available')}")
        lines.append(f"- TTS Available: {status.get('tts_available')}")
        lines.append(f"- FFmpeg Available: {status.get('ffmpeg_available')}")
        lines.append(f"- Selected TTS Engine: {status.get('selected_tts_engine')}")

        return "\n".join(lines)


def create_gradio_app():
    """Create and configure Gradio interface"""

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

    with gr.Blocks(css=custom_css, title="GalFlowAI - Video Commercial Generator") as demo:

        gr.Markdown("# GalFlowAI - Video Commercial Generator")
        gr.Markdown("Generate short video commercials for social media using AI")

        # --- Tab 1: Video Generation ---
        with gr.Tab("Geracao"):
            with gr.Row():
                with gr.Column(scale=2):
                    gr.Markdown("### Input Parameters")

                    product_input = gr.Textbox(
                        label="Product Name",
                        placeholder="Enter your product name...",
                        value="Amazing Product"
                    )

                    audience_input = gr.Textbox(
                        label="Target Audience",
                        placeholder="Describe your target audience...",
                        value="Young adults aged 18-35"
                    )

                    with gr.Row():
                        duration_input = gr.Slider(
                            minimum=10,
                            maximum=60,
                            value=30,
                            step=5,
                            label="Duration (seconds)"
                        )

                        style_input = gr.Dropdown(
                            choices=["viral", "premium", "direct"],
                            value="viral",
                            label="Style"
                        )

                    generate_btn = gr.Button("Generate Commercial", variant="primary")

                with gr.Column(scale=1):
                     gr.Markdown("### Status")

                     status_output = gr.Markdown()
                     refresh_btn = gr.Button("Refresh Status")

            gr.Markdown("### Generated Video")

            with gr.Row():
                video_output = gr.Video(label="Your Commercial")
                error_output = gr.Markdown(visible=False)

            gr.Markdown("### Instructions")
            gr.Markdown("""
1. Fill in the product name and target audience
2. Adjust duration and style
3. Click 'Generate Commercial'
4. Wait for the video to be generated (may take several minutes)
5. Preview and download your commercial

**Note:** First generation may take longer as models need to be loaded.
""")

            def on_generate(product, audience, duration, style, progress=gr.Progress()):
                result = web_interface.generate_commercial_web(
                    product=product,
                    target_audience=audience,
                    duration=duration,
                    style=style,
                    progress=progress
                )

                if result and result.startswith("ERROR"):
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

        # --- Tab 2: Logs ---
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

        # --- Tab 3: Metrics ---
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

        # --- Tab 4: Diagnostic ---
        with gr.Tab("Diagnostico"):
            gr.Markdown("### Diagnostico do Sistema")

            diagnostic_output = gr.Textbox(
                label="Informacoes de Diagnostico",
                lines=20,
                max_lines=40
            )

            gr.Markdown("Copie o texto acima para compartilhar informacoes de diagnostico.")

            refresh_diagnostic_btn = gr.Button("Gerar Diagnostico")

            def refresh_diagnostic():
                return copy_diagnostic_bundle()

            refresh_diagnostic_btn.click(
                refresh_diagnostic,
                outputs=[diagnostic_output]
            )

    return demo


if __name__ == "__main__":
    try:
        import gradio
        print(f"Gradio version: {gradio.__version__}")
    except ImportError:
        print("Gradio not found. Installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio"])
        import gradio

    print("Starting GalFlowAI Web Interface...")
    print("Access at: http://127.0.0.1:7860")

    demo = create_gradio_app()
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        debug=True
    )
