# Root Cause Matrix — GalFlowAI P0 Recovery

| ID | Bug | File | Lines (before fix) | Root Cause | Impact | Fix |
|----|-----|------|-------------------|------------|--------|-----|
| UI-210 | Aprovar roteiro não persiste | `gradio_app.py` | 106-113 | `on_approve_script` setava `app_state_val["script_approved"] = True` em memória apenas, sem chamar `approve_script()` de `script_service`. | Script nunca era salvo em disco como `script_approved.md`/`.json`. Pipeline enxergava roteiro não aprovado. | Adicionado `from app.services.script_service import approve_script` e chamada `approve_script(project_id)` com verificação de retorno. |
| UI-209 | Salvar edição manual ignora texto | `gradio_app.py` | 393-399 | `on_save_edit` recebia `script_text` mas chamava `generate_script_with_provider("Edicao manual salva", "template")` — gerava script dummy no lugar do texto digitado pelo usuário. | Edições manuais do usuário eram perdidas. | Callback agora recebe `app_state` como input e chama `save_manual_edit(pid, script_text, ...)`, atualizando `app_state_val["script"]` com o texto real. |
| — | Render bypassa aprovação | `gradio_app.py` | 324-355 | `on_render_scenes` criava `script_approved.md` incondicionalmente via `(script_path / "script_approved.md").write_text(...)` antes de renderizar, sem verificar `app_state_val.get("script_approved")`. | Render podia acontecer sem aprovação, quebrando o fluxo stage-gated. | Adicionado gate `if not app_state_val.get("script_approved", False): return ... ERRO`. Removido write unconditional de `script_approved.md`. |
| PROV-304 | Provider selecionado falha silenciosamente | `gradio_app.py` + `script_service.py` | 91-104 + 55-120 | `generate_script_with_provider` faz fallback para TemplateProvider quando o provider selecionado falha, mas o resultado não expunha o fallback ao usuário. UI hardcodava qualidade como "template". | Usuário não via que o provider selecionado falhou. Parecia que o provider escolhido funcionou normalmente. | Adicionado `fallback_note` no status_md de `on_generate_script` quando `quality == "fallback"`. Qualidade agora lida do resultado em vez de hardcoded. |

## Resumo

4 bugs P0 identificados, todos corrigidos:
- **3 bugs de binding/estado** (UI-210, UI-209, gate bypass) — falha na ligação entre callback UI e serviço real
- **1 bug de observabilidade** (PROV-304) — falha silenciosa mascarada por fallback correto

## Anti-regressão

- Testes existentes: 828 passed (excluindo 1 pre-existing git audit count)
- Regressão: **zero**
- Cobertura de approval gate: tests em `test_ui_workflow_order.py` e `test_h10_contract.py`
