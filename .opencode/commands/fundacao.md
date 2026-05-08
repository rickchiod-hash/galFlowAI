---
description: Criar fundação K-only do GalFlowAI
agent: build
---

Implemente a fundação do GalFlowAI.

Crie estrutura modular, se ainda não existir:
- app/
- app/adapters/
- app/pipeline/
- app/jobs/
- app/services/
- app/ui/
- app/utils/
- tests/
- scripts/
- docs/

Crie:
- app/config.py com todos os paths K-only;
- app/hardware.py para detectar disco, RAM, GPU, VRAM, CUDA e torch.cuda.is_available();
- app/logging_config.py;
- app/safety.py com backup antes de sobrescrever;
- scripts/check_environment.bat;
- scripts/start_app.bat.

Critério de aceite:
- rodar check_environment sem escrever no C:;
- gerar log;
- exibir preset recomendado para GTX 1660 Super.
