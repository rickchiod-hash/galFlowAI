# 12_DEPENDENCIAS_E_BLOQUEIOS — GalFlowAI

## Dependências que não devem bloquear P0

- Qdrant/Chroma.
- Redis/RQ.
- React.
- Wan VACE.
- Modelos 14B/16B.
- Remote render.
- MCP remoto.

## Dependências externas permitidas somente como futuro opcional

| Dependência | Uso | Fase | Obrigatória? | Guardrail |
|---|---|---|---:|---|
| Qdrant local | vector memory | P2 | Não | `VECTOR_MEMORY_ENABLED=false` por padrão |
| Chroma | protótipo vetorial | P2 | Não | adapter opcional |
| Redis/RQ | fila avançada | P3 | Não | SQLite job ledger antes |
| React | UI avançada | P3 | Não | Gradio por etapas antes |
| MCP | ferramentas externas | P3 | Não | desabilitado por padrão |
| Wan VACE 1.3B | referência/máscara | P3 | Não | fallback FFmpeg/WanGP |
