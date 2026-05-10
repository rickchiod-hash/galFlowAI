# 06_HISTORIAS_REFINADAS — GalFlowAI

Formato baseado em Card, Conversation e Confirmation. Cada história deve permanecer pequena, estimável e testável.

## GOV-001 — Criar checkpoint diário permanente

**Épico:** EPIC-000 Proteção contra regressão  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/00_STATUS_EXECUTIVO.md`

### História
Como mantenedor do GalFlowAI, eu quero um arquivo único de continuidade atualizado em toda sessão, para retomar o projeto em outra sessão sem perda de contexto.

### Evidências
- `docs/project-control/00_STATUS_EXECUTIVO.md` — contém 10 seções obrigatórias, atualizado nesta sessão
- `docs/project-control/10_DAILY_LOG.md` — formato padrão, 4 entradas de sessão
- `docs/project-control/13_CHECKPOINTS_DE_SESSAO.md` — presente
- `tests/test_checkpoint.py` — 3 testes criados (existence, sections, format)
- Pytest: 3 passed, 446 coletados sem erro
- Commit: 3132eb0

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: 00_STATUS_EXECUTIVO.md.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `GOV-001` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `GOV-001` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## GOV-002 — Criar fonte de verdade do produto

**Épico:** EPIC-000 Proteção contra regressão  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/reference/PROJECT_REFERENCE_CONTEXT.md`

### História
Como responsável de produto, eu quero um documento imutável de escopo, para impedir drift de nome, fluxo e arquitetura.

### Evidências
- `docs/reference/PROJECT_REFERENCE_CONTEXT.md` — 8 seções obrigatórias, status "FONTE DE VERDADE DO PRODUTO", "Alteração permitida somente com ADR"
- `tests/test_product_context.py` — 4 testes (existence, sections, keywords, truth source)
- Pytest: 4 passed, 453 coletados sem erro
- Commit: 3132eb0

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: PROJECT_REFERENCE_CONTEXT.md.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `GOV-002` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `GOV-002` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## GOV-003 — Criar matriz de preservação de features

**Épico:** EPIC-000 Proteção contra regressão  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/reference/FEATURE_PRESERVATION_MATRIX.md`

### História
Como QA/Tech Lead, eu quero uma matriz de features obrigatórias, para impedir remoção silenciosa de providers, fallbacks e telas.

### Evidências
- `docs/reference/FEATURE_PRESERVATION_MATRIX.md` — 8 colunas, 10 features obrigatórias, 6 P1
- `tests/test_feature_matrix.py` — 5 testes (existence, columns, mandatory, P1, removibility)
- Pytest: 5 passed, 458 coletados sem erro
- Commit: (nesta sessão)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: FEATURE_PRESERVATION_MATRIX.md.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `GOV-003` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `GOV-003` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## GOV-004 — Padronizar TODOs rastreáveis

**Épico:** EPIC-000 Proteção contra regressão  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/09_GAPS_TODOS_E_DIVIDAS.md`

### História
Como desenvolvedor sênior, eu quero TODOs vinculados a histórias, para que dívida técnica tenha dono, critério e backlog.

### Evidências
- `docs/project-control/09_GAPS_TODOS_E_DIVIDAS.md` — política, formato obrigatório, padrão TODO(GAL-XXX)
- `tests/test_todo_policy.py` — 4 testes (existence, sections, pattern, no generic)
- Pytest: 4 passed, 462 coletados sem erro
- Varredura de código: 0 TODOs genéricos encontrados
- Commit: (nesta sessão)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: TODO_GOVERNANCE.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `GOV-004` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `GOV-004` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## GOV-005 — Criar ADR obrigatório para remoções

**Épico:** EPIC-000 Proteção contra regressão  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/11_DECISOES_TECNICAS_ADR.md`

### História
Como arquiteto, eu quero registrar decisões de remoção/substituição, para preservar rastreabilidade e rollback.

### Evidências
- `docs/project-control/11_DECISOES_TECNICAS_ADR.md` — template ADR-000 com 10 campos, ADR-001..ADR-005 iniciais
- `tests/test_adr_policy.py` — 3 testes (existence, template, references)
- Pytest: 3 passed, 465 coletados sem erro
- Commit: (nesta sessão)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: ADR_TEMPLATE.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `GOV-005` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `GOV-005` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## GOV-006 — Adicionar AGENTS e Skill do GalFlowAI

**Épico:** EPIC-000 Proteção contra regressão  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `AGENTS.md e .opencode/skills/galflowai/SKILL.md`

### História
Como operador do OpenCode, eu quero instruções permanentes do projeto, para que o agente siga o mesmo padrão em toda sessão.

### Evidências
- `AGENTS.md` — GalFlowAI governance, Standing Orders, TODO policy
- `.opencode/skills/galflowai/SKILL.md` — documentos obrigatórios, ordem, guardrails
- `tests/test_agents.py` — 4 testes (AGENTS existence, content, SKILL existence, content)
- Pytest: 4 passed, 469 coletados sem erro
- Commit: (nesta sessão)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: AGENTS/SKILL.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `GOV-006` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `GOV-006` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## CORE-100 — Auditar histórico Git desde o primeiro commit

**Épico:** EPIC-100 Diagnóstico e recuperação  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/01_AUDITORIA_HISTORICO_GIT.md`

### História
Como responsável técnico, eu quero mapear o que foi implementado/removido, para resgatar features perdidas com evidência.

### Evidências
- `docs/project-control/01_AUDITORIA_HISTORICO_GIT.md` — atualizado com 132 commits, HEAD 63839e7, 7 perguntas obrigatórias respondidas
- `tests/test_git_audit.py` — 5 testes (file exists, sections, git evidence, questions, commit count)
- Pytest: 5 passed (CORE-100), 33 passed (all governance)
- Commit: (nesta sessão)
- Gap encontrado: docs/reference/ não estava no git — corrigido (3 arquivos commitados)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Contexto funcional: Git Audit.

### Evidências obrigatórias
- `01_AUDITORIA_HISTORICO_GIT.md` — tabela de marcos, arquivos deletados, 7 perguntas respondidas.
- Commits: 067938a (MVP) a 63839e7 (GOV-006) — 132 commits analisados.
- `test_git_audit.py` — 5 testes implementados e passando.
- Nenhuma feature obrigatória removida. All 6 LLM providers, WanGP, FFmpeg, TTS preservados.

### Critérios de aceite
Ver `CORE-100` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `CORE-100` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## CORE-101 — Mapear estado atual do projeto

**Épico:** EPIC-100 Diagnóstico e recuperação  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/02_MAPA_ATUAL_DO_PROJETO.md`

### História
Como desenvolvedor, eu quero um mapa atual de tecnologias, entradas e módulos, para iniciar refatorações sem suposição.

### Evidências
- `docs/project-control/02_MAPA_ATUAL_DO_PROJETO.md` — 6 seções: raiz, tecnologias (12+), estrutura de diretórios completa, entrypoints (4), features obrigatórias, riscos (5)
- `tests/test_project_map.py` — 5 testes (file exists, sections, technologies, entrypoints, feature matrix ref)
- Pytest: 5 passed (CORE-101), 33 passed (all governance)
- Commit: (nesta sessão)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Contexto funcional: Mapa atual.

### Evidências obrigatórias
- `02_MAPA_ATUAL_DO_PROJETO.md` — tecnologias, diretórios, entrypoints, riscos identificados.
- 6 módulos LLM providers, 2 engines de vídeo (WanGP + FFmpeg), 2 UIs (Gradio + FastAPI).
- 23+ testes existentes em tests/.
- Risco confirmado: docs/reference/ não commitado (corrigido nesta sessão).

### Critérios de aceite
Ver `CORE-101` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `CORE-101` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## CORE-102 — Validar diferença entre documentação e código

**Épico:** EPIC-100 Diagnóstico e recuperação  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/03_ARQUITETURA_ATUAL.md`

### História
Como QA, eu quero comparar docs com código, para separar fato implementado de roadmap.

### Evidências
- `docs/project-control/03_ARQUITETURA_ATUAL.md` — preenchido com validação sistemática de 22 claims, 5 tabelas (providers, vídeo, áudio, features, regras arquiteturais), acoplamentos, fluxo real vs documentado, 6 gaps (G1-G6)
- Comparação doc vs código: 16 PRESENTE, 5 DIFERENTE (GPT-compatible não implementado, Piper doc desatualizada, fluxo superdimensionado, API chama adapter direto, docs/reference não commitado), 0 AUSENTE
- `tests/test_doc_code_gap.py` — 5 testes (file exists, sections, providers, gaps, gap patterns)
- Pytest: 5 passed (CORE-102), 38 passed (all governance — 9 histórias)
- Commit: (nesta sessão)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Contexto funcional: Audit docs/code.

### Evidências obrigatórias
- `03_ARQUITETURA_ATUAL.md` — 22 claims validadas, 6 gaps documentados com tipo, doc diz, código faz, impacto, ação.
- Documentos validados: PROJECT_REFERENCE_CONTEXT.md (11 claims), FEATURE_PRESERVATION_MATRIX.md (5 claims), 04_ARQUITETURA_ALVO.md (3 claims).
- Código escaneado: 80+ arquivos .py, playbooks, docs.
- Gaps encontrados: GPT-compatible endpoint não implementado, Piper doc desatualizada, fluxo de 22 etapas irreal, API viola regra de adapter direto.

### Critérios de aceite
Ver `CORE-102` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `CORE-102` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## UI-200 — Restaurar fluxo por etapas na documentação

**Épico:** EPIC-200 UX e fluxo de produto  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/19_STORY_MAP.md`

### História
Como criador de comerciais, eu quero seguir etapas validáveis, para aprovar roteiro/cenas antes de gastar GPU.

### Evidências
- `docs/project-control/19_STORY_MAP.md` reescrito — fluxo de 7 etapas com gates de validação (Briefing → Roteiro → Cenas → Prompts → Narração → Vídeo → Montagem), story map por atividade, 5 regras de fluxo
- `tests/test_story_map.py` — 5 testes (file exists, step flow, steps listed, validation gates, flow rules)
- Pytest: 5 passed (UI-200), 43 passed (all governance — 10 histórias)
- Commit: (nesta sessão)

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Contexto funcional: UI_STEP_FLOW.

### Evidências obrigatórias
- `19_STORY_MAP.md` — fluxo visual com 7 etapas, cada uma com gate de validação.
- Etapas mapeadas ao código real: Briefing→main.py, Roteiro→script_service, Cenas→scene_splitter, Prompts→prompt_builder, Narração→tts_adapter, Vídeo→wangp_adapter/ffmpeg_adapter, Montagem→ffmpeg_adapter.
- Regras documentadas: roteiro aprovado antes de cenas (UI-202), TTS falha não quebra, WanGP fallback FFmpeg.

### Critérios de aceite
Ver `UI-200` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `UI-200` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## UI-201 — Gerar roteiro sem renderizar vídeo

**Épico:** EPIC-200 UX e fluxo de produto  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/19_STORY_MAP.md`

### História
Como usuário do GalFlowAI, eu quero gerar e revisar roteiro isoladamente, para evitar render caro com roteiro ruim.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: UI roteiro.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `UI-201` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `UI-201` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## UI-202 — Bloquear cenas sem roteiro aprovado

**Épico:** EPIC-200 UX e fluxo de produto  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/19_STORY_MAP.md`

### História
Como QA, eu quero bloquear a etapa de cenas sem aprovação, para preservar o fluxo de validação humana.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: UI aprovação.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `UI-202` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `UI-202` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## UI-203 — Resgatar telas de logs, métricas e diagnóstico

**Épico:** EPIC-200 UX e fluxo de produto  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/19_STORY_MAP.md`

### História
Como operador, eu quero ver logs, métricas e diagnóstico copiável, para debugar sem depender do terminal.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Observabilidade UI.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `UI-203` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `UI-203` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## ARCH-300 — Criar use cases por etapa

**Épico:** EPIC-300 Arquitetura limpa  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 8 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/04_ARQUITETURA_ALVO.md`

### História
Como arquiteto, eu quero que UI/API chamem use cases, para reduzir acoplamento com pipeline/adapters.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Use cases.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `ARCH-300` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `ARCH-300` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa  
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## ARCH-301 — Criar Result Object padrão ✅ CONCLUÍDA

**Épico:** EPIC-300 Arquitetura limpa  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/04_ARQUITETURA_ALVO.md`

### História
Como desenvolvedor, eu quero respostas padronizadas de sucesso/falha, para não propagar exceções e mensagens genéricas.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Result object.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `ARCH-301` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `ARCH-301` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa  
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## ARCH-302 — Centralizar configuração e paths

**Épico:** EPIC-300 Arquitetura limpa  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/12_DEPENDENCIAS_E_BLOQUEIOS.md`

### História
Como operador local, eu quero paths configuráveis e K-friendly, para evitar hardcoded C: e ambiente quebrado.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Config paths.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `ARCH-302` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `ARCH-302` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## PROV-300 — Preservar registry de providers LLM

**Épico:** EPIC-400 Providers e fallbacks  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/LLM_PROVIDER_PLAYBOOK.md`

### História
Como usuário offline, eu quero múltiplos providers locais preservados, para continuar criando roteiros sem cloud obrigatória. 

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Provider registry. 

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade. 
- Teste(s) existentes ou ausência documentada. 
- Impacto na Feature Preservation Matrix, se aplicável. 

### Critérios de aceite
Ver `PROV-300` em `07_CRITERIOS_ACEITE_GHERKIN.md`. 

### Testes
Ver `PROV-300` em `08_PLANO_DE_TESTES.md`. 

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa  
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [ ] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## PROV-301 — Garantir TemplateProvider como fallback ✅

**Épico:** EPIC-400 Providers e fallbacks  
**Prioridade:** Alta  
**Status:** Concluída  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/LLM_PROVIDER_PLAYBOOK.md`

### História
Como usuário sem LLM local, eu quero fallback template, para gerar roteiro mínimo quando provider falhar.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Template fallback.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `PROV-301` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `PROV-301` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## PROV-302 — Criar testes de provider fallback

**Épico:** EPIC-400 Providers e fallbacks  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/LLM_PROVIDER_PLAYBOOK.md`

### História
Como QA, eu quero teste de falha de LLM → template, para evitar regressão de fallback.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Provider tests.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `PROV-302` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `PROV-302` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## PIPE-400 — Criar JobState formal

**Épico:** EPIC-500 Pipeline confiável  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/17_REFACTORING_PLAN.md`

### História
Como operador, eu quero status claro por job/etapa, para acompanhar queued/running/succeeded/failed/canceled.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: JobState.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `PIPE-400` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `PIPE-400` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## PIPE-401 — Criar idempotency key por etapa

**Épico:** EPIC-500 Pipeline confiável  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/17_REFACTORING_PLAN.md`

### História
Como usuário com GPU limitada, eu quero evitar rerender duplicado, para economizar tempo e VRAM.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Idempotency.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `PIPE-401` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `PIPE-401` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## PIPE-402 — Criar cache por hash de artefatos

**Épico:** EPIC-500 Pipeline confiável  
**Prioridade:** Média  
**Status:** Concluída ✅  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/17_REFACTORING_PLAN.md`

### História
Como usuário, eu quero reaproveitar resultados idênticos, para acelerar iterações e evitar custo repetido.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Cache.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `PIPE-402` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `PIPE-402` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## PIPE-403 — Definir SQLite WAL/job ledger P1

**Épico:** EPIC-500 Pipeline confiável  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/17_REFACTORING_PLAN.md`

### História
Como desenvolvedor, eu quero um ledger local de jobs, para rastrear progresso sem Redis obrigatório.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Job ledger.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `PIPE-403` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `PIPE-403` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VIS-500 — Criar schema Ingredient Registry

**Épico:** EPIC-600 Consistência visual  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VECTOR_MEMORY_PLAYBOOK.md`

### História
Como criador de comerciais, eu quero registrar produtos/personagens/cenários, para manter consistência entre cenas.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Ingredient Registry.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VIS-500` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VIS-500` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VIS-501 — Criar schema Visual Bible

**Épico:** EPIC-600 Consistência visual  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VECTOR_MEMORY_PLAYBOOK.md`

### História
Como diretor visual, eu quero fixar referências aprovadas, para reduzir drift visual.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Visual Bible.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VIS-501` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VIS-501` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VIS-502 — Criar schema SceneContract

**Épico:** EPIC-600 Consistência visual  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`

### História
Como pipeline, eu quero contratos por cena, para transformar roteiro em instruções testáveis.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: SceneContract.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VIS-502` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VIS-502` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VIS-503 — Criar Prompt Compiler por engine

**Épico:** EPIC-600 Consistência visual  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 8 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`

### História
Como engine router, eu quero prompts específicos por provider, para usar FFmpeg/WanGP/VACE sem gambiarra.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: PromptCompiler.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VIS-503` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VIS-503` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## RND-600 — Criar RenderPlan mínimo

**Épico:** EPIC-700 Render e performance  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`

### História
Como render planner, eu quero escolher engine por cena com motivo, para usar GPU e fallback com previsibilidade.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: RenderPlan.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `RND-600` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `RND-600` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## RND-601 — Manter FFmpeg como fallback universal

**Épico:** EPIC-700 Render e performance  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`

### História
Como usuário, eu quero exportar mesmo sem engine IA, para sempre obter um MP4 mínimo.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: FFmpeg fallback.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `RND-601` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `RND-601` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## RND-602 — Adicionar perfil GTX 1660 Super

**Épico:** EPIC-700 Render e performance  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`

### História
Como usuário com 6GB VRAM, eu quero perfil seguro 480p/512p, para evitar OOM e travamentos.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: GPU Budget.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `RND-602` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `RND-602` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## RND-603 — Registrar Wan VACE 1.3B como futuro opcional

**Épico:** EPIC-700 Render e performance  
**Prioridade:** Baixa  
**Status:** Pendente  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`

### História
Como arquiteto, eu quero documentar VACE como futuro adapter, para não forçar engine pesada agora.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Wan VACE TODO.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `RND-603` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `RND-603` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## AUD-700 — Criar AudioPlan e narration_script.md

**Épico:** EPIC-800 Audio  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/AUDIO_TTS_PROVIDER_PLAYBOOK.md`

### História
Como produtor de vídeo, eu quero roteiro de narração por cena, para controlar TTS, SRT e revisão humana.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: AudioPlan.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `AUD-700` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `AUD-700` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## AUD-701 — Gerar áudio por cena com fallback

**Épico:** EPIC-800 Audio  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/AUDIO_TTS_PROVIDER_PLAYBOOK.md`

### História
Como usuário, eu quero audio/scene_XXX.wav quando TTS funcionar, para sincronizar narração com cenas.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Per-scene audio.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `AUD-701` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `AUD-701` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## AUD-702 — Gerar SRT por timing de cena

**Épico:** EPIC-800 Audio  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/AUDIO_TTS_PROVIDER_PLAYBOOK.md`

### História
Como criador de conteúdo, eu quero legendas básicas, para usar vídeo em redes sociais sem áudio.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: SRT.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `AUD-702` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `AUD-702` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## AUD-703 — Criar SFX manifest

**Épico:** EPIC-800 Audio  
**Prioridade:** Baixa  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/AUDIO_TTS_PROVIDER_PLAYBOOK.md`

### História
Como produtor, eu quero registrar licença e origem de SFX, para evitar uso indevido de assets.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: SFX manifest.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `AUD-703` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `AUD-703` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VEC-800 — Criar VectorStoreAdapter sem runtime obrigatório

**Épico:** EPIC-900 IA vetorial futura  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VECTOR_MEMORY_PLAYBOOK.md`

### História
Como arquiteto, eu quero uma porta vetorial opcional, para preparar memória sem acoplar backend.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: VectorStoreAdapter.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VEC-800` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VEC-800` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VEC-801 — Criar MemoryQualityGate

**Épico:** EPIC-900 IA vetorial futura  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VECTOR_MEMORY_PLAYBOOK.md`

### História
Como QA de dados, eu quero impedir indexação de rascunho ruim, para evitar contaminação semântica.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: MemoryQualityGate.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VEC-801` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VEC-801` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VEC-802 — Planejar Qdrant local opcional

**Épico:** EPIC-900 IA vetorial futura  
**Prioridade:** Baixa  
**Status:** Pendente  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VECTOR_MEMORY_PLAYBOOK.md`

### História
Como arquiteto, eu quero Qdrant local como backend alvo, para evoluir com payload e filtros.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Qdrant.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VEC-802` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VEC-802` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## VEC-803 — Planejar Chroma como protótipo opcional

**Épico:** EPIC-900 IA vetorial futura  
**Prioridade:** Baixa  
**Status:** Pendente  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VECTOR_MEMORY_PLAYBOOK.md`

### História
Como desenvolvedor, eu quero Chroma como caminho rápido, para testar retrieval textual com baixo atrito.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Chroma.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `VEC-803` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `VEC-803` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## OBS-900 — Criar logs estruturados por etapa

**Épico:** EPIC-1000 Observabilidade  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/04_ARQUITETURA_ALVO.md`

### História
Como operador, eu quero eventos por etapa com CAUSA|CORREÇÃO, para diagnosticar falhas sem olhar código.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Logs.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `OBS-900` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `OBS-900` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## OBS-901 — Criar métricas mínimas por job

**Épico:** EPIC-1000 Observabilidade  
**Prioridade:** Alta  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/04_ARQUITETURA_ALVO.md`

### História
Como PO técnico, eu quero medir tempo, fallback e erro por etapa, para priorizar melhorias reais.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Métricas.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `OBS-901` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `OBS-901` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## QA-1002 — Criar teste UI não chama adapters

**Épico:** EPIC-1100 QA contínuo  
**Prioridade:** Média  
**Status:** Concluída  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/04_ARQUITETURA_ALVO.md`

### História
Como arquiteto, eu quero impedir acoplamento UI→adapter, para proteger separação de responsabilidades.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Import boundary.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `QA-1002` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `QA-1002` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [x] Commit criado

## QA-1003 — Criar teste E2E WanGP falha → FFmpeg

**Épico:** EPIC-1100 QA contínuo  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 5 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`

### História
Como QA, eu quero validar fallback real do pipeline, para garantir MP4 mesmo sem IA de vídeo.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: E2E fallback.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `QA-1003` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `QA-1003` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## QA-1004 — Criar teste TTS falha → export sem áudio

**Épico:** EPIC-1100 QA contínuo  
**Prioridade:** Média  
**Status:** Concluída  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/AUDIO_TTS_PROVIDER_PLAYBOOK.md`

### História
Como QA, eu quero validar que TTS não bloqueia MP4, para preservar entrega final.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: TTS fallback.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `QA-1004` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `QA-1004` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## SEC-1100 — Criar política MCP seguro

**Épico:** EPIC-1200 Segurança e ferramentas  
**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `mcp/README_MCP_OPTIONAL.md`

### História
Como operador do agente, eu quero MCP desabilitado por padrão, para evitar ferramentas amplas sem revisão.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: MCP safe.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `SEC-1100` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `SEC-1100` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado

## QA-1000 — Criar teste antirregressão de naming

**Prioridade:** Alta  
**Status:** Concluída ✅  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/reference/PROJECT_REFERENCE_CONTEXT.md`

### História
Como mantenedor, eu quero um teste automatizado que detecte nomes legados (FlowForgeAI, Gal AI, etc.) em arquivos .py e .md, para preservar a identidade GalFlowAI.

### Contexto técnico
- Nomes legados estavam espalhados por 15+ arquivos .py e 30+ .md
- O commit de rename ee05f5c (REF-01) foi incompleto
- O teste usa git grep e busca recursiva para detectar regressões
- Windows encoding issue: subprocess requer encoding=utf-8

### Evidências obrigatórias
- `tests/test_naming_regression.py` — 5 testes
- 5/5 passando após 3 iterações de fix

### Critérios de aceite
1. ✅ Teste detecta FlowForgeAI em .py e .md
2. ✅ Teste detecta Gal AI em .py e .md
3. ✅ Teste verifica arquivos chave usam GalFlowAI
4. ✅ Teste verifica commit REF-01 existe
5. ✅ Teste verifica git grep não encontra FlowForgeAI em tracked files

### Testes
`tests/test_naming_regression.py` — execução: `pytest tests/test_naming_regression.py -v`

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [ ] Commit criado

## QA-1001 — Criar teste de presença de providers/fallbacks

**Prioridade:** Alta  
**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Arquivo de contexto obrigatório:** `docs/reference/FEATURE_PRESERVATION_MATRIX.md`

### História
Como mantenedor, eu quero um teste que verifique a presença de todos os providers e fallbacks obrigatórios, para preservar a operação local-first.

### Contexto técnico
- 5 LLM providers: TemplateProvider, LMStudioProvider, KoboldCppProvider, LlamaCppProvider, GPT4AllProvider
- Fallback chain: LM Studio > KoboldCpp > LlamaCpp > GPT4All > TemplateProvider (sempre disponível)
- TTS: TTSAdapter com silence fallback (sempre disponível)
- Vídeo: WanGPAdapter (primário) + FFmpegAdapter (fallback obrigatório)
- Matrix: FEATURE_PRESERVATION_MATRIX.md com 10 itens obrigatórios

### Evidências obrigatórias
- `tests/test_provider_presence.py` — 8 testes
- 8/8 passando

### Critérios de aceite
1. ✅ Teste verifica todos os 5 LLM provider files existem
2. ✅ Teste verifica classes dos providers existem nos arquivos
3. ✅ Teste verifica fallback files existem (TTS, vídeo, router)
4. ✅ Teste verifica ProviderRouter referencia TemplateProvider como fallback
5. ✅ Teste verifica TTSAdapter tem silence fallback
6. ✅ Teste verifica FFmpegAdapter como vídeo fallback + WanGP primário
7. ✅ Teste verifica FEATURE_PRESERVATION_MATRIX entradas obrigatórias
8. ✅ Teste verifica referências nos config_models.py

### Testes
`tests/test_provider_presence.py` — execução: `pytest tests/test_provider_presence.py -v`

### Definition of Ready
- [x] Independente
- [x] Negociável
- [x] Valiosa
- [x] Estimável
- [x] Pequena o suficiente
- [x] Testável
- [x] Possui contexto técnico
- [x] Possui arquivo de referência
- [x] Possui critérios Gherkin
- [x] Possui teste planejado

### Definition of Done
- [x] Critérios atendidos
- [x] Testes criados/atualizados
- [x] Docs e backlog atualizados
- [x] Status executivo atualizado
- [x] Daily log atualizado
- [ ] Commit criado

## SEC-1101 — Criar política de secrets e arquivos sensíveis

**Prioridade:** Média  
**Status:** Pendente  
**Estimativa:** 2 SP  
**Arquivo de contexto obrigatório:** `docs/project-control/12_DEPENDENCIAS_E_BLOQUEIOS.md`

### História
Como mantenedor, eu quero evitar commit de chaves e paths pessoais, para proteger ambiente e clientes.

### Contexto técnico
Esta história deve ser validada no código e no histórico Git antes de implementação. Se a evidência não existir, registrar `EVIDÊNCIA INSUFICIENTE` no status executivo. Contexto funcional: Secrets.

### Evidências obrigatórias
- Arquivo(s) atual(is) relacionados.
- Commit(s) que criaram/alteraram/removeram a capacidade.
- Teste(s) existentes ou ausência documentada.
- Impacto na Feature Preservation Matrix, se aplicável.

### Critérios de aceite
Ver `SEC-1101` em `07_CRITERIOS_ACEITE_GHERKIN.md`.

### Testes
Ver `SEC-1101` em `08_PLANO_DE_TESTES.md`.

### Definition of Ready
- [ ] Independente
- [ ] Negociável
- [ ] Valiosa
- [ ] Estimável
- [ ] Pequena o suficiente
- [ ] Testável
- [ ] Possui contexto técnico
- [ ] Possui arquivo de referência
- [ ] Possui critérios Gherkin
- [ ] Possui teste planejado

### Definition of Done
- [ ] Critérios atendidos
- [ ] Testes criados/atualizados
- [ ] Docs e backlog atualizados
- [ ] Status executivo atualizado
- [ ] Daily log atualizado
- [ ] Commit criado
