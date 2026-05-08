# FEATURE_PRESERVATION_MATRIX — GalFlowAI

Uso obrigatório em todo PR. Se um item obrigatório sumir, o PR deve falhar ou exigir ADR.

| Feature | Tipo | Obrigatória | História vinculada | Arquivo de contexto | Como validar | Teste esperado | Pode remover? |
|---|---|---:|---|---|---|---|---:|
| Nome GalFlowAI | naming | Sim | CORE-003 | PROJECT_REFERENCE_CONTEXT.md | grep por nomes legados fora de histórico | `test_naming_galflowai.py` | Não |
| Roteiro editável | UI/use case | Sim | UI-102 | UI_STEP_FLOW.md | gerar e editar roteiro sem render | regressão UI | Não |
| Aprovação de roteiro | fluxo | Sim | UI-103 | UI_STEP_FLOW.md | cenas bloqueadas sem aprovação | integração | Não |
| TemplateProvider | provider | Sim | PROV-301 | LLM_PROVIDER_PLAYBOOK.md | LLM falha → template | unit fallback | Não |
| FFmpeg fallback | provider | Sim | RND-503 | VIDEO_RENDER_PROVIDER_PLAYBOOK.md | WanGP falha → FFmpeg | E2E mockado | Não |
| Providers locais | provider | Sim | PROV-300 | LLM_PROVIDER_PLAYBOOK.md | registry lista todos os providers | contrato provider | Não |
| Logs | observabilidade | Sim | OBS-801 | ARCHITECTURE_FLOW_REFERENCE.md | tela/endpoint retorna eventos | contrato API + UI | Não |
| Métricas | observabilidade | Sim | OBS-802 | ARCHITECTURE_FLOW_REFERENCE.md | tempo, fallback, erro por etapa | contrato API | Não |
| Status diário | governança | Sim | GOV-001 | 00_STATUS_EXECUTIVO.md | arquivo atualizado no fim da sessão | checklist | Não |
| TODO rastreável | governança | Sim | GOV-004 | TODO_POLICY.md | TODO possui story id | static test | Não |
| SceneContracts | domínio | P1 | VIS-402 | ARCHITECTURE_FLOW_REFERENCE.md | cada cena tem contrato | unit schema | Não após validar |
| Visual Bible | domínio | P1 | VIS-401 | VECTOR_MEMORY_PLAYBOOK.md | assets aprovados/canônicos | unit schema | Não após validar |
| Ingredient Registry | domínio | P1 | VIS-400 | VECTOR_MEMORY_PLAYBOOK.md | ingredientes versionados | unit schema | Não após validar |
| RenderPlan | domínio | P1 | RND-500 | VIDEO_RENDER_PROVIDER_PLAYBOOK.md | engine decidida com motivo | unit planner | Não após validar |
| AudioPlan | domínio | P1 | AUD-600 | AUDIO_TTS_PROVIDER_PLAYBOOK.md | TTS falha não quebra MP4 | unit fallback | Não após validar |
| VectorMemory disabled | feature flag | P2 | VEC-700 | VECTOR_MEMORY_PLAYBOOK.md | disabled por padrão | config test | Não após validar |
