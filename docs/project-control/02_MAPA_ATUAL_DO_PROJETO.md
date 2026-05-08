# 02_MAPA_ATUAL_DO_PROJETO — GalFlowAI

Preencher somente com evidência local.

## Raiz real do projeto

- Caminho: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta`
- Evidência: `.git` presente, `README.md`, `app/` com código fonte, `tests/`.

## Tecnologias detectadas

| Tecnologia | Evidência | Papel no projeto | Risco |
|---|---|---|---|
| Python 3.12+ | `app/*.py`, `requirements` (implícito) | Toda a lógica | Baixo |
| Gradio | `app/ui/gradio_app.py`, `app/main.py` | UI principal | Médio (sintaxe complexa) |
| FastAPI | `app/api.py` | API REST | Baixo |
| FFmpeg | `app/adapters/ffmpeg_adapter.py`, `scripts/check_ffmpeg.py` | Montagem/fallback | Médio (caminhos Windows) |
| WanGP | `app/adapters/wangp_adapter.py` | Vídeo opcional | Alto (6GB VRAM) |
| TTS | `app/adapters/tts_adapter.py` | Narração | Baixo |

## Entrypoints

| Arquivo | Função | Evidência | Observação |
|---|---|---|---|
| `run_galFlowAI.py` | Iniciar app | Presente na raiz | Entrada principal |
| `app/main.py` | Gradio UI + lógica principal | Presente | 1200+ linhas, contém handlers de UI |
| `app/api.py` | FastAPI endpoints | Presente | ~800 linhas, 20+ endpoints |
| `scripts/start_flowforgeai_standard.bat` | BAT padrão com env vars | Presente | Configura variáveis de ambiente |

## Estado das features obrigatórias

Use `docs/reference/FEATURE_PRESERVATION_MATRIX.md` como checklist.
