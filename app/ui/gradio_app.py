"""Gradio Web Interface for GalFlowAI"""

import sys
import os
import tempfile
import logging
from pathlib import Path
from typing import Optional

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT))

import gradio as gr

# Configure logging
from app.logging_config import setup_logger
logger = setup_logger("galflowai", "info")

from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
from app.services.log_service import get_recent_logs, get_log_summary, copy_diagnostic_bundle


class WebInterface:
    """Web interface for GalFlowAI"""
    
    def __init__(self):
        self.pipeline = None
        self.current_progress = 0
        self.current_message = ""
        
    def init_pipeline(self):
        """Initialize pipeline if not already done"""
        if self.pipeline is None:
            self.pipeline = VideoGenerationPipeline()
            logger.info("Pipeline initialized for web interface")
    
    def progress_callback(self, progress: int, message: str):
        """Callback for pipeline progress updates"""
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
        """
        Generate commercial via web interface
        
        Args:
            product: Product name
            target_audience: Target audience
            duration: Duration in seconds
            style: Style (viral, premium, direct)
            progress: Gradio progress indicator
            
        Returns:
            Path to final video or None if failed
        """
        try:
            self.init_pipeline()
            
            # Update progress
            progress(0, desc="Starting...")
            
            # Generate a project ID
            import time
            project_id = f"web_{int(time.time())}"
            
            # Run pipeline with progress callback
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
                # Return error as a markdown text
                return f"ERROR: {error_msg}"
                
        except Exception as e:
            logger.error(f"Error in web interface: {e}", exc_info=True)
            return f"ERROR: {str(e)}"
    
    def get_status(self) -> dict:
        """Get pipeline status"""
        self.init_pipeline()
        return self.pipeline.get_pipeline_status()
    
    def check_availability(self) -> str:
        """Check what's available"""
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
    
    # Custom CSS
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
        
        gr.Markdown("# 🎬 GalFlowAI - Video Commercial Generator")
        gr.Markdown("Generate short video commercials for social media using AI")
        
        with gr.Row():
            with gr.Column(scale=2):
                gr.Markdown("### 📝 Input Parameters")
                
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
                
                generate_btn = gr.Button("🎬 Generate Commercial", variant="primary")
             
            with gr.Column(scale=1):
                 gr.Markdown("### 📊 Status")
                 
                 status_output = gr.Markdown()
                 refresh_btn = gr.Button("🔄 Refresh Status")
                 
                 gr.Markdown("### 📋 Central de Logs")
                 with gr.Row():
                     log_level_filter = gr.Dropdown(
                         choices=["INFO", "WARN", "ERROR"],
                         value="INFO",
                         label="Nível"
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
                 refresh_logs_btn = gr.Button("🔄 Atualizar Logs")
                 diagnostic_btn = gr.Button("📋 Diagnóstico Copiável")
        
        gr.Markdown("### 🎥 Generated Video")
        
        with gr.Row():
            video_output = gr.Video(label="Your Commercial")
            error_output = gr.Markdown(visible=False)
        
        gr.Markdown("### 📋 Instructions")
        gr.Markdown("""
        1. Fill in the product name and target audience
        2. Adjust duration and style
        3. Click 'Generate Commercial'
        4. Wait for the video to be generated (may take several minutes)
        5. Preview and download your commercial
        
        **Note:** First generation may take longer as models need to be loaded.
        """)
        
        # Event handlers
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
         
        # Initial status load
        demo.load(
            lambda: web_interface.check_availability(),
            outputs=[status_output]
        )
        
        # Logs event handlers
        def refresh_logs(level, search, limit):
            logs_data = get_recent_logs(level=level, search=search if search else None, limit=int(limit))
            return logs_data.get("logs", [])
        
        refresh_logs_btn.click(
            refresh_logs,
            inputs=[log_level_filter, log_search, log_limit],
            outputs=[logs_output]
        )
        
        def show_diagnostic():
            return copy_diagnostic_bundle()
        
        diagnostic_btn.click(
            show_diagnostic,
            inputs=None,
            outputs=gr.Textbox(label="Diagnóstico", lines=10, visible=True)
        )
    
    return demo


if __name__ == "__main__":
    # Check if dependencies are available
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
