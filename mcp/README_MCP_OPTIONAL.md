# MCP (Model Context Protocol) — Opcional e Desabilitado por Padrao

## Decisao arquitetural

MCP **esta desabilitado por padrao** no GalFlowAI.
Consulte ADR-002 em `docs/project-control/11_DECISOES_TECNICAS_ADR.md`.

## Por que MCP esta desabilitado

1. **Superficie de ferramenta ampla** — MCP expoe ferramentas que podem levar o agente a usar recursos desnecessarios.
2. **Vazamento de contexto** — Sem politica de seguranca, MCP pode vazar contexto do projeto para ferramentas externas.
3. **Prioridade MVP** — O foco atual e pipeline local-first sem dependencia de ferramentas externas.

## Quando ativar MCP

- Apos implementar **SEC-1100** (esta politica).
- Apos revisao manual das ferramentas MCP disponiveis.
- Apenas com ferramentas restritas e revisadas.

## Como ativar (futuro)

1. Criar arquivo `mcp.json` ou configurar via `opencode.jsonc`.
2. Listar apenas ferramentas aprovadas.
3. Nunca expor ferramentas de acesso a sistema de arquivos amplo ou rede.

## Referencias

- `docs/project-control/11_DECISOES_TECNICAS_ADR.md` — ADR-002
- `docs/project-control/16_MCP_SKILLS_GUIDE.md` — Guia de skills MCP
- `docs/project-control/12_DEPENDENCIAS_E_BLOQUEIOS.md` — Dependencias que nao bloqueiam P0
