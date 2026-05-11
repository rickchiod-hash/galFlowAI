# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-10 (tarde)
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 28/49
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 21 (49 - 28 concluídas - 0 em andamento)
Percentual concluído: 57,1%

**Aritmética:** 49 histórias únicas no backlog (UI-204 adicionada). 28 Concluídas + 0 Em andamento + 21 Pendentes = 49.

## Estado atual

- Branch atual: feature/RND-602-perfil-gtx-1660-super
- Último commit analisado: b5c4d1d — "feat(domain): implement RenderPlan (RND-600)"
- Fase atual: Fase 5 — Pipeline e produto
- História atual: RND-602 — Adicionar perfil GTX 1660 Super ✅
- Próxima ação recomendada: RND-603 (Registrar Wan VACE 1.3B como futuro opcional)

### Playbooks criados nesta sessão

| Arquivo | Stories | Concluídas | Pendentes |
|---------|---------|-----------|----------|
| `LLM_PROVIDER_PLAYBOOK.md` | PROV-300, PROV-301, PROV-302 | 3 | 0 |
| `VIDEO_RENDER_PROVIDER_PLAYBOOK.md` | VIS-502, VIS-503, RND-600..603, QA-1003 | 4 | 3 |
| `AUDIO_TTS_PROVIDER_PLAYBOOK.md` | AUD-700..703, QA-1004 | 1 | 4 |
| `VECTOR_MEMORY_PLAYBOOK.md` | VIS-500, VIS-501, VEC-800..803 | 2 | 4 |
| `QA_ANTI_HALLUCINATION_PLAYBOOK.md` | QA-1000, QA-1001, QA-1002 | 2 | 1 |
| **Total** | **21 histórias cobertas** | **8** | **16** |

> **Novas funcionalidades:** RND-602 — GpuProfile + GpuProfileCatalog integrados ao RenderPlanService. Perfil GTX 1660 Super (6GB) com resoluções seguras (480p/512p). Catálogo com 3 perfis (GTX 1660 Super, RTX 3060, Fallback CPU). 22 novos testes (40 total em test_render_plan.py).

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

### O que foi feito nesta sessão (Sessão 6 — RND-602)

- **RND-602 ✅:** Adicionado perfil GTX 1660 Super para evitar OOM em 6GB VRAM.
  - `GpuProfile` dataclass em `app/domain/render_plan.py` — define nome, VRAM, resoluções máximas/recomendadas, VRAM estimada por engine
  - `GpuProfileCatalog` — catálogo estático com 3 perfis: GTX 1660 Super (6GB), RTX 3060 (12GB), Fallback CPU/FFmpeg
  - `RenderPlanService` integrado com perfil: `generate_plan()` aceita `gpu_profile` opcional, `_select_engine()` usa VRAM do perfil, resolução varia por qualidade (DRAFT=480x360, STANDARD=recomendada, HIGH=máxima)
  - `SceneRenderAssignment.resolution` e `RenderPlan.max_resolution` adicionados
  - 22 novos testes (40 total): GpuProfile, GpuProfileCatalog, resolução por perfil/qualidade, engine selection com perfis, VRAM estimates por perfil
  - 222/222 testes passando (0 falhas)
- **Próxima recomendada:** RND-603 (Registrar Wan VACE 1.3B como futuro opcional)

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

### Arquivos alterados nesta sessão

- `app/domain/render_plan.py` — +GpuProfile, GpuProfileCatalog, resolução por perfil, integração com RenderPlanService
- `tests/test_render_plan.py` — +22 testes (GpuProfile, catalog, resolução, engine selection por perfil)

### Comandos executados

- `pytest tests/test_render_plan.py -v` — 40/40 passed (18 RND-600 + 22 RND-602)
- `pytest tests/test_ffmpeg_fallback.py -v` — 15/15 passed
- `pytest (domínios core: scene_contract + prompt_compiler + visual_bible + ingredient_registry + provider_fallback)` — 222/222 passed

### Evidências usadas

- Commit base: b5c4d1d (início da sessão)
- Branch: feature/RND-602-perfil-gtx-1660-super
- Testes: 222/222 passando (0 falhas)
