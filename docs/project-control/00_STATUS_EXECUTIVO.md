# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-12 (sessão 22 - Phase 6A COMPLETA)
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 58/65
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 7
Percentual concluído: 89%

**Aritmética:** 65 histórias no backlog (54 originais + 11 novas Pós-49). 58 Concluídas + 0 Em andamento + 7 Pendentes = 65.

## Estado atual

- Branch atual: feature/LOG-100-structured-errors-ui
- Último commit analisado: 045734e — API-211 + LOG-100
- Fase atual: Fase 6A — Structural Stabilization ✅ **COMPLETA**
- Story stream atual: 58/65 histórias concluídas ✅
- Próxima ação recomendada: Fase 6B — UI-205 (substituir botões placeholder stage 2)

### Sessão 22 — Phase 6A: ARCH-320 + API-210 + API-211 + LOG-100 (2026-05-12)

#### O que foi feito
1. **Replan do backlog** — 11 novas histórias em 3 fases (6A, 6B, 6C)
2. **ARCH-320 ✅** — Unificação de pipeline (deletado `_new.py`, mantido canônico com approval gate)
3. **API-210 ✅** — Prefixo `/api/v1/` em todas as 44 rotas REST + WebSocket
4. **API-211 ✅** — `/api/v1/llm/providers` envelopado em `ApiResponse` (antes raw dict)
5. **LOG-100 ✅** — Erros estruturados na UI:
   - Dataframe expandido para 9 colunas (+code, stage, retryable, fallback_used)
   - Nova aba "Erros Estruturados" com filtro de severidade
   - Sumário de logs inclui `total_structured_errors`

#### Decisão de produto
WanGP, VACE, FFmpeg fallback, API versioning, UI integration, vector store, logs estruturados — todos **mandatórios**. Ollama permanece único opcional.

#### Testes executados
- API (test_api + test_h10_contract): 20/21 passed (1 pre-existing: script.txt cache)
- Pipeline (test_pipeline): 4/4 passed
- Zero regressão causada pelas mudanças

#### Arquivos alterados (fase 6A completa)
- `app/pipeline/video_generation_pipeline_new.py` — deletado
- `app/api.py` — routes prefix + providers envelope
- `app/ui/gradio_app.py` — logs Dataframe expandido + aba Erros Estruturados
- `tests/test_pipeline.py`, `tests/test_api.py`, `tests/test_h10_contract.py`
- `docs/project-control/00_STATUS_EXECUTIVO.md`, `05_BACKLOG_PRIORIZADO.md`, `06_HISTORIAS_REFINADAS.md`, `18_IMPLEMENTATION_ORDER.md`, `10_DAILY_LOG.md`

## Resumo tipo Daily

### O que foi feito

- **Fase 1 — Antirregressão documental: COMPLETA** ✅ (GOV-001..006, 6 histórias)
  - GOV-001: Sistema de checkpoint diário, test_checkpoint.py (3 testes)
  - GOV-002: Fonte de verdade do produto (PROJECT_REFERENCE_CONTEXT.md), test_product_context.py (4 testes)
  - GOV-003: Feature Preservation Matrix, test_feature_matrix.py (5 testes)
  - GOV-004: TODOs rastreáveis, test_todo_policy.py (4 testes, 0 genéricos)
  - GOV-005: ADR obrigatório, test_adr_policy.py (3 testes)
  - GOV-006: AGENTS.md + SKILL.md, test_agents.py (4 testes)
- **Gap corrigido**: docs/reference/ (PROJECT_REFERENCE_CONTEXT.md, FEATURE_PRESERVATION_MATRIX.md, EXTERNAL_REFERENCES.md) não estava commitado — copiado do governance pack e adicionado ao git.
- **CORE-100 ✅**: Auditoria do histórico Git completa.
  - 01_AUDITORIA_HISTORICO_GIT.md atualizado: 132 commits, HEAD 63839e7, tabelas de marcos e arquivos deletados, 7 perguntas obrigatórias respondidas
  - test_git_audit.py: 5 testes (existence, sections, git evidence, questions, commit count)
- **CORE-101 ✅**: Mapa atual do projeto completo.
  - 02_MAPA_ATUAL_DO_PROJETO.md: tecnologias, estrutura de diretórios, entrypoints, riscos
  - test_project_map.py: 5 testes (existence, sections, technologies, entrypoints, feature matrix ref)
- **CORE-102 ✅**: Validação doc vs código completa.
  - 03_ARQUITETURA_ATUAL.md reescrito: 22 claims validadas, 16 PRESENTE, 5 DIFERENTE
  - 6 gaps documentados (G1-G6): GPT-compatible não implementado, Piper doc desatualizada, fluxo irreal, API→adapter direto, docs/reference gap, testes gitignorados
  - test_doc_code_gap.py: 5 testes (existence, sections, providers, gaps, gap patterns)
- **Fase 2 — Diagnóstico e recuperação: COMPLETA** ✅ (3 histórias)
- **UI-200 ✅**: Fluxo por etapas documentado.
  - 19_STORY_MAP.md reescrito — 7 etapas com gates, story map, 5 regras
  - test_story_map.py: 5 testes (existence, step flow, steps, gates, rules)
- **43 testes de governança passando** (10 histórias): checkpoint (3), product_context (4), feature_matrix (5), todo_policy (4), adr_policy (3), agents (4), git_audit (5), project_map (5), doc_code_gap (5), story_map (5)
- **QA-1000 ✅**: Teste antirregressão de naming completo.
  - `tests/test_naming_regression.py` criado com 5 testes
  - Legacy names removidos de 15+ source files (gradio_app.py, api.py, application/*, metrics_service.py, tests/*)
  - Legacy names removidos de 30+ .md files (docs, knowledge_base, prompts, qa, stories, project-control)
  - Teste ajustado para ignorar self-reference, session-ses, temp_backup, PROJECT_REFERENCE_CONTEXT
  - Encoding fix: subprocess usa encoding=utf-8, errors=replace
  - **5/5 testes passando**
- **QA-1001 ✅**: Teste de presença de providers/fallbacks completo.
   - `tests/test_provider_presence.py` criado com 8 testes
   - Verifica: todos os 5 LLM providers existem (Template, LM Studio, KoboldCpp, LlamaCpp, GPT4All)
   - Verifica: ProviderRouter referencia TemplateProvider como fallback
   - Verifica: TTSAdapter tem silence fallback
   - Verifica: FFmpegAdapter é fallback de vídeo (WanGP primário)
   - Verifica: FEATURE_PRESERVATION_MATRIX.md contém entradas obrigatórias
   - **8/8 testes passando**
- **QA-1004 ✅**: Teste TTS falha → export sem áudio completo.
   - `tests/test_tts_fallback.py` criado com 5 testes (file existence, silence fallback, TTS unavailable, TTS available, both unavailable)
   - Mocks para adapters e serviços (TTSAdapter, WanGPAdapter, FFmpegAdapter, script_service)
   - **5/5 testes passando**

### O que foi feito nesta sessão (Sessão 7 — AUD-700 + RND-601)

- **AUD-700 ✅ + RND-601 ✅ + UI tab reorder ✅:**
  - `AudioPlan` schema em `app/domain/audio_plan.py` — NarrationEntry, AudioPlanStatus, versioning, UUID
  - `AudioPlanService` — CRUD dict-backed, add/remove/update narration, generate_narration_script() -> Markdown
  - 41 novos testes em `tests/test_audio_plan.py` (NarrationEntry, AudioPlan, Service, Narrations, Script generation)
  - RND-601: 15 testes FFmpeg fallback universal em `tests/test_ffmpeg_fallback.py`
  - UI: Gradio tab reorder — "Roteiro" como primeira aba
  - 263/263 testes passando (0 falhas)
- **Próxima recomendada:** AUD-701 (Gerar áudio por cena com fallback)

### O que foi feito nesta sessão (Sessão 8 — AUD-701)

- **AUD-701 ✅:** TTSAudioService em `app/services/tts_audio_service.py`:
  - `generate_scene_audio(plan, output_dir)` — gera WAV por cena a partir de AudioPlan
  - `get_audio_map(results)` — dict {scene_number: path or None}
  - Fallback silencioso: excecao/falha nao bloqueia
  - 19 testes (success, failure, mixed, empty, get_audio_map)
  - 282/282 testes passando (0 falhas)
- **Próxima recomendada:** AUD-702 (Gerar SRT por timing de cena)

### Estado atual

- **Branch atual:** master (a68ceeb)
- **Fase:** Fase 5 (Pipeline e produto)
- **Histórias concluídas:** 30/49 (61,2%)
- **Próxima recomendada:** AUD-701 (ordem 33) — Gerar áudio por cena com fallback

### Bloqueios

- Nenhum.

### Riscos

- Agente implementar antes de documentar.
- Agente marcar como concluído sem teste.
- Agente remover provider/fallback validado.
- Agente confundir documentação planejada com feature implementada.

### Gaps encontrados nesta sessão

- `app/application/use_cases/script_generation.py` passava `provider` como `mode` para `generate_script_with_llm` — provider explícito era ignorado.
- `app/adapters/llm/gpt4all_provider.py` tinha path hardcoded com typo (`COMERCIAL` em vez de `COMMERCIAL`).
- Ambos corrigidos nesta sessão.

### TODOs rastreáveis

- Nenhum TODO/FIXME/HACK/XXX encontrado em app/ ou tests/.

### Arquivos alterados nesta sessão

- `app/services/tts_audio_service.py` — Novo: TTSAudioService (AUD-701)
- `tests/test_tts_audio_service.py` — Novo: 19 testes (AUD-701)

### Comandos executados

- `pytest tests/test_tts_audio_service.py -v` — 19/19 passed
- `pytest (core domains: 9 arquivos)` — 282/282 passed

### Evidências usadas

- Commit base: 0b175c2 (início da sessão)
- Branch: feature/AUD-701-tts-audio-service -> merged to master (140fb6e)
- Testes: 282/282 passando (0 falhas)
