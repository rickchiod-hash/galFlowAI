# LLM_PROVIDER_PLAYBOOK — GalFlowAI

## Visão geral

Este playbook documenta os providers de LLM do GalFlowAI. O sistema suporta múltiplos providers locais opcionais com um TemplateProvider como fallback universal. Nenhum provider LLM depende de cloud/API paga obrigatória.

Providers atualmente registrados:
- **TemplateProvider** — fallback universal, gera roteiro mínimo sem LLM
- **LMStudioProvider** — conexão com LM Studio local
- **KoboldCppProvider** — conexão com KoboldCpp
- **LlamaCppProvider** — conexão com llama.cpp
- **GPT4AllProvider** — conexão com GPT4All

## Stories mapeadas

| Story ID | Título | Status | SP | Prioridade | DoR completo |
|----------|--------|--------|----|-----------|-------------|
| PROV-300 | Preservar registry de providers LLM | Concluída | 5 | Alta | Sim |
| PROV-301 | Garantir TemplateProvider como fallback | Concluída | 3 | Alta | Sim |
| PROV-302 | Criar testes de provider fallback | Concluída | 3 | Alta | Sim |

### PROV-300 — Preservar registry de providers LLM

**Status:** Concluída  
**Estimativa:** 5 SP  
**Épico:** EPIC-400 Providers e fallbacks  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#prov-300`  
**Testes:** `08_PLANO_DE_TESTES.md#prov-300`  

Garantir que todos os 5 providers LLM (TemplateProvider, LMStudioProvider, KoboldCppProvider, LlamaCppProvider, GPT4AllProvider) permaneçam registrados e funcionais. Provider existente não pode ser removido sem ADR.

### PROV-301 — Garantir TemplateProvider como fallback

**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Épico:** EPIC-400 Providers e fallbacks  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#prov-301`  
**Testes:** `08_PLANO_DE_TESTES.md#prov-301`  

Quando todos os providers LLM falham, o TemplateProvider deve gerar um roteiro mínimo para não bloquear o pipeline. O fallback deve ser testado e garantido.

### PROV-302 — Criar testes de provider fallback

**Status:** Concluída  
**Estimativa:** 3 SP  
**Épico:** EPIC-400 Providers e fallbacks  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#prov-302`  
**Testes:** `08_PLANO_DE_TESTES.md#prov-302`  

Criar testes automatizados que validam: (1) falha de LLM → template funciona, (2) registry contém todos os providers, (3) fallback chain está correta.

**Arquivos:**
- `tests/test_provider_fallback.py` — 21 testes (TemplateProvider, config, fallback chain mockado)
- `tests/test_template_fallback.py` — pré-existente (4 testes legados)

## Arquitetura / Decisões

### Registry pattern
Os providers são registrados via dicionário/registry no módulo de providers. A resolução usa chain-of-responsibility: tentativa → falha → próximo.

### TemplateProvider
Provider sintético que não depende de modelo carregado. Gera saída formatada com placeholders. Usado como fallback final.

### Preservação de providers
Nenhum provider existente pode ser removido sem ADR (ver `11_DECISOES_TECNICAS_ADR.md`). Todo provider novo deve ser opcional.

## Regras de preservação

1. **Provider novo deve ser opcional** — nunca obrigatório para o pipeline básico
2. **Provider existente não pode ser removido sem ADR** — documentar motivo, impacto, data
3. **TemplateProvider é fallback obrigatório** — não pode ser removido ou despriorizado
4. **Registry deve ser testado** — PROV-302 cobre teste de presença
5. **Todos os providers LLM devem ser local-first** — sem dependência de cloud/API paga

## Referências

- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — PROV-300, PROV-301, PROV-302
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — descrição detalhada (linhas 806-942)
- `docs/project-control/07_CRITERIOS_ACEITE_GHERKIN.md` — critérios Gherkin
- `docs/project-control/08_PLANO_DE_TESTES.md` — plano de testes
- `docs/project-control/11_DECISOES_TECNICAS_ADR.md` — ADRs de provider
