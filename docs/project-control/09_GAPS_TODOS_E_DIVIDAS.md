# 09_GAPS_TODOS_E_DIVIDAS — GalFlowAI

## Política

Todo gap, TODO ou dívida precisa ter ID, origem, evidência, impacto, história relacionada e próxima ação.

## Formato obrigatório

```md
## GAP-XXX — Título

- Tipo: funcional | técnico | arquitetura | QA | documentação | dependência
- Origem:
- Evidência:
- Impacto:
- História relacionada:
- Como validar:
- Próxima ação:
- Status:
```

## TODO no código

Padrão obrigatório:

```python
# TODO(GAL-XXX, type=blocked|debt|follow-up): resumo
# Contexto: ...
# Evidência: ...
# Dependência: ...
# Critério de aceite: ...
# Backlog: docs/project-control/05_BACKLOG_PRIORIZADO.md#gal-xxx
```

TODO genérico é proibido.

## Resultado da varredura de código

- **GalFlowAI|GalFlowAI**: 0 ocorrências em código funcional (apenas em PROMPT.md do pack).
- **TODO|FIXME|HACK|XXX**: 0 ocorrências em `app/`, `docs/`, `tests/`.
- **bare except:** encontrado em `app/main.py`, `app/adapters/ffmpeg_adapter.py`, `app/adapters/translator_adapter.py`, `app/adapters/tts_adapter.py`, `app/services/metrics_service.py`, `app/application/use_cases/` (alguns casos), testes. Necessita auditoria para substituir por `except Exception:`.
- **C: paths**: encontrado em docs de instalação: `docs/INSTALAR_KOBOLDCPP_K.md`, `docs/INSTALAR_LM_STUDIO_K.md`, `docs/LLM_LOCAL_SEM_API_KEY.md`, `docs/MOTORES_ROTEIRO_TELA.md`, `docs/VIDEO_PIPELINE.md`. São referências de instalação de ferramentas, não código funcional.

## Gaps iniciais a validar

| ID | Gap | História | Evidência necessária | Status |
|---|---|---|---|---|
| GAP-001 | Estado real do último commit não auditado | CORE-100 | `git log -1 --oneline` — feito: 7017ea8 | Concluído |
| GAP-002 | Diferença docs/código não mapeada | CORE-102 | auditoria docs/code — feita em 03_ARQUITETURA_ATUAL.md | Concluído |
| GAP-003 | UI atual precisa ser comparada ao fluxo por etapas | UI-200 | app/main.py + screenshot — story map reescrito em 19_STORY_MAP.md | Concluído |
| GAP-004 | Providers precisam ser listados por código real | PROV-300 | provider registry/adapters — mapeado em LLM_PROVIDER_PLAYBOOK.md | Concluído |
| GAP-005 | bare except: em arquivos fonte | CORE-101 | varredura grep — corrigido para `except Exception:` em 12 locais | Concluído |
| GAP-006 | C: paths em documentação | DOC-103 | varredura grep — referências informativas em docs de instalação, não são hardcoded paths de código | Mantido como documentação |
| GAP-007 | TODO_TECNICO sem história vinculada em 3 arquivos | GAL-930..935 | script_service.py:18, pipeline.py:28, api.py:53 | Corrigido — convertido para TODO(GAL-XXX) |
| GAP-008 | 42/44 rotas API sem type hint de retorno | GAL-935 | api.py | Corrigido — adicionado `-> JSONResponse` |
| GAP-009 | Legacy pipeline modules duplicam use cases | GAL-936 | `pipeline/script_generator.py`, `scene_splitter.py`, `prompt_builder.py` | ✅ Concluído — removido em S38, commitado S39 |
| GAP-010 | async wrappers sobre sync blocking calls | GAL-937 | `provider_router.py`, `script_service.py`, `provider_strategy.py` | Em resolução — convertido sync em S39 |
| GAP-011 | Test coverage baixo em script_service.py | GAL-932 | 1 teste apenas | Documentado — pendente |
| GAP-012 | Sem teste E2E fallback WanGP→FFmpeg | GAL-934 | — | Documentado — pendente |
| GAP-013 | Piper adapter prints em `__main__` | — | `piper_adapter.py:362-382` | Mantido como test block — não afeta produção |
