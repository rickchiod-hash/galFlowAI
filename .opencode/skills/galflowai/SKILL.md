# GalFlowAI Skill — OpenCode

Use esta skill quando trabalhar no GalFlowAI.

## Objetivo

Manter o projeto modular, local-first, testável, rastreável e sem regressão.

## Documentos obrigatórios antes de codar

1. `docs/reference/PROJECT_REFERENCE_CONTEXT.md`
2. `docs/reference/FEATURE_PRESERVATION_MATRIX.md`
3. `docs/project-control/00_STATUS_EXECUTIVO.md`
4. `docs/project-control/05_BACKLOG_PRIORIZADO.md`
5. `docs/project-control/06_HISTORIAS_REFINADAS.md`
6. Playbook do tema da história:
   - providers LLM: `docs/playbooks/LLM_PROVIDER_PLAYBOOK.md`
   - vídeo/render: `docs/playbooks/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`
   - áudio/TTS: `docs/playbooks/AUDIO_TTS_PROVIDER_PLAYBOOK.md`
   - IA vetorial: `docs/playbooks/VECTOR_MEMORY_PLAYBOOK.md`
   - QA: `docs/playbooks/QA_ANTI_HALLUCINATION_PLAYBOOK.md`

## Ordem de execução

1. Auditar estado atual.
2. Escolher história priorizada.
3. Validar DoR.
4. Implementar menor incremento possível.
5. Rodar testes.
6. Atualizar checkpoint.
7. Commitar.

## Guardrails

- Não remover fallbacks.
- Não trocar stack sem ADR.
- Não usar modelo pesado como default.
- Não mascarar erro como `Erro` genérico.
- Não finalizar sem atualizar `00_STATUS_EXECUTIVO.md`.
