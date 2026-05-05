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
    create_new_version, restore_previous_version, approve_script,
    load_current_script, load_script_versions
)
from app.logging_config import setup_logger

logger = setup_logger()

def create_commercial(briefing, motor_llm="Automático local", progress=gr.Progress()):
    try:
        if not briefing:
            return "Erro: informe o briefing.", None, "", "", "", ""
        
        progress(0, desc="Iniciando...")
        
        # Convert UI selection to mode (implementa motores locais)
        mode_map = {
            "Automático local": "auto",
            "Template local": "template",
            "LM Studio local": "lmstudio",
            "KoboldCpp local": "koboldcpp",
            "GPT4All local": "gpt4all",
            "llama.cpp local": "llamacpp"
        }
        mode = mode_map.get(motor_llm, "auto")
        
        progress(0.3, desc="Gerando roteiro...")
        
        # Run pipeline
        result = run_auto_pipeline("", briefing, mode=mode)
        
        progress(0.7, desc="Carregando resultados...")
        
        if result["status"] == "completed":
            project_id = result.get("project_id", "")
            status = "Sucesso! " + ", ".join(result["logs"])
            video = result.get("video_preview", None)
            # Garantir que video seja None se não for arquivo válido
            if video and isinstance(video, str) and len(video) > 0 and Path(video).exists():
                status = status + "\nVideo: " + video
            else:
                video = None
            
            # Carrega roteiro: primeiro do resultado do pipeline
            script_text = result.get("script", "")
            
            # Se vazio, tenta load_current_script
            if not script_text:
                script = load_current_script(project_id)
                if script and script.get("script"):
                    script_text = script.get("script")
            
            # Se ainda vazio, lê o arquivo diretamente usando Path global
            if not script_text:
                script_file = Path(f"K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects/{project_id}/script/script.txt")
                if script_file.exists():
                    script_text = script_file.read_text(encoding="utf-8")
            
            # Show provider info
            provider_info = result.get("provider_info", {})
            provider_msg = "Motor usado: %s (%.2fs)" % (
                provider_info.get("provider", "Template"),
                provider_info.get("time",0)
            )
            
            progress(1.0, desc="Concluído!")
            return status, video, script_text, provider_msg, "", project_id
        else:
            error_msg = "Erro: " + ", ".join(result["logs"])
            return error_msg, None, "", "Falha no roteiro", "", ""
    except Exception as e:
        return "Erro: " + str(e), None, "", "Erro interno", "", ""

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
        result = create_new_version(project_id)
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

with gr.Blocks(title="GalFlowAI") as demo:
    gr.Markdown("# GalFlowAI")
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
        return create_commercial(briefing, motor)
        # result: status, video, script_text, provider_msg, action_status, project_id
        # Garante que script_text não seja None
        # script_text = result[2] if result[2] else ""
        # return result[0], result[1], script_text, result[3], result[4], result[5]
    
    btn.click(
        on_create,
        inputs=[briefing, motor_llm],
        outputs=[status, video_preview, script_editor, provider_info, action_status, current_project_id]
    )
    
    def on_save(project_id, script):
        if not project_id:
            return "Erro: Nenhum projeto carregado", ""
        result = save_edit(project_id, script)
        return result[0], result[1]
    
    btn_save.click(
        on_save,
        inputs=[current_project_id, script_editor],
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
        
        def generate_video_wrapper(product, audience, duration, style, keywords_text, progress=gr.Progress()):
            """Wrapper para gerar vídeo com indicador de progresso"""
            try:
                import httpx
                from app.pipeline.video_generation_pipeline import VideoGenerationPipeline
                
                progress(0.1, desc="Iniciando geração de vídeo...")
                
                # Processa keywords
                keywords = None
                if keywords_text:
                    keywords = [k.strip() for k in keywords_text.split(",") if k.strip()]
                
                progress(0.3, desc="Conectando aos serviços...")
                
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
                        progress(0.8, desc="Vídeo gerado com sucesso!")
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
                progress(0.5, desc="Executando pipeline local...")
                pipeline = VideoGenerationPipeline()
                result = pipeline.generate_commercial(
                    project_id="manual_" + product.replace(" ", "_"),
                    product=product,
                    target_audience=audience,
                    duration_seconds=duration,
                    style=style,
                    keywords=keywords
                )
                
                progress(0.9, desc="Finalizando...")
                
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
                    None
                )
                
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
    
    # ========== Tab: Central de Logs ==========
    with gr.Tab("📋 Logs e Diagnóstico"):
        gr.Markdown("# Central de Logs")
        gr.Markdown("Acompanhe eventos, avisos e erros da aplicação em tempo real controlado.")
        
        # Cards de resumo
        with gr.Row():
            with gr.Column(scale=1):
                info_count = gr.Number(label="Total INFO", value=0)
            with gr.Column(scale=1):
                warn_count = gr.Number(label="Total WARN", value=0)
            with gr.Column(scale=1):
                error_count = gr.Number(label="Total ERROR", value=0)
            with gr.Column(scale=2):
                last_error_display = gr.Textbox(label="Último erro", interactive=False)
            with gr.Column(scale=2):
                last_update_display = gr.Textbox(label="Última atualização", interactive=False)
        
        # Filtro e busca
        with gr.Row():
            level_filter = gr.Dropdown(
                choices=["Todos", "INFO", "WARN", "ERROR"],
                value="Todos",
                label="Filtrar por nível"
            )
            search_box = gr.Textbox(
                label="Buscar nos logs",
                placeholder="Ex: FFmpeg, provider, project_id, erro, roteiro",
                value=""
            )
        
        # Tabela de logs
        logs_table = gr.DataFrame(
            headers=["Horário", "Nível", "Módulo", "Projeto", "Job", "Mensagem", "Sugestão"],
            label="Logs Recentes",
            interactive=False
        )
        
        # Console bruto
        raw_console = gr.Textbox(
            label="Console Bruto (últimas linhas)",
            lines=15,
            interactive=False,
            max_lines=500
        )
        
        # Botões
        with gr.Row():
            btn_update = gr.Button("🔄 Atualizar logs", variant="primary")
            btn_clear = gr.Button("🧹 Limpar visualização")
            btn_copy = gr.Button("📋 Copiar diagnóstico")
            btn_open_folder = gr.Button("📁 Abrir pasta de logs")
            btn_open_file = gr.Button("📄 Abrir arquivo de log")
            btn_pause = gr.Button("⏸ Pausar atualização automática")
            btn_resume = gr.Button("▶ Retomar atualização automática")
        
        status_logs = gr.Textbox(label="Status", interactive=False)
        
        # Variável de estado para controlar pausa
        auto_update_paused = gr.State(value=False)
        
        # Funções síncronas para logs (conforme instruções: "NEM TUDO DEVE SER ASYNC")
        def update_logs(level_filter, search_text):
            """Atualiza logs - síncrono conforme instruções."""
            try:
                from app.services.log_service import get_recent_logs, get_log_summary
                
                # Converte filtro
                level_map = {"Todos": None, "INFO": "info", "WARN": "warn", "ERROR": "error"}
                level = level_map.get(level_filter, None)
                
                # Busca logs
                result = get_recent_logs(level=level, search=search_text if search_text else None, limit=200)
                logs = result.get("logs", [])
                
                # Atualiza tabela
                if logs:
                    import pandas as pd
                    df = pd.DataFrame(logs)
                else:
                    df = pd.DataFrame(columns=["horario", "nivel", "modulo", "projeto", "job", "mensagem", "sugestao"])
                
                # Console bruto
                console_text = ""
                for log in logs[:50]:
                    console_text += f"{log.get('horario', '')} [{log.get('nivel', '')}] {log.get('mensagem', '')}\n"
                
                # Resumo
                summary = get_log_summary()
                
                return (
                    df,
                    console_text,
                    summary.get("total_info", 0),
                    summary.get("total_warn", 0),
                    summary.get("total_error", 0),
                    summary.get("last_error", "")[:200],
                    summary.get("last_update", ""),
                    "Logs atualizados." if not summary.get("message") else summary.get("message")
                )
            except Exception as e:
                return (
                    pd.DataFrame(),
                    f"Erro ao ler logs: {str(e)}",
                    0, 0, 0, "",
                    "",
                    f"Erro: {str(e)}"
                )
        
        def clear_view():
            import pandas as pd
            return (
                pd.DataFrame(columns=["horario", "nivel", "modulo", "projeto", "job", "mensagem", "sugestao"]),
                "",
                0, 0, 0, "",
                "",
                "Visualização limpa."
            )
        
        def copy_diagnostic():
            try:
                from app.services.log_service import copy_diagnostic_bundle
                bundle = copy_diagnostic_bundle()
                return f"Diagnóstico copiável:\n\n{bundle}"
            except Exception as e:
                return f"Erro ao gerar diagnóstico: {str(e)}"
        
        def open_folder():
            try:
                from app.services.log_service import open_logs_folder
                result = open_logs_folder()
                return result.get("message", "")
            except Exception as e:
                return f"Erro: {str(e)}"
        
        def open_log_file():
            try:
                import subprocess
                from pathlib import Path
                log_file = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/logs/galflowai.log")
                if log_file.exists():
                    subprocess.Popen(f'explorer "{log_file}"')
                    return "Arquivo de log aberto."
                else:
                    return "Arquivo de log ainda não existe."
            except Exception as e:
                return f"Erro: {str(e)}"
        
        # Callbacks
        btn_update.click(
            update_logs,
            inputs=[level_filter, search_box],
            outputs=[logs_table, raw_console, info_count, warn_count, error_count, last_error_display, last_update_display, status_logs]
        )
        
        btn_clear.click(
            clear_view,
            outputs=[logs_table, raw_console, info_count, warn_count, error_count, last_error_display, last_update_display, status_logs]
        )
        
        btn_copy.click(
            copy_diagnostic,
            outputs=[status_logs]
        )
        
        btn_open_folder.click(
            open_folder,
            outputs=[status_logs]
        )
        
        btn_open_file.click(
            open_log_file,
            outputs=[status_logs]
        )
        
        # Timer para atualização automática (gr.Timer é aceitável conforme instruções)
        timer = gr.Timer(2.0, active=True)  # 2 segundos conforme instruções
        
        def timer_callback(level_filter, search_text, is_paused):
            if is_paused:
                return gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), gr.update(), "Atualização automática pausada."
            return update_logs(level_filter, search_text)
        
        timer.tick(
            timer_callback,
            inputs=[level_filter, search_box, auto_update_paused],
            outputs=[logs_table, raw_console, info_count, warn_count, error_count, last_error_display, last_update_display, status_logs]
        )
        
        # Botões de pausar/retomar
        def pause_update():
            return True, "Atualização automática pausada."
        
        def resume_update():
            return False, "Atualização automática retomada."
        
        btn_pause.click(
            pause_update,
            outputs=[auto_update_paused, status_logs]
        )
        
        btn_resume.click(
            resume_update,
            outputs=[auto_update_paused, status_logs]
        )
    
    # ========== Tab: Dashboard de Projetos ==========
    with gr.Tab("📊 Dashboard de Projetos"):
        gr.Markdown("# Dashboard de Projetos")
        gr.Markdown("Visão geral de todos os projetos criados.")
        
        with gr.Row():
            with gr.Column(scale=1):
                btn_refresh = gr.Button("🔄 Atualizar Lista", variant="primary")
            with gr.Column(scale=3):
                projects_count = gr.Number(label="Total de Projetos", value=0)
        
        projects_table = gr.DataFrame(
            headers=["ID", "Nome", "Data", "Status", "Vídeo", "Ações"],
            label="Projetos",
            interactive=False
        )
        
        # Detalhes do projeto selecionado
        with gr.Row():
            with gr.Column():
                proj_details = gr.JSON(label="Detalhes do Projeto", visible=False)
            with gr.Column():
                proj_status = gr.Textbox(label="Status do Projeto", interactive=False)
        
        gr.Markdown("### Ações em Lote")
        with gr.Row():
            btn_open_folder = gr.Button("📁 Abrir Pasta do Projeto")
            btn_delete = gr.Button("🗑️ Excluir Projeto", variant="stop")
        
        dashboard_status = gr.Textbox(label="Status", interactive=False)
        
        def load_projects():
            """Carrega lista de projetos do diretório."""
            try:
                from pathlib import Path
                import json
                from datetime import datetime
                
                projects_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects")
                if not projects_dir.exists():
                    return [], 0, "Diretório de projetos não encontrado.", {}
                
                projects = []
                for proj_dir in sorted(projects_dir.iterdir(), reverse=True):
                    if proj_dir.is_dir():
                        # Tenta ler project.json
                        proj_file = proj_dir / "project.json"
                        status = "❓ Desconhecido"
                        has_video = "❌"
                        
                        if proj_file.exists():
                            try:
                                data = json.loads(proj_file.read_text(encoding="utf-8"))
                                status = data.get("status", status)
                                if (proj_dir / "final" / "commercial.mp4").exists():
                                    has_video = "✅"
                            except:
                                pass
                        else:
                            # Tenta detectar status pelos arquivos
                            if (proj_dir / "final" / "commercial.mp4").exists():
                                status = "✅ Concluído"
                                has_video = "✅"
                            elif (proj_dir / "renders").exists():
                                status = "🎬 Renderizando"
                            elif (proj_dir / "prompts").exists():
                                status = "📝 Roteiro"
                            elif (proj_dir / "script").exists():
                                status = "📝 Roteiro"
                        
                        # Extrai nome amigável
                        dir_name = proj_dir.name
                        parts = dir_name.split("_")
                        nome = " ".join(parts[2:]) if len(parts) > 2 else dir_name
                        
                        projects.append([
                            dir_name,
                            nome,
                            parts[0] + "_" + parts[1] if len(parts) >= 2 else "N/A",
                            status,
                            has_video,
                            "Ver"
                        ])
                
                return projects, len(projects), f"{len(projects)} projetos encontrados.", {}
                
            except Exception as e:
                return [], 0, f"Erro: {str(e)}", {}
        
        def open_project_folder(proj_id):
            """Abre pasta do projeto."""
            try:
                from pathlib import Path
                import subprocess
                
                proj_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects") / proj_id
                if proj_dir.exists():
                    subprocess.Popen(f'explorer "{proj_dir}"')
                    return f"Pasta aberta: {proj_dir}"
                return "Projeto não encontrado."
            except Exception as e:
                return f"Erro: {str(e)}"
        
        def get_project_details(proj_id):
            """Retorna detalhes do projeto."""
            try:
                from pathlib import Path
                import json
                
                proj_dir = Path("K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/projects") / proj_id
                if not proj_dir.exists():
                    return {}, "Projeto não encontrado."
                
                details = {
                    "id": proj_id,
                    "path": str(proj_dir),
                    "exists": True,
                    "files": {}
                }
                
                # Verifica arquivos
                for subdir in ["brief", "script", "prompts", "storyboard", "renders", "audio", "final"]:
                    subdir_path = proj_dir / subdir
                    details["files"][subdir] = subdir_path.exists()
                
                # Lê project.json se existir
                proj_file = proj_dir / "project.json"
                if proj_file.exists():
                    try:
                        data = json.loads(proj_file.read_text(encoding="utf-8"))
                        details["data"] = data
                    except:
                        pass
                
                return details, "Detalhes carregados."
                
            except Exception as e:
                return {}, f"Erro: {str(e)}"
        
        btn_refresh.click(
            load_projects,
            outputs=[projects_table, projects_count, dashboard_status, proj_details]
        )
        
        # Carrega projetos ao iniciar
        demo.load(
            load_projects,
            outputs=[projects_table, projects_count, dashboard_status, proj_details]
        )
    
if __name__ == "__main__":
    print("Iniciando GalFlowAI em http://127.0.0.1:7860")
    demo.launch(server_name="127.0.0.1", server_port=7860)

