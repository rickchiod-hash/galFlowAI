# Script Editable (Roteiro Editável) - Gal AI

> Este arquivo foi mantido por compatibilidade e agora aponta para a documentação atual.

A versão consolidada e atualizada está em:

- [`docs/ROTEIRO_EDITAVEL.md`](./ROTEIRO_EDITAVEL.md)

## Endpoints válidos no momento
- `POST /api/projects/{id}/script/save-manual-edit`
- `POST /api/projects/{id}/script/improve`
- `POST /api/projects/{id}/script/more-viral`
- `POST /api/projects/{id}/script/more-premium`
- `POST /api/projects/{id}/script/more-direct`
- `POST /api/projects/{id}/script/new-version`
- `POST /api/projects/{id}/script/restore-previous`
- `POST /api/projects/{id}/script/approve`
- `GET /api/projects/{id}/script/current`
- `GET /api/projects/{id}/script/versions`

> Nota: endpoint `.../script/complement` não está exposto atualmente em `app/api.py`.
