# História H07 — Fila de jobs

Como sistema, quero enfileirar tarefas para manter a UI responsiva e evitar concorrência na GPU.

## Critérios de aceite
- Jobs possuem ID e status.
- UI mostra progresso.
- Cancelamento funciona antes do job começar.
- Lock impede dois renders de vídeo simultâneos.
