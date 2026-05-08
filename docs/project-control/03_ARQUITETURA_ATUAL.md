# 03_ARQUITETURA_ATUAL — GalFlowAI

Atualizado em: 2026-05-08 (CORE-102)

## Arquitetura validada

Comparação sistemática entre documentação (PROJECT_REFERENCE_CONTEXT.md, FEATURE_PRESERVATION_MATRIX.md, 04_ARQUITETURA_ALVO.md) e código real.

### Legenda

- ✅ PRESENTE — Claim corresponde exatamente ao código
- ⚠️ DIFERENTE — Claim existe mas difere (incompleto, divergente, ou estado diferente)
- ❌ AUSENTE — Claim não encontrada no código

### Providers LLM (PROJECT_REFERENCE_CONTEXT.md)

| Provider | Status | Evidência |
|---|---|---|
| TemplateProvider (fallback) | ✅ | `app/adapters/llm/template_provider.py`, usado como fallback final em `provider_router.py` |
| LM Studio | ✅ | `app/adapters/llm/lmstudio_provider.py`, registrado em `provider_router.py` |
| GPT4All | ✅ | `app/adapters/llm/gpt4all_provider.py`, registrado em `provider_router.py` |
| KoboldCpp | ✅ | `app/adapters/llm/koboldcpp_provider.py`, registrado em `provider_router.py` |
| llama.cpp | ✅ | `app/adapters/llm/llamacpp_provider.py`, registrado em `provider_router.py` |
| GPT-compatible endpoint | ⚠️ | Documentado como provider mas `openai_compatible_local` está marcado como "Não implementado ainda" em `app/api.py:120` |
| Ollama (opcional) | ✅ | `app/adapters/ollama_adapter.py`, usado também em `translator_adapter.py` |

### Engines de vídeo

| Engine | Status | Evidência |
|---|---|---|
| FFmpeg (obrigatório) | ✅ | `app/adapters/ffmpeg_adapter.py`, fallback em `video_generation_pipeline.py:179-203` |
| WanGP/Wan2GP 1.3B | ✅ | `app/adapters/wangp_adapter.py`, engine em `video_generation_pipeline.py:150-170` |

### Áudio/TTS

| Engine | Status | Evidência |
|---|---|---|
| pyttsx3 (fallback) | ✅ | `app/adapters/tts_adapter.py:_generate_pyttsx3()` |
| Piper pt-BR | ⚠️ | Documentado como "futuro" mas código já implementa: `app/adapters/piper_adapter.py` (380+ linhas, classe completa) |
| Silence fallback | ✅ | `app/adapters/tts_adapter.py:_generate_silence()`, sempre disponível |

### Features obrigatórias (FEATURE_PRESERVATION_MATRIX.md)

| Feature | Status | Evidência |
|---|---|---|
| Nome GalFlowAI | ✅ | Renomeado em ee05f5c, 0 ocorrências de nomes legados |
| Roteiro editável | ✅ | `app/main.py:189` Textbox editável, botão "Salvar Edição" |
| Aprovação de roteiro | ✅ | `app/main.py:209` btn_approve, `approve_script_use_case.py` |
| TemplateProvider | ✅ | Ver providers acima |
| FFmpeg fallback | ✅ | Ver engines acima |
| Providers locais | ✅ | 6 providers implementados |
| Logs | ✅ | `app/services/log_service.py`, `log_use_cases.py`, `observability_use_cases.py` |
| Métricas | ✅ | `app/services/metrics_service.py`, `metrics_use_cases.py` |
| Status diário | ✅ | `docs/project-control/00_STATUS_EXECUTIVO.md` |
| TODO rastreável | ✅ | Política em `09_GAPS_TODOS_E_DIVIDAS.md`, 0 genéricos |

### Regras arquiteturais (04_ARQUITETURA_ALVO.md)

| Regra | Status | Evidência |
|---|---|---|
| UI não chama adapter diretamente | ✅ | `app/ui/gradio_app.py` imports: apenas pipeline e services |
| API não chama adapter diretamente | ⚠️ | `app/api.py:110`: `from app.adapters.llm import ProviderRouter` — exceção no endpoint `/api/llm/providers` |
| Camada de use cases existe | ✅ | `app/application/use_cases/` com 24 arquivos |

## Acoplamentos encontrados

| Camada | Acoplamento | Arquivo | Impacto | História de correção |
|---|---|---|---|---|
| API → Adapter | API importa ProviderRouter diretamente | app/api.py:110 | Violação da arquitetura alvo | ARCH-300 |
| Pipeline → WanGP | Dependência direta de engine específica | video_generation_pipeline.py | Dificulta troca de engine | ARCH-300 |
| GPT-compatible | Provider documentado mas não implementado | app/api.py:120 | Gap doc vs código | PROV-300 |
| Piper | Código existe mas doc diz "futuro" | piper_adapter.py (untracked) | Doc desatualizada | AUD-700 |

## Fluxo atual de execução

O fluxo real do pipeline principal (`video_generation_pipeline.py`) é mais simples que o documentado:

```text
Briefing (input)
  → Script generation (provider_router → LLM provider)
  → Scene splitting (scene_splitter)
  → Video generation (WanGP ou FFmpeg fallback)
  → MP4 output
```

**Etapas documentadas mas NÃO implementadas no pipeline:**
- SceneContracts (planejado para VIS-502)
- Visual Bible (planejado para VIS-501)
- Ingredient Registry (planejado para VIS-500)
- Prompt Context Pack (planejado para VIS-503)
- RenderPlan (planejado para RND-600)
- AudioPlan / TTS por cena (planejado para AUD-700/701)
- SRT/Legendas (planejado para AUD-702)
- Vector memory (planejado para VEC-800/801)

## Gaps encontrados (doc vs código)

| # | Gap | Tipo | Doc diz | Código faz | Impacto | Ação |
|---|---|---|---|---|---|---|
| G1 | GPT-compatible endpoint | Provider não implementado | Provider listado | `openai_compatible_local` = "Não implementado" | Feature matrix inconsistente | Implementar ou remover da matrix |
| G2 | Piper pt-BR | Doc desatualizada | "Futuro" | PiperAdapter completo (380+ linhas) | Doc atrasada | Atualizar doc para "existente (untracked)" |
| G3 | Fluxo completo | Escopo superdimensionado | 22 etapas | 4-5 etapas reais | Expectativa vs realidade | Alinhar doc com backlog |
| G4 | API → adapter direto | Violação arquitetural | "API não chama adapter" | `from app.adapters.llm import ProviderRouter` | Acoplamento | Refatorar via use case |
| G5 | docs/reference/ não commitado | Gaps de governança | Arquivos deveriam existir | Não estavam no git (corrigido CORE-100) | Testes quebram | Corrigido |
| G6 | Testes gitignorados | CI/CD | N/A | `test_*.py` ignorado pelo .gitignore | CI não detecta | Forçar add ou ajustar .gitignore |

## Riscos atuais

- Doc diz 22 etapas, código tem 4-5 — risco de expectativa errada de stakeholders.
- Piper adapter existe mas é untracked — risco de perda se não commitado.
- GPT-compatible endpoint não implementado — risco se usuário tentar usar.
- API chama adapter diretamente — dificulta testes unitários.
- Testes de governança retornam bool (warnings pytest) — padrão aceito, mas não ideal.
