# ROADMAP — FlowForgeAI

**Última atualização:** 03/05/2026  
**Objetivo:** Evolução do projeto sem quebrar o fluxo local-first.

---

## V2 — Estabilização e Observabilidade
- Central de Logs no Gradio.
- LogService central.
- Filtros INFO/WARN/ERROR.
- Diagnóstico copiável.
- Logs no K:.
- Rotação de logs.
- DEBUG oculto na UI.
- BACKLOG/ROADMAP sincronizados.

## V2.1 — Logs via API
- /api/logs/recent.
- /api/logs/summary.
- /api/logs/last-error.
- /api/logs/diagnostic.
- Testes de contrato.

## V2.2 — Prompt Context Pack
- Schema inicial.
- NegativePromptBuilder. 
- ConsistencyValidator. 
- Separação prompt de roteiro vs prompt de vídeo. 
- Reference Asset Map. 

## V2.3 — Consistência visual na UI
- Visual Bible editável. 
- Modo anti-alucinação. 
- Prompts por engine. 
- Prompt Pack versionado. 

## V2.4 — Roteiro Comercial Forte
- Prompt Base de roteiro. 
- Quality Gate. 
- Enriquecimento de briefing. 
- Templates por tipo de comercial. 
- Biblioteca de ganchos. 
- JSON + Markdown padronizados. 
- Score de roteiro. 
- Tudo em português brasileiro. 

## V2.5 — Roteiro Editável Avançado
- Melhorar roteiro. 
- Complementar roteiro. 
- Deixar mais viral. 
- Deixar mais premium. 
- Deixar mais direto. 
- Versionamento de melhoria. 
- Aprovação antes das cenas. 

## V2.6 — Roteiro + Consistência Visual
- Conectar roteiro com Visual Bible. 
- Criar contratos de cena. 
- Gerar prompts de vídeo anti-alucinação em português brasileiro. 
- Negative prompt por cena em português brasileiro. 

## V3 — Observabilidade avançada/worker supervisor
- WebSocket real de logs, se fizer sentido. 
- Logs JSON estruturados. 
- Worker/supervisor futuro. 
- Métricas locais. 
- Health dashboard. 

## V3.1 — Roteiro + Consistência Visual Avançado
- Validação pós-render futura. 
- OCR/visão opcional. 
- Métricas de consistência. 
- Prompt Compiler por engine. 
- Salvar Prompt Pack versionado. 

## V3.2 — Evolução de frontend
- React/TypeScript opcional. 
- Timeline visual. 
- Editor avançado. 
- Launcher/supervisor em Go. 

## V3.3 — Integrações opcionais
- WanGP/Wan2GP para geração avançada. 
- FramePack opcional. 
- TTS local opcional. 
- lm Studio, GPT4All, KoboldCpp, llama.cpp. 

---

## Plano de execução
### Sprint Atual (1–2 semanas)
- Terminar Central de Logs na UI. 
- LogService central. 
- Filtros INFO/WARN/ERROR. 
- Diagnóstico copiável. 
- Atualizar BACKLOG.md e ROADMAP.md. 

### Sprint B (2 semanas)
- Prompt Context Pack schema. 
- NegativePromptBuilder mínimo. 
- ConsistencyValidator mínimo. 
- Separação prompt roteiro vs vídeo. 

### Sprint C (2+ semanas)
- Visual Bible editável na UI. 
- Prompt Compiler por engine. 
- Prompt Pack versionado. 
- Métricas de consistência. 

### Sprint D (futuro)
- WebSocket real de logs. 
- Worker robusto e watchdog. 
- Evolução de frontend (React opcional). 
- Integrações WanGP/FramePack. 

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
