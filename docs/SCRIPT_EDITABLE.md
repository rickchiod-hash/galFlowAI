# Roteiro Editável - Gal AI

## Visão Geral

O usuário pode editar o roteiro gerado antes de prosseguir para cenas/vídeo.

## Fluxo

1. **Gerar Roteiro** (via LLM ou Template)
2. **Exibir na UI** (campo editável)
3. **Editar Manualmente** (o usuário altera o texto)
4. **Salvar Edição** (cria nova versão)
5. **Melhorar/Complementar** (botões de ação)
6. **Aprovar** (marca como pronto para cenas)

## Botões Disponíveis

### Edição
- **Salvar Edição Manual** → `POST /api/projects/{id}/script/save-manual-edit`
- **Melhorar Roteiro** → `POST /api/projects/{id}/script/improve`
- **Complementar** → `POST /api/projects/{id}/script/complement`

### Estilo
- **Mais Viral** → `POST /api/projects/{id}/script/more-viral`
- **Mais Premium** → `POST /api/projects/{id}/script/more-premium`
- **Mais Direto** → `POST /api/projects/{id}/script/more-direct`

### Versões
- **Nova Versão** → `POST /api/projects/{id}/script/new-version`
- **Restaurar Anterior** → `POST /api/projects/{id}/script/restore-previous`
- **Aprovar Roteiro** → `POST /api/projects/{id}/script/approve`

## Estrutura de Arquivos por Projeto

```
projects/<project_id>/script/
  script_v001.md          # Versão 1
  script_v001.json         # Metadados v1
  script_v002.md          # Versão 2
  script_v002.json        # Metadados v2
  script_approved.md      # Roteiro aprovado
  script_approved.json    # Metadados aprovado
  script_versions.json    # Lista de versões
```

## Formato do `script_versions.json`

```json
[
  {
    "version": "v001",
    "timestamp": "2026-05-03T00:46:00",
    "note": "Geração inicial",
    "script": "[Cena 1: Introducao]...",
    "status": "Draft",
    "provider_used": "TemplateProvider",
    "response_time_seconds": 0.5,
    "quality_score": 80
  },
  {
    "version": "v002",
    "timestamp": "2026-05-03T00:50:00",
    "note": "Edição manual",
    "script": "[Cena 1: Introducao - 5s]...",
    "status": "Approved",
    "provider_used": "Manual",
    "response_time_seconds": 0,
    "quality_score": 90
  }
]
```

## Regras

1. **Toda alteração cria nova versão** (nunca sobrescreve)
2. **Versão aprovada é usada para cenas** (script_approved.md)
3. **Se tentar criar cenas sem aprovação** → avisar: "Aprove o roteiro antes de criar cenas."
4. **Máximo de 10 versões** (pode ajustar)
5. **Versões podem ser deletadas** (mas aprovada nunca)

## UI (Gradio)

```python
with gr.Blocks() as demo:
    # Área do roteiro
    script_editor = gr.Textbox(
        label="Roteiro (editável)",
        lines=15,
        value=load_current_script(project_id)
    )
    
    with gr.Row():
        btn_save = gr.Button("Salvar Edição")
        btn_improve = gr.Button("Melhorar")
        btn_viral = gr.Button("Mais Viral")
        btn_premium = gr.Button("Mais Premium")
        btn_direct = gr.Button("Mais Direto")
    
    with gr.Row():
        btn_new_version = gr.Button("Nova Versão")
        btn_restore = gr.Button("Restaurar Anterior")
        btn_approve = gr.Button("Aprovar Roteiro", variant="primary")
    
    versions_list = gr.DataFrame(label="Versões")
```

## FastAPI Endpoints

### GET /api/projects/{id}/script/current
Retorna roteiro atual (ou aprovado se existir).

### GET /api/projects/{id}/script/versions
Lista todas as versões.

### POST /api/projects/{id}/script/save-manual-edit
Salva edição manual como nova versão.

### POST /api/projects/{id}/script/improve
Melhora roteiro atual.

### POST /api/projects/{id}/script/more-viral
Torna mais viral.

### POST /api/projects/{id}/script/approve
Aprova versão atual para produção.

## Testes

```python
def test_script_editing_flow():
    # 1. Gerar roteiro
    result = generate_script("comercial teste")
    assert result["ok"] == True
    
    # 2. Editar manualmente
    edited = result["script_markdown"] + "\n[Cena extra]..."
    save_result = save_manual_edit(project_id, edited)
    assert save_result["ok"] == True
    assert "v002" in save_result["version"]
    
    # 3. Aprovar
    approve_result = approve_script(project_id)
    assert approve_result["ok"] == True
    assert Path("script_approved.md").exists()
```

## Próximos Passos

1. **Integrar edição na UI Gradio** (app/main.py)
2. **Completar todos os endpoints** no app/api.py
3. **Criar script_versions.json** automáticamente
4. **Adicionar botão "Aprovar"** na UI
5. **Validar se roteiro aprovado existe** antes de criar cenas

---

**Versão:** 1.0  
**Data:** 03/05/2026  
**Status:** Fluxo implementado, falta integrar na UI
