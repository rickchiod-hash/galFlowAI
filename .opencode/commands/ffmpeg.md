---
description: Implementar fallback e montagem com FFmpeg
agent: build
---

Implemente app/adapters/ffmpeg_adapter.py.

Funções:
- criar storyboard estático em vídeo usando imagens, texto e duração;
- transformar imagens em clipes;
- concatenar cenas em ordem;
- converter para 30 FPS;
- exportar MP4 final;
- gerar versão 9:16, 1:1 e 16:9 quando possível;
- salvar comando FFmpeg executado em logs.

Critério de aceite:
- sem WanGP, o sistema ainda deve gerar final_30fps_preview.mp4.
