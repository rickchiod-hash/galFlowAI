"""Exemplo de uso do VideoService - Geração de comercial completo"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))


def progress_callback(progress: int, message: str):
    """Callback simples para mostrar progresso"""
    bar_length = 30
    filled = int(bar_length * progress / 100)
    bar = "#" * filled + "-" * (bar_length - filled)
    print(f"[{bar}] {progress}% - {message}")


def main():
    """Exemplo principal"""
    print("=== GalFlowAI - Exemplo de Geração de Vídeo ===\n")
    
    # Importa o serviço
    from app.services.video_service import VideoService
    
    # Cria o serviço
    print("Inicializando VideoService...")
    service = VideoService()
    
    # Verifica status
    status = service.get_status()
    print(f"Status: {status}\n")
    
    if not status["available"]:
        print("ERRO: Nenhum motor de vídeo disponível!")
        print("Certifique-se de que WanGP ou FFmpeg está instalado.")
        return
    
    # Configuração do comercial
    print("Configurando geração de comercial...")
    project_id = "20260505_120000_exemplo"
    product = "GalFlowAI - Gerador de Vídeos"
    target_audience = "Criadores de conteúdo, marqueteiros, pequenas empresas"
    
    print(f"Projeto: {project_id}")
    print(f"Produto: {product}")
    print(f"Público: {target_audience}")
    print(f"Provedor: {status['preferred_provider']}\n")
    
    # Gera o comercial
    print("Iniciando geração...\n")
    result = service.generate_commercial(
        project_id=project_id,
        product=product,
        target_audience=target_audience,
        duration_seconds=30,
        style="viral",
        progress_callback=progress_callback
    )
    
    # Mostra resultado
    print("\n" + "="*50)
    if result["success"]:
        print("SUCESSO! Comercial gerado:")
        print(f"  Vídeo final: {result.get('final_video')}")
        print(f"  Roteiro: {result.get('script_path')}")
        print(f"  Cenas: {result.get('scenes_count')}")
        print(f"  Cenas com sucesso: {result.get('scenes_succeeded')}")
        print(f"  Provedor usado: {result.get('provider_used')}")
    else:
        print("FALHA ao gerar comercial:")
        print(f"  Erro: {result.get('error')}")
    print("="*50)


if __name__ == "__main__":
    main()
