# AUDIO_TTS_PROVIDER_PLAYBOOK — GalFlowAI

## Visão geral

Este playbook documenta os providers de áudio/TTS do GalFlowAI. O pipeline de áudio gera narração, legendas e efeitos sonoros a partir do roteiro de cada cena. TTS é opcional — o pipeline não pode ser bloqueado por falha de áudio.

Componentes de áudio:
- **AudioPlan** — roteiro de narração por cena + narration_script.md
- **TTS Engine** — gera WAV por cena (opcional)
- **SRT Generator** — gera legendas baseadas no timing das cenas
- **SFX Manifest** — registro de licença e origem de assets sonoros

## Stories mapeadas

| Story ID | Título | Status | SP | Prioridade | DoR completo |
|----------|--------|--------|----|-----------|-------------|
| AUD-700 | Criar AudioPlan e narration_script.md | Concluída | 5 | Alta | Sim |
| AUD-701 | Gerar áudio por cena com fallback | Concluída | 5 | Média | Sim |
| AUD-702 | Gerar SRT por timing de cena | Pendente | 3 | Média | Não |
| AUD-703 | Criar SFX manifest | Pendente | 3 | Baixa | Não |
| QA-1004 | Criar teste TTS falha → export sem áudio | Concluída | 3 | Média | Pendente playbook |

### AUD-700 — Criar AudioPlan e narration_script.md

**Status:** Concluída ✅  
**Estimativa:** 5 SP  
**Épico:** EPIC-800 Audio  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#aud-700`  
**Testes:** `08_PLANO_DE_TESTES.md#aud-700`  

AudioPlan schema + AudioPlanService implementados. 41 testes. Commit `a68ceeb`.

### AUD-701 — Gerar áudio por cena com fallback

**Status:** Concluída ✅  
**Estimativa:** 5 SP  
**Épico:** EPIC-800 Audio  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#aud-701`  
**Testes:** `08_PLANO_DE_TESTES.md#aud-701`  

TTSAudioService implementado em `app/services/tts_audio_service.py`. Gera `scene_{n:03d}.wav` por cena a partir do AudioPlan. Fallback silencioso: falha TTS nao bloqueia. 19 testes. Commit `140fb6e`.

### AUD-702 — Gerar SRT por timing de cena

**Status:** Pendente  
**Estimativa:** 3 SP  
**Épico:** EPIC-800 Audio  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#aud-702`  
**Testes:** `08_PLANO_DE_TESTES.md#aud-702`  

Gerar arquivo SRT com legendas baseadas no timing de cada cena. Permite que o vídeo seja usado em redes sociais sem áudio.

### AUD-703 — Criar SFX manifest

**Status:** Pendente  
**Estimativa:** 3 SP  
**Épico:** EPIC-800 Audio  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#aud-703`  
**Testes:** `08_PLANO_DE_TESTES.md#aud-703`  

Registrar licença, origem e metadados de cada asset sonoro (SFX). Prevenir uso indevido de assets sem licença.

### QA-1004 — Criar teste TTS falha → export sem áudio

**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Épico:** EPIC-1100 QA contínuo  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#qa-1004`  
**Testes:** `08_PLANO_DE_TESTES.md#qa-1004`  

Teste que valida: quando TTS falha, o pipeline não bloqueia — o MP4 final é gerado sem áudio.

## Arquitetura / Decisões

### Pipeline de áudio
AudioPlan → TTS Engine → WAV por cena → (SRT Generator opcional)

### TTS opcional
TTS não é obrigatório para o pipeline de vídeo. Falha de TTS resulta em vídeo sem áudio, não em erro de pipeline.

### SFX manifest separado
Assets sonoros são registrados em manifesto separado com licença e origem. Não fazem parte do pipeline principal.

## Regras de preservação

1. **TTS nunca bloqueia o pipeline** — falha = sem áudio, não sem vídeo
2. **AudioPlan é o contrato central** — toda narração passa por ele
3. **SRT é derivado do AudioPlan** — nunca gerado independentemente
4. **SFX manifest é documental** — não afeta a execução do pipeline
5. **Provider de TTS novo deve ser opcional** — nunca exigir TTS para MP4 mínimo

## Referências

- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — AUD-700..703, QA-1004
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — descrição detalhada (linhas 1496-1678, 2140-2184)
- `docs/project-control/07_CRITERIOS_ACEITE_GHERKIN.md` — critérios Gherkin
- `docs/project-control/08_PLANO_DE_TESTES.md` — plano de testes
- `docs/project-control/11_DECISOES_TECNICAS_ADR.md` — ADRs de áudio
