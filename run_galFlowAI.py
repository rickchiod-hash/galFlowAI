import sys
import os

# Mudar para o diretorio do projeto (single L)
os.chdir(r"K:\AI_VIDEO_COMMERCIAL_STUDIO\opencodegalpasta")

# Configurar variaveis de ambiente
os.environ['PIP_CACHE_DIR'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\pip'
os.environ['HF_HOME'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\huggingface'
os.environ['TORCH_HOME'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\torch'
os.environ['XDG_CACHE_HOME'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\cache'
os.environ['TEMP'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\temp'
os.environ['TMP'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\temp'
os.environ['OLLAMA_MODELS'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\models\ollama'
os.environ['GIT_PYTHON_GIT_EXECUTABLE'] = r'K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\Library\bin\git.exe'

print("="*60)
print("galFlowAI - Iniciando aplicacao...")
print("Python:", sys.version)
print("="*60)

from app.main import demo

if __name__ == "__main__":
    print("\nServidor rodando em http://127.0.0.1:7860\n")
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
        quiet=False
    )
