import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import gradio as gr
from pipelines.auto_pipeline import run_auto_pipeline
from app.adapters.llm import ProviderRouter

def create(brief, motor_llm="auto"):
    try:
        if not brief:
            return "Erro: informe o briefing.", None, ""
        
        # Detect available providers
        router = ProviderRouter()
        available = router.detect_available()
        
        # Generate script with selected mode
        mode_map = {
            "Automático local": "auto",
            "Template local": "safe",
            "LM Studio local": "safe",
            "KoboldCpp local": "safe",
            "GPT4All local": "safe",
            "llama.cpp local": "safe"
        }
        mode = mode_map.get(motor_llm, "auto")
        
        result = run_auto_pipeline("", brief, mode=mode)
        
        if result["status"] == "completed":
            status = "Sucesso! " + ", ".join(result["logs"])
            video = result.get("video_preview", "")
            if video:
                status = status + "\nVideo: " + video
            
            # Show provider info
            provider_info = result.get("provider_info", {})
            provider_msg = "Motor usado: %s (%.2fs)" % (
                provider_info.get("provider", "Template"),
                provider_info.get("time", 0)
            )
            
            return status, video, provider_msg
        else:
            return "Erro: " + ", ".join(result["logs"]), None, "Falha no roteiro"
    except Exception as e:
        return "Erro: " + str(e), None, "Erro interno"

with gr.Blocks(title="FlowForgeAI") as demo:
    gr.Markdown("# FlowForgeAI")
    gr.Markdown("Estudio local para comerciais curtos com IA - GTX 1660 Super")
    
    with gr.Row():
        with gr.Column(scale=2):
            briefing = gr.Textbox(
                label="Briefing do comercial", 
                lines=6, 
                placeholder="Ex: Quero vender um boneco colecionavel impresso em 3D..."
            )
            motor_llm = gr.Radiobuttons(
                choices=["Automático local", "Template local", "LM Studio local", 
                         "KoboldCpp local", "GPT4All local", "llama.cpp local"],
                label="Motor de roteiro",
                value="Automático local",
                info="Use Automático para detectar LLMs disponíveis. Template sempre funciona."
            )
        with gr.Column(scale=1):
            btn = gr.Button("Criar comercial", variant="primary")
    
    output = gr.Textbox(label="Status", lines=4, interactive=False)
    video_preview = gr.Video(label="Preview do Video", visible=True)
    provider_info = gr.Textbox(label="Motor de Roteiro", interactive=False)
    
    btn.click(
        create, 
        inputs=[briefing, motor_llm], 
        outputs=[output, video_preview, provider_info]
    )

if __name__ == "__main__":
    print("Iniciando FlowForgeAI em http://127.0.0.1:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860)