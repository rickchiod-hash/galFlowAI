---
description: Integrar WanGP/Wan2GP com preset seguro
agent: build
---

Crie o adaptador WanGP sem quebrar a instalação existente.

Arquivo alvo:
- app/adapters/wangp_adapter.py

Requisitos:
- detectar K:\AI_VIDEO_COMMERCIAL_STUDIO\engines\Wan2GP;
- não reinstalar WanGP;
- não alterar arquivos do WanGP sem backup;
- gerar comandos reproduzíveis por cena;
- capturar stdout/stderr em logs;
- default seguro para GTX 1660 Super:
  - Wan2.1
  - Text2Video 1.3B ou Image2Video/Fun InP 1.3B quando referência existir
  - 480x832 para 9:16
  - 49 frames
  - 20 steps ou menos no preview
  - uma cena por vez
- bloquear 14B como padrão.

Se a CLI/headless do WanGP não estiver clara, crie adaptador com modo manual assistido: o app gera prompt, negative prompt, configurações e caminho de saída para o usuário colar na UI do WanGP.
