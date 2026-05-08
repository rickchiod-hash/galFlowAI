# 05_BACKLOG_PRIORIZADO — GalFlowAI

Backlog ordenado por valor, risco técnico, dependência e capacidade de entrega.

## Ordem recomendada

| Ordem | ID | História | Prioridade | SP | Status | Dependência | Motivo da prioridade |
|---:|---|---|---|---:|---|---|---|
| 1 | GOV-001 | Criar checkpoint diário permanente | Alta | 2 | Concluída | Nenhuma | para retomar o projeto em outra sessão sem perda de contexto |
| 2 | GOV-002 | Criar fonte de verdade do produto | Alta | 2 | Pendente | Nenhuma | para impedir drift de nome, fluxo e arquitetura |
| 3 | GOV-003 | Criar matriz de preservação de features | Alta | 3 | Pendente | Nenhuma | para impedir remoção silenciosa de providers, fallbacks e telas |
| 4 | GOV-004 | Padronizar TODOs rastreáveis | Alta | 2 | Pendente | Nenhuma | para que dívida técnica tenha dono, critério e backlog |
| 5 | GOV-005 | Criar ADR obrigatório para remoções | Alta | 2 | Pendente | Nenhuma | para preservar rastreabilidade e rollback |
| 6 | GOV-006 | Adicionar AGENTS e Skill do GalFlowAI | Alta | 3 | Pendente | Nenhuma | para que o agente siga o mesmo padrão em toda sessão |
| 7 | CORE-100 | Auditar histórico Git desde o primeiro commit | Alta | 5 | Pendente | GOV-001..GOV-006 | para resgatar features perdidas com evidência |
| 8 | CORE-101 | Mapear estado atual do projeto | Alta | 3 | Pendente | GOV-001..GOV-006 | para iniciar refatorações sem suposição |
| 9 | CORE-102 | Validar diferença entre documentação e código | Alta | 5 | Pendente | GOV-001..GOV-006 | para separar fato implementado de roadmap |
| 10 | UI-200 | Restaurar fluxo por etapas na documentação | Alta | 3 | Pendente | CORE-100..CORE-102 | para aprovar roteiro/cenas antes de gastar GPU |
| 11 | UI-201 | Gerar roteiro sem renderizar vídeo | Alta | 5 | Pendente | CORE-100..CORE-102 | para evitar render caro com roteiro ruim |
| 12 | UI-202 | Bloquear cenas sem roteiro aprovado | Alta | 5 | Pendente | CORE-100..CORE-102 | para preservar o fluxo de validação humana |
| 13 | UI-203 | Resgatar telas de logs, métricas e diagnóstico | Alta | 5 | Pendente | CORE-100..CORE-102 | para debugar sem depender do terminal |
| 14 | ARCH-300 | Criar use cases por etapa | Alta | 8 | Pendente | CORE-100..CORE-102 | para reduzir acoplamento com pipeline/adapters |
| 15 | ARCH-301 | Criar Result Object padrão | Alta | 5 | Pendente | CORE-100..CORE-102 | para não propagar exceções e mensagens genéricas |
| 16 | ARCH-302 | Centralizar configuração e paths | Alta | 3 | Pendente | CORE-100..CORE-102 | para evitar hardcoded C: e ambiente quebrado |
| 17 | PROV-300 | Preservar registry de providers LLM | Alta | 5 | Pendente | CORE-100..CORE-102 | para continuar criando roteiros sem cloud obrigatória |
| 18 | PROV-301 | Garantir TemplateProvider como fallback | Alta | 3 | Pendente | CORE-100..CORE-102 | para gerar roteiro mínimo quando provider falhar |
| 19 | PROV-302 | Criar testes de provider fallback | Alta | 3 | Pendente | CORE-100..CORE-102 | para evitar regressão de fallback |
| 20 | PIPE-400 | Criar JobState formal | Alta | 5 | Pendente | Arquitetura/base P0 validada | para acompanhar queued/running/succeeded/failed/canceled |
| 21 | PIPE-401 | Criar idempotency key por etapa | Alta | 5 | Pendente | Arquitetura/base P0 validada | para economizar tempo e VRAM |
| 22 | PIPE-402 | Criar cache por hash de artefatos | Média | 5 | Pendente | Arquitetura/base P0 validada | para acelerar iterações e evitar custo repetido |
| 23 | PIPE-403 | Definir SQLite WAL/job ledger P1 | Média | 5 | Pendente | Arquitetura/base P0 validada | para rastrear progresso sem Redis obrigatório |
| 24 | VIS-500 | Criar schema Ingredient Registry | Alta | 5 | Pendente | Arquitetura/base P0 validada | para manter consistência entre cenas |
| 25 | VIS-501 | Criar schema Visual Bible | Alta | 5 | Pendente | Arquitetura/base P0 validada | para reduzir drift visual |
| 26 | VIS-502 | Criar schema SceneContract | Alta | 5 | Pendente | Arquitetura/base P0 validada | para transformar roteiro em instruções testáveis |
| 27 | VIS-503 | Criar Prompt Compiler por engine | Média | 8 | Pendente | Arquitetura/base P0 validada | para usar FFmpeg/WanGP/VACE sem gambiarra |
| 28 | RND-600 | Criar RenderPlan mínimo | Alta | 5 | Pendente | Arquitetura/base P0 validada | para usar GPU e fallback com previsibilidade |
| 29 | RND-601 | Manter FFmpeg como fallback universal | Alta | 3 | Pendente | Arquitetura/base P0 validada | para sempre obter um MP4 mínimo |
| 30 | RND-602 | Adicionar perfil GTX 1660 Super | Alta | 3 | Pendente | Arquitetura/base P0 validada | para evitar OOM e travamentos |
| 31 | RND-603 | Registrar Wan VACE 1.3B como futuro opcional | Baixa | 2 | Pendente | Arquitetura/base P0 validada | para não forçar engine pesada agora |
| 32 | AUD-700 | Criar AudioPlan e narration_script.md | Alta | 5 | Pendente | Arquitetura/base P0 validada | para controlar TTS, SRT e revisão humana |
| 33 | AUD-701 | Gerar áudio por cena com fallback | Média | 5 | Pendente | Arquitetura/base P0 validada | para sincronizar narração com cenas |
| 34 | AUD-702 | Gerar SRT por timing de cena | Média | 3 | Pendente | Arquitetura/base P0 validada | para usar vídeo em redes sociais sem áudio |
| 35 | AUD-703 | Criar SFX manifest | Baixa | 3 | Pendente | Arquitetura/base P0 validada | para evitar uso indevido de assets |
| 36 | VEC-800 | Criar VectorStoreAdapter sem runtime obrigatório | Média | 3 | Pendente | Arquitetura/base P0 validada | para preparar memória sem acoplar backend |
| 37 | VEC-801 | Criar MemoryQualityGate | Média | 5 | Pendente | Arquitetura/base P0 validada | para evitar contaminação semântica |
| 38 | VEC-802 | Planejar Qdrant local opcional | Baixa | 3 | Pendente | Arquitetura/base P0 validada | para evoluir com payload e filtros |
| 39 | VEC-803 | Planejar Chroma como protótipo opcional | Baixa | 2 | Pendente | Arquitetura/base P0 validada | para testar retrieval textual com baixo atrito |
| 40 | OBS-900 | Criar logs estruturados por etapa | Alta | 5 | Pendente | Arquitetura/base P0 validada | para diagnosticar falhas sem olhar código |
| 41 | OBS-901 | Criar métricas mínimas por job | Alta | 5 | Pendente | Arquitetura/base P0 validada | para priorizar melhorias reais |
| 42 | QA-1000 | Criar teste antirregressão de naming | Alta | 2 | Pendente | Arquitetura/base P0 validada | para preservar identidade GalFlowAI |
| 43 | QA-1001 | Criar teste de presença de providers/fallbacks | Alta | 3 | Pendente | Arquitetura/base P0 validada | para preservar operação local-first |
| 44 | QA-1002 | Criar teste UI não chama adapters | Média | 3 | Pendente | Arquitetura/base P0 validada | para proteger separação de responsabilidades |
| 45 | QA-1003 | Criar teste E2E WanGP falha → FFmpeg | Média | 5 | Pendente | Arquitetura/base P0 validada | para garantir MP4 mesmo sem IA de vídeo |
| 46 | QA-1004 | Criar teste TTS falha → export sem áudio | Média | 3 | Pendente | Arquitetura/base P0 validada | para preservar entrega final |
| 47 | SEC-1100 | Criar política MCP seguro | Média | 2 | Pendente | Arquitetura/base P0 validada | para evitar ferramentas amplas sem revisão |
| 48 | SEC-1101 | Criar política de secrets e arquivos sensíveis | Média | 2 | Pendente | Arquitetura/base P0 validada | para proteger ambiente e clientes |

## Próxima história recomendada

**GOV-002 — Criar fonte de verdade do produto.** Impede drift de nome, fluxo e arquitetura.

## Regras de priorização

1. Antirregressão antes de feature.
2. Evidência antes de refactor.
3. Fluxo por etapas antes de engine nova.
4. Fallback antes de provider premium.
5. Teste antes de declarar conclusão.
