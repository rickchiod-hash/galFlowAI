import os
from pathlib import Path

# Read current BACKLOG.md
backlog_path = Path("K:/AI_VIDEO_COMMERCIAL_STUDIO/opencodegalpasta/BACKLOG.md")
with open(backlog_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define missing sections (all in Portuguese Brazilian, no "prompts visuais em inglês")
missing_sections = """

## Backlog — Arquitetura de Prompt Anti-Alucinação para Vídeo

### P1-AV-01 — Criar Prompt Context Pack schema
Contexto:
Prompts soltos por cena causam perda de personagem/produto, mudança de cor, objetos inventados e inconsistência entre cenas.

Critério de aceite:
- schema para visual_bible, locked_objects, style_lock, color_palette_lock, forbidden_changes, scene_contracts, global_negative_prompt, per_scene_negative_prompt e consistency_checklist;
- teste unitário para celular branco, fantasia medieval e boneco 3D;
- sem alterar o pipeline de render nesta etapa.

### P1-AV-02 — Criar NegativePromptBuilder mínimo
Contexto:
O negative prompt atual não garante bloqueio de mudanças críticas.

Critério de aceite:
- se briefing contém "celular branco”, incluir black phone, blue phone, color drift, extra camera, logo artifacts;
- se briefing contém “fantasia preta dourada”, bloquear troca de cor, roupa moderna e perda de detalhes dourados.

### P1-AV-03 — Criar ConsistencyValidator mínimo
Contexto:
O sistema não deve renderizar prompt inconsistente.

Critério de aceite:
- validar cor travada;
- validar objeto principal;
- validar objetos proibidos;
- validar negative prompt;
- validar uma ação principal por cena;
- se falhar, não renderizar e mostrar erro em português.

### P1-AV-04 — Separar prompt de roteiro e prompt de vídeo
Contexto:
Roteiro vende; prompt de vídeo preserva identidade, produto, câmera e movimento.

Critério de aceite:
- criar templates separados para roteiro, vídeo, I2V e T2V;
- prompts de vídeo em português brasileiro;
- UI continua em português.

### P1-AV-05 — Preparar Reference Asset Map
Contexto:
Imagem de referência precisa virar artefato rastreável.

Critério de aceite:
- salvar uploads em projects/<project_id>/assets/reference/;
- criar reference_asset_map.json;
- cada asset deve ter id, tipo, path, uso permitido e cenas associadas.

### P2-AV-06 — Visual Bible editável na UI
Contexto:
Usuário precisa revisar e corrigir identidade visual antes de gerar vídeo.

Critério de aceite:
- seção “Consistência visual”;
- descrição fixa;
- cores que não podem mudar;
- materiais;
- objetos obrigatórios;
- objetos proibidos;
- modo anti-alucinação;
- salvar em project/visual_context.

### P2-AV-07 — Compilar prompt por engine
Contexto:
WanGP, FFmpeg fallback e futuros engines não consomem prompts iguais.

Critério de aceite:
- compiler com modos wangp_i2v, wangp_t2v, ffmpeg_storyboard e generic_video;
- se imagem de referência existir, preferir I2V;
- salvar prompts por cena.

### P2-AV-08 — Salvar Prompt Pack versionado
Contexto:
Edição de visual bible e prompt precisa ser rastreável.

Critério de aceite:
- prompt_pack_v001.json;
- prompt_pack_v002.json;
- prompt_pack_approved.json;
- cada render aponta para prompt_version.

### P2-AV-09 — Métricas de consistência
Contexto:
Sem métricas, ajuste de prompt vira chute.

Critério de aceite:
- object_lock_score;
- color_lock_score;
- forbidden_object_score;
- negative_prompt_score;
- prompt_specificity_score;
- score abaixo do threshold bloqueia render.

### P3-AV-10 — Validação pós-render futura
Contexto:
Mesmo prompt bom pode falhar.

Critério de aceite:
- documentar como futuro;
- não implementar OCR/visão agora;
- não adicionar dependência pesada.

## Críticas por módulo

### Front / Gradio
- precisa usar gr.State para project_id real;
- remover project_id dummy;
- padronizar Gal AI em vez de FlowForgeAI;
- mover textos restantes para PT-BR;
- separar tabs: Briefing, Roteiro, Consistência Visual, Cenas, Geração, Resultado, Logs e Diagnóstico;
- melhorar erro por etapa;
- diferenciar Preview FFmpeg de Vídeo IA;
- adicionar status de provider;
- adicionar status de prompt pack;
- evitar lógica pesada de pipeline dentro da UI.

### Backend / Services
- ScriptService deve ser fonte única;
- criar use cases gradualmente;
- padronizar envelope de erro;
- adicionar idempotency key;
- centralizar config;
- logs com project_id, job_id, provider e fallback_used;
- providers fake para teste;
- métricas locais;
- versionamento de prompt;
- contratos de prompt por engine.

### API / FastAPI
- planejar versão futura /api/v1;
- criar testes de contrato;
- WebSocket não pode ficar placeholder para sempre;
- jobs precisam estado real;
- operações longas não devem bloquear request;
- OpenAPI precisa refletir endpoints reais;
- healthcheck deve validar componentes;
- erro deve ter code/message/details/retryable;
- API não deve duplicar lógica da UI;
- endpoints de prompt pack devem ser planejados.

### Integração / Pipeline
- WanGP opcional precisa contrato claro;
- FFmpeg fallback precisa teste de concat/path;
- TTS precisa sincronização e fallback validado;
- PromptBuilder precisa anti-alucinação;
- lock de GPU max_gpu_jobs=1;
- cache de prompt/render/TTS;
- cada render precisa registrar prompt_version;
- separar T2V e I2V;
- validar prompt antes de render;
- não renderizar se consistência falhar.

### Observabilidade / Logs
- logs devem ter project_id, job_id, provider, fallback_used e etapa;
- DEBUG nunca aparece na UI;
- leitura de logs deve ser limitada;
- diagnóstico não pode expor segredo;
- FastAPI pode expor logs por endpoint, mas WebSocket é opcional;
- Central de Logs deve continuar funcionando sem FastAPI;
- logs devem ficar no K:;
- rotação obrigatória para evitar arquivo gigante;
- erro de log não pode quebrar app;
- backlog e troubleshooting devem ser atualizados com problemas reais.
"""

# Append to BACKLOG.md
with open(backlog_path, 'a', encoding='utf-8') as f:
    f.write(missing_sections)

print("Missing sections appended successfully")
print("Total length:", len(content) + len(missing_sections), "chars")
