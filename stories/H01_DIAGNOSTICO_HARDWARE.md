# História H01 — Diagnóstico de hardware

Como sistema, quero detectar CPU, RAM, GPU, VRAM, CUDA, torch.cuda.is_available e espaço livre para escolher presets seguros.

## Critérios de aceite
- Detecta GTX 1660 Super ou informa GPU não identificada.
- Se VRAM <= 6 GB, recomenda 1.3B, 480p, 49 frames, uma cena por vez.
- Bloqueia 14B como padrão.
- Exibe diagnóstico na UI e em log.
