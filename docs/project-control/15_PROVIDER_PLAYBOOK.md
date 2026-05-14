# 15_PROVIDER_PLAYBOOK — GalFlowAI

Este arquivo é o roteador central para todos os playbooks específicos de provider.

## Resumo de stories

| Playbook | Stories vinculadas | Status |
|----------|-------------------|--------|
| `LLM_PROVIDER_PLAYBOOK.md` | PROV-300, PROV-301, PROV-302 | 3 Concluídas |
| `VIDEO_RENDER_PROVIDER_PLAYBOOK.md` | VIS-502, VIS-503, RND-600, RND-601, RND-602, RND-603, QA-1003, RND-610, RND-611, RND-612 | 10 Concluídas |
| `AUDIO_TTS_PROVIDER_PLAYBOOK.md` | AUD-700, AUD-701, AUD-702, AUD-703, QA-1004 | 5 Concluídas |
| `VECTOR_MEMORY_PLAYBOOK.md` | VIS-500, VIS-501, VEC-800, VEC-801, VEC-802, VEC-803, VEC-810, VEC-811 | 8 Concluídas |
| `QA_ANTI_HALLUCINATION_PLAYBOOK.md` | QA-1000, QA-1001, QA-1002 | 3 Concluídas |

**Total de histórias cobertas: 29** (das 65 do backlog)

## Providers LLM

Ver `docs/project-control/LLM_PROVIDER_PLAYBOOK.md`.

## Vídeo/render

Ver `docs/project-control/VIDEO_RENDER_PROVIDER_PLAYBOOK.md`.

## Áudio/TTS

Ver `docs/project-control/AUDIO_TTS_PROVIDER_PLAYBOOK.md`.

## IA vetorial

Ver `docs/project-control/VECTOR_MEMORY_PLAYBOOK.md`.

## QA e anti-alucinação

Ver `docs/project-control/QA_ANTI_HALLUCINATION_PLAYBOOK.md`.

## Regra geral

Provider novo deve ser opcional. Provider existente não pode ser removido sem ADR (ver `11_DECISOES_TECNICAS_ADR.md`).
