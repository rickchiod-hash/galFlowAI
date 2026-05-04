# Prompt para OpenCode — Refatoração Modular + Cobertura de Testes

Use este prompt no OpenCode:

```text
Leia primeiro `qa/QA_TEST_PLAN.md`.

Objetivo:
- Aumentar cobertura de testes com cenários reais.
- Refatorar incrementalmente sem quebrar endpoints/fallbacks atuais.
- Aplicar SOLID e padrões (Strategy, Factory, Adapter, Result Object).

Passos obrigatórios:
1) Implementar testes T1, T2 e T3 do QA plan.
2) Criar `app/application/use_cases/` e mover lógica de negócio da API para use cases.
3) Manter `app/api.py` como controller fino.
4) Padronizar erros: `{ok, code, message, details}`.
5) Preservar fallback obrigatório: TemplateProvider e FFmpeg.
6) Rodar:
   - `pytest -q`
   - `pytest --cov=app --cov-report=term-missing --cov-report=xml`
   - `python -m py_compile app/api.py`
7) Atualizar `qa/QA_TEST_PLAN.md` com status [feito|pendente] por item.

Restrições:
- Não alterar contratos públicos de endpoint sem documentação/compatibilidade.
- Não depender de internet, GPU real ou API paga para testes.
- Não fazer big-bang rewrite; entregar por etapas pequenas.
```
