# 01_AUDITORIA_HISTORICO_GIT — GalFlowAI

Atualizado em: 2026-05-14

## Objetivo

Mapear, com evidência, o que existia, o que foi removido, o que regrediu e o que precisa ser resgatado.

## Comandos executados

```bash
git status --short
git branch --show-current
git rev-list --count HEAD
git log --oneline --reverse
git log --name-status --reverse
git log --all --grep="remove\|delete\|refactor\|fix\|feat\|todo\|wip" --regexp-ignore-case
git log --diff-filter=D --name-only --format="%h %s"
```

### Resultados

- Branch: master
- Total de commits: 268
- HEAD: 5da797b "fix(debt): resolve pre-existing git audit count and validate_script_quality case bug" (Thu May 14 2026)
- Primeiro commit: 067938a "feat: galFlowAI MVP - interface Gradio com barra de progresso" (Sat May 2 14:35:18 2026 -0300)
- Período: 6 dias de desenvolvimento (02/05 a 08/05/2026)
- Autores: Henrique Luiz, rickchiod-hash
- Working tree: untracked files (user's pending work — piper_adapter, checkpoint_manager, job_state, stages/, use_cases, utils/)
- Branch local logs-feature também existe (Central de Logs na UI)

## Tabelas

### Arquivos deletados no histórico (7 arquivos)

| Commit | Arquivo | Tipo | Motivo |
|---|---|---|---|
| dbb133f | BACKLOG_REFINADO.md | delete | Limpeza de docs antigos do backlog |
| dbb133f | PROGRESSO_ATUAL.md | delete | Limpeza de relatórios de progresso antigos |
| dbb133f | PROGRESSO_FINAL.md | delete | Limpeza de relatórios de progresso antigos |
| dbb133f | RESUMO_FINAL.md | delete | Limpeza de resumos antigos |
| dbb133f | STATUS_ATUAL.md | delete | Limpeza de status antigos |
| dbb133f | STATUS_FINAL.md | delete | Limpeza de status antigos |
| b20cd77 | tests/integration/test_api_contract.py | delete | Removeu teste duplicado |

### Principais marcos no histórico

| Commit | Tipo | Descrição | Impacto |
|---|---|---|---|
| 067938a | feat | MVP inicial — Gradio + barra de progresso | Fundação do projeto |
| 26a0644 | feat | Pipeline real ativo — remove mock, integra FFmpeg | Pipeline funcional |
| acd5ed2 | feat | WanGP 1.3B + FFmpeg fallback | Engine de vídeo |
| 0c19382 | feat | TTS offline integrado | Áudio funcional |
| 3ea7b9e | feat | 6 LLM Providers + FastAPI V2 + Script Service | Providers completos |
| d3c9af6 | refactor | H1+H2: identidade API + bare except removido | Qualidade de código |
| dbb133f | feat | H3: GPT4All, LMStudio, KoboldCpp, LlamaCpp | Infra LLM completa |
| ee05f5c | refactor | REF-01: GalFlowAI → GalFlowAI | Renomeação completa |
| b78e025 | feat | Central de Logs na UI | Observabilidade |
| 3132eb0 | docs | Import governance pack v2 | Governança adicionada |
| 63839e7 | docs | GOV-006: AGENTS + Skill | Fase 1 completa |

### Arquivos mais alterados (top 10)

| Arquivo | Commits |
|---|---|
| app/main.py | 15+ |
| app/api.py | 10+ |
| README.md | 10+ |
| BACKLOG.md | 8+ |
| pipelines/auto_pipeline.py | 7+ |
| app/services/script_service.py | 6+ |
| app/config.py | 5+ |
| app/adapters/llm/provider_router.py | 5+ |
| app/pipeline/script_generator.py | 4+ |
| app/pipeline/video_generation_pipeline.py | 4+ |

## Perguntas obrigatórias

1. **Quais telas existiam e sumiram?** — Nenhuma. Gradio (app/main.py) e FastAPI (app/api.py) continuam presentes. Branch logs-feature adicionou tela de Central de Logs.

2. **Quais providers foram removidos, renomeados ou escondidos?** — Nenhum provider removido. Todos os 6 LLM providers preservados (Template, LM Studio, GPT4All, KoboldCpp, LlamaCpp, GPT-compatible/Ollama). WanGP e FFmpeg presentes. TTS (pyttsx3/silence) presente. Piper adapter como untracked (pendente).

3. **Quais fallbacks foram alterados?** — Nenhum. TemplateProvider presente como fallback de roteiro. FFmpeg presente como fallback de vídeo. TTS: pyttsx3/silence presente.

4. **Quais docs dizem que algo existe, mas o código não comprova?** — PROJECT_REFERENCE_CONTEXT.md e FEATURE_PRESERVATION_MATRIX.md estavam apenas na cópia COMERCIAL (runtime), não commitados no git. Corrigido em CORE-100.

5. **Quais TODOs foram resolvidos e quais ficaram órfãos?** — 0 TODOs encontrados no código (confirmado por varredura).

6. **Quais arquivos mais mudaram nos últimos commits?** — app/main.py, docs/project-control/* (governance), AGENTS.md, tests/*.py.

7. **O último commit aproxima ou afasta o produto do fluxo por etapas?** — Neutro: GOV-006 é documental (AGENTS/SKILL). Não altera fluxo do produto.
