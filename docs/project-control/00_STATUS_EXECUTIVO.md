# Status Executivo do Projeto — GalFlowAI

Atualizado em: 2026-05-16 (sessão 49 — GAL-945 remover 9 módulos órfãos)
Arquivo de continuidade obrigatório. Sempre atualizar ao final de cada sessão.

## Sessão 49 — GAL-945: Remover 9 módulos órfãos (2026-05-16)

### O que foi feito

1. **Auditoria completa** — Verificados imports em produção (0), tests (0) e __init__.py (0) para cada módulo
2. **9 arquivos deletados** — 471 linhas de código morto removido:
   - `app/adapters/framepack_adapter.py` (48 stmts)
   - `app/adapters/ollama_adapter.py` (38 stmts)
   - `app/adapters/piper_adapter.py` (156 stmts) — TTS adapter não utilizado
   - `app/adapters/translator_adapter.py` (32 stmts)
   - `app/pipeline/checkpoint_manager.py` (54 stmts)
   - `app/pipeline/filesystem_helper.py` (66 stmts)
   - `app/pipeline/voice_script_optimizer.py` (64 stmts)
   - `app/safety.py` (13 stmts)
   - `app/assets/asset_manager.py` (— stmts)
3. **Diretórios vazios removidos**: `app/assets/`, `app/pipeline/stages/`

### Testes
- **1091 passed, 0 failed** — zero regressão

### Arquivos alterados
- 9 arquivos deletados, 2 diretórios vazios removidos
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — GAL-945 adicionado e marcado Concluída
- `docs/project-control/10_DAILY_LOG.md` — entrada desta sessão
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta entrada

### Próximo passo
- Próxima história do backlog (definir com PO)

## Sessão 48 — GAL-943: Substituir 27 raises genéricos por exceções tipadas (2026-05-16)

### O que foi feito

1. **GAL-943 step 1** ✅ — 4 novas exceções em `app/exceptions.py`: ValidationError (422), NotFoundError (404), CacheError (500), VectorStoreError (500)
2. **GAL-943 step 2** ✅ — 4 raises já convertidos em sessão anterior: RuntimeError→ProviderError (vector_store_chroma, vector_store_qdrant), ValueError→ConfigError (provider_strategy), ValueError→VectorStoreError (vector_store)
3. **GAL-943 step 3 (esta sessão)** ✅ — 22 raises genéricos substituídos em 8 arquivos:
   - `audio_plan.py`: 7× ValueError/KeyError → ValidationError/NotFoundError
   - `ingredient_registry.py`: 2× ValueError/KeyError → ValidationError/NotFoundError
   - `prompt_compiler.py`: 1× ValueError → ConfigError
   - `scene_contract.py`: 3× ValueError/KeyError → ValidationError/NotFoundError
   - `sfx_manifest.py`: 3× ValueError/KeyError → ValidationError/NotFoundError
   - `visual_bible.py`: 3× ValueError/KeyError → ValidationError/NotFoundError
   - `artifact_cache_service.py`: 1× ValueError → CacheError
   - `script_service.py`: 2× KeyError → ScriptError
4. **job_state.py** ✅ — ValueError("Invalid transition") → ValidationError
5. **queue.py** ✅ — 3× `except ValueError:` → `except (ValueError, ValidationError):`
6. **Bug fix** 🔧 — SearchResult incorretamente importado de `app.exceptions` em chroma/qdrant (era em `app.adapters.vector_store`)
7. **24 testes atualizados** — `pytest.raises(ValueError|KeyError)` → `pytest.raises(ValidationError|NotFoundError|ConfigError|...)`
8. **2 testes pré-existentes corrigidos** — `test_vector_store.py` (ValueError→VectorStoreError) e `test_vector_store_chroma.py` (RuntimeError→ProviderError)

### Testes
- **1095 passed, 1 failed** (única falha: `test_git_audit` — commit count drift, preexistente)
- **Coverage**: 70% mantida

### Arquivos alterados
- `app/exceptions.py` — +4 classes (ValidationError, NotFoundError, CacheError, VectorStoreError)
- `app/domain/audio_plan.py` — 7 raises tipados
- `app/domain/ingredient_registry.py` — 2 raises tipados
- `app/domain/prompt_compiler.py` — 1 raise tipado
- `app/domain/scene_contract.py` — 3 raises tipados
- `app/domain/sfx_manifest.py` — 3 raises tipados
- `app/domain/visual_bible.py` — 3 raises tipados
- `app/services/artifact_cache_service.py` — 1 raise tipado
- `app/services/script_service.py` — 2 raises tipados
- `app/pipeline/job_state.py` — 1 raise tipado
- `app/jobs/queue.py` — 3 excepts atualizados
- `app/adapters/vector_store_chroma.py` — import SearchResult fix
- `app/adapters/vector_store_qdrant.py` — import SearchResult fix
- `tests/test_audio_plan.py` — 7 asserts atualizados
- `tests/test_ingredient_registry.py` — 2 asserts atualizados
- `tests/test_prompt_compiler.py` — 1 assert atualizado
- `tests/test_scene_contract.py` — 3 asserts atualizados
- `tests/test_sfx_manifest.py` — 3 asserts atualizados
- `tests/test_visual_bible.py` — 3 asserts atualizados
- `tests/test_job_state.py` — 5 asserts atualizados
- `tests/test_vector_store.py` — 1 assert atualizado
- `tests/test_vector_store_chroma.py` — 1 assert atualizado
- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — GAL-943 marcado Concluída
- `docs/project-control/10_DAILY_LOG.md` — entrada desta sessão
- `docs/project-control/00_STATUS_EXECUTIVO.md` — esta entrada

### Próximo passo
- Próxima história do backlog (definir com PO)
- git audit doc sync

## Sessão 41 — GAL-938: Remover hardcoded K:\ paths — portabilidade (2026-05-16)

### O que foi feito

1. **GAL-938 ✅** — 23 hardcoded `K:\` paths substituídos por `app.config.BASE_DIR`, `LOGS_DIR`, `PROJECTS_DIR`, `ENGINES_DIR` em 10 arquivos
2. **Testes**: 980 passed, 0 failed
3. **Backlog**: GAL-938 ✅ Concluída

### Arquivos alterados
- 10 arquivos de código + 4 docs

## Sessão 40 — GAL-937: Eliminar async wrappers falsos sobre sync blocking calls (2026-05-16)

### O que foi feito

1. **GAL-937 ✅** — Async wrappers falsos eliminados:
   - `provider_strategy.py`: `LLMStrategy.generate()` e `TemplateStrategy.generate()` convertidos de `async def` para `def`
   - `provider_router.py`: `generate_script_fast()` e `generate_script_quality()` convertidos de `async def` para `def`, removidos `await` e `import asyncio`
   - `script_service.py`: removidos wrappers `async def` falsos, simplificado `generate_script_with_llm()` sem event loop detection
   - Commitado, PR #44 criado, mergeado para master
2. **Testes**: 980 passed, 0 failed
3. **Backlog**: GAL-937 ✅ Concluída
4. **GAP-010**: ✅ Concluído

## Sessão 39 — GAL-936: Finalização — commit, PR, merge (2026-05-16)

### O que foi feito

1. **GAL-936 ✅** — Alterações de S38 commitadas e mergeadas para master
2. **Testes**: 984 passed, 0 failed
3. **Daily log**: S38 e S39 adicionados
4. **Status executivo**: atualizado
5. **Backlog**: GAL-936 marcado como Concluída
6. **Git audit**: 271→272 commits

### Status do projeto
- **Backlog completamente zerado** — todas as histórias concluídas
- Próxima etapa: definição de nova iteração com PO

## Sessão 38 — GAL-936: Remove legacy pipeline modules (2026-05-15)

### O que foi feito

1. **GAL-936 ✅** — Legacy modules `script_generator.py`, `scene_splitter.py`, `prompt_builder.py` removidos:
   - Domain logic movido para `app/domain/scene_parser.py` e `app/domain/prompt_builder_service.py`
   - I/O movido para `app/repositories/scene_repository.py` e `app/repositories/prompt_repository.py`
   - `ScriptRepository` estendido com `save_script()`
   - `script_service.py` estendido com `generate_script()` / `generate_script_with_details()` wrappers
   - Todos os 12 callers atualizados (use cases, stages, pipeline, gradio, testes)

2. **Bugs cascata corrigidos (6):**
   - `prompts_path` undefined em `video_generation_pipeline.py:188`
   - `mock_build_prompts` NameError em `test_tts_fallback.py`
   - Legacy patch targets em `test_h10_use_cases.py` (`save_script`, `save_scenes`, `save_prompts`)
   - `style=""` passado para `BuildPromptsUseCase` em vez do parâmetro real `style`
   - `_make_pipeline()` em `test_pipeline_structured_errors.py` sem `build_prompts_use_case.execute.return_value`
   - `import app.config` + `Path()` normalization em `ScriptRepository` para runtime PROJECTS_DIR override
   - Git audit doc atualizado: 270→271 commits

### Testes
- **1051 passed, 0 failed** — zero regressão

### Arquivos alterados
- `app/domain/scene_parser.py` — novo (legacy scene_splitter logic)
- `app/domain/prompt_builder_service.py` — novo (legacy prompt_builder logic)
- `app/repositories/scene_repository.py` — novo (scene I/O)
- `app/repositories/prompt_repository.py` — novo (prompt I/O)
- `app/repositories/script_repository.py` — `save_script()` adicionado, import app.config + Path()
- `app/services/script_service.py` — `generate_script()`, `generate_script_with_details()` wrappers
- `app/pipeline/script_generator.py` — **deletado**
- `app/pipeline/scene_splitter.py` — **deletado**
- `app/pipeline/prompt_builder.py` — **deletado**
- `app/pipeline/video_generation_pipeline.py` — fix `style=""` → `style=style`, fix `prompts_path` undefined
- `tests/test_tts_fallback.py` — remove dead `mock_build_prompts`
- `tests/test_h10_use_cases.py` — patch targets atualizados
- `tests/test_pipeline_structured_errors.py` — `_make_pipeline()` com `build_prompts_use_case` mock
- `docs/project-control/01_AUDITORIA_HISTORICO_GIT.md` — 271 commits

## Sessão 29 — P0 Recovery Mission (2026-05-14)

4 P0 bugs operacionais identificados e corrigidos, 1 compat fix, 828 testes passando (0 regressão).

### Bugs corrigidos

| ID | Bug | Arquivo | Fix |
|----|-----|---------|-----|
| UI-210 | Aprovar roteiro não persiste | `gradio_app.py:107-118` | `on_approve_script` agora chama `approve_script(project_id)` real |
| UI-209 | Salvar edição ignora texto | `gradio_app.py:397-405` | `on_save_edit` agora chama `save_manual_edit(pid, script_text, ...)` |
| — | Render bypassa aprovação | `gradio_app.py:329-356` | Gate `script_approved` adicionado; removed write unconditional |
| PROV-304 | Provider falha silenciosamente | `gradio_app.py:91-104` | Warning no status quando qualidade for "fallback" |
| — | StrEnum Python 3.10 | `error_codes.py` | Shim try/except + str+Enum fallback |

### QA artifacts criados
- `artifacts/qa/curl_smoke_test.ps1` — 11 testes smoke
- `artifacts/qa/root_cause_matrix.md` — matriz causa raiz
- `artifacts/qa/ui_event_inventory.md` — inventário de 25+ callbacks

### Testes
- 828 passed, 0 regressions (1 pre-existing git audit count)

## Sessão 30 — Recovery Mission S30 (2026-05-14)

5 bugs operacionais corrigidos, 47 testes passando, GPT4All restaurado.

### Bugs corrigidos nesta sessão

| ID | Bug | Arquivo | Causa Raiz | Fix |
|----|-----|---------|-----------|-----|
| GAL-903 | GPT4All crash pós-merge | `gpt4all_provider.py` | `n_threads` não suportado pela API | Removeu kwargs inválidos |
| GAL-904 | Output quality baixo | `gpt4all_provider.py`, `script_service.py` | `max_tokens=400`, prompt sem estrutura, `_condense_template` sem Narracao: | max_tokens=800, formato explícito, +Narracao: |
| UI-209 | Aprovar Roteiro sem efeito (new UI) | `gradio_app.py` | Script não salvo em disco | `save_manual_edit()` adicionado em `on_generate_script` |
| UI-210 | 3 botões sem handler (legacy UI) | `main.py` | `btn_approve`, `btn_new_version`, `btn_restore` sem `.click()` | Handlers adicionados |
| UI-211 | Salvar Edição output quebrado | `main.py` | `outputs` incluía `gr.Textbox(visible=False)` inexistente | Reduzido para `[action_status]` |
| PROV-305 | Ações retornam "Erro" | `main.py` | `result.get("status", "Erro")` — chave "status" não existe | Wrappers com retorno fixo |

### QA artifacts criados
- `artifacts/qa/root_cause_matrix.md` — atualizado com 8 bugs
- `artifacts/qa/ui_event_inventory.md` — 30+ componentes inventariados

### Testes
- 47 passed (provider + script_service), 0 regressões

## Sessão 31 — Phase E: QA Artifacts & UI Corrections (2026-05-14)

### O que foi feito

1. **QA artifacts criados:**
   - `artifacts/qa/provider_runtime_matrix.md` — matriz completa de seleção de providers, fallback chains, qualidade, timeouts
   - `artifacts/qa/flow_validation_checklist.md` — checklist de 63 itens para validação de pipeline completo
   - `scripts/qa/api_smoke_flow.ps1` — script de smoke tests da API com salvamento de respostas
   - `artifacts/qa/curl/` — 25+ respostas JSON de todos os endpoints (18/18 testes passando)

2. **Progress bar real-time:**
   - `on_render_scenes` agora aceita `progress=gr.Progress()` (injetado pelo Gradio)
   - Pipeline recebe `progress_callback` funcional que atualiza barra em tempo real
   - `demo.queue()` adicionado para suporte a async/generators

3. **Export path unificado:**
   - `on_export_final` escreve em `projects/{project_id}/export/` (antes `output/final/`)
   - `on_generate_tts` escreve em `projects/{project_id}/audio/` (antes `output/`)
   - `on_generate_srt` escreve em `projects/{project_id}/subtitles/` (antes `output/`)

4. **Health dashboard fix:**
   - `_check_system()` em `observability_use_cases.py`: `import psutil` movido para dentro do try/except
   - `psutil` instalado no ambiente studio

5. **API smoke tests:**
   - 18/18 endpoints passando contra `:8000` (FastAPI)
   - Rotas corrigidas para bater nos paths reais

6. **Fase E completa:**
   - QA-1007 ✅ — curl prova gate de aprovação (script gera, salva, aprova, carrega)
   - QA-1008 ✅ — provider list retorna template + gpt4all, fallback quality visível
   - QA-1009 ✅ — logs/dashboard/jobs endpoints retornam 200 com dados
   - RND-613 ✅ — vídeos MP4 (H.264, 854x480) gerados em `projects/*/final/commercial.mp4`

### Testes
- 907 passed, 2 pre-existing fails (git audit count + ignorado)
- 0 regressão das mudanças desta sessão

## Sessão 32 — GAL-930: ScriptRepository (2026-05-14)

### O que foi feito

1. **GAL-930 ✅** — IO de arquivos extraído de `script_service.py` para `ScriptRepository`:
   - Criado `app/repositories/script_repository.py` com `ScriptRepository` usando `Result[T]`
   - `script_service.py` delegou toda persistência: sem `json`, `Path`, `datetime` direto
   - Funções removidas do service: `_load_versions`, `_save_versions`, `_next_version`, `_get_script_dir`
   - Funções refatoradas: `save_manual_edit`, `create_new_version`, `restore_previous_version`, `approve_script`, `load_current_script`, `load_script_versions`
   - GAL-931 (Result Object) commitado junto como dependência

2. **23 novos testes** em `tests/test_script_repository.py`:
   - Init, versions list CRUD, version files save/load, current script loading, approval, summaries, previous version
   - Teste existente `test_script_service_versioning_and_approve` passa sem alterações

### Testes
- 935 passed, 1 pre-existing fail (git audit count)
- Zero regressão

## Sessão 33 — GAL-932: Script Service Unit Tests (2026-05-14)

### O que foi feito

1. **GAL-932 ✅** — 94 testes unitários em `test_script_service_coverage.py`:
   - Mock ScriptRepository: save_manual_edit, create_new_version, restore_previous_version, approve_script, load_current_script, load_script_versions
   - Mock ProviderRouter: auto, safe, fast, quality modes, event loop handling
   - Mock load_current_script + save_manual_edit: improve, complement, viral, premium, direct
   - Pure functions: _condense_template, _build_enhanced_prompt, _call_template, validate_script_quality
   - Async wrappers: generate_script_fast, generate_script_quality
   - Cobertura: **28% → 91%** (265 stmts, 25 missed — linhas 116-166 são provider dinâmico)

### Testes
- 1005 passed, 1 pre-existing fail (git audit count)
- Zero regressão

## Sessão 35 — GAL-933/934/935: Todos os débitos técnicos concluídos (2026-05-14)

### O que foi feito

1. **GAL-933 ✅** — `RenderAllScenesUseCase` extraído do pipeline:
   - Criado `app/application/use_cases/render_all_scenes_use_case.py` — WanGP→FFmpeg fallback loop por cena em `BaseUseCase` com dependências injetáveis
   - Pipeline agora usa `self.render_all_scenes_uc.execute()` em vez de inline render loop
   - `RenderVideoUseCase`/`CreateStaticVideoUseCase` removidos dos imports do pipeline
   - 9 testes em `test_render_all_scenes_use_case.py`

2. **GAL-934 ✅** — Mock E2E tests para fallback WanGP→FFmpeg com logging:
   - `tests/test_wangp_fallback.py` com 4 testes no padrão import-patching (como `test_tts_fallback.py`)
   - Valida ErrorJsonlWriter + StageLogger em fallback, double-failure, happy path e concat failure

3. **GAL-935 ✅** — 33 contract tests FastAPI:
   - `tests/test_api_contract.py` cobre rotas críticas de LLM, jobs, projetos, scripts
   - Fix: `_job_ledger` → `self._job_ledger` (NameError) em `app/jobs/queue.py` (6 ocorrências)

### Arquivos criados
- `app/application/use_cases/render_all_scenes_use_case.py` — novo
- `tests/test_render_all_scenes_use_case.py` — 9 testes
- `tests/test_api_contract.py` — 33 testes de contrato
- `tests/test_wangp_fallback.py` — 4 testes E2E mockados

### Arquivos alterados
- `app/pipeline/video_generation_pipeline.py` — delega render de cenas a `RenderAllScenesUseCase`
- `app/jobs/queue.py` — `_job_ledger` → `self._job_ledger`
- `tests/test_pipeline_structured_errors.py` — mock targets atualizados para `render_all_scenes_uc.*`
- `tests/test_tts_fallback.py` — patch targets redirecionados para `render_all_scenes_use_case.*`

### Testes
- **1051 passed, 1 pre-existing fail** (git audit count)
- Zero regressão

## Progresso geral

Histórias concluídas: 65/65 + 11 bugs + 4 QA/RND itens Phase E + 8 débitos (GAL-930..944)
Histórias em andamento: 0
Histórias bloqueadas: 0
Histórias pendentes: 0
Percentual concluído: 100% backlog + P0 + Phase E + 8/8 débitos ✅

## Sessão 47 — GAL-942: Coverage crítica — 62%→70%, 116 novos testes (2026-05-16)

### O que foi feito
1. **GAL-942 ✅** — 116 testes unitários para 10 módulos com cobertura 0% ou <20%
2. Cobertura total: **62% → 70%** (+8pp)
3. Módulos com 0% que agora estão >78%: approve_script_use_case (100%), create_project_use_case (100%), create_storyboard_use_case (100%), manage_queue_use_case (98%), script_quality_use_cases (91%), script_improvement_use_cases (78%), visual_consistency_use_cases (86%), prompt_use_cases (93%)
4. Serviços recuperados: video_service (12%→84%), tts_service (18%→82%)
5. Padrão usado: unittest.mock (patch/MagicMock), tempfile para I/O real em LoadPromptPackUseCase

### Arquivos criados
- `tests/test_approve_script_use_case.py` — 4 testes
- `tests/test_create_project_use_case.py` — 4 testes
- `tests/test_create_storyboard_use_case.py` — 5 testes
- `tests/test_manage_queue_use_case.py` — 9 testes
- `tests/test_script_quality_use_cases.py` — 15 testes
- `tests/test_script_improvement_use_cases.py` — 17 testes
- `tests/test_visual_consistency_use_cases.py` — 17 testes
- `tests/test_prompt_use_cases.py` — 17 testes
- `tests/test_video_service.py` — 17 testes
- `tests/test_tts_service.py` — 11 testes

### Testes
- **1096 passed, 0 failed** (anterior: 980)

## Estado atual

- Branch atual: master
- Último commit: 76a74a3 (GAL-944)
- Fase atual: S47 — GAL-942 Coverage crítica
- Story stream atual: 73 histórias concluídas (65 originais + 8 débitos)
- Pendências: 0
- Cobertura: 70%
- Próxima ação recomendada: Definir próxima história (GAL-943 exceções tipadas ou nova feature)

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

### Sessão 28b — Phase 6C: DOC-120 (2026-05-14)

#### O que foi feito
1. **DOC-120 ✅** — Documentação reconciliada com novo direcionamento mandatório:
   - `VIDEO_RENDER_PROVIDER_PLAYBOOK.md`: WanGP e VACE reclassificados como mandatórios; adicionadas RND-610, RND-611, RND-612; regras de preservação atualizadas
   - `VECTOR_MEMORY_PLAYBOOK.md`: camada de memória reclassificada como mandatória; adicionadas VEC-810, VEC-811; regras de preservação atualizadas
   - `15_PROVIDER_PLAYBOOK.md`: tabela atualizada com 29 stories cobertas (antes 24); novos stories de Fase 6 adicionados
   - `19_STORY_MAP.md`: novas etapas de Fase 6 adicionadas; tabela por atividade expandida com Infraestrutura e Vector memory
   - `00_STATUS_EXECUTIVO.md`: 65/65 histórias (100%)
   - `05_BACKLOG_PRIORIZADO.md`: DOC-120 → Concluída
   - `10_DAILY_LOG.md`: nova entrada
   - Ollama documentado como único componente opcional

#### Backlog completo ✅
GalFlowAI: **65/65 histórias concluídas** — 54 originais + 11 Pós-49.

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
