# Contexto do FlowForgeAI

O FlowForgeAI é uma plataforma local para criação semi-automática de comerciais, propagandas e vídeos curtos para redes sociais.

Objetivo: o usuário escreve o briefing, envia imagens do produto se quiser, e o sistema organiza roteiro, cenas, prompts, renderização por cena, narração, montagem final e exportação em MP4, preferencialmente vertical 9:16, 30 FPS e até 1080p por upscaling quando possível.

A aplicação deve rodar primeiro no PC local, em Windows, no disco K:, sem depender de serviços pagos.

Hardware real:
- Ryzen 5 5600
- GTX 1660 Super 6 GB VRAM
- 16 GB RAM
- disco K: como raiz obrigatória

Limitação central: 6 GB VRAM. O sistema deve priorizar modelos leves, cenas curtas, 480p/512p, upscaling posterior, FFmpeg para montagem, e evitar modelos 14B como padrão.
