# 05_BACKLOG_PRIORIZADO — GalFlowAI

Backlog ordenado por valor, risco técnico, dependência e capacidade de entrega.

## Ordem recomendada

| Ordem | ID | História | Prioridade | SP | Status | Dependência | Motivo da prioridade |
|---:|---|---|---|---:|---|---|---|
| 1 | GOV-001 | Criar checkpoint diário permanente | Alta | 2 | Concluída | Nenhuma | para retomar o projeto em outra sessão sem perda de contexto |
| 2 | GOV-002 | Criar fonte de verdade do produto | Alta | 2 | Concluída | Nenhuma | para impedir drift de nome, fluxo e arquitetura |
| 3 | GOV-003 | Criar matriz de preservação de features | Alta | 3 | Concluída | Nenhuma | para impedir remoção silenciosa de providers, fallbacks e telas |
| 4 | GOV-004 | Padronizar TODOs rastreáveis | Alta | 2 | Concluída | Nenhuma | para que dívida técnica tenha dono, critério e backlog |
| 5 | GOV-005 | Criar ADR obrigatório para remoções | Alta | 2 | Concluída | Nenhuma | para preservar rastreabilidade e rollback |
| 6 | GOV-006 | Adicionar AGENTS e Skill do GalFlowAI | Alta | 3 | Concluída | Nenhuma | para que o agente siga o mesmo padrão em toda sessão |
| 7 | CORE-100 | Auditar histórico Git desde o primeiro commit | Alta | 5 | Concluída | GOV-001..GOV-006 | para resgatar features perdidas com evidência |
| 8 | CORE-101 | Mapear estado atual do projeto | Alta | 3 | Concluída | GOV-001..GOV-006 | para iniciar refatorações sem suposição |
| 9 | CORE-102 | Validar diferença entre documentação e código | Alta | 5 | Concluída | GOV-001..GOV-006 | para separar fato implementado de roadmap |
| 10 | UI-200 | Restaurar fluxo por etapas na documentação | Alta | 3 | Concluída | CORE-100..CORE-102 | para aprovar roteiro/cenas antes de gastar GPU |
| 11 | UI-201 | Gerar roteiro sem renderizar vídeo | Alta | 5 | Concluída | CORE-100..CORE-102 | commit cde0ce2 — endpoint POST /api/projects/{id}/script/generate |
| 12 | UI-202 | Bloquear cenas sem roteiro aprovado | Alta | 5 | Concluída | CORE-100..CORE-102 | commit f713ca6 — gate de aprovação antes de split de cenas |
| 13 | UI-203 | Resgatar telas de logs, métricas e diagnóstico | Alta | 5 | Concluída | CORE-100..CORE-102 | para debugar sem depender do terminal |
| 14 | ARCH-300 | Criar use cases por etapa | Alta | 8 | Concluída | CORE-100..CORE-102 | para reduzir acoplamento com pipeline/adapters |
| 15 | ARCH-301 | Criar Result Object padrão | Alta | 5 | Concluída | CORE-100..CORE-102 | para não propagar exceções e mensagens genéricas |
| 16 | ARCH-302 | Centralizar configuração e paths | Alta | 3 | Concluída | CORE-100..CORE-102 | para evitar hardcoded C: e ambiente quebrado |
| 17 | PROV-300 | Preservar registry de providers LLM | Alta | 5 | Concluída | CORE-100..CORE-102 | ProviderRouter + TemplateProvider existentes (commit 2da23f1) |
| 18 | PROV-301 | Garantir TemplateProvider como fallback | Alta | 3 | Concluída | CORE-100..CORE-102 | TemplateProvider em app/adapters/llm/template_provider.py (commit ac2c0ee) |
| 19 | PROV-302 | Criar testes de provider fallback | Alta | 3 | Concluída | CORE-100..CORE-102 | para evitar regressão de fallback |
| 20 | PIPE-400 | Criar JobState formal | Alta | 5 | Concluída | Arquitetura/base P0 validada | commit 60d09e5 — JobState com enum + transições guardadas |
| 21 | PIPE-401 | Criar idempotency key por etapa | Alta | 5 | Concluída | Arquitetura/base P0 validada | commit 851aaa1 — IdempotencyKeyService |
| 22 | PIPE-402 | Criar cache por hash de artefatos | Média | 5 | Concluída | Arquitetura/base P0 validada | commit [hash_do_commit] — cache de artefatos por hash SHA-256 integrado nas etapas do pipeline |
| 23 | PIPE-403 | Definir SQLite WAL/job ledger P1 | Média | 5 | Concluída | Arquitetura/base P0 validada | para rastrear progresso sem Redis obrigatório |
| 24 | VIS-500 | Criar schema Ingredient Registry | Alta | 5 | Concluída | Arquitetura/base P0 validada | commit a1d2c09 — IngredientRegistry com CRUD versionado e 27 testes |
| 25 | VIS-501 | Criar schema Visual Bible | Alta | 5 | Concluída | Arquitetura/base P0 validada | para reduzir drift visual |
| 26 | VIS-502 | Criar schema SceneContract | Alta | 5 | Concluída | Arquitetura/base P0 validada | para transformar roteiro em instruções testáveis |
| 27 | VIS-503 | Criar Prompt Compiler por engine | Média | 8 | Concluída | Arquitetura/base P0 validada | para usar FFmpeg/WanGP/VACE sem gambiarra |
| 28 | RND-600 | Criar RenderPlan mínimo | Alta | 5 | Concluída | Arquitetura/base P0 validada | para usar GPU e fallback com previsibilidade |
| 29 | RND-601 | Manter FFmpeg como fallback universal | Alta | 3 | Concluída | Arquitetura/base P0 validada | para sempre obter um MP4 mínimo |
| 30 | RND-602 | Adicionar perfil GTX 1660 Super | Alta | 3 | Concluída | Arquitetura/base P0 validada | para evitar OOM e travamentos |
| 31 | RND-603 | Registrar Wan VACE 1.3B como futuro opcional | Baixa | 2 | Concluída | Arquitetura/base P0 validada | VACE documentado no VIDEO_RENDER_PROVIDER_PLAYBOOK.md — EngineType definido, PromptCompiler suporta, VRAM 2048MB/cena estimada |
| 32 | AUD-700 | Criar AudioPlan e narration_script.md | Alta | 5 | Concluída | Arquitetura/base P0 validada | commit a68ceeb — AudioPlan schema + AudioPlanService CRUD + generate_narration_script → narration_script.md. 41 testes. |
| 33 | AUD-701 | Gerar áudio por cena com fallback | Média | 5 | Concluída | Arquitetura/base P0 validada | commit 140fb6e — TTSAudioService: gera WAV por cena a partir de AudioPlan com fallback silencioso. 19 testes. |
| 34 | AUD-702 | Gerar SRT por timing de cena | Média | 3 | Concluída | Arquitetura/base P0 validada | commit 9c90700 — SRTService: gera legendas SRT a partir de AudioPlan com timing sequencial. 22 testes. |
| 35 | AUD-703 | Criar SFX manifest | Baixa | 3 | Concluída | Arquitetura/base P0 validada | commit d3fbfe7 — SFXManifest: schema + CRUD + busca. 31 testes. |
| 36 | VEC-800 | Criar VectorStoreAdapter sem runtime obrigatório | Média | 3 | Concluída | Arquitetura/base P0 validada | commit 9012c29 — VectorStoreAdapter (ABC) + InMemoryVectorStore + cosine_similarity. 25 testes. |
| 37 | VEC-801 | Criar MemoryQualityGate | Média | 5 | Concluída | Arquitetura/base P0 validada | commit f3a2dc9 — MemoryQualityGate com validate_ingredient/validate_bible_entry. 13 testes. |
| 38 | VEC-802 | Planejar Qdrant local opcional | Baixa | 3 | Concluída | Arquitetura/base P0 validada | plano documentado no VECTOR_MEMORY_PLAYBOOK.md — QdrantStore, prereqs, criterios ativacao |
| 39 | VEC-803 | Planejar Chroma como protótipo opcional | Baixa | 2 | Concluída | Arquitetura/base P0 validada | plano documentado no VECTOR_MEMORY_PLAYBOOK.md — ChromaStore, comparacao Qdrant vs Chroma |
| 40 | OBS-900 | Criar logs estruturados por etapa | Alta | 5 | Concluída | Arquitetura/base P0 validada | StageLogger em app/domain/stage_logger.py — eventos por etapa com causa+correcao. 12 testes. |
| 41 | OBS-901 | Criar métricas mínimas por job | Alta | 5 | Concluída | Arquitetura/base P0 validada | JobMetrics em app/domain/job_metrics.py — metricas por etapa: tempo, fallback, erro. 10 testes. |
| 42 | QA-1000 | Criar teste antirregressão de naming | Alta | 2 | Concluída | Arquitetura/base P0 validada | para preservar identidade GalFlowAI |
| 43 | QA-1001 | Criar teste de presença de providers/fallbacks | Alta | 3 | Concluída | Arquitetura/base P0 validada | para preservar operação local-first |
| 44 | QA-1002 | Criar teste UI não chama adapters | Média | 3 | Concluída | Arquitetura/base P0 validada | para proteger separação de responsabilidades |
| 45 | QA-1003 | Criar teste E2E WanGP falha → FFmpeg | Média | 5 | Concluída | Arquitetura/base P0 validada | para garantir MP4 mesmo sem IA de vídeo |
| 46 | QA-1004 | Criar teste TTS falha → export sem áudio | Média | 3 | Concluída | Arquitetura/base P0 validada | para preservar entrega final |
| 47 | UI-204 | Criar tela de Configurações na UI | Baixa | 3 | Concluída | UI-203 | ConfigService + aba Configuracoes na UI com provedor, qualidade, duracao, caminhos. 16 testes. |
| 48 | SEC-1100 | Criar política MCP seguro | Média | 2 | Concluída | Arquitetura/base P0 validada | mcp/README_MCP_OPTIONAL.md criado — MCP desabilitado por padrao. 5 testes. |
| 49 | SEC-1101 | Criar política de secrets e arquivos sensíveis | Média | 2 | Concluída | Arquitetura/base P0 validada | SECRETS_POLICY.md criado + .gitignore atualizado (env/credentials). 6 testes. |

## Backlog Pós-49 — Fase 6 (Mandatory Technical Gaps)

Backlog expandido por decisão de produto (2026-05-12): WanGP, VACE, FFmpeg fallback, API versioning, UI integrada, vector store, logs estruturados na UI e fluxo stage-gated são **mandatórios**. Ollama permanece único opcional.

### Fase 6A — Structural Stabilization (zero mudança funcional visível)

| Ordem | ID | História | Prioridade | SP | Status | Dependência |
|------:|---|---------|:---------:|:--:|:------:|:-----------:|
| 50 | ARCH-320 | Unificar pipeline old/new, deletar `_new.py` | Alta | 2 | ✅ Concluída | Nenhuma |
| 51 | API-210 | Adicionar prefixo `/api/v1/` em todas as rotas | Alta | 5 | Pendente | Nenhuma |
| 52 | API-211 | Envelopar resposta de `/api/llm/providers` em `ApiResponse` | Alta | 3 | Pendente | Nenhuma |
| 53 | LOG-100 | Conectar erros estruturados ao Dataframe de logs na UI | Alta | 5 | Pendente | Nenhuma |

### Fase 6B — Mandatory Functional Integration

| Ordem | ID | História | Prioridade | SP | Status | Dependência |
|------:|---|---------|:---------:|:--:|:------:|:-----------:|
| 54 | UI-205 | Substituir botões placeholder do estágio 2 por chamadas reais de use case | Alta | 8 | ✅ Concluída | ARCH-320 |
| 55 | RND-610 | Hardening do WanGP adapter (telemetria, erros estruturados) | Alta | 8 | ✅ Concluída | LOG-100 |
| 56 | RND-611 | Pipeline fallback chama `log_structured_error` | Alta | 5 | ✅ Concluída | RND-610 |
| 57 | RND-612 | Criar `app/adapters/vace_adapter.py` | Alta | 8 | ✅ Concluída | ARCH-320 |

### Fase 6C — Complete Platform

| Ordem | ID | História | Prioridade | SP | Status | Dependência |
|------:|---|---------|:---------:|:--:|:------:|:-----------:|
| 58 | VEC-810 | Implementar Qdrant vector store backend | Média | 8 | ✅ Concluída | Fase 6B |
| 59 | VEC-811 | Implementar Chroma vector store backend | Média | 5 | ✅ Concluída | Fase 6B |
| 60 | DOC-120 | Reconciliar documentação com novo direcionamento mandatório | Média | 3 | Pendente | Fase 6C |

**Total novas histórias: 11** | **SP total novo: 56** | **SP acumulado: 54 + 56 = 110**

## Próxima história recomendada

**VEC-811 concluída.** Próxima: **DOC-120** — Reconciliar documentação com novo direcionamento mandatório.

## Regras de priorização

1. Antirregressão antes de feature.
2. Evidência antes de refactor.
3. Fluxo por etapas antes de engine nova.
4. Fallback antes de provider premium.
5. Teste antes de declarar conclusão.
6. **Phase 6A antes de 6B antes de 6C** — nunca inverter a anti-break order.
