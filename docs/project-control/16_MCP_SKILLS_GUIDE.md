# 16_MCP_SKILLS_GUIDE — GalFlowAI

## Decisão

- Principal: `AGENTS.md` + `.opencode/skills/galflowai/SKILL.md`.
- Opcional: `opencode.jsonc` com `instructions` apontando para docs.
- Futuro: MCP local e restrito.

## Onde colocar

- `AGENTS.md`: raiz do projeto.
- `.opencode/AGENTS.md`: instruções complementares do OpenCode.
- `.opencode/skills/galflowai/SKILL.md`: habilidade específica do projeto.
- `opencode.jsonc`: raiz do projeto, se quiser carregar instruções por config.
- `mcp/`: apenas exemplos/documentação, não ativo por padrão.

## Por que não ativar MCP agora

MCP aumenta superfície de ferramenta e contexto. Sem política de segurança, pode induzir o agente a usar ferramentas demais ou vazar contexto. Primeiro estabilize governança e testes.
