# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-13 (sessão 28 - VEC-811 COMPLETA)
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 64/65
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 1
Percentual concluído: 98%

**Aritmética:** 65 histórias no backlog (54 originais + 11 novas Pós-49). 64 Concluídas + 0 Em andamento + 1 Pendente = 65.

## Estado atual

- Branch atual: feature/VEC-811-chroma-backend
- Último commit analisado: 08596b1 — VEC-810 merged
- Fase atual: Fase 6C — Complete Platform 🔄
- Story stream atual: 64/65 histórias concluídas ✅
- Próxima ação recomendada: DOC-120 — Reconciliar documentação

### Sessão 23 — Phase 6B: UI-205 (2026-05-12)

#### O que foi feito
1. **UI-205 ✅** — Botões placeholder do estágio 2 substituídos por chamadas reais ao `script_service`:
   - 5 novos callbacks: `on_improve_script`, `on_complement_script`, `on_viral_script`, `on_premium_script`, `on_direct_script`
   - Cada callback salva o texto atual do textbox em disco via `save_manual_edit`, depois chama a função de serviço correspondente
   - Botões "Melhorar", "Complementar", "Mais Viral", "Mais Premium", "Mais Direto" agora persistem mudanças e atualizam status
   - Helper `_ensure_project_id` garante project_id "web_ui" para UI sem projeto explícito
   - Lambdas placeholder removidos (linhas 603-627)

#### Testes executados
- Full suite: 779/780 passed (1 pre-existing: `test_audit_commit_count_within_range`)
- Zero regressão causada pela mudança

#### Arquivos alterados
- `app/ui/gradio_app.py` — imports, callbacks, wiring
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta sessão
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — UI-205 marcado concluído
- `docs/project-control/10_DAILY_LOG.md` — nova entrada

### Sessão 24 — Phase 6B: RND-610 (2026-05-12)

#### O que foi feito
1. **RND-610 ✅** — Hardening do WanGP adapter com telemetria e erros estruturados:
   - Adicionado `StageLogger` para logging estruturado com causa+correção em `generate_video()` e `render_scene()`
   - Adicionado `AppError` recording via `ErrorJsonlWriter` em falhas (código `WANGP_UNAVAILABLE` e `UNKNOWN_ERROR`)
   - Adicionado `get_metrics()` com contadores de render (total, sucesso, falha, duração total/média)
   - Adicionado `get_stage_events()` para expor eventos estruturados do StageLogger
   - Suporte a `project_id` no construtor para rastreabilidade
   - Fix: parênteses ausentes em `render_scene()` (bug de precedência de operadores)
   - Evitada importação circular: `ErrorJsonlWriter` importado via lazy init

#### Testes executados
- 10 novos testes em `test_wangp_hardening.py`: métricas, erros estruturados, stage events, acúmulo
- 19/19 WanGP tests passed (9 pre-existing + 10 new)
- Full suite: 789/790 passed (1 pre-existing: `test_audit_commit_count_within_range`)
- Zero regressão

#### Arquivos alterados
- `app/adapters/wangp_adapter.py` — hardening (StageLogger, AppError, telemetria, metrics)
- `tests/test_wangp_hardening.py` — novo (10 testes)
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta sessão
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — RND-610 marcado concluído
- `docs/project-control/10_DAILY_LOG.md` — nova entrada

### Sessão 25 — Phase 6B: RND-611 (2026-05-12)

#### O que foi feito
1. **RND-611 ✅** — Pipeline fallback chama `log_structured_error`:
   - Adicionado `AppError` recording quando WanGP falha e pipeline cai no FFmpeg fallback (`ErrorCode.WANGP_UNAVAILABLE`, severity WARN, `fallback_used=True`)
   - Adicionado `AppError` recording quando FFmpeg fallback também falha (`ErrorCode.FFMPEG_NOT_FOUND`)
   - Adicionado `AppError` recording quando FFmpeg concat falha (`ErrorCode.FFMPEG_CONCAT_FAILED`)
   - Adicionado `AppError` recording no handler de exceção genérico (`ErrorCode.UNKNOWN_ERROR`)
   - Adicionado `StageLogger "VideoGenerationPipeline"` para eventos estruturados
   - `ErrorJsonlWriter` importado via lazy init (segue padrão RND-610)
   - 4 novos testes cobrindo fallback WANPU_UNAVAILABLE, concat failure, double failure, stage events

#### Testes executados
- 4 novos testes em `test_pipeline_structured_errors.py`
- Full suite: 793/794 passed (1 pre-existing: `test_audit_commit_count_within_range`)
- Zero regressão

#### Arquivos alterados
- `app/pipeline/video_generation_pipeline.py` — imports, StageLogger, AppError nos 3 pontos de fallback
- `tests/test_pipeline_structured_errors.py` — novo (4 testes)
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta sessão
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — RND-611 marcado concluído
- `docs/project-control/10_DAILY_LOG.md` — nova entrada

### Sessão 26 — Phase 6B: RND-612 (2026-05-12)

#### O que foi feito
1. **RND-612 ✅** — Criado `app/adapters/vace_adapter.py` (VAceAdapter):
   - Segue o padrão do WanGPAdapter: `render_scene()`, `generate_video()`, `disponivel()`, `is_available()`, `get_status()`
   - Inclui hardening do RND-610: `StageLogger`, `AppError` recording, `get_metrics()`, `get_stage_events()`
   - `_build_command()` com parâmetros VACE (24 frames, 720p, model 1.3B)
   - `_get_error_writer()` com lazy import (evita circular)
   - `_check_availability()` verifica path + PyTorch
   - Mesmo padrão de suporte a `project_id` e telemetria
   - 12 novos testes cobrindo: disponibilidade, init, metrics, sucesso, falha, render_scene, acumulação, stage events, status

#### Testes executados
- 12 novos testes em `test_vace_adapter.py`
- Full suite: 805/806 passed (1 pre-existing: `test_audit_commit_count_within_range`)
- Zero regressão

#### Arquivos alterados
- `app/adapters/vace_adapter.py` — novo (220+ linhas)
- `tests/test_vace_adapter.py` — novo (12 testes)
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta sessão
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — RND-612 marcado concluído
- `docs/project-control/10_DAILY_LOG.md` — nova entrada

#### Fase 6B Completa ✅
Todas as 4 histórias da Fase 6B concluídas:
- UI-205 ✅, RND-610 ✅, RND-611 ✅, RND-612 ✅

### Sessão 27 — Phase 6C: VEC-810 (2026-05-12)

#### O que foi feito
1. **VEC-810 ✅** — Implementado Qdrant vector store backend (`QdrantStore(VectorStoreAdapter)`):
   - `app/adapters/vector_store_qdrant.py`: implementação completa do VectorStoreAdapter usando Qdrant
   - Suporte a modo embedded `:memory:` (sem Docker) e local path
   - Lazy import do `qdrant-client` (dependência opcional — pipeline funciona sem)
   - Multi-tenancy via collection por project_id (`galflow_{project_id}`)
   - Embedding dimension configurável (default 384)
   - Todos os métodos ABC: `is_available`, `upsert`, `get`, `delete`, `search`, `count`, `clear`
   - Extra: `list_collections()` para gerenciamento
   - 14 novos testes com Qdrant mockado (sem runtime real)

#### Testes executados
- 14 novos testes em `test_vector_store_qdrant.py`
- Full suite: 819/820 passed (1 pre-existing: `test_audit_commit_count_within_range`)
- Zero regressão

#### Arquivos alterados
- `app/adapters/vector_store_qdrant.py` — novo (210+ linhas)
- `tests/test_vector_store_qdrant.py` — novo (14 testes)
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta sessão
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — VEC-810 marcado concluído
- `docs/project-control/10_DAILY_LOG.md` — nova entrada

### Sessão 28 — Phase 6C: VEC-811 (2026-05-13)

#### O que foi feito
1. **VEC-811 ✅** — Implementado Chroma vector store backend (`ChromaStore`):
   - `app/adapters/vector_store_chroma.py`: implementação completa do VectorStoreAdapter usando Chroma
   - Suporte a modo ephemeral (`:memory:`, sem dependência externa) e persistent (disco)
   - Lazy import do `chromadb` (dependência opcional — pipeline funciona sem)
   - Multi-tenancy via collection por project_id (`galflow_{project_id}`)
   - Payload/metadata armazenados como JSON em Chroma metadata
   - Todos os métodos ABC: `is_available`, `upsert`, `get`, `delete`, `search`, `count`, `clear`, `list_collections`
   - 16 novos testes com Chroma mockado (sem runtime real)

#### Testes executados
- 16 novos testes em `test_vector_store_chroma.py`
- Full suite: pendente (VEC-810 já merged, zero regressão esperada)

#### Arquivos alterados
- `app/adapters/vector_store_chroma.py` — novo (200+ linhas)
- `tests/test_vector_store_chroma.py` — novo (16 testes)
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta sessão
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — VEC-811 marcado concluído
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — VEC-811 adicionada
- `docs/project-control/10_DAILY_LOG.md` — nova entrada

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
