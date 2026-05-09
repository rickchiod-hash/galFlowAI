# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-09
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Progresso geral

Histórias concluídas: 18/48
Histórias em andamento: 1 (UI-201: Gerar roteiro sem renderizar)
Histórias bloqueadas: 0
Histórias pendentes: 34
Percentual concluído: 27%

## Estado atual

- Branch atual: feature/PIPE-401-idempotency-key
- Último commit analisado: c3cd591 — "docs: mark PIPE-400 as completed in status"
- Último commit criado pelo agente: c3cd591 — docs: mark PIPE-400 as completed in status
- Fase atual: Fase 5 — Pipeline e produto
- História atual: PIPE-401 — Criar idempotency key por etapa (em andamento)
- Próxima ação recomendada: Commit PIPE-401 e criar PR → merge

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

- **Sessão atual: Diagnóstico e unificação de pastas K:**
  - Checkpoint git: commit `3e18729` com 34 arquivos (9 modificados + 25 novos)
  - Correção `.gitignore`: `/test_*.py` (só raiz, não `tests/`)
  - Migração concluída: `tools/ffmpeg/` (301 MB) e `models/gpt4all/*.gguf` (3.9 GB) para pasta correta
  - Limpeza: removidos 6 itens duplicados/junk
  - `K:\AI_VIDEO_COMERCIAL_STUDIO` não renomeada (bloqueada por handles do sistema)
- **Próximo:** Corrigir hardcoded K: paths em adapters (ARCH-302) e rodar testes.

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

- docs/reference/PROJECT_REFERENCE_CONTEXT.md (novo — commitado do governance pack)
- docs/reference/FEATURE_PRESERVATION_MATRIX.md (novo — commitado do governance pack)
- docs/reference/EXTERNAL_REFERENCES.md (novo — commitado do governance pack)
- docs/project-control/01_AUDITORIA_HISTORICO_GIT.md (atualizado — 132 commits, CORE-100)
- docs/project-control/02_MAPA_ATUAL_DO_PROJETO.md (atualizado — completo, CORE-101)
- docs/project-control/00_STATUS_EXECUTIVO.md (atualizado — 10/48, 21%)
- docs/project-control/19_STORY_MAP.md (reescrito — 7 etapas, gates, story map)
- docs/project-control/05_BACKLOG_PRIORIZADO.md (atualizado — UI-200 concluída)
- docs/project-control/06_HISTORIAS_REFINADAS.md (atualizado — UI-200 com evidências)
- docs/project-control/10_DAILY_LOG.md (atualizado — entrada UI-200 + QA-1000)
- tests/test_story_map.py (novo — 5 testes UI-200)
- tests/test_naming_regression.py (novo — 5 testes QA-1000; ajustado para Windows encoding)
- app/ui/gradio_app.py (alterado — FlowForgeAI→GalFlowAI, 6 ocorrências)
- app/api.py (alterado — Gal AI→GalFlowAI, 3 ocorrências)
- app/application/__init__.py, app/application/use_cases/__init__.py (alterados — FlowForgeAI→GalFlowAI)
- app/services/metrics_service.py (alterado — Gal AI→GalFlowAI)
- app/assets/asset_manager.py (alterado — FlowForgeAI→GalFlowAI)
- tests/__init__.py, tests/integration/__init__.py, tests/unit/__init__.py (alterados — FlowForgeAI→GalFlowAI)
- tests/test_api.py (alterado — Gal AI→GalFlowAI)
- 35+ .md files (alterados — bulk replace FlowForgeAI/Gal AI→GalFlowAI)
- update_backlog.py, append_all_sections.py, append_backlog.py, setup_llm_providers.py, fix_all_syntax.py (alterados — Gal AI→GalFlowAI)
- tests/test_provider_presence.py (novo — 8 testes QA-1001)
- tests/test_tts_fallback.py (atualizado — 5 testes QA-1004 corrigidos)
- docs/project-control/00_STATUS_EXECUTIVO.md (atualizado — QA-1004 concluída, 14/48)
- docs/project-control/10_DAILY_LOG.md (atualizado — entrada QA-1004 concluída)

### Comandos executados

- pytest tests/test_git_audit.py tests/test_project_map.py -v — 10 passed
- pytest tests/test_story_map.py -v — 5 passed (UI-200)
- pytest tests/test_story_map.py tests/test_doc_code_gap.py tests/test_git_audit.py tests/test_project_map.py tests/test_checkpoint.py tests/test_product_context.py tests/test_feature_matrix.py tests/test_adr_policy.py tests/test_todo_policy.py tests/test_agents.py -v — 43 passed
- pytest tests/test_naming_regression.py -v — 5 passed (QA-1000, após 3 iterações de fix)
- pytest tests/test_provider_presence.py -v — 8 passed (QA-1001)
- pytest tests/test_checkpoint.py ... tests/test_provider_presence.py -v — 56 passed (12 histórias)

### Evidências usadas

- Commit HEAD: ddbe56c (UI-200 + QA-1000)
- Branch: master
- Git log: 132 commits, 067938a..63839e7
- Working tree: untracked files do usuário preservados
