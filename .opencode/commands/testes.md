---
description: Criar testes e smoke tests
agent: build
---

Crie testes PyTest e scripts de smoke test.

Cobrir:
- criação de projeto;
- geração de roteiro fallback;
- geração de cenas;
- criação de prompts;
- montagem FFmpeg fallback;
- validação de paths K-only;
- bloqueio de 14B como padrão;
- backup antes de sobrescrever.

Criar scripts:
- scripts/run_tests.bat
- scripts/smoke_create_project.bat

Critério de aceite:
- pytest passa;
- smoke test gera um projeto exemplo e um preview MP4.
