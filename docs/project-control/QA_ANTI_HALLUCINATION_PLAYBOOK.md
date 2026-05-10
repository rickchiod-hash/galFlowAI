# QA_ANTI_HALLUCINATION_PLAYBOOK — GalFlowAI

## Visão geral

Este playbook documenta as políticas de QA e anti-alucinação do GalFlowAI. Define testes automatizados que preservam a integridade do código e previnem regressões. A camada de QA é contínua e executada em todo build.

Domínios de QA cobertos:
- **Antirregressão de naming** — detecta nomes legados (FlowForgeAI, Gal AI, etc.)
- **Presença de providers** — verifica que providers e fallbacks não foram removidos
- **Barreira de importação** — impede que UI chame adapters diretamente
- **Fallback E2E** — valida fallback WanGP → FFmpeg (ver `VIDEO_RENDER_PROVIDER_PLAYBOOK.md`)
- **TTS fallback** — valida que falha de TTS não bloqueia MP4 (ver `AUDIO_TTS_PROVIDER_PLAYBOOK.md`)

## Stories mapeadas

| Story ID | Título | Status | SP | Prioridade | DoR completo |
|----------|--------|--------|----|-----------|-------------|
| QA-1000 | Criar teste antirregressão de naming | Concluída | 2 | Alta | Sim |
| QA-1001 | Criar teste de presença de providers/fallbacks | Concluída | 3 | Alta | Sim |
| QA-1002 | Criar teste UI não chama adapters | Concluída | 3 | Média | Sim |

### QA-1000 — Criar teste antirregressão de naming

**Status:** Concluída ✅  
**Estimativa:** 2 SP  
**Épico:** EPIC-1100 QA contínuo  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#qa-1000`  
**Testes:** `08_PLANO_DE_TESTES.md#qa-1000`  

Teste automatizado que detecta nomes legados (FlowForgeAI, Gal AI, etc.) em arquivos .py e .md. Usa git grep e busca recursiva. Preserva a identidade GalFlowAI.

**Evidência:** `tests/test_naming_regression.py` — 5/5 testes passando.

### QA-1001 — Criar teste de presença de providers/fallbacks

**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Épico:** EPIC-1100 QA contínuo  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#qa-1001`  
**Testes:** `08_PLANO_DE_TESTES.md#qa-1001`  

Teste que verifica a presença de todos os providers e fallbacks obrigatórios: 5 LLM providers + TemplateProvider como fallback + FFmpeg como fallback de render.

### QA-1002 — Criar teste UI não chama adapters

**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Épico:** EPIC-1100 QA contínuo  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#qa-1002`  
**Testes:** `08_PLANO_DE_TESTES.md#qa-1002`  

Teste que impede importação direta de adapters pela camada UI. Preserva a separação de responsabilidades (UI → use cases → adapters).

## Políticas anti-alucinação

### 1. Verificação de fontes
Nenhuma resposta do agente deve afirmar existência de código, funcionalidade ou teste sem evidência. Toda afirmação deve referenciar arquivo, linha ou commit.

### 2. Preservação de contexto
Antes de alterar qualquer arquivo, ler os arquivos de contexto obrigatórios definidos na história. Não presumir estrutura ou comportamento.

### 3. Testes como barreira
Todo PR deve passar pelos testes de QA. Falha de teste bloqueia merge. Testes de presença (QA-1001) rodam em todo build.

### 4. Naming legado
FlowForgeAI, Gal AI, e outros nomes legados são proibidos em qualquer arquivo. O teste QA-1000 detecta regressões automaticamente.

### 5. Provider/fremover
Nenhum provider existente pode ser removido sem ADR. O teste QA-1001 detecta remoção não documentada.

### 6. Separação de camadas
UI nunca chama adapters diretamente. Use cases são a ponte obrigatória. QA-1002 valida essa regra.

## Testes vinculados a outros playbooks

As seguintes stories de QA dependem de playbooks específicos e estão documentadas neles:

| Story | Playbook | Descrição |
|-------|----------|-----------|
| QA-1003 | `VIDEO_RENDER_PROVIDER_PLAYBOOK.md` | Teste E2E fallback WanGP → FFmpeg |
| QA-1004 | `AUDIO_TTS_PROVIDER_PLAYBOOK.md` | Teste TTS falha → export sem áudio |

## Regras de preservação

1. **QA-1000, QA-1001, QA-1002 são obrigatórios** — rodam em todo build
2. **Teste de naming (QA-1000) é o primeiro a rodar** — detecta contaminação legada
3. **Nenhum provider pode ser removido sem QA-1001 detectar** — o teste valida presença
4. **UI nunca importa adapter** — QA-1002 é barreira de arquitetura
5. **Anti-alucinação é política, não código** — documentada aqui, executada por revisão

## Referências

- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — QA-1000, QA-1001, QA-1002
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — descrição detalhada (linhas 1956-2092)
- `docs/project-control/07_CRITERIOS_ACEITE_GHERKIN.md` — critérios Gherkin
- `docs/project-control/08_PLANO_DE_TESTES.md` — plano de testes
- `docs/reference/FEATURE_PRESERVATION_MATRIX.md` — matriz de preservação
- `tests/test_naming_regression.py` — implementação do teste QA-1000
