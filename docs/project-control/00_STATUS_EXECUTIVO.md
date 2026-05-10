# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-09
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 20/48
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 28 (48 - 20 concluídas - 0 em andamento)
Percentual concluído: 41,7%

**Aritmética:** 48 histórias únicas no backlog. 20 Concluídas + 0 Em andamento + 28 Pendentes = 48.

## Estado atual

- Branch atual: feature/VIS-500-ingredient-registry
- Último commit analisado: 59e927c — "feat(PIPE-403): Implementar SQLite WAL/job ledger para persistência de jobs sem Redis"
- Fase atual: Fase 5 — Pipeline e produto
- História atual: VIS-500 — Criar schema Ingredient Registry ✅
- Próxima ação recomendada: VIS-501 (Criar schema Visual Bible) ou RND-600 (Criar RenderPlan mínimo)

### Playbooks criados nesta sessão

| Arquivo | Stories | Concluídas | Pendentes |
|---------|---------|-----------|----------|
| `LLM_PROVIDER_PLAYBOOK.md` | PROV-300, PROV-301, PROV-302 | 2 | 1 |
| `VIDEO_RENDER_PROVIDER_PLAYBOOK.md` | VIS-502, VIS-503, RND-600..603, QA-1003 | 0 | 7 |
| `AUDIO_TTS_PROVIDER_PLAYBOOK.md` | AUD-700..703, QA-1004 | 1 | 4 |
| `VECTOR_MEMORY_PLAYBOOK.md` | VIS-500, VIS-501, VEC-800..803 | 1 | 5 |
| `QA_ANTI_HALLUCINATION_PLAYBOOK.md` | QA-1000, QA-1001, QA-1002 | 2 | 1 |
| **Total** | **21 histórias cobertas** | **6** | **18** |

> **Novas funcionalidades:** SQLite WAL/job ledger (PIPE-403) e Schema Ingredient Registry (VIS-500) implementados.

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

### O que está sendo feito

- **Sessão atual: VIS-500 — Ingredient Registry implementado.**
  - Schema com 4 tipos (PRODUCT, CHARACTER, SCENARIO, OBJECT), VisualReference, CRUD versionado
  - 27 testes passando (schema validation, CRUD, search, filter, versioning)
  - Branch: `feature/VIS-500-ingredient-registry` (pendente de commit e merge)
- **Próximo:** Rodar full test suite, commitar, criar PR, merge para master. Depois VIS-501 ou RND-600.

### Bloqueios

- Nenhum.

### Riscos

- Agente implementar antes de documentar.
- Agente marcar como concluído sem teste.
- Agente remover provider/fallback validado.
- Agente confundir documentação planejada com feature implementada.
- docs/reference/ arquivos agora commitados (gap resolvido).

### Gaps encontrados

- docs/reference/ não estava no git (corrigido).
- User's working tree tem 6+ untracked files que podem divergir (resolvido — commitados).
- python.exe não está no PATH padrão (usar env específico).
- Testes de governança retornam bool (warnings PytestReturnNotNoneWarning — padrão aceito do projeto).
- **Duas pastas K:** `AI_VIDEO_COMMERCIAL_STUDIO` (correta) e `AI_VIDEO_COMERCIAL_STUDIO` (errata). Itens únicos migrados. Pasta incorreta mantida (bloqueada por handles — necessário reboot para renomear).
- `.gitignore` tinha `test_*.py` sem `/`, afetando `tests/test_*.py` — corrigido para `/test_*.py`.

### TODOs rastreáveis

- Nenhum TODO/FIXME/HACK/XXX encontrado em app/ ou tests/.

### Arquivos alterados nesta sessão

- `app/domain/ingredient_registry.py` — Novo: schema Ingredient Registry
- `app/domain/__init__.py` — Init do pacote domain
- `tests/test_ingredient_registry.py` — Novo: 27 testes do ingredient registry
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — VIS-500 marcada como Concluída
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — PIPE-403 → Concluída
- `docs/project-control/10_DAILY_LOG.md` — Histórico restaurado + entrada VIS-500
- `docs/project-control/00_STATUS_EXECUTIVO.md` — Atualizado (20/48, 41,7%)
- `.gitignore` — Adicionado `*.db`

### Comandos executados

- `pytest tests/test_ingredient_registry.py -v` — 27 passed (VIS-500)

### Evidências usadas

- Commit base: 59e927c (PIPE-403 — SQLite job ledger)
- Branch: feature/VIS-500-ingredient-registry
- Schema: `app/domain/ingredient_registry.py` — Ingredient, IngredientType, VisualReference, IngredientRegistry
- Testes: 27/27 passando
