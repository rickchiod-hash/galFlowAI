# Roadmap FlowForgeAI

## Fase 0 — Auditoria e fundação
Entregável: diagnóstico K-only, mapa de pastas, validação de ambiente, plano de implementação.

## Fase 1 — MVP Gradio + projeto local
Entregável: app em 127.0.0.1:7860, criação de projeto e salvamento de project.json.

## Fase 2 — Roteiro, cenas e prompts
Entregável: gerar roteiro comercial, dividir cenas e criar prompts positivos/negativos.

## Fase 3 — Fallback FFmpeg
Entregável: gerar storyboard estático e final_30fps_preview.mp4 sem IA pesada.

## Fase 4 — Integração WanGP segura
Entregável: adaptador para WanGP com preset 1.3B, 480p, cena por vez, logs e cancelamento.

## Fase 5 — Fila e jobs
Entregável: fila local com lock de GPU; depois Redis/RQ se necessário.

## Fase 6 — Áudio, TTS e legendas
Entregável: narração offline, áudio por cena e legendas básicas.

## Fase 7 — Polimento e QA
Entregável: testes, README, scripts BAT, validação de não uso do C:.
