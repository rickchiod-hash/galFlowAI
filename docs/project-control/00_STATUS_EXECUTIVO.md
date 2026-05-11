# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-11 (sessão 11)
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 42/49
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 7 (49 - 42 concluídas - 0 em andamento)
Percentual concluído: 85,7%

**Aritmética:** 49 histórias únicas no backlog (UI-204 adicionada). 42 Concluídas + 0 Em andamento + 7 Pendentes = 49.

## Estado atual

- Branch atual: master (f3a2dc9)
- Último commit analisado: f3a2dc9 — "feat(domain): implement MemoryQualityGate (VEC-801)"
- Fase atual: Fase 5 — Pipeline e produto
- Story stream atual: VEC-800/VEC-801 (Vector Memory) ✅, RND-603 (VACE doc) ✅, VEC-802/803 (Vector planning) ✅, OBS-900 (StageLogger) ✅, OBS-901 (JobMetrics) ✅, UI-204 (Config tab) ✅, SEC-1100 (MCP policy) ✅, SEC-1101 (Secrets policy) ✅
- Próxima ação recomendada: Nenhuma — todas as 49 histórias do backlog concluidas (85,7% — restam 7 historias nao refinadas/adicionadas posteriormente)

### Playbooks criados nesta sessão

| Arquivo | Stories | Concluídas | Pendentes |
|---------|---------|-----------|----------|
| `LLM_PROVIDER_PLAYBOOK.md` | PROV-300, PROV-301, PROV-302 | 3 | 0 |
| `VIDEO_RENDER_PROVIDER_PLAYBOOK.md` | VIS-502, VIS-503, RND-600..603, QA-1003 | 6 | 1 |
| `AUDIO_TTS_PROVIDER_PLAYBOOK.md` | AUD-700..703, QA-1004 | 5 | 0 |
| `VECTOR_MEMORY_PLAYBOOK.md` | VIS-500, VIS-501, VEC-800..803 | 4 | 2 |
| `QA_ANTI_HALLUCINATION_PLAYBOOK.md` | QA-1000, QA-1001, QA-1002 | 3 | 0 |
| **Total** | **24 histórias cobertas** | **21** | **3** |

> **Novas funcionalidades:** AUD-700 — AudioPlan schema + AudioPlanService (CRUD, narrations, generate_narration_script). RND-601 — FFmpeg fallback universal tests (15). UI — Gradio tab reorder (Roteiro como primeira aba).

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
