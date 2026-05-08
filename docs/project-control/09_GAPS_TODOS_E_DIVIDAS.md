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

- **FlowForgeAI|Gal AI**: 0 ocorrências em código funcional (apenas em PROMPT.md do pack).
- **TODO|FIXME|HACK|XXX**: 0 ocorrências em `app/`, `docs/`, `tests/`.
- **bare except:** encontrado em `app/main.py`, `app/adapters/ffmpeg_adapter.py`, `app/adapters/translator_adapter.py`, `app/adapters/tts_adapter.py`, `app/services/metrics_service.py`, `app/application/use_cases/` (alguns casos), testes. Necessita auditoria para substituir por `except Exception:`.
- **C: paths**: encontrado em docs de instalação: `docs/INSTALAR_KOBOLDCPP_K.md`, `docs/INSTALAR_LM_STUDIO_K.md`, `docs/LLM_LOCAL_SEM_API_KEY.md`, `docs/MOTORES_ROTEIRO_TELA.md`, `docs/VIDEO_PIPELINE.md`. São referências de instalação de ferramentas, não código funcional.

## Gaps iniciais a validar

| ID | Gap | História | Evidência necessária | Status |
|---|---|---|---|---|
| GAP-001 | Estado real do último commit não auditado | CORE-100 | `git log -1 --oneline` — feito: 7017ea8 | Concluído |
| GAP-002 | Diferença docs/código não mapeada | CORE-102 | auditoria docs/code | Pendente |
| GAP-003 | UI atual precisa ser comparada ao fluxo por etapas | UI-200 | app/main.py + screenshot | Pendente |
| GAP-004 | Providers precisam ser listados por código real | PROV-300 | provider registry/adapters | Pendente |
| GAP-005 | bare except: em arquivos fonte | CORE-101 | varredura grep — corrigido para `except Exception:` em 12 locais | Concluído |
| GAP-006 | C: paths em documentação | DOC-103 | varredura grep — referências informativas em docs de instalação, não são hardcoded paths de código | Mantido como documentação |
