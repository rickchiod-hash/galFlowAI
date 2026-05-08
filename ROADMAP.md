# ROADMAP — GalFlowAI

**Última atualização:** 06/05/2026  
**Objetivo:** Evolução do projeto sem quebrar o fluxo local-first.

---

## V2 — Estabilização e Observabilidade (CONCLUÍDO)
- Central de Logs no Gradio.
- LogService central.
- Filtros INFO/WARN/ERROR.
- Diagnóstico copiável.
- Logs no K:.
- Rotação de logs.
- DEBUG oculto na UI.
- BACKLOG/ROADMAP sincronizados.

## V2.1 — Logs via API (CONCLUÍDO H13)
- /api/logs/recent.
- /api/logs/summary.
- /api/logs/last-error.
- /api/logs/diagnostic.
- Testes de contrato (11/11 passando).

## V2.2 — Prompt Context Pack (CONCLUÍDO H14)
- Schema inicial.
- NegativePromptBuilder. 
- ConsistencyValidator. 
- Separação prompt de roteiro vs prompt de vídeo. 
- Reference Asset Map. 
- Testes (12/12 passando).

## V2.3 — Consistência visual na UI (CONCLUÍDO H17)
- Visual Bible editável. 
- Modo anti-alucinação. 
- Prompts por engine. 
- Prompt Pack versionado. 
- Testes (13/13 passando).

## V2.4 — Roteiro Comercial Forte (CONCLUÍDO H15)
- Prompt Base de roteiro. 
- Quality Gate. 
- Enriquecimento de briefing. 
- Templates por tipo de comercial. 
- Biblioteca de ganchos. 
- JSON + Markdown padronizados. 
- Score de roteiro. 
- Tudo em português brasileiro. 
- Testes (13/13 passando).

## V2.5 — Roteiro Editável Avançado (CONCLUÍDO H16)
- Melhorar roteiro. 
- Complementar roteiro. 
- Deixar mais viral. 
- Deixar mais premium. 
- Deixar mais direto. 
- Versionamento de melhoria. 
- Aprovação antes das cenas. 
- Testes (11/11 passando).

## V2.6 — Roteiro + Consistência Visual (CONCLUÍDO H17)
- Conectar roteiro com Visual Bible. 
- Criar contratos de cena. 
- Gerar prompts de vídeo anti-alucinação em português brasileiro. 
- Negative prompt por cena em português brasileiro. 
- Testes (13/13 passando).

## V3 — Observabilidade avançada/worker supervisor (CONCLUÍDO H18)
- WebSocket real de logs, se fizer sentido. 
- Logs JSON estruturados. 
- Worker/supervisor futuro. 
- Métricas locais. 
- Health dashboard. 
- Testes (6/6 passando).

## V3.1 — Refatoração e Documentação (CONCLUÍDO 06/05/2026)

### REF-01: Refatoração Rename GalFlowAI → GalFlowAI ✅
- **Status:** Concluído
- **Escopo:** Substituído "GalFlowAI" por "GalFlowAI" em 15+ arquivos (.py, .md, .bat).
- **Arquivos afetados:** api.py, use_cases, services, testes, README, BACKLOG.
- **Evidência:** 0 ocorrências restantes de "GalFlowAI".

### DOC-21 a DOC-40: 20 Melhorias README ✅
| ID | Melhoria | Status |
|---|---|---|
| DOC-21 | Logos Oficiais (galflowai_logo_master.png, galflowai_app_icon.png) | ✅ |
| DOC-22 | Total de Testes (314 coletados) | ✅ |
| DOC-23 | 84+ Novos Testes H11-H18 | ✅ |
| DOC-24 | K-only Environment (sem C:) | ✅ |
| DOC-25 | Padronização de Erros (CAUSA | CORREÇÃO) | ✅ |
| DOC-26 | Variáveis Obrigatórias (AGENTS.md) | ✅ |
| DOC-27 | Riscos Ativos (seção com tabela) | ✅ |
| DOC-28 | Onboarding Rápido (seção dedicada) | ✅ |
| DOC-29 | Naming Oficial com Logos | ✅ |
| DOC-30 | Estrutura de Diretórios com Logos | ✅ |
| DOC-31 | Histórico de Refatoração | ✅ |
| DOC-32 | Começando em 5 Minutos Atualizado | ✅ |
| DOC-33 | Rodar Testes Atualizado (314) | ✅ |
| DOC-34 | Roadmap H19-H20 | ✅ |
| DOC-35 | Cobertura Atual (seção detalhada) | ✅ |
| DOC-36 | Governança com Logos | ✅ |
| DOC-37 | Backup Sistêmico (nota) | ✅ |
| DOC-38 | Fallback FFmpeg (nota) | ✅ |
| DOC-39 | Sumário Atualizado (Riscos, Onboarding) | ✅ |
| DOC-40 | Estado Atual do Projeto (revisão completa) | ✅ |

## V3.2 — Evolução de frontend (PENDENTE)
- React/TypeScript opcional. 
- Timeline visual. 
- Editor avançado. 
- Launcher/supervisor em Go. 

## V3.3 — Integrações opcionais (PENDENTE)
- WanGP/Wan2GP para geração avançada. 
- FramePack opcional. 
- TTS local opcional. 
- lm Studio, GPT4All, KoboldCpp, llama.cpp. 

## H19-H20 — Próximas Histórias (Planejadas)

| ID | História (3 pontos) | Status | Planejado |
|---|---|---|---|
| H19 | **API Versioning & Contract Tests**<br>1. Validate: contratos atuais mapeados<br>2. Execute: criar /api/v1 e testes de contrato<br>3. Return: contratos versionados e testes | 🟨 Pendente | Sprint B |
| H20 | **E2E Fallback Tests**<br>1. Validate: cenários de falha mapeados<br>2. Execute: criar testes E2E para fallback FFmpeg<br>3. Return: cobertura de falhas | 🟨 Pendente | Sprint B |

---

## Plano de execução

### Sprint A (1–2 semanas) — **Pendências Críticas (Em andamento)**
- RC-01, RC-02, RC-03, RC-04
- DOC-07, DOC-09, DOC-12, DOC-16, DOC-18, DOC-20
- REF-01 ✅, DOC-21 a DOC-40 ✅

### Sprint B (2 semanas) — **Observabilidade e Cobertura**
- RC-05 ✅, RC-06
- DOC-10
- H19 (API Versioning)
- H20 (E2E Fallback Tests)
- Criar testes E2E para fluxo completo

### Sprint C (2+ semanas) — **Governança e Maturidade**
- RC-07
- DOC-08, DOC-11, DOC-13, DOC-14, DOC-17, DOC-19
- Implantar ADRs leves

---

## Itens congelados (não fazer agora)
- Reescrita completa da UI em React sem estabilizar contratos da API. 
- Dependência obrigatória de cloud/API paga. 
- Troca massiva de stack sem baseline de performance/confiabilidade. 
- Implementar OCR/visão agora. 
- Criar dependência pesada. 
- Usar "prompts visuais em inglês" - REMOVIDO. 

---

## Regras de aceite
1. **Não quebrar fluxo vigente** (gerar roteiro → editar/aprovar → cenas → preview → MP4). 
2. **Melhorar observabilidade** (logs, erro claro, rastreabilidade por `project_id`/`job_id`). 
3. **Aumentar robustez** sem impor dependências cloud ou lock-in externo. 
4. **Permitir rollback fácil** (mudanças pequenas, feature flags quando aplicável). 
5. **Tudo em português brasileiro** - nunca "prompts visuais em inglês". 
6. **NÃO implementar agora** - apenas backlog/planejamento. 
7. **Naming oficial:** GalFlowAI (nunca GalFlowAI). 
8. **Logos oficiais:** usar `galflowai_logo_master.png` e `galflowai_app_icon.png`. 

---

## Resumo de Entregas (06/05/2026)
- ✅ Refatoração GalFlowAI → GalFlowAI (REF-01)
- ✅ 20 melhorias README (DOC-21 a DOC-40)
- ✅ Atualização BACKLOG.md com novas histórias
- ✅ Atualização ROADMAP.md com status
- ✅ Total: 314 testes coletados, 84+ novos testes H11-H18
- ✅ Padronização de erros (CAUSA | CORREÇÃO)
- ✅ Ambiente K-only (sem C:)
