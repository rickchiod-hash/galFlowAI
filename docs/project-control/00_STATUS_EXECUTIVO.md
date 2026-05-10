# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-09
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 25/48
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 23 (48 - 25 concluídas - 0 em andamento)
Percentual concluído: 52,1%

**Aritmética:** 48 histórias únicas no backlog. 25 Concluídas + 0 Em andamento + 23 Pendentes = 48.

## Estado atual

- Branch atual: master
- Último commit analisado: ab334b2 — "docs: fix outdated status and backlog after session review"
- Fase atual: Fase 4 — Refatoração segura / Fase 5 — Pipeline e produto
- História atual: PROV-302 — Criar testes de provider fallback ✅
- Próxima ação recomendada: RND-600 (Criar RenderPlan mínimo)

### Playbooks criados nesta sessão

| Arquivo | Stories | Concluídas | Pendentes |
|---------|---------|-----------|----------|
| `LLM_PROVIDER_PLAYBOOK.md` | PROV-300, PROV-301, PROV-302 | 3 | 0 |
| `VIDEO_RENDER_PROVIDER_PLAYBOOK.md` | VIS-502, VIS-503, RND-600..603, QA-1003 | 2 | 5 |
| `AUDIO_TTS_PROVIDER_PLAYBOOK.md` | AUD-700..703, QA-1004 | 1 | 4 |
| `VECTOR_MEMORY_PLAYBOOK.md` | VIS-500, VIS-501, VEC-800..803 | 2 | 4 |
| `QA_ANTI_HALLUCINATION_PLAYBOOK.md` | QA-1000, QA-1001, QA-1002 | 2 | 1 |
| **Total** | **21 histórias cobertas** | **7** | **17** |

> **Novas funcionalidades:** SQLite WAL/job ledger (PIPE-403), Ingredient Registry (VIS-500) e Visual Bible (VIS-501) implementados.

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

### O que foi feito nesta sessão

- **VIS-501 (merge):** PR #8 mergeado para master (`006ca21`). Visual Bible já estava implementado (33 testes).
- **VIS-502 ✅:** SceneContract schema criado — `app/domain/scene_contract.py` (205 linhas). CameraDirective, IngredientAssignment, SceneContract, SceneContractService com CRUD/search/reorder/versioning. 42 testes. PR #9 merged → `c7c0842`.
- **VIS-503 ✅:** PromptCompiler criado — `app/domain/prompt_compiler.py` (254 linhas). EngineType (WAN_GP/FFMPEG/VACE), CompiledPrompt, PromptCompilerService com compilação específica por engine. 44 testes. PR #10 merged → `0ed7bdf`.
- **PROV-302 ✅:** Testes de fallback chain — `tests/test_provider_fallback.py` (21 testes). TemplateProvider, config, ProviderRouter mockado. PR #11 merged → `0d95b8f`.
- **Total:** 107 testes novos, 4 PRs mergeados, 3 histórias concluídas.

### Estado atual

- **Branch atual:** master (`0d95b8f`)
- **Fase:** Fase 4 (Refatoração segura) / Fase 5 (Pipeline e produto)
- **Histórias concluídas:** 24/48 (50,0%)
- **Próxima recomendada:** UI-203 (ordem 13) — Resgatar telas de logs, métricas e diagnóstico

### Bloqueios

- Nenhum.

### Riscos

- Agente implementar antes de documentar.
- Agente marcar como concluído sem teste.
- Agente remover provider/fallback validado.
- Agente confundir documentação planejada com feature implementada.

### Gaps encontrados nesta sessão

- `00_STATUS_EXECUTIVO.md` estava desatualizado (referenciava VIS-501 como "sessão atual").
- `05_BACKLOG_PRIORIZADO.md` recomendava VIS-502 como próxima (já concluída).
- Ambos corrigidos nesta revisão.

### TODOs rastreáveis

- Nenhum TODO/FIXME/HACK/XXX encontrado em app/ ou tests/.

### Arquivos criados nesta sessão

- `app/domain/scene_contract.py` — Novo: 205 linhas (VIS-502)
- `tests/test_scene_contract.py` — Novo: 42 testes (VIS-502)
- `app/domain/prompt_compiler.py` — Novo: 254 linhas (VIS-503)
- `tests/test_prompt_compiler.py` — Novo: 44 testes (VIS-503)
- `tests/test_provider_fallback.py` — Novo: 21 testes (PROV-302)

### Comandos executados

- `pytest tests/test_scene_contract.py -v` — 42/42 passed
- `pytest tests/test_prompt_compiler.py -v` — 44/44 passed
- `pytest tests/test_provider_fallback.py -v` — 21/21 passed
- `pytest (todos os domínios + governança)` — 177/177 passed

### Evidências usadas

- Commit base: d35b57e (início da sessão)
- Master final: 0d95b8f (PROV-302 merged)
- Branches mergeadas: feature/VIS-502-scene-contract, feature/VIS-503-prompt-compiler, feature/PROV-302-fallback-tests
- Testes: 177/177 passando (0 falhas)
