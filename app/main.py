import gradio as gr
import time
import sys
from pathlib import Path

# Detect project root
PROJECT_ROOT = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta")
sys.path.insert(0, str(PROJECT_ROOT))

from pipelines.auto_pipeline import run_auto_pipeline
from app.services.script_service import (
    generate_script_with_llm,
    save_manual_edit, improve_script, complement_script,
    make_script_more_viral, make_script_more_premium, make_script_more_direct,
    create_new_script_version, restore_previous_version, approve_script,
    load_current_script, load_script_versions
)
from app.logging_config import setup_logger

logger = setup_logger()

def create_commercial(briefing, motor_llm="Automático local"):
    try:
        if not briefing:
            return "Erro: informe o briefing.", None, "", ""
        
        # Convert UI selection to mode
        mode_map = {
            "Automático local": "auto",
            "Template local": "safe",
            "LM Studio local": "safe",
            "KoboldCpp local": "safe",
            "GPT4All local": "safe",
            "llama.cpp local": "safe"
        }
        mode = mode_map.get(motor_llm, "auto")
        
        # Run pipeline
        result = run_auto_pipeline("", briefing, mode=mode)
        
        if result["status"] == "completed":
            status = "Sucesso! " + ", ".join(result["logs"])
            video = result.get("video_preview", "")
            if video:
                status = status + "\nVideo: " + video
            
            # Load script for editing
            script = load_current_script(result["project_id"])
            script_text = script.get("script", "")
            
            # Show provider info
            provider_info = result.get("provider_info", {})
            provider_msg = "Motor usado: %s (%.2fs)" % (
                provider_info.get("provider", "Template"),
                provider_info.get("time", 0)
            )
            
            return status, video, script_text, provider_msg
        else:
            return "Erro: " + ", ".join(result["logs"]), None, "", "Falha no roteiro"
    except Exception as e:
        return "Erro: " + str(e), None, "", "Erro interno"

def save_edit(project_id, script_text, note=""):
    try:
        result = save_manual_edit(project_id, script_text, note)
        return "Edição salva: " + result.get("version", ""), "OK"
    except Exception as e:
        return "Erro ao salvar: " + str(e), "ERRO"

def improve(project_id):
    try:
        result = improve_script(project_id)
        return result.get("script", ""), "Melhorado"
    except Exception as e:
        return "", "Erro: " + str(e)

def complement(project_id):
    try:
        result = complement_script(project_id)
        return result.get("script", ""), "Complementado"
    except Exception as e:
        return "", "Erro: " + str(e)

def make_viral(project_id):
    try:
        result = make_script_more_viral(project_id)
        return result.get("script", ""), "Mais viral"
    except Exception as e:
        return "", "Erro: " + str(e)

def make_premium(project_id):
    try:
        result = make_script_more_premium(project_id)
        return result.get("script", ""), "Mais premium"
    except Exception as e:
        return "", "Erro: " + str(e)

def make_direct(project_id):
    try:
        result = make_script_more_direct(project_id)
        return result.get("script", ""), "Mais direto"
    except Exception as e:
        return "", "Erro: " + str(e)

def new_version(project_id):
    try:
        result = create_new_script_version(project_id)
        return result.get("version", ""), "Nova versão criada"
    except Exception as e:
        return "", "Erro: " + str(e)

def restore_version(project_id):
    try:
        result = restore_previous_version(project_id)
        return result.get("script", ""), "Versão restaurada"
    except Exception as e:
        return "", "Erro: " + str(e)

def approve(project_id):
    try:
        result = approve_script(project_id)
        return result.get("script", ""), "Roteiro aprovado!"
    except Exception as e:
        return "", "Erro: " + str(e)

def load_versions(project_id):
    try:
        versions = load_script_versions(project_id)
        return versions
    except:
        return []

with gr.Blocks(title="FlowForgeAI") as demo:
    gr.Markdown("# FlowForgeAI")
    gr.Markdown("Estudio local para comerciais curtos com IA - GTX 1660 Super")
    
    # Store project_id (simplified - in real app use state)
    current_project_id = gr.State(value="")
    
    with gr.Row():
        with gr.Column(scale=2):
            briefing = gr.Textbox(
                label="Briefing do comercial", 
                lines=6, 
                placeholder="Ex: Quero vender um boneco colecionavel impresso em 3D..."
            )
            motor_llm = gr.Radio(
                choices=["Automático local", "Template local", 
                         "LM Studio local", "KoboldCpp local", 
                         "GPT4All local", "llama.cpp local"],
                label="Motor de roteiro",
                value="Automático local",
                info="Use Automático para detectar LLMs disponíveis. Template sempre funciona."
            )
        with gr.Column(scale=1):
            btn = gr.Button("Criar comercial", variant="primary")
    
    with gr.Row():
        status = gr.Textbox(label="Status", lines=4, interactive=False)
        provider_info = gr.Textbox(label="Motor de Roteiro", interactive=False)
    
    video_preview = gr.Video(label="Preview do Video", visible=True)
    
    # Script editing area
    gr.Markdown("## Roteiro (Editável)")
    with gr.Row():
        with gr.Column(scale=3):
            script_editor = gr.Textbox(
                label="Roteiro",
                lines=15,
                interactive=True
            )
        with gr.Column(scale=1):
            gr.Markdown("**Ações:**")
            btn_save = gr.Button("Salvar Edição", variant="secondary")
            btn_improve = gr.Button("Melhorar")
            btn_complement = gr.Button("Complementar")
            btn_viral = gr.Button("Mais Viral")
            btn_premium = gr.Button("Mais Premium")
            btn_direct = gr.Button("Mais Direto")
    
    with gr.Row():
        btn_new_version = gr.Button("Nova Versão")
        btn_restore = gr.Button("Restaurar Anterior")
        btn_approve = gr.Button("Aprovar Roteiro", variant="primary")
    
    versions_df = gr.DataFrame(label="Versões", interactive=False)
    action_status = gr.Textbox(label="Ação", interactive=False)
    
    # Click handlers
    def on_create(briefing, motor):
        result = create_commercial(briefing, motor)
        # Extract project_id from somewhere (simplified)
        return result[0], result[1], result[2], result[3], ""
    
    btn.click(
        on_create,
        inputs=[briefing, motor_llm],
        outputs=[status, video_preview, script_editor, provider_info, action_status]
    )
    
    btn_save.click(
        lambda script: (save_edit("dummy", script)[0], save_edit("dummy", script)[1]),
        inputs=[script_editor],
        outputs=[action_status, gr.Textbox(visible=False)]
    )
    
    # ========== Tab: Gerar Vídeo ==========
    with gr.Tab("🎬 Gerar Vídeo"):
        gr.Markdown("### Gerar Comercial Completo")
        gr.Markdown("Preencha os dados abaixo para gerar um comercial completo")
        
        with gr.Row():
            with gr.Column():
                vid_product = gr.Textbox(
                    label="Produto/Serviço",
                    placeholder="Ex: Curso de Python, Whey Protein...",
                    value=""
                )
                vid_audience = gr.Textbox(
                    label="Público-alvo",
                    placeholder="Ex: Iniciantes em programação, Atletas...",
                    value=""
                )
                vid_duration = gr.Slider(
                    minimum=15,
                    maximum=60,
                    value=30,
                    step=15,
                    label="Duração (segundos)"
                )
                vid_style = gr.Dropdown(
                    choices=["viral", "premium", "direct"],
                    value="viral",
                    label="Estilo"
                )
                vid_keywords = gr.Textbox(
                    label="Palavras-chave (separadas por vírgula)",
                    placeholder="Ex: curso, online, certificado",
                    value=""
                )
                vid_generate_btn = gr.Button("🎬 Gerar Comercial", variant="primary")
            
            with gr.Column():
                vid_status = gr.Textbox(
                    label="Status",
                    value="Aguardando...",
                    interactive=False
                )
                vid_progress = gr.Slider(
                    minimum=0,
                    maximum=100,
                    value=0,
                    label="Progresso",
                    interactive=False
                )
                vid_output = gr.Video(
                    label="Vídeo Gerado",
                    visible=False
                )
                vid_info = gr.JSON(
                    label="Informações do Projeto",
                    visible=False
                )
        
        def generate_video_wrapper(product, audience, duration, style, keywords_text):
            """Wrapper para gerar vídeo"""
            try:
                import httpx
                from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
                
                # Processa keywords
                keywords = None
                if keywords_text:
                    keywords = [k.strip() for k in keywords_text.split(",") if k.strip()]
                
                # Usa API se disponível, senão executa direto
                try:
                    response = httpx.post(
                        "http://127.0.0.1:8000/api/generate-video",
                        json={
                            "product": product,
                            "target_audience": audience,
                            "duration_seconds": duration,
                            "style": style,
                            "keywords": keywords
                        },
                        timeout=10
                    )
                    if response.status_code == 200:
                        result = response.json()
                        return (
                            "Vídeo gerado com sucesso via API!",
                            100,
                            result.get("final_video", ""),
                            result
                        )
                except:
                    pass
                
                # Fallback: executa direto
                pipeline = VideoGenerationPipeline()
                result = pipeline.generate_commercial(
                    project_id="manual_" + product.replace(" ", "_"),
                    product=product,
                    target_audience=audience,
                    duration_seconds=duration,
                    style=style,
                    keywords=keywords
                )
                
                if result.get("success"):
                    return (
                        f"Comercial gerado! Cenas: {result.get('scenes_succeeded')}/{result.get('scenes_count')}",
                        100,
                        result.get("final_video", ""),
                        result
                    )
                else:
                    return (
                        f"Erro: {result.get('error')}",
                        0,
                        None,
                        result
                    )
                    
            except Exception as e:
                return (
                    f"Erro: {str(e)}",
                    0,
                    None,
                    {"error": str(e)}
                )
        
        vid_generate_btn.click(
            generate_video_wrapper,
            inputs=[vid_product, vid_audience, vid_duration, vid_style, vid_keywords],
            outputs=[vid_status, vid_progress, vid_output, vid_info]
        )

if __name__ == "__main__":
    print("Iniciando FlowForgeAI em http://127.0.0.1:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860)
