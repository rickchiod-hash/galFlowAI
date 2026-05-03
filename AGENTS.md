# FlowForgeAI — Regras do Agente OpenCode

## Missão
Criar e evoluir um software local-first para geração de comerciais curtos para redes sociais, rodando primeiro em Windows no disco K:, com interface web em http://127.0.0.1:7860.

## Nome do produto
Nome final: FlowForgeAI.
O nome do projeto deve terminar com AI.

## Contexto operacional obrigatório
- Raiz operacional: K:\AI_VIDEO_COMMERCIAL_STUDIO
- Pasta de trabalho OpenCode: K:\AI_VIDEO_COMMERCIAL_STUDIO\opencodegalpasta
- Não instalar, baixar, cachear, gerar temporários ou modelos no C:.
- Usar o ambiente existente quando possível:
  - K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio
  - Python atual pode ser 3.10.20 se já estiver funcionando com WanGP.
  - Só propor Python 3.11 em ambiente isolado se não quebrar nada.
- WanGP/Wan2GP já existe em:
  - K:\AI_VIDEO_COMMERCIAL_STUDIO\engines\Wan2GP
- FramePack já existe em:
  - K:\AI_VIDEO_COMMERCIAL_STUDIO\engines\FramePack
- Imagens de referência ficam em:
  - K:\AI_VIDEO_COMMERCIAL_STUDIO\assets\reference

## Hardware real
- CPU: AMD Ryzen 5 5600, 6 cores / 12 threads.
- RAM: 16 GB DDR4.
- GPU: NVIDIA GTX 1660 Super 6 GB VRAM.
- Disco principal: K:.

## Restrições absolutas
1. Não usar RunPod.
2. Não usar serviço pago obrigatório.
3. Não usar API paga como dependência do MVP.
4. Não apagar ambientes existentes.
5. Não reinstalar se já existe.
6. Não baixar modelos repetidos.
7. Não usar modelos 14B como padrão.
8. Não quebrar WanGP já instalado.
9. Criar backup antes de sobrescrever arquivo.
10. Toda alteração relevante deve gerar log.
11. Se VRAM <= 6 GB, usar preset seguro: 1.3B, 480p/512p, cenas curtas, uma geração de vídeo por vez.
12. Se não tiver certeza, criar relatório e pedir validação antes de alterar algo sensível.

## Variáveis de ambiente obrigatórias
Configurar sempre que executar scripts:
- PIP_CACHE_DIR=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\pip
- HF_HOME=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\huggingface
- TORCH_HOME=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\torch
- XDG_CACHE_HOME=K:\AI_VIDEO_COMMERCIAL_STUDIO\cache
- TEMP=K:\AI_VIDEO_COMMERCIAL_STUDIO\temp
- TMP=K:\AI_VIDEO_COMMERCIAL_STUDIO\temp
- OLLAMA_MODELS=K:\AI_VIDEO_COMMERCIAL_STUDIO\models\ollama
- GIT_PYTHON_GIT_EXECUTABLE=K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\Library\bin\git.exe

## Stack inicial
- UI: Gradio.
- Backend: Python modular. FastAPI opcional se necessário para API/WebSocket.
- Banco local: SQLite.
- Jobs: fila local no MVP; depois Redis/RQ se viável.
- Vídeo IA: WanGP/Wan2GP 1.3B como motor principal.
- Motor experimental: FramePack.
- Montagem: FFmpeg como prioridade.
- Fallback: storyboard estático com imagem + texto + narração + FFmpeg.
- LLM local: Ollama, se disponível; fallback por templates determinísticos.
- TTS: começar com placeholder ou pyttsx3/offline; depois Kokoro/Coqui se viável.

## Arquitetura alvo
Fluxo: Briefing -> Roteiro -> Cenas -> Prompts -> Assets -> Render de cenas -> Montagem FFmpeg -> MP4 final.

Pastas por projeto:
projects\YYYYMMDD_HHMMSS_nome
  brief\
  script\
  prompts\
  storyboard\
  renders\
  audio\
  final\
  logs\
  project.json

## Padrão de implementação
- Primeiro crie um MVP mock funcional.
- Depois integre motores reais por adaptadores.
- Nunca acople diretamente UI ao WanGP; use services/adapters.
- Todo comando de render deve ser reproduzível e salvo em logs.
- Toda cena deve ter ID, duração, prompt positivo, prompt negativo, status e caminho de saída.
- Deve ser possível refazer apenas uma cena.

## Padrão de resposta do agente
Ao terminar uma tarefa, sempre informar:
1. arquivos criados/alterados;
2. comandos executados;
3. riscos encontrados;
4. como testar;
5. próximo comando recomendado.
