import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import gradio as gr
from pipelines.auto_pipeline import run_auto_pipeline

def create(brief):
    try:
        if not brief:
            return "Erro: informe o briefing."
        
        result = run_auto_pipeline("", brief)
        
        if result["status"] == "completed":
            status = "Sucesso! " + ", ".join(result["logs"])
            video = result.get("video_preview", "")
            if video:
                status = status + "\nVideo: " + video
            return status
        else:
            return "Erro: " + ", ".join(result["logs"])
    except Exception as e:
        return "Erro: " + str(e)

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
        with gr.Column(scale=1):
            btn = gr.Button("Criar comercial", variant="primary")
    
    output = gr.Textbox(label="Status", lines=4, interactive=False)

    btn.click(
        create, 
        inputs=[briefing], 
        outputs=[output]
    )

if __name__ == "__main__":
    print("Iniciando FlowForgeAI em http://127.0.0.1:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860)