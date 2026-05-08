# 02_MAPA_ATUAL_DO_PROJETO — GalFlowAI

Atualizado em: 2026-05-08 (CORE-101)

## Raiz real do projeto

- Caminho: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta` (runtime, COMERCIAL com acento)
- Caminho git: `K:\AI_VIDEO_COMMERCIAL_STUDIO\opencodegalpasta` (COMMERCIAL sem acento)
- Evidência: `.git` presente, `app/` com código fonte, `tests/` com 23+ testes
- Branch: master
- HEAD: 63839e7 (132 commits, 5 dias de desenvolvimento)

## Tecnologias detectadas

| Tecnologia | Evidência | Papel | Risco |
|---|---|---|---|
| Python 3.12 | app/*.py, requirements implícito | Lógica principal | Baixo |
| Gradio | app/ui/gradio_app.py, app/main.py | UI principal | Médio (sintaxe complexa) |
| FastAPI | app/api.py | API REST | Baixo |
| FFmpeg | app/adapters/ffmpeg_adapter.py | Montagem/fallback de vídeo | Médio (caminhos Windows) |
| WanGP | app/adapters/wangp_adapter.py | Engine de vídeo IA opcional | Alto (VRAM 6GB) |
| TTS (pyttsx3) | app/adapters/tts_adapter.py | Narração TTS fallback | Baixo |
| Piper | app/adapters/piper_adapter.py (untracked) | TTS pt-BR futuro | Médio (não commitado) |
| Template | app/adapters/llm/template_provider.py | Fallback de roteiro | Baixo |
| LM Studio | app/adapters/llm/lmstudio_provider.py | Provider LLM opcional | Médio |
| GPT4All | app/adapters/llm/gpt4all_provider.py | Provider LLM opcional | Médio |
| KoboldCpp | app/adapters/llm/koboldcpp_provider.py | Provider LLM opcional | Médio |
| LlamaCpp | app/adapters/llm/llamacpp_provider.py | Provider LLM opcional | Médio |
| Ollama | app/adapters/ollama_adapter.py | Provider LLM opcional | Baixo |
| Framepack | app/adapters/framepack_adapter.py | Processamento de frames | Baixo |
| Translator | app/adapters/translator_adapter.py | Tradução de roteiro | Baixo |
| pytest | tests/*.py | Testes | Baixo |
| SQLite | app/pipeline/job_state.py (untracked) | Job ledger futuro | Médio (não commitado) |

## Estrutura de diretórios

```
app/
├── adapters/
│   ├── llm/               # 6 providers + router + strategy
│   ├── ffmpeg_adapter.py
│   ├── framepack_adapter.py
│   ├── ollama_adapter.py
│   ├── piper_adapter.py (untracked)
│   ├── translator_adapter.py
│   ├── tts_adapter.py
│   └── wangp_adapter.py
├── application/
│   └── use_cases/         # 20+ use cases
├── assets/
│   └── asset_manager.py
├── jobs/
│   └── queue.py
├── pipeline/
│   ├── stages/            # 6 stages (audio, prompt, scene, script, text, video)
│   ├── checkpoint_manager.py (untracked)
│   ├── filesystem_helper.py (untracked)
│   ├── job_state.py (untracked)
│   ├── prompt_builder.py
│   ├── scene_splitter.py
│   ├── script_generator.py
│   ├── video_generation_pipeline.py
│   └── voice_script_optimizer.py (untracked)
├── services/
│   ├── log_service.py
│   ├── metrics_service.py
│   ├── script_service.py
│   ├── tts_service.py
│   └── video_service.py
├── ui/
│   └── gradio_app.py
├── utils/
│   └── timeout_retry.py (untracked)
├── api.py
├── config.py
├── config_models.py
├── exceptions.py
├── hardware.py
├── logging_config.py
├── main.py
├── project_manager.py
└── safety.py
```

## Entrypoints

| Arquivo | Função | Evidência | Observação |
|---|---|---|---|
| run_galFlowAI.py | Iniciar app Gradio | Presente na raiz | Entrada principal |
| app/main.py | Gradio UI + lógica principal | Presente | UI principal com tabs |
| app/api.py | FastAPI endpoints | Presente | 20+ endpoints REST |
| app/ui/gradio_app.py | Módulo Gradio separado | Presente | UI modular |
| scripts/start_*.bat | BATs de inicialização | Vários scripts | Config env vars |

## Estado das features obrigatórias

Ver `docs/reference/FEATURE_PRESERVATION_MATRIX.md` como checklist completo.

Resumo:
- 10 features obrigatórias listadas (Nome, Roteiro, Aprovação, TemplateProvider, FFmpeg, Providers, Logs, Métricas, Status, TODO)
- 6 features P1 (SceneContracts, Visual Bible, Ingredient Registry, RenderPlan, AudioPlan, VectorMemory)
- Nenhuma feature obrigatória foi removida no histórico git
- 7 arquivos deletados no total (6 docs antigos + 1 teste duplicado)

## Riscos identificados

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| docs/reference/* .md não commitados | Confirmado | Testes falham | CORE-100 corrigiu: arquivos copiados do pack |
| User's untracked files (6+ arquivos) podem divergir | Alto | Perda de trabalho em andamento | Commitar pendências ou documentar |
| Dual directory (COMERCIAL/COMMERCIAL) drift | Alto | Sincronização quebrada | Sincronizar manualmente a cada alteração |
| python.exe não está no PATH | Confirmado | Scripts BAT falham | Usar env específico |
| Testes de governança em __main__ (não pytest) | Médio | Não coletados automaticamente | Migrar para pytest functions |
