import gradio as gr
import time

def create(brief, progress=gr.Progress()):
    if not brief:
        return "Erro: informe o briefing."
    
    for i in range(0, 101, 10):
        time.sleep(0.1)
        progress(i / 100)
    
    return "galFlowAI: Comercial criado com sucesso! (MVP Mock)"

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
    
    output = gr.Textbox(label="Status", interactive=False)
    
    btn.click(
        create, 
        inputs=briefing, 
        outputs=output
    )

if __name__ == "__main__":
    print("Iniciando galFlowAI em http://127.0.0.1:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860)
