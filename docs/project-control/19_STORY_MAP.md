# 19_STORY_MAP — GalFlowAI

Story map por jornada do usuário/produto.

## Fluxo por etapas validáveis

Cada etapa tem um **gate de validação**: a etapa seguinte não executa sem aprovação da anterior.

```text
ETAPA 1: BRIEFING
  │   Usuário: insere produto, público-alvo, estilo, duração
  │   Sistema: salva projeto
  ▼
[GATE] Briefing preenchido? → Sim
  │
ETAPA 2: ROTEIRO (implementado)
  │   Sistema: gera roteiro via LLM (provider_router → modelo selecionado)
  │   Usuário: edita, melhora, complementa, define estilo
  │           aprova (btn_approve) ou rejeita
  ▼
[GATE] Roteiro aprovado? → Sim
  │
ETAPA 3: CENAS (implementado)
  │   Sistema: divide roteiro em cenas (scene_splitter)
  │           salva em storyboard/scenes.json
  │   Usuário: (futuro: revisa cenas)
  ▼
[GATE] Cenas OK? → Sim (automático)
  │
ETAPA 4: PROMPTS (implementado)
  │   Sistema: gera prompts de vídeo por cena (prompt_builder)
  │           salva em prompts/prompts.json
  ▼
[GATE] Prompts OK? → Sim (automático)
  │
ETAPA 5: NARRAÇÃO (implementado)
  │   Sistema: gera áudio TTS (tts_adapter → pyttsx3/silence/piper)
  │           salva em audio/narration.wav
  ▼
[GATE] Áudio OK? → Sim (fallback silence)
  │
ETAPA 6: VÍDEO (implementado)
  │   Sistema: renderiza cada cena (wangp_adapter → ffmpeg_adapter fallback)
  │           salva em renders/scene_XXX.mp4
  ▼
[GATE] Pelo menos 1 cena renderizada? → Sim
  │
ETAPA 7: MONTAGEM FINAL (implementado)
  │   Sistema: concatena vídeos + áudio via FFmpeg
  │           salva em final/commercial.mp4
  ▼
[GATE] MP4 gerado? → Sucesso!
```

### Etapas planejadas (futuras)

| Etapa | História | Status |
|---|---|---|---|
| SceneContracts | VIS-502 | Concluída |
| Visual Bible | VIS-501 | Concluída |
| Ingredient Registry | VIS-500 | Concluída |
| Prompt Context Pack | VIS-503 | Concluída |
| RenderPlan | RND-600 | Concluída |
| AudioPlan por cena | AUD-700, AUD-701 | Concluída |
| SRT/Legendas | AUD-702 | Concluída |
| Vector memory | VEC-800..803 | Concluída |

## Story map por atividade

| Atividade | Passos | Histórias | MVP |
|---|---|---|---:|
| Governar projeto | status, backlog, ADR, preservação | GOV-001..GOV-006 | Sim |
| Diagnosticar estado real | Git, código, docs, gaps | CORE-100..CORE-102 | Sim |
| Entrar briefing | produto, público, estilo, duração | UI-201 (parcial) | Sim |
| Criar roteiro | LLM provider, template, edição, aprovação | UI-201, PROV-300, PROV-301 | Sim |
| Aprovar roteiro | versionar, aprovar, bloquear próximas etapas | UI-202 | Sim |
| Dividir em cenas | split automático, revisão | UI-201 (parcial) | Sim |
| Gerar prompts | prompt builder por cena | VIS-503 | P1 |
| Renderizar | WanGP, FFmpeg fallback, cache | RND-600..RND-603 | Sim |
| Narrar | TTS, áudio por cena, SRT, SFX | AUD-700..AUD-703 | P1 |
| Observar | logs, métricas, diagnóstico | OBS-900, OBS-901, UI-203 | Sim |
| Evoluir memória | vector adapter, quality gate | VEC-800..VEC-803 | P2 |

## Regras do fluxo

1. **Roteiro deve ser aprovado antes de gerar cenas.** (UI-202)
2. **Cenas geradas antes de prompts.** (fluxo atual)
3. **TTS falha não quebra vídeo:** fallback silence. (PROJECT_REFERENCE_CONTEXT.md)
4. **WanGP falha → FFmpeg:** fallback universal. (PROJECT_REFERENCE_CONTEXT.md)
5. **Cada etapa salva artefato em disco** para rastreabilidade e retomada.
