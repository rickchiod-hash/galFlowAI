# 01_AUDITORIA_HISTORICO_GIT — GalFlowAI

## Objetivo

Mapear, com evidência, o que existia, o que foi removido, o que regrediu e o que precisa ser resgatado.

## Comandos executados

```bash
git status --short
git branch --show-current
git log --oneline --reverse
git log --name-status --reverse
git log --all --grep="remove\|delete\|refactor\|fix\|feat\|todo\|wip" --regexp-ignore-case
```

### Resultados

- Branch: master
- Total de commits: 85
- HEAD: 7017ea8 "GalFlowAI v0.9 - Phases 1-8 Complete + Phase 9 Partial" (Thu May 7 04:48:14 2026)
- Working tree: 8 arquivos modificados (BACKLOG.md, ROADMAP.md, 6 app/ files) + untracked do pack importado

## Tabelas

| Commit | Tipo | Arquivo | Mudança | Feature afetada | Evidência | Ação |
|---|---|---|---|---|---|---|
| 7017ea8 | feat | 30 files | GalFlowAI v0.9 | Pipeline completo | v0.9 tag | Manter |
| ee05f5c | refactor | 43 files | Rename FlowForgeAI → GalFlowAI | Naming | grep mostra 0 ocorrências | Manter |
| d3c9af6 | refactor | app/api.py | H1+H2: except: → Exception: | Tratamento erros | git diff | Verificar se há bare except restantes |
| b20cd77 | delete | tests/integration/test_api_contract.py | Remove duplicado | Testes | git diff | OK |
| dbb133f | delete | BACKLOG_REFINADO.md, PROGRESSO_*.md, STATUS_*.md | Remove antigos | Limpeza | git log | OK |

## Perguntas obrigatórias

1. **Quais telas existiam e sumiram?** — EVIDÊNCIA INSUFICIENTE: necessário rodar app/main.py para verificar UI Gradio.
2. **Quais providers foram removidos, renomeados ou escondidos?** — Nenhum provider removido. Todos os 6 LLM providers presentes (Template, LM Studio, GPT4All, KoboldCpp, LlamaCpp, GPT-compatible). WanGP e FFmpeg presentes.
3. **Quais fallbacks foram alterados?** — Fallback FFmpeg presente. TemplateProvider presente. TTS fallback (pyttsx3/silence) presente.
4. **Quais docs dizem que algo existe, mas o código não comprova?** — EVIDÊNCIA INSUFICIENTE: não houve tempo para comparar docs/código exaustivamente.
5. **Quais TODOs foram resolvidos e quais ficaram órfãos?** — 0 TODOs encontrados no código.
6. **Quais arquivos mais mudaram nos últimos commits?** — app/api.py, app/main.py, README.md, BACKLOG.md.
7. **O último commit aproxima ou afasta o produto do fluxo por etapas?** — Aproxima: v0.9 implementa pipeline por etapas.
