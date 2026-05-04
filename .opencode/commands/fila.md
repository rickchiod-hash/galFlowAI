---
description: Implementar fila local e lock de GPU
agent: build
---

Implemente fila de jobs.

Comece com fila local persistida em SQLite/JSON, sem exigir Redis.
Depois deixe adaptador opcional para Redis/RQ.

Requisitos:
- job_id;
- tipo do job;
- status: queued, running, failed, done, canceled;
- logs por job;
- cancelamento cooperativo;
- lock de GPU para impedir duas renderizações de vídeo simultâneas;
- processamento assíncrono no app para não travar a UI.

Critério de aceite:
- enfileirar render de cena;
- consultar status;
- cancelar job antes de começar;
- UI continuar responsiva.
