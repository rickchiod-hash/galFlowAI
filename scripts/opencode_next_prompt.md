# Prompt para próxima execução (não executar agora)

```text
Contexto: NÃO executar mudanças agora. Apenas preparar e enfileirar backlog técnico para continuidade da implementação atual.

1) Antes de tudo, faça sincronização Git:
- Verifique branch atual: `git branch -vv`
- Configure upstream se necessário: `git branch --set-upstream-to=origin/<branch> <branch_local>`
- Rode: `git pull --rebase`

2) Leia obrigatoriamente estes arquivos antes de codar:
- `BACKLOG.md`
- `qa/QA_TEST_PLAN.md`
- `scripts/opencode_refactor_prompt.md`
- `README.md`

3) Continuar a implementação atual (sem ruptura):
- Preservar endpoints existentes.
- Preservar fallback TemplateProvider e FFmpeg.
- Não introduzir dependência cloud.

4) Colocar na fila de revisão/criação/melhoria (ordem):
- Itens P0/P1 do BACKLOG.
- Fases T1/T2/T3 de testes do QA plan.
- Gaps faltantes descritos no BACKLOG (contratos de erro, concorrência, timeout/retry/backoff, métricas, validação de arquivos).

5) Item obrigatório pós-etapa atual (`[Pasted ~5 lines]`):
- Criar 3 testes unitários cobrindo cenários principais e falhas.
- Criar cenários de automação e chamadas de API.
- Aumentar cobertura com cenários realistas para achar gaps.
- Revisar e atualizar `qa/QA_TEST_PLAN.md` com status [feito|pendente].

6) Entrega esperada:
- Plano curto do que será implementado (sem executar tudo de uma vez).
- Commits pequenos por componente.
- Relatório final com: testes criados, cobertura obtida, gaps remanescentes.
```
