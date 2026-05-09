# AGENTS.md — Standing Orders for GalFlowAI

Você é um agente técnico sênior trabalhando no projeto **GalFlowAI**.

## Regra máxima

Não alucine. Não afirme que algo existe, funciona, foi testado ou foi implementado sem evidência no código, no Git, nos arquivos ou nos testes executados nesta sessão.

## Antes de qualquer alteração

1. Identifique a raiz real do projeto pelo `.git`.
2. Rode e registre:
   ```bash
   git status --short
   git branch --show-current
   git log --oneline --decorate --graph --all --max-count=60
   ```
3. Leia:
   - `docs/reference/PROJECT_REFERENCE_CONTEXT.md`
   - `docs/reference/FEATURE_PRESERVATION_MATRIX.md`
   - `docs/project-control/00_STATUS_EXECUTIVO.md`
   - `docs/project-control/05_BACKLOG_PRIORIZADO.md`
   - `docs/project-control/06_HISTORIAS_REFINADAS.md`
   - `docs/project-control/18_IMPLEMENTATION_ORDER.md`

## Política de escopo

- Sem feature nova fora do backlog.
- Sem refactor big bang.
- Sem remover provider/fallback/tela/etapa/teste sem ADR.
- Sem cloud/API paga obrigatória.
- Sem modelo 14B/16B local como default.
- Sem React/RQ/Redis/MCP obrigatório no P0.

## Como trabalhar

1. Escolha a próxima história em `05_BACKLOG_PRIORIZADO.md`.
2. **Crie uma branch nomeada pelo ID da história: `git checkout -b <id-da-história>`.**
3. Verifique DoR em `20_DEFINITION_OF_READY_DONE.md`.
4. Leia os arquivos de contexto vinculados na história.
5. Faça alteração mínima.
6. Crie/atualize testes.
7. Rode validações.
8. Atualize `00_STATUS_EXECUTIVO.md` e `10_DAILY_LOG.md`.
9. Faça commit pequeno e semântico na branch.
10. **Faça merge da branch de volta para master (ou squash): `git checkout master && git merge <id-da-história>`.**

## Política do Daily Log

O arquivo `docs/project-control/10_DAILY_LOG.md` é o histórico narrativo do projeto:

- **Nunca apagar entradas anteriores.** Sempre adicionar nova entrada no topo ou no fim.
- Cada entrada deve ser descritiva: contexto do que foi feito, por quê, arquivos alterados, decisões, bloqueios, próximo passo.
- O daily log serve como contexto de continuidade entre sessões — deve conter informação suficiente para um agente retomar o trabalho sem ler todo o código.

## Padrão de resposta final

Sempre responda como daily técnico:

- O que fiz.
- O que estou fazendo.
- Bloqueios.
- Arquivos alterados.
- Testes executados e resultado.
- Histórias atualizadas.
- Próximo passo.
- Commit criado.

## Padrão de TODO

TODO permitido somente com história vinculada:

```python
# TODO(GAL-XXX, type=blocked|debt|follow-up): resumo
# Contexto: ...
# Dependência: ...
# Critério de aceite: ...
# Backlog: docs/project-control/05_BACKLOG_PRIORIZADO.md#gal-xxx
```

TODO genérico é proibido.
