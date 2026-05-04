# Roteiro Editável

Este documento descreve o fluxo de edição, versionamento e aprovação de roteiro no Gal AI.

## Fluxo
1. Gerar roteiro inicial (provider local ou template).
2. Editar manualmente na interface.
3. Salvar nova versão.
4. Aplicar melhorias (quando disponível).
5. Aprovar versão final para geração de cenas.

## Arquivos de versão
```text
projects/<project_id>/script/
  script_v001.md
  script_v001.json
  script_v002.md
  script_approved.md
  script_approved.json
  script_versions.json
```

## Endpoints relacionados
- `POST /api/projects/{id}/script/save-manual-edit`
- `POST /api/projects/{id}/script/improve`
- `POST /api/projects/{id}/script/approve`
- `GET /api/projects/{id}/script/current`
- `GET /api/projects/{id}/script/versions`
