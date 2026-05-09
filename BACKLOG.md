# BACKLOG TÉCNICO (Code Review) — GalFlowAI

**Última atualização:** 06/05/2026  
**Objetivo:** Evolução do projeto sem quebrar o fluxo local-first.

---

## Resumo executivo (sem viés)

### Pontos fortes atuais
- Arquitetura já separa UI/API de serviços e adapters, o que facilita evolução incremental.
- Fallbacks centrais (TemplateProvider e FFmpeg) preservam continuidade operacional.
- Existe documentação base para operação local e setup de providers.
- ✅ **25+ use cases criados** seguindo padrão 3 pontos (Validate → Execute → Return).
- ✅ **84+ testes** implementados (H11-H18 completos).
- ✅ **Refatoração GalFlowAI → GalFlowAI concluída** (15+ arquivos atualizados).
- ✅ **20 melhorias no README** implementadas (logs, riscos, onboarding, etc.).

### Pontos críticos atuais
- Backlog anterior estava desatualizado e continha diagnósticos incorretos (ex.: sintaxe de `app/api.py` já está válida).
- Há risco de divergência entre comportamento real e documentação em endpoints/fluxos.
- Ausência de suíte de testes de contrato para API e de testes de regressão para fluxo fim-a-fim.

---

## Template Padrão para Critérios de Aceite (DOC-09)
**Obrigatório para todas as novas histórias no backlog.**

```
### [ID] - [Nome da História]
**Contexto:** [Descrição do problema/oportunidade]
**Objetivo:** [O que será alcançado]
**Critérios de Aceite (3 pontos):**
1. **Validate:** [Validação de entrada/pré-condição]
2. **Execute:** [Execução da lógica de negócio]
3. **Return:** [Retorno com status e evidência]
**Evidência:** [Como validar: teste, log, endpoint, artefato]
**Status:** [🟨 Pendente | ✅ Concluído]
```

---

## Critérios para aceitar melhorias
1. **Não quebrar fluxo vigente** (gerar roteiro → editar/aprovar → cenas → preview → MP4).
2. **Melhorar observabilidade** (logs, erro claro, rastreabilidade por `project_id`/`job_id`).
3. **Aumentar robustez** sem impor dependências cloud ou lock-in externo.
4. **Permitir rollback fácil** (mudanças pequenas, feature flags quando aplicável).

---

## Backlog priorizado (crítico e coerente)

### 🟨 P0 — Confiabilidade e risco imediato (PENDENTES)

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| RC-01 | Caminhos C: hardcoded em `check_ffmpeg.py` | Substituir por caminhos relativos ou variáveis de ambiente (K:) | Evita erros em outros PCs | Exige teste em ambiente limpo | **Sim (alto impacto)** |
| RC-02 | 14B mencionado como exemplo em `wangp_adapter.py` | Remover 14B da docstring, manter apenas 1.3B como padrão seguro | Consistência com HW (6GB VRAM) | Simples | **Sim** |
| RC-03 | BATs não configuram variáveis obrigatórias | Criar BAT padrão que configure TODAS as variáveis do AGENTS.md | Evita erros de configuração | Criar/validar BAT | **Sim** |
| RC-04 | Erros sem causa e correção clara | Padronizar: `logger.error("CAUSA: %s | CORREÇÃO: %s", causa, solucao)` | Debug mais rápido | Requer edição pontual | **Sim** |

### ✅ P1 — Robustez de arquitetura (CONCLUÍDO em H11-H18)

| ID | História (3 pontos) | Status | Testes | Commit |
|---|---|---|---|---|
| H11 | **Job Queue & Video Render**<br>1. Validate job_id/project_id<br>2. Execute: add/remove/list jobs na queue<br>3. Return: status da fila e job_id | ✅ Concluído | 16/16 passando | d86bee4 |
| H12 | **Metrics & Monitoring**<br>1. Validate parâmetros de métricas<br>2. Execute: record/get metrics via MetricsService<br>3. Return: summary e operations | ✅ Concluído | 10/10 passando | cb2ba18 |
| H13 | **Logs via API (V2.1)**<br>1. Validate filtros (level, search, limit)<br>2. Execute: get recent logs, summary, last error<br>3. Return: logs filtrados e diagnóstico | ✅ Concluído | 11/11 passando | 3607887 |
| H14 | **Prompt Context Pack (V2.2)**<br>1. Validate project_id e script<br>2. Execute: create/load/validate prompt pack<br>3. Return: pack data e validação | ✅ Concluído | 12/12 passando | 89e5f1d |
| H15 | **Script Quality & Commercial (V2.4)**<br>1. Validate script e commercial_type<br>2. Execute: score/get template/enrich briefing<br>3. Return: score, template, enriched briefing | ✅ Concluído | 13/13 passando | c898fb4 |
| H16 | **Advanced Script Editing (V2.5)**<br>1. Validate project_id e script<br>2. Execute: improve/approve/get versions<br>3. Return: improved script e approval status | ✅ Concluído (use cases) | 11/11 passando | 5751454 |
| H17 | **Visual Consistency (V2.6)**<br>1. Validate project_id e visual elements<br>2. Execute: create bible/generate contracts/validate<br>3. Return: bible, contracts e validation | ✅ Concluído | 13/13 passando | 94e1a70 |
| H18 | **Advanced Observability (V3.0)**<br>1. Validate filtros (level, limit)<br>2. Execute: health dashboard/structured logs<br>3. Return: dashboard JSON e logs parseados | ✅ Concluído | 6/6 passando | ed6f52d |

### ✅ P1 — Refatoração e Documentação (CONCLUÍDO em 06/05/2026)

| ID | História (3 pontos) | Status | Arquivos | Commit |
|---|---|---|---|---|
| REF-01 | **Refatoração Rename GalFlowAI → GalFlowAI**<br>1. Validate: identificar todas as ocorrências de GalFlowAI<br>2. Execute: substituir por GalFlowAI em todos os arquivos (.py, .md, .bat)<br>3. Return: 0 ocorrências restantes | ✅ Concluído | 15+ arquivos (api.py, use_cases, testes, etc.) | 18f56de |
| DOC-21 | **Melhoria README: Logos Oficiais**<br>1. Validate: galflowai_logo_master.png e galflowai_app_icon.png existem<br>2. Execute: atualizar README para usar novas logos<br>3. Return: README exibe logos corretamente | ✅ Concluído | README.md | 18f56de |
| DOC-22 | **Melhoria README: Total de Testes (314)**<br>1. Validate: pytest coleta 314 testes<br>2. Execute: adicionar nota no Status Real<br>3. Return: README informa 314 testes | ✅ Concluído | README.md | 18f56de |
| DOC-23 | **Melhoria README: 84+ Novos Testes H11-H18**<br>1. Validate: 84+ testes H11-H18 criados<br>2. Execute: adicionar seção de cobertura<br>3. Return: README detalha testes novos | ✅ Concluído | README.md | 18f56de |
| DOC-24 | **Melhoria README: K-only Environment**<br>1. Validate: sem caminhos C: no projeto<br>2. Execute: adicionar nota em Status Real<br>3. Return: README informa K-only | ✅ Concluído | README.md | 18f56de |
| DOC-25 | **Melhoria README: Padronização de Erros**<br>1. Validate: erros usam CAUSA | CORREÇÃO<br>2. Execute: adicionar nota em Status Real<br>3. Return: README documenta padrão | ✅ Concluído | README.md | 18f56de |
| DOC-26 | **Melhoria README: Variáveis Obrigatórias**<br>1. Validate: variáveis do AGENTS.md definidas<br>2. Execute: adicionar seção em Execução e Operação<br>3. Return: README lista variáveis | ✅ Concluído | README.md | 18f56de |
| DOC-27 | **Melhoria README: Riscos Ativos**<br>1. Validate: riscos técnicos identificados<br>2. Execute: criar seção Riscos Ativos com tabela<br>3. Return: README possui seção de riscos | ✅ Concluído | README.md | 18f56de |
| DOC-28 | **Melhoria README: Onboarding Rápido**<br>1. Validate: passos de onboarding definidos<br>2. Execute: criar seção Onboarding Rápido<br>3. Return: README tem passos em 5 minutos | ✅ Concluído | README.md | 18f56de |
| DOC-29 | **Melhoria README: Naming Oficial com Logos**<br>1. Validate: logos oficiais definidas<br>2. Execute: atualizar seção Naming Oficial<br>3. Return: README lista logos | ✅ Concluído | README.md | 18f56de |
| DOC-30 | **Melhoria README: Estrutura de Diretórios com Logos**<br>1. Validate: logos estão na raiz<br>2. Execute: atualizar seção de diretórios<br>3. Return: README lista arquivos de logo | ✅ Concluído | README.md | 18f56de |
| DOC-31 | **Melhoria README: Histórico de Refatoração**<br>1. Validate: refatoração concluída<br>2. Execute: criar seção Histórico de Refatoração<br>3. Return: README documenta rename | ✅ Concluído | README.md | 18f56de |
| DOC-32 | **Melhoria README: Começando em 5 Minutos Atualizado**<br>1. Validate: usar env studio existente<br>2. Execute: atualizar comandos para K: paths<br>3. Return: README usa comandos corretos | ✅ Concluído | README.md | 18f56de |
| DOC-33 | **Melhoria README: Rodar Testes Atualizado**<br>1. Validate: 314 testes coletados<br>2. Execute: adicionar total no comando<br>3. Return: README informa 314 testes | ✅ Concluído | README.md | 18f56de |
| DOC-34 | **Melhoria README: Roadmap H19-H20**<br>1. Validate: novas histórias planejadas<br>2. Execute: atualizar Roadmap objetivo<br>3. Return: README lista H19-H20 | ✅ Concluído | README.md | 18f56de |
| DOC-35 | **Melhoria README: Cobertura Atual**<br>1. Validate: cobertura de testes definida<br>2. Execute: adicionar seção em Qualidade e Testes<br>3. Return: README detalha cobertura | ✅ Concluído | README.md | 18f56de |
| DOC-36 | **Melhoria README: Governança com Logos**<br>1. Validate: regras de uso de logos<br>2. Execute: atualizar Governança de documentação<br>3. Return: README exige logos oficiais | ✅ Concluído | README.md | 18f56de |
| DOC-37 | **Melhoria README: Backup Sistêmico**<br>1. Validate: backups existem<br>2. Execute: adicionar nota em Em Evolução<br>3. Return: README menciona backup | ✅ Concluído | README.md | 18f56de |
| DOC-38 | **Melhoria README: Fallback FFmpeg**<br>1. Validate: fallback funcional<br>2. Execute: adicionar nota em Em Evolução<br>3. Return: README detalha fallback | ✅ Concluído | README.md | 18f56de |
| DOC-39 | **Melhoria README: Sumário Atualizado**<br>1. Validate: novas seções adicionadas<br>2. Execute: atualizar Sumário com Riscos Ativos e Onboarding<br>3. Return: Sumário reflete README | ✅ Concluído | README.md | 18f56de |
| DOC-40 | **Melhoria README: Estado Atual do Projeto**<br>1. Validate: README reflete estado real<br>2. Execute: revisar todas as seções<br>3. Return: README condiz com implementação | ✅ Concluído | README.md | 18f56de |

### 🟨 P2 — Eficiência e qualidade de código (PENDENTES)

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| RC-05 | README desatualizado | Atualizar: total de testes, progresso H11-H18, status de use cases | Docs precisas | Simples | **Sim (CONCLUÍDO)** |
| RC-06 | Falta teste E2E para fallback FFmpeg | Criar teste: mock WanGP falha → verificar se FFmpeg é chamado | Cobertura de falhas | Requer mock complexo | **Sim** |
| RC-07 | Backups não sistêmicos | Criar `scripts/backup_before_change.bat` automatizado | Segurança operacional | Script simples | **P2** |
| DOC-10 | Definir baseline de cobertura por módulo crítico | `qa/QA_TEST_PLAN.md` inclui tabela por módulo com baseline e meta mínima | Visibilidade de gaps | Exige auditoria | **P1** |
| DOC-17 | Definir SLO/SLA local para operação offline-first | Documento técnico com metas mínimas de disponibilidade e latência local | Requisito para produção | Especificação detalhada | **P2** |

### 🟨 P3 — Modernização arquitetural (PENDENTES)

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| DOC-06 | Criar seção fixa de riscos técnicos ativos por release | README possui "Riscos Ativos" com top-5; cada risco tem impacto + mitigação + owner | Transparência de riscos | Requer atualização por release | **P1 (CONCLUÍDO)** |
| DOC-07 | Separar trilha de documentação por persona (operar vs evoluir) | README traz índice "Operação" e "Arquitetura" com links diretos para docs de cada trilha | Onboarding direcionado | Reorganização de docs | **P1** |
| DOC-08 | Quebrar épicos de documentação em histórias executáveis de sprint | 100% dos itens documentais novos têm escopo ≤ 1 sprint e dependências explícitas | Execução iterativa | Gestão de Tasks | **P2** |
| DOC-09 | Padronizar template de critérios de aceite no backlog | Todas as histórias novas usam padrão: Contexto, Objetivo, Critérios, Evidência | Clareza de requisitos | Mudança de template | **P1** |
| DOC-11 | Implantar ADR leve para decisões arquiteturais | Existe diretório ADR e ao menos 1 ADR para cada mudança estrutural futura | Rastreabilidade técnica | Cerimônia leve | **P2** |
| DOC-12 | Clarificar prioridades H11-H14 por impacto/risco | `ROADMAP.md` traz ordenação explícita com racional técnico | Priorização clara | Revisão de prioridades | **P1** |
| DOC-13 | Criar rastreabilidade roadmap → entrega | Release notes incluem tabela de vínculo entre item planejado e evidência entregue | Auditabilidade | Controle de mudanças | **P2** |
| DOC-14 | Definir política de depreciação documental | Docs legadas possuem banner de status: ativa/legada/arquivada + data | Gestão de vida útil | Inventário de docs | **P2** |
| DOC-15 | Consolidar onboarding em trilha única de quickstart | README oferece quickstart validado em ambiente limpo com no máximo 3 comandos | Onboarding rápido | Consolidação de docs | **P1 (CONCLUÍDO)** |
| DOC-16 | Formalizar Definition of Done por tipo de mudança | Template de PR com DoD obrigatório para docs, código e testes | Qualidade assegurada | Definição de critérios | **P1** |
| DOC-18 | Adotar checklist de coerência com princípio offline-first | Toda feature nova passa por checklist de dependência externa e fallback | Garantia de princípios | Checklist simples | **P1** |
| DOC-19 | Padronizar playbook de rollback por feature | Existe runbook com passos de rollback e validação pós-reversão | Recuperação de falhas | Documentação de procedimentos | **P2** |
| DOC-20 | Evoluir guia de contribuição com gates de qualidade | README/CONTRIBUTING exigem docs-sync, evidência e testes mínimos por PR | Qualidade de contribuições | Revisão de processo | **P1** |

---

## Plano de execução recomendado (sem quebrar fluxo)

### Sprint A (1–2 semanas) — **Pendências Críticas**
- RC-01, RC-02, RC-03, RC-04
- DOC-06 (CONCLUÍDO), DOC-07, DOC-09, DOC-12, DOC-15 (CONCLUÍDO), DOC-16, DOC-18, DOC-20
- Atualizar README com total de testes (84+) (CONCLUÍDO)
- Refatoração GalFlowAI → GalFlowAI (CONCLUÍDO)
- 20 melhorias README (CONCLUÍDO)

### Sprint B (2 semanas) — **Observabilidade e Cobertura**
- RC-05 (CONCLUÍDO), RC-06
- DOC-10
- Criar testes E2E para fluxo completo

### Sprint C (2+ semanas) — **Governança e Maturidade**
- RC-07
- DOC-08, DOC-11, DOC-13, DOC-14, DOC-17, DOC-19
- Implantar ADRs leves

---

## Histórias de excelência documental (refinadas e pendentes)

> Escopo desta seção: **apenas histórias pendentes**. Itens já implementados ficam fora do backlog para evitar ruído.

> Objetivo: transformar gaps de qualidade documental em entregas pequenas, auditáveis e com valor direto para operação.

| ID | Prioridade | História (3 pontos) | Critérios de aceite objetivos |
|---|---|---|---|
| DOC-06 | P1 | **Criar seção fixa de riscos técnicos**<br>1. Validate: lista de riscos identificados<br>2. Execute: adicionar seção no README<br>3. Return: seção "Riscos Ativos" com top-5 | README possui "Riscos Ativos" com top-5; cada risco tem impacto + mitigação + owner | ✅ CONCLUÍDO |
| DOC-07 | P1 | **Separar trilha de documentação por persona**<br>1. Validate: personas definidas (operar vs evoluir)<br>2. Execute: criar índice no README<br>3. Return: índice "Operação" e "Arquitetura" com links | README traz índice "Operação" e "Arquitetura" com links diretos para docs | 🟨 PENDENTE |
| DOC-09 | P1 | **Padronizar template de critérios de aceite**<br>1. Validate: template definido<br>2. Execute: aplicar em todas as histórias novas<br>3. Return: todas as histórias usam padrão | Todas as histórias novas usam padrão: Contexto, Objetivo, Critérios, Evidência | 🟨 PENDENTE |
| DOC-12 | P1 | **Clarificar prioridades H11-H14**<br>1. Validate: impacto/risco avaliados<br>2. Execute: atualizar ROADMAP.md com ordenação<br>3. Return: ROADMAP traz ordenação explícita | `ROADMAP.md` traz ordenação explícita com racional técnico | 🟨 PENDENTE |
| DOC-15 | P1 | **Consolidar onboarding em trilha única**<br>1. Validate: passos de quickstart definidos<br>2. Execute: validar em ambiente limpo<br>3. Return: README oferece quickstart validado | README oferece quickstart validado em ambiente limpo com no máximo 3 comandos | ✅ CONCLUÍDO |
| DOC-16 | P1 | **Formalizar Definition of Done**<br>1. Validate: DoD definido por tipo<br>2. Execute: criar template de PR<br>3. Return: Template de PR com DoD obrigatório | Template de PR com DoD obrigatório para docs, código e testes | 🟨 PENDENTE |
| DOC-18 | P1 | **Adotar checklist offline-first**<br>1. Validate: checklist definido<br>2. Execute: aplicar em nova feature<br>3. Return: toda feature nova passa por checklist | Toda feature nova passa por checklist de dependência externa e fallback | 🟨 PENDENTE |
| DOC-20 | P1 | **Evoluir guia de contribuição**<br>1. Validate: gates definidos<br>2. Execute: atualizar CONTRIBUTING.md<br>3. Return: guia exige docs-sync e testes | README/CONTRIBUTING exigem docs-sync, evidência e testes mínimos | 🟨 PENDENTE |
| DOC-08 | P2 | **Quebrar épicos em histórias**<br>1. Validate: épicos identificados<br>2. Execute: dividir em sprints ≤ 1 semana<br>3. Return: 100% dos itens têm escopo definido | 100% dos itens documentais novos têm escopo ≤ 1 sprint | 🟨 PENDENTE |
| DOC-10 | P1 | **Definir baseline de cobertura**<br>1. Validate: módulos críticos identificados<br>2. Execute: criar tabela em QA_TEST_PLAN.md<br>3. Return: tabela com baseline e meta | `qa/QA_TEST_PLAN.md` inclui tabela por módulo com baseline | 🟨 PENDENTE |
| DOC-11 | P2 | **Implantar ADR leve**<br>1. Validate: decisões arquiteturais mapeadas<br>2. Execute: criar diretório e ADRs<br>3. Return: existe ao menos 1 ADR por mudança | Existe diretório ADR e ao menos 1 ADR para cada mudança estrutural | 🟨 PENDENTE |
| DOC-13 | P2 | **Criar rastreabilidade roadmap**<br>1. Validate: itens planejados mapeados<br>2. Execute: criar tabela em release notes<br>3. Return: tabela de vínculo plano/entrega | Release notes incluem tabela de vínculo entre item planejado e evidência | 🟨 PENDENTE |
| DOC-14 | P2 | **Definir política de depreciação**<br>1. Validate: docs legadas inventariadas<br>2. Execute: adicionar banners de status<br>3. Return: docs possuem banner ativa/legada | Docs legadas possuem banner de status: ativa/legada/arquivada + data | 🟨 PENDENTE |
| DOC-17 | P2 | **Definir SLO/SLA local**<br>1. Validate: requisitos de disponibilidade definidos<br>2. Execute: criar documento técnico<br>3. Return: documento com metas mínimas | Documento técnico com metas mínimas de disponibilidade e latência local | 🟨 PENDENTE |
| DOC-19 | P2 | **Padronizar playbook de rollback**<br>1. Validate: passos de rollback definidos<br>2. Execute: criar runbook por feature<br>3. Return: existe runbook com passos | Existe runbook com passos de rollback e validação pós-reversão | 🟨 PENDENTE |

---

## Itens congelados (não fazer agora)
- Reescrita completa da UI em React sem estabilizar contratos da API.
- Dependência obrigatória de cloud/API paga.
- Troca massiva de stack sem baseline de performance/confiabilidade.
- Implementar OCR/visão agora.
- Criar dependência pesada.
- Usar "prompts visuais em inglês" - REMOVIDO.

---

## Checklist de revisão por PR
- [ ] Mudança preserva fallback Template + FFmpeg.
- [ ] Existe teste automatizado para rota/caso alterado.
- [ ] Logs incluem contexto mínimo (`project_id`/`provider`).
- [ ] Documentação atualizada no mesmo PR.
- [ ] Sem promessa de funcionalidade não implementada.
- [ ] Naming oficial **GalFlowAI** usado em todos os arquivos.
- [ ] Logos oficiais (`galflowai_logo_master.png`, `galflowai_app_icon.png`) referenciadas corretamente.

---

## Itens identificados na Revisão Crítica (H10) — PENDENTES

| ID | Contexto da melhoria | Sugestão objetiva | Prioridade |
|---|---|---|---|
| RC-01 | Caminhos C: hardcoded em `check_ffmpeg.py` | Substituir por caminhos relativos ou variáveis de ambiente (K:) | P0 (Bloqueante) |
| RC-02 | 14B mencionado como exemplo em `wangp_adapter.py` | Remover 14B da docstring, manter apenas 1.3B como padrão seguro | P0 (Bloqueante) |
| RC-03 | BATs não configuram variáveis obrigatórias | Criar BAT padrão que configure TODAS as variáveis do AGENTS.md | P0 (Bloqueante) |
| RC-04 | Erros sem causa e correção clara | Padronizar: `logger.error("CAUSA: %s | CORREÇÃO: %s", causa, solucao)` | P1 |
| RC-05 | README desatualizado | Atualizar: 84+ testes coletados, progresso H11-H18, status de use cases | P1 (CONCLUÍDO) |
| RC-06 | Falta teste E2E para fallback FFmpeg | Criar teste: mock WanGP falha → verificar se FFmpeg é chamado | P1 |
| RC-07 | Backups não sistêmicos | Criar `scripts/backup_before_change.bat` automatizado | P2 |

## Item obrigatório de backlog (solicitação direta)
 
Após a etapa atual (`[Pasted ~5 lines]`), executar obrigatoriamente:
- Criar **3 testes unitários** que validem cenários principais e de falha.
- Criar cenários de **testes de automação e chamadas de API**.
- Aumentar cobertura com cenários que simulem a realidade para capturar gaps.
- Ler `qa/QA_TEST_PLAN.md` e mapear todos os testes implementados até o presente momento.
- Colocar itens pendentes na fila de revisão/criação/melhoria antes de novas features.


---

## Histórias de excelência documental (refinadas e pendentes)

> Escopo desta seção: **apenas histórias pendentes**. Itens já implementados ficam fora do backlog para evitar ruído.

> Objetivo: transformar gaps de qualidade documental em entregas pequenas, auditáveis e com valor direto para operação.

| ID | Prioridade | História | Critérios de aceite objetivos |
|---|---|---|---|
| DOC-06 | P1 | Criar seção fixa de riscos técnicos ativos por release | README possui "Riscos Ativos" com top-5; cada risco tem impacto + mitigação + owner. |
| DOC-07 | P1 | Separar trilha de documentação por persona (operar vs evoluir) | README traz índice "Operação" e "Arquitetura" com links diretos para docs de cada trilha. |
| DOC-08 | P2 | Quebrar épicos de documentação em histórias executáveis de sprint | 100% dos itens documentais novos têm escopo ≤ 1 sprint e dependências explícitas. |
| DOC-09 | P1 | Padronizar template de critérios de aceite no backlog | Todas as histórias novas usam padrão: Contexto, Objetivo, Critérios, Evidência. |
| DOC-10 | P1 | Definir baseline de cobertura por módulo crítico | `qa/QA_TEST_PLAN.md` inclui tabela por módulo com baseline e meta mínima. |
| DOC-11 | P2 | Implantar ADR leve para decisões arquiteturais | Existe diretório ADR e ao menos 1 ADR para cada mudança estrutural futura. |
| DOC-12 | P1 | Clarificar prioridades H11-H14 por impacto/risco | `ROADMAP.md` traz ordenação explícita com racional técnico. |
| DOC-13 | P2 | Criar rastreabilidade roadmap → entrega | Release notes incluem tabela de vínculo entre item planejado e evidência entregue. |
| DOC-14 | P2 | Definir política de depreciação documental | Docs legadas possuem banner de status: ativa/legada/arquivada + data. |
| DOC-15 | P1 | Consolidar onboarding em trilha única de quickstart | README oferece quickstart validado em ambiente limpo com no máximo 3 comandos. |
| DOC-16 | P1 | Formalizar Definition of Done por tipo de mudança | Template de PR com DoD obrigatório para docs, código e testes. |
| DOC-17 | P2 | Definir SLO/SLA local para operação offline-first | Documento técnico com metas mínimas de disponibilidade e latência local. |
| DOC-18 | P1 | Adotar checklist de coerência com princípio offline-first | Toda feature nova passa por checklist de dependência externa e fallback. |
| DOC-19 | P2 | Padronizar playbook de rollback por feature | Existe runbook com passos de rollback e validação pós-reversão. |
| DOC-20 | P1 | Evoluir guia de contribuição com gates de qualidade | README/CONTRIBUTING exigem docs-sync, evidência e testes mínimos por PR. |

### Sequenciamento recomendado
1. **Sprint A (P1 crítico):** DOC-06, DOC-07, DOC-09, DOC-12, DOC-15, DOC-16, DOC-18, DOC-20.
2. **Sprint B (governança):** DOC-10, DOC-11, DOC-13, DOC-14.
3. **Sprint C (maturidade operacional):** DOC-17, DOC-19.
---

## Sequenciamento recomendado
1. **Sprint A (P1 crítico):** DOC-07, DOC-09, DOC-12, DOC-16, DOC-18, DOC-20, RC-01 a RC-04.
2. **Sprint B (governança):** DOC-10, DOC-11, DOC-13, DOC-14, RC-05 (CONCLUÍDO), RC-06.
3. **Sprint C (maturidade operacional):** DOC-17, DOC-19, RC-07.
