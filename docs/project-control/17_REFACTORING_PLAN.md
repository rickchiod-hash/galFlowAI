# 17_REFACTORING_PLAN — GalFlowAI

## Princípio

Refatorar em fatias pequenas, protegidas por testes e por feature preservation.

## Ordem técnica recomendada

1. Criar testes antirregressão de naming/providers/fallbacks.
2. Criar Result Object padrão.
3. Extrair use cases de roteiro/aprovação/cenas.
4. Formalizar JobState.
5. Formalizar SceneContract, RenderPlan e AudioPlan.
6. Centralizar config e paths.
7. Separar adapters por porta/interface.
8. Adicionar idempotência e cache.
9. Melhorar UI por etapas.
10. Só depois pensar em vector/render/audio avançado.

## Refactors proibidos no P0

- Trocar Gradio por React.
- Trocar storage por Postgres.
- Exigir Redis/RQ.
- Exigir Qdrant/Chroma.
- Reescrever pipeline inteiro.
