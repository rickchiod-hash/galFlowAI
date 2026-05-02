import gradio as gr
import time
from pathlib import Path

def create_commercial(briefing, progress=gr.Progress()):
    if not briefing:
        return "Erro: informe o briefing.", None, "Erro: briefing vazio"
    
    try:
        progress(0.1, "Criando projeto...")
        from app.project_manager import create_project
        project = create_project("comercial")
        pid = project["id"]
        
        progress(0.2, "Gerando roteiro...")
        from app.pipeline.script_generator import generate_script, save_script
        script = generate_script(briefing, pid)
        save_script(pid, script)
        
        progress(0.4, "Dividindo em cenas...")
        from app.pipeline.scene_splitter import split_script_into_scenes, save_scenes
        scenes = split_script_into_scenes(script, pid)
        save_scenes(pid, scenes)
        
        progress(0.6, "Renderizando cenas...")
        from app.adapters.ffmpeg_adapter import create_storyboard_video
        video = create_storyboard_video(pid, scenes)
        
        progress(0.8, "Gerando narracao...")
        from app.adapters.tts_adapter import generate_project_narration
        audios = generate_project_narration(pid, script)
        
        progress(1.0, "Concluido!")
        
        if video and Path(video).exists():
            return "galFlowAI: Comercial criado com sucesso!", str(video), "Video: %s" % Path(video).name
        else:
            return "galFlowAI: Projeto criado, mas video nao gerado.", None, "Verifique logs"
            
    except Exception as e:
        return "Erro: %s" % str(e), None, "Falha no pipeline"

with gr.Blocks(title="galFlowAI") as demo:
    gr.Markdown("# galFlowAI")
    gr.Markdown("Estudio local para comerciais curtos com IA")
    
    with gr.Row():
        briefing = gr.Textbox(
            label="Briefing do comercial", 
            lines=4, 
            placeholder="Ex: Quero vender um boneco colecionavel impresso em 3D..."
        )
        btn = gr.Button("Criar comercial", variant="primary", scale=1)
    
    with gr.Row():
        status = gr.Textbox(label="Status", interactive=False)
        output_file = gr.File(label="Video gerado", interactive=False)
    
    log_output = gr.Textbox(label="Log", interactive=False, lines=2)
    
    btn.click(
        create_commercial, 
        inputs=briefing, 
        outputs=[status, output_file, log_output]
    )

if __name__ == "__main__":
    print("Iniciando galFlowAI em http://127.0.0.1:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860)
