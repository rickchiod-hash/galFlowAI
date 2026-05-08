# Fluxo de Implementação GalFlowAI — Status e Revisão

## Comando para Revisar e Executar em Ordem:
```
powershell -Command "& 'K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\scripts\revisar_fluxo.ps1'"
```

---

## Mapeamento de Etapas (em ordem)

| # | Etapa | Status | Validação | Pode Pular? |
|---|--------|--------|-------------|---------------|
| 1 | `/inicio` | ✅ 100% | Auditoria concluída, relatório em `docs/RELATORIO_ANALISE_AMBIENTE.md` | Sim |
| 2 | `/analise` | ✅ 100% | Relatório de análise criado e validado | Sim |
| 3 | `/fundacao` | ✅ 100% | Estrutura `app/`, `scripts/`, `config.py`, `hardware.py` criados | Sim |
| 4 | `/ui` | ✅ 100% | Interface GalFlowAI em português, Gradio Blocks, título "GalFlowAI" | Sim |
| 5 | `/projeto` | ✅ 100% | `project_manager.py` funcionando, pastas em K: | Sim |
| 6 | `/roteiro` | ✅ 100% | `script_generator.py` funcionando | Sim |
| 7 | `/storyboard` | ✅ 100% | `scene_splitter.py`, `prompt_builder.py` funcionando | Sim |
| 8 | `/ffmpeg` | ✅ 100% | `ffmpeg_adapter.py` criado, storyboard funcionando | Sim |
| 9 | `/fila` | ✅ 100% | `app/jobs/queue.py` criado, JobQueue funcionando | Sim |
| **10** | **`/wangp`** | ✅ **100% VALIDADO** | **WanGP adapter criado, 1.3B seguro para GTX 1660** | **Não** |
| 11 | `/tts` | 🔄 **Em implementação** | Narração offline (pyttsx3/Kokoro) | Não |
| 12 | `/testes` | ⏳ Pendente | Test suite (`tests/`) | Não |
| 13 | `/docs` | ⏳ Pendente | Documentação em português (`README.md`) | Não |
| 14 | `/qa` | ⏳ Pendente | Validação final, aceite | Não |

---

## Etapa 10: `/wangp` — ✅ 100% VALIDADO

**Objetivo:** Integrar WanGP/Wan2GP como motor de vídeo seguro (1.3B, 480p/512p).

**Critérios atingidos:**
1. ✅ `app/adapters/wangp_adapter.py` criado
2. ✅ Adapter verifica existência de `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP`
3. ✅ Preset 1.3B forçado para GTX 1660 Super (6GB VRAM)
4. ✅ Uma cena por vez (lock de GPU)
5. ✅ Fallback para FFmpeg se WanGP falhar
6. ✅ Não quebra WanGP existente
7. ✅ Logs em português

**Arquivos criados/alterados:**
- `app/adapters/wangp_adapter.py` (novo)
- `state/FLUXO_STATUS.md` (atualizado)

---

## Nome do App
- **GalFlowAI** (confirmado, não "GalFlow AI" nem "GalFlowAI")
- Interface título: `GalFlowAI`
- Janela: `http://127.0.0.1:7860`

---

## Como Testar Após Cada Etapa:
1. Execute: `scripts\start_app.bat`
2. Acesse: `http://127.0.0.1:7860`
3. Crie um comercial automático com briefing de teste
4. Verifique se pastas são criadas em `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\projects`
5. Confirme que nenhum arquivo vai para C:
6. Valide logs em `logs/`

---

**Status atual:** Iniciando `/tts` (Text-to-Speech)...
