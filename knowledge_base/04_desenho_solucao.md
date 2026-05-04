# Desenho de solução

Usuário -> Gradio UI -> Orquestrador Python -> Services -> Adapters -> Storage K:

Fluxo:
1. Briefing
2. Geração de roteiro
3. Split de cenas
4. Prompts por cena
5. Render ou importação de clipes
6. Montagem FFmpeg
7. Exportação final

Componentes:
- app/main.py: sobe Gradio
- app/config.py: paths e variáveis K-only
- app/hardware.py: diagnóstico GPU/RAM/disco/CUDA
- app/project_manager.py: cria e retoma projetos
- app/pipeline/script_generator.py: roteiro
- app/pipeline/scene_splitter.py: cenas
- app/pipeline/prompt_builder.py: prompts positivos e negativos
- app/adapters/wangp_adapter.py: integração WanGP
- app/adapters/ffmpeg_adapter.py: montagem e fallback
- app/adapters/tts_adapter.py: voz
- app/jobs/queue.py: fila local ou RQ
- app/logging_config.py: logs
