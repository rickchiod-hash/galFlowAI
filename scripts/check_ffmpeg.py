"""Verifica e configura FFmpeg para o projeto"""

import os
import sys
from pathlib import Path

def find_ffmpeg():
    """Procura FFmpeg em caminhos conhecidos"""
    # Caminhos para verificar
    paths_to_check = [
        # Caminho encontrado anteriormente (mas arquivo não existe)
        r"K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP\ffmpeg_bins\ffmpeg.exe",
        # Caminhos alternativos
        r"K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Library\bin\ffmpeg.exe",
        r"K:\AI_VIDEO_COMERCIAL_STUDIO\tools\ffmpeg.exe",
        r"C:\Program Files\ffmpeg\bin\ffmpeg.exe",
        r"C:\ffmpeg\bin\ffmpeg.exe",
    ]
    
    for path in paths_to_check:
        if os.path.exists(path):
            print(f"FFmpeg encontrado: {path}")
            return path
    
    # Tenta via PATH
    import shutil
    ffmpeg_in_path = shutil.which("ffmpeg")
    if ffmpeg_in_path:
        print(f"FFmpeg encontrado no PATH: {ffmpeg_in_path}")
        return ffmpeg_in_path
    
    print("FFmpeg não encontrado em caminhos conhecidos.")
    return None

def main():
    print("=== Verificação de FFmpeg ===")
    ffmpeg_path = find_ffmpeg()
    
    if ffmpeg_path:
        print(f"\nFFmpeg disponível: {ffmpeg_path}")
        # Atualiza o arquivo de configuração se necessário
        print("\nPara configurar manualmente, edite app/adapters/ffmpeg_adapter.py")
    else:
        print("\nFFmpeg não encontrado.")
        print("Para instalar:")
        print("1. Baixe de https://ffmpeg.org/download.html")
        print("2. Extraia para K:\\AI_VIDEO_COMERCIAL_STUDIO\\tools\\ffmpeg")
        print("3. Ou instale via gerenciador de pacotes (chocolatey, scoop)")

if __name__ == "__main__":
    main()
