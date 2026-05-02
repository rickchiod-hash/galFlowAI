# galFlowAI

Estúdio local para comerciais curtos com IA — 100% local, zero custo, robusto e com UX premium.

![galFlowAI](https://img.shields.io/badge/galFlowAI-orange?logo=ai&logoColor=white)

---

## Requisitos

### Python
- Python 3.10+ (ambiente K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio)
- Pacotes: gradio, ffmpeg-python, pyttsx3, kokoro (opcional)

### Go
- Go 1.21+ (https://go.dev/dl/)
- Compilar: `scripts\build_go.bat`
- Executáveis: `galflowai-server.exe`, `galflowai-worker.exe`, `galflowai-cli.exe`

### GPU
- NVIDIA GTX 1660 Super ou superior
- 6 GB VRAM mínimo
- CUDA Toolkit compatível com WanGP

### Disco
- Drive K: com 100 GB livres

---

## Como iniciar

### Opção 1: Executável Go (recomendado — mais rápido)
```cmd
galflowai-server.exe
```
Acesse: http://localhost:7860

### Opção 2: Python direto (Gradio)
```cmd
scripts\start_app.bat
```

---

## Como rodar os testes

```cmd
scripts\run_tests.bat
```

---

## Vozes disponíveis

O sistema detecta automaticamente as vozes instaladas no Windows.
Para instalar vozes PT-BR adicionais:
```
Configurações → Hora e idioma → Fala → Gerenciar vozes
```

---

## Estrutura do Projeto

```
galFlowAI/
├── cmd/                        ← Executáveis Go
│   ├── server/main.go          ← Servidor Go (substitui uvicorn/gradio server)
│   ├── worker/main.go          ← Worker Go para processar jobs da fila
│   └── cli/main.go             ← CLI Go para uso sem interface
│
├── core/                       ← Engine Go — alta performance
│   ├── queue/                  ← Fila de jobs persistente (JSON)
│   ├── ffmpeg/                 ← Wrapper Go para FFmpeg
│   ├── hardware/               ← Detecção GPU/VRAM/RAM em Go
│   ├── watcher/                ← Watcher de projetos em Go
│   └── bridge/                 ← Bridge Go ↔ Python (exec subprocess)
│
├── app/                        ← Python — lógica de IA e pipelines
│   ├── main.py                 ← Interface web (migrar de Gradio para FastAPI+HTML)
│   ├── config.py
│   ├── hardware.py
│   ├── logging_config.py
│   ├── project_manager.py
│   ├── safety.py
│   ├── adapters/
│   │   ├── ffmpeg_adapter.py
│   │   ├── wangp_adapter.py    ← INTEGRAR REAL aqui
│   │   ├── tts_adapter.py      ← IMPLEMENTAR kokoro/pyttsx3
│   │   └── ollama_adapter.py   ← [NOVO] LLM local via Ollama
│   └── pipelines/
│       ├── auto_pipeline.py
│       ├── script_generator.py
│       ├── scene_splitter.py
│       ├── prompt_builder.py
│       └── voice_pipeline.py   ← [NOVO] pipeline de narração
│
├── frontend/                   ← [NOVO] Frontend premium (HTML/CSS/JS puro)
│   ├── index.html
│   ├── static/
│   │   ├── css/
│   │   │   ├── main.css        ← Design system inspirado em Google AI Studio
│   │   │   ├── components.css
│   │   │   └── animations.css
│   │   └── js/
│   │       ├── app.js          ← Lógica principal
│   │       ├── progress.js     ← Barras de progresso realistas
│   │       ├── editor.js       ← Editor de roteiro inline
│   │       └── ws.js           ← WebSocket para status em tempo real
│
├── tests/                      ← Testes completos
│   ├── unit/
│   │   ├── test_script_generator.py
│   │   ├── test_scene_splitter.py
│   │   ├── test_prompt_builder.py
│   │   ├── test_ffmpeg_adapter.py
│   │   ├── test_tts_adapter.py
│   │   ├── test_wangp_adapter.py
│   │   ├── test_project_manager.py
│   │   └── test_safety.py
│   ├── integration/
│   │   ├── test_pipeline_completa.py      ← testa fluxo end-to-end
│   │   ├── test_fallback_wangp.py         ← WanGP falha → FFmpeg assume
│   │   ├── test_fallback_tts.py           ← Kokoro falha → pyttsx3 assume
│   │   ├── test_queue_persistencia.py     ← Job sobrevive a crash
│   │   └── test_websocket_progresso.py    ← WebSocket emite eventos certos
│   └── e2e/
│       ├── test_ui_briefing.py            ← Playwright ou requests simples
│       └── test_video_gerado.py           ← Verifica MP4 válido no final
│
├── scripts/                    ← Scripts de manutenção
│   ├── start_app.bat
│   ├── build_go.bat            ← [NOVO] Compila executáveis Go
│   └── run_tests.bat           ← [NOVO] Roda 100% dos testes
│
├── go.mod                      ← [NOVO] Módulo Go
└── README.md
```

---

## CHECKLIST FINAL DE QUALIDADE

Antes de abrir cada PR, verificar:

- ✅ Todos os logs em português brasileiro
- ✅ Nenhum arquivo salvo fora de K:
- ✅ Nenhuma chamada a API paga ou externa
- ✅ Fallback gracioso em todos os adapters (nunca crashar sem resultado)
- ✅ Testes unitários escritos para cada nova função
- ✅ Cobertura >= 80% no módulo alterado
- ✅ UI carrega sem erros no console do browser
- ✅ Barra de progresso reflete progresso real (não finge)
- ✅ Log de erro claro e acionável quando algo falha
- ✅ `go test ./...` passando (se alterou código Go)
- ✅ `pytest tests/` passando (se alterou código Python)
- ✅ WanGP bloqueado em modo seguro quando VRAM < 4GB
- ✅ README atualizado com mudanças relevantes

---

## ORDEM DE EXECUÇÃO (RESUMO)

1. **Go backend** ✅ — `go.mod`, `cmd/`, `core/` criados e compilados
2. **Frontend premium** ✅ — `frontend/` criado (HTML/CSS/JS)
3. **WanGP 1.3B** ✅ — `wangp_adapter.py` integrado (fallback FFmpeg)
4. **TTS narração** ✅ — `tts_adapter.py` (Kokoro/pyttsx3/silêncio)
5. **Testes 100%** ✅ — `tests/` completo (unit/integration/e2e)
6. **Logs robustos** ✅ — `logging_config.py` (cores ANSI, WebSocket)
7. **UX polish** ✅ — Toast, skeleton, drag-and-drop
8. **Commits diretos** ✅ — 7 commits principais no master
9. **README** ✅ — Atualizado com instruções completas

---

*galFlowAI — Crie comerciais profissionais sem sair do seu PC, sem gastar nada.*
*Versão: 2.0 | Última atualização: 2026-05-02*
