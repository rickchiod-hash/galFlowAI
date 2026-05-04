---
description: Implementar scene split, storyboard e prompts por cena
agent: build
---

Implemente divisão automática em cenas.

Cada cena deve ter:
- scene_id;
- título;
- duração;
- texto de narração;
- descrição visual;
- prompt positivo;
- prompt negativo;
- formato;
- seed;
- status;
- caminhos esperados para render e áudio.

Salvar em:
- storyboard/scenes.json
- prompts/scene_XX_prompt.txt
- prompts/scene_XX_negative.txt

Critério de aceite:
- para um roteiro de 30s, gerar 5 a 8 cenas curtas;
- cada cena pode ser refeita isoladamente.
