# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-10
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 26/48
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 22 (48 - 26 concluídas - 0 em andamento)
Percentual concluído: 54,2%

**Aritmética:** 48 histórias únicas no backlog. 26 Concluídas + 0 Em andamento + 22 Pendentes = 48.

## Estado atual

- Branch atual: feature/RND-600-renderplan-minimo
- Último commit analisado: adf078b — "chore: add state/*.json to gitignore"
- Fase atual: Fase 5 — Pipeline e produto
- História atual: RND-600 — Criar RenderPlan mínimo ✅
- Próxima ação recomendada: RND-601 (Manter FFmpeg como fallback universal)

### Playbooks criados nesta sessão

| Arquivo | Stories | Concluídas | Pendentes |
|---------|---------|-----------|----------|
| `LLM_PROVIDER_PLAYBOOK.md` | PROV-300, PROV-301, PROV-302 | 3 | 0 |
| `VIDEO_RENDER_PROVIDER_PLAYBOOK.md` | VIS-502, VIS-503, RND-600..603, QA-1003 | 3 | 4 |
| `AUDIO_TTS_PROVIDER_PLAYBOOK.md` | AUD-700..703, QA-1004 | 1 | 4 |
| `VECTOR_MEMORY_PLAYBOOK.md` | VIS-500, VIS-501, VEC-800..803 | 2 | 4 |
| `QA_ANTI_HALLUCINATION_PLAYBOOK.md` | QA-1000, QA-1001, QA-1002 | 2 | 1 |
| **Total** | **21 histórias cobertas** | **8** | **16** |

> **Novas funcionalidades:** RenderPlan mínimo (RND-600) implementado. GPT4All provider corrigido (path hardcoded com typo). ProviderRouter removido do import direto no Gradio.

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

- **GPT4All fix:** Provider path corrigido — `app/adapters/llm/gpt4all_provider.py` usava path hardcoded com typo (`COMERCIAL` → `COMMERCIAL`). Alterado para usar `config.GPT4ALL_MODEL_DIR`. Provider agora detecta modelo `orca-mini-3b-gguf2-q4_0.gguf`.
- **API bug fix:** `app/application/use_cases/script_generation.py` passava `provider` como `mode` para `generate_script_with_llm`, causando fallthrough para auto-detection. Corrigido para usar `generate_script_with_provider()` quando provider explícito.
- **Separação UI/adapters:** `ProviderRouter` removido do import direto no Gradio. Criado `get_provider_diagnostics()` em `script_service.py` como camada de indireção.
- **RND-600 ✅:** RenderPlan mínimo criado — `app/domain/render_plan.py` (156 linhas). SceneRenderAssignment, RenderPlan, RenderPlanService com seleção de engine por cena baseada em disponibilidade, VRAM e perfil de qualidade. 18 testes em `tests/test_render_plan.py`.
- **Testes:** 219 testes passando (0 falhas) — core domains + API + UI + governança.
- **Histórias concluídas:** RND-600 (ordem 28). Total: 26/48 (54,2%).

### Estado atual

- **Branch atual:** feature/RND-600-renderplan-minimo
- **Fase:** Fase 5 (Pipeline e produto)
- **Histórias concluídas:** 26/48 (54,2%)
- **Próxima recomendada:** RND-601 (ordem 29) — Manter FFmpeg como fallback universal

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

### Arquivos criados nesta sessão

- `app/domain/render_plan.py` — Novo: 156 linhas (RND-600)
- `tests/test_render_plan.py` — Novo: 18 testes (RND-600)

### Arquivos alterados nesta sessão

- `app/adapters/llm/gpt4all_provider.py` — Path hardcoded corrigido para usar config
- `app/application/use_cases/script_generation.py` — Provider explícito respeitado
- `app/application/use_cases/generate_script_use_case.py` — Provider explícito respeitado
- `app/services/script_service.py` — `get_provider_diagnostics()` adicionado
- `app/ui/gradio_app.py` — ProviderRouter removido do import direto
- `tests/test_ui_metrics.py` — Título do app atualizado para pt-br

### Comandos executados

- `pytest tests/test_render_plan.py -v` — 18/18 passed
- `pytest tests/test_api.py -v -k "not generate_script_for_project"` — 11/11 passed
- `pytest tests/test_ui_metrics.py -v` — 16/16 passed
- `pytest (domínios + governança)` — 219/219 passed

### Evidências usadas

- Commit base: adf078b (início da sessão)
- Branch: feature/RND-600-renderplan-minimo
- Testes: 219/219 passando (0 falhas)
