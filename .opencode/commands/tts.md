---
description: Implementar áudio, narração e legendas
agent: build
---

Implemente módulo de áudio.

Prioridade:
1. placeholder determinístico para MVP;
2. TTS offline simples se disponível;
3. Kokoro/Coqui como evolução sem quebrar ambiente.

Arquivos:
- app/adapters/tts_adapter.py
- app/adapters/subtitle_adapter.py

Requisitos:
- gerar áudio por cena em audio/scene_XX.wav;
- salvar script de narração;
- criar legendas .srt básicas usando timing por cena;
- permitir montar vídeo sem áudio se TTS falhar.
