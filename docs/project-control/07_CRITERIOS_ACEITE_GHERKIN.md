# 07_CRITERIOS_ACEITE_GHERKIN — GalFlowAI

Critérios binários. Evite subjetividade. Use Dado/Quando/Então.

## GOV-001 — Criar checkpoint diário permanente

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/00_STATUS_EXECUTIVO.md` e validou o estado real no Git/código  
Quando a história `GOV-001` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## GOV-002 — Criar fonte de verdade do produto

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/reference/PROJECT_REFERENCE_CONTEXT.md` e validou o estado real no Git/código  
Quando a história `GOV-002` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## GOV-003 — Criar matriz de preservação de features

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/reference/FEATURE_PRESERVATION_MATRIX.md` e validou o estado real no Git/código  
Quando a história `GOV-003` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## GOV-004 — Padronizar TODOs rastreáveis

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/09_GAPS_TODOS_E_DIVIDAS.md` e validou o estado real no Git/código  
Quando a história `GOV-004` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## GOV-005 — Criar ADR obrigatório para remoções

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/11_DECISOES_TECNICAS_ADR.md` e validou o estado real no Git/código  
Quando a história `GOV-005` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## GOV-006 — Adicionar AGENTS e Skill do GalFlowAI

### Cenário 1 — Caminho feliz

Dado que o agente leu `AGENTS.md e .opencode/skills/galflowai/SKILL.md` e validou o estado real no Git/código  
Quando a história `GOV-006` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## CORE-100 — Auditar histórico Git desde o primeiro commit

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/01_AUDITORIA_HISTORICO_GIT.md` e validou o estado real no Git/código  
Quando a história `CORE-100` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## CORE-101 — Mapear estado atual do projeto

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/02_MAPA_ATUAL_DO_PROJETO.md` e validou o estado real no Git/código  
Quando a história `CORE-101` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## CORE-102 — Validar diferença entre documentação e código

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/03_ARQUITETURA_ATUAL.md` e validou o estado real no Git/código  
Quando a história `CORE-102` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## UI-200 — Restaurar fluxo por etapas na documentação

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/19_STORY_MAP.md` e validou o estado real no Git/código  
Quando a história `UI-200` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## UI-201 — Gerar roteiro sem renderizar vídeo

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/19_STORY_MAP.md` e validou o estado real no Git/código  
Quando a história `UI-201` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## UI-202 — Bloquear cenas sem roteiro aprovado

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/19_STORY_MAP.md` e validou o estado real no Git/código  
Quando a história `UI-202` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## UI-203 — Resgatar telas de logs, métricas e diagnóstico

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/19_STORY_MAP.md` e validou o estado real no Git/código  
Quando a história `UI-203` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## ARCH-300 — Criar use cases por etapa

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/04_ARQUITETURA_ALVO.md` e validou o estado real no Git/código  
Quando a história `ARCH-300` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## ARCH-301 — Criar Result Object padrão

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/04_ARQUITETURA_ALVO.md` e validou o estado real no Git/código  
Quando a história `ARCH-301` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## ARCH-302 — Centralizar configuração e paths

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/12_DEPENDENCIAS_E_BLOQUEIOS.md` e validou o estado real no Git/código  
Quando a história `ARCH-302` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## PROV-300 — Preservar registry de providers LLM

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/LLM_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `PROV-300` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## PROV-301 — Garantir TemplateProvider como fallback

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/LLM_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `PROV-301` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## PROV-302 — Criar testes de provider fallback

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/LLM_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `PROV-302` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## PIPE-400 — Criar JobState formal

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/17_REFACTORING_PLAN.md` e validou o estado real no Git/código  
Quando a história `PIPE-400` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## PIPE-401 — Criar idempotency key por etapa

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/17_REFACTORING_PLAN.md` e validou o estado real no Git/código  
Quando a história `PIPE-401` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## PIPE-402 — Criar cache por hash de artefatos

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/17_REFACTORING_PLAN.md` e validou o estado real no Git/código  
Quando a história `PIPE-402` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## PIPE-403 — Definir SQLite WAL/job ledger P1

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/17_REFACTORING_PLAN.md` e validou o estado real no Git/código  
Quando a história `PIPE-403` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VIS-500 — Criar schema Ingredient Registry

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VECTOR_MEMORY_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VIS-500` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VIS-501 — Criar schema Visual Bible

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VECTOR_MEMORY_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VIS-501` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VIS-502 — Criar schema SceneContract

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VIS-502` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VIS-503 — Criar Prompt Compiler por engine

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VIS-503` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## RND-600 — Criar RenderPlan mínimo

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `RND-600` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## RND-601 — Manter FFmpeg como fallback universal

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `RND-601` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## RND-602 — Adicionar perfil GTX 1660 Super

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `RND-602` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## RND-603 — Registrar Wan VACE 1.3B como futuro opcional

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `RND-603` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## AUD-700 — Criar AudioPlan e narration_script.md

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/AUDIO_TTS_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `AUD-700` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## AUD-701 — Gerar áudio por cena com fallback

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/AUDIO_TTS_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `AUD-701` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## AUD-702 — Gerar SRT por timing de cena

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/AUDIO_TTS_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `AUD-702` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## AUD-703 — Criar SFX manifest

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/AUDIO_TTS_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `AUD-703` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VEC-800 — Criar VectorStoreAdapter sem runtime obrigatório

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VECTOR_MEMORY_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VEC-800` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VEC-801 — Criar MemoryQualityGate

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VECTOR_MEMORY_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VEC-801` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VEC-802 — Planejar Qdrant local opcional

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VECTOR_MEMORY_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VEC-802` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## VEC-803 — Planejar Chroma como protótipo opcional

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VECTOR_MEMORY_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `VEC-803` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## OBS-900 — Criar logs estruturados por etapa

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/04_ARQUITETURA_ALVO.md` e validou o estado real no Git/código  
Quando a história `OBS-900` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## OBS-901 — Criar métricas mínimas por job

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/04_ARQUITETURA_ALVO.md` e validou o estado real no Git/código  
Quando a história `OBS-901` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## QA-1000 — Criar teste antirregressão de naming

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/reference/FEATURE_PRESERVATION_MATRIX.md` e validou o estado real no Git/código  
Quando a história `QA-1000` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## QA-1001 — Criar teste de presença de providers/fallbacks

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/reference/FEATURE_PRESERVATION_MATRIX.md` e validou o estado real no Git/código  
Quando a história `QA-1001` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## QA-1002 — Criar teste UI não chama adapters

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/04_ARQUITETURA_ALVO.md` e validou o estado real no Git/código  
Quando a história `QA-1002` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## QA-1003 — Criar teste E2E WanGP falha → FFmpeg

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `QA-1003` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## QA-1004 — Criar teste TTS falha → export sem áudio

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/playbooks/AUDIO_TTS_PROVIDER_PLAYBOOK.md` e validou o estado real no Git/código  
Quando a história `QA-1004` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## SEC-1100 — Criar política MCP seguro

### Cenário 1 — Caminho feliz

Dado que o agente leu `mcp/README_MCP_OPTIONAL.md` e validou o estado real no Git/código  
Quando a história `SEC-1100` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio

## SEC-1101 — Criar política de secrets e arquivos sensíveis

### Cenário 1 — Caminho feliz

Dado que o agente leu `docs/project-control/12_DEPENDENCIAS_E_BLOQUEIOS.md` e validou o estado real no Git/código  
Quando a história `SEC-1101` for executada  
Então o resultado deve ser registrado com evidência, arquivos alterados, testes e atualização do status executivo

### Cenário 2 — Evidência insuficiente

Dado que o agente não encontrou arquivo, commit ou teste que comprove a hipótese  
Quando ele for atualizar a história  
Então deve marcar `EVIDÊNCIA INSUFICIENTE` e não deve afirmar que a funcionalidade existe

### Cenário 3 — Regressão protegida

Dado que a história impacta feature obrigatória da matriz  
Quando a alteração for feita  
Então o teste de regressão correspondente deve existir ou a pendência deve ser registrada como bloqueio
