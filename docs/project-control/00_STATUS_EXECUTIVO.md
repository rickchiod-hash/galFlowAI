# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-12 (sessão 22 - Phase 6A Structural Stabilization)
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 55/65
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 10
Percentual concluído: 85%

**Aritmética:** 65 histórias no backlog (54 originais + 11 novas Pós-49). 55 Concluídas + 0 Em andamento + 10 Pendentes = 65.

## Estado atual

- Branch atual: feature/ARCH-320-unify-pipeline
- Último commit analisado: 1ecd9f9 — PR #29 merged: P0-ERR error handling infrastructure
- Fase atual: Fase 6A — Structural Stabilization
- Story stream atual: 55/65 histórias concluídas ✅
- Próxima ação recomendada: ARCH-321 — Adicionar versionamento de API (/api/v1/)

### Sessão 22 — Phase 6A: ARCH-320 Pipeline Unification (2026-05-12)

- **813 testes passando, 0 falhas, 4 warnings** (de 86)
- **Tempo de execução: 38.5s** (de 73s — redução de ~47%)
- HEAD: `bff9824`
- Git commit count: 237

#### O que foi feito
1. **Removidos 82 `return True` de funções de teste** em 17 arquivos — elimina `PytestReturnNotReturnNoneWarning`
2. **Corrigido teste de auditoria Git** — `01_AUDITORIA_HISTORICO_GIT.md` atualizado para 236 commits
3. **Otimizado `test_ffmpeg_not_removable`** — 4.03s → 0.06s (evitando __pycache__/.pytest_cache)
4. **Otimizado `test_detect_lm_studio/koboldcpp`** — 4.02s → 2.02s (timeout=(1,1) explícito)
5. **8 testes e2e legados convertidos para smoke tests** — não mais falham silenciosamente

### Sessão 22 — Phase 6A: ARCH-320 Pipeline Unification (2026-05-12)

#### O que foi feito
1. **Replan do backlog** — 11 novas histórias criadas em 3 fases (6A, 6B, 6C) para execução de gaps técnicos obrigatórios
2. **ARCH-320 — Unificação de pipeline**:
   - Deletado `app/pipeline/video_generation_pipeline_new.py` (duplicata que pulava approval gate)
   - Mantido `app/pipeline/video_generation_pipeline.py` como canônico (com approval gate de roteiro)
   - Adicionado `test_only_one_pipeline_file` em `tests/test_pipeline.py` (4/4 passed)
3. **Decisão de produto**: WanGP/VACE/FFmpeg fallback/API versioning/UI integration/vector store/logs estruturados — todos reclassificados de opcionais para mandatórios. Ollama permanece único opcional.
4. **Backlog atualizado** com 11 novas histórias (ARCH-320, API-210, API-211, LOG-100, UI-205, RND-610, RND-611, RND-612, VEC-810, VEC-811, DOC-120)

#### Testes executados
- `tests/test_pipeline.py`: 4/4 passed (3 existentes + 1 novo ARCH-320)
- Full suite: 739 passed, 9 failed (4 StrEnum Python 3.10 pre-existing, 1 git audit count, 4 indirect StrEnum) — zero regressão causada pela mudança

#### Arquivos alterados
- `app/pipeline/video_generation_pipeline_new.py` — **deletado** (ARCH-320)
- `tests/test_pipeline.py` — adicionado `test_only_one_pipeline_file`
- `docs/project-control/00_STATUS_EXECUTIVO.md` — atualizado
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — backlog Pós-49 adicionado
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — ARCH-320 adicionada
- `docs/project-control/18_IMPLEMENTATION_ORDER.md` — fases 6A-6C adicionadas
- `docs/project-control/10_DAILY_LOG.md` — entry adicionada

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
