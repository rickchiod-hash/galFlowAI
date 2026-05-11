# VIDEO_RENDER_PROVIDER_PLAYBOOK — GalFlowAI

## Visão geral

Este playbook documenta os providers de renderização de vídeo do GalFlowAI. O pipeline de vídeo transforma roteiro em cenas visuais usando engines locais com fallback para FFmpeg (sempre disponível).

Engines de renderização:
- **FFmpeg** — fallback universal, sempre disponível, gera MP4 mínimo com imagem estática
- **WanGP** — engine IA local (GPU NVIDIA), gera vídeo por diffusion
- **Wan VACE 1.3B** — futuro opcional, documentado para quando GPU superior estiver disponível

## Stories mapeadas

| Story ID | Título | Status | SP | Prioridade | DoR completo |
|----------|--------|--------|----|-----------|-------------|
| VIS-502 | Criar schema SceneContract | Concluída | 5 | Alta | Sim |
| VIS-503 | Criar Prompt Compiler por engine | Concluída | 8 | Média | Sim |
| RND-600 | Criar RenderPlan mínimo | Concluída | 5 | Alta | Sim |
| RND-601 | Manter FFmpeg como fallback universal | Concluída | 3 | Alta | Sim |
| RND-602 | Adicionar perfil GTX 1660 Super | Concluída | 3 | Alta | Sim |
| RND-603 | Registrar Wan VACE 1.3B como futuro opcional | Pendente | 2 | Baixa | Não |
| QA-1003 | Criar teste E2E WanGP falha → FFmpeg | Pendente | 5 | Média | Não |

### VIS-502 — Criar schema SceneContract

**Status:** Concluída  
**Estimativa:** 5 SP  
**Épico:** EPIC-600 Consistência visual  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vis-502`  
**Testes:** `08_PLANO_DE_TESTES.md#vis-502`  

Schema que define contrato por cena: descrição visual, ingredients referenciados, duração, transição. Transforma roteiro em instruções testáveis para a engine de render.

**Arquivos:**
- `app/domain/scene_contract.py` — SceneContract, CameraDirective, IngredientAssignment, SceneContractService
- `tests/test_scene_contract.py` — 42 testes (schemas, CRUD, search, filter, reorder, versioning)

### VIS-503 — Criar Prompt Compiler por engine

**Status:** Concluída  
**Estimativa:** 8 SP  
**Épico:** EPIC-600 Consistência visual  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vis-503`  
**Testes:** `08_PLANO_DE_TESTES.md#vis-503`  

Compilador que traduz SceneContract em prompts específicos por engine (FFmpeg, WanGP, VACE). Cada engine recebe instruções no formato adequado.

**Arquivos:**
- `app/domain/prompt_compiler.py` — EngineType, PromptFormat, CompiledPrompt, EngineParameter, PromptCompilerService
- `tests/test_prompt_compiler.py` — 44 testes (compilação WanGP/FFmpeg/VACE, multi-engine, registry, parâmetros)

### RND-600 — Criar RenderPlan mínimo

**Status:** Concluída  
**Estimativa:** 5 SP  
**Épico:** EPIC-700 Render e performance  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#rnd-600`  
**Testes:** `08_PLANO_DE_TESTES.md#rnd-600`  

Plano que escolhe engine por cena com base em: (1) disponibilidade da engine, (2) VRAM disponível, (3) perfil de qualidade configurado. Decide qual engine renderiza cada cena.

**Arquivos:**
- `app/domain/render_plan.py` — SceneRenderAssignment, RenderPlan, RenderPlanService (156 linhas)
- `tests/test_render_plan.py` — 18 testes (engine selection, VRAM limits, quality profiles, fallback chain)

### RND-601 — Manter FFmpeg como fallback universal

**Status:** Concluída  
**Estimativa:** 3 SP  
**Épico:** EPIC-700 Render e performance  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#rnd-601`  
**Testes:** `08_PLANO_DE_TESTES.md#rnd-601`  

FFmpeg é o fallback universal de renderização. Mesmo sem GPU/engine IA, o sistema deve gerar um MP4 mínimo (imagem estática + transições básicas).

**Arquivos:**
- `tests/test_ffmpeg_fallback.py` — 15 testes (adapter existência, pipeline fallback, RenderPlan, mandatory matrix)

### RND-602 — Adicionar perfil GTX 1660 Super

**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Épico:** EPIC-700 Render e performance  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#rnd-602`  
**Testes:** `08_PLANO_DE_TESTES.md#rnd-602`  

Perfil de GPU para GTX 1660 Super (6GB VRAM): resolução segura 480p/512p (standard/recommended), 832x512 (max), orçamento de VRAM = 3072 MB por cena WanGP. Perfil integrado ao `GpuProfileCatalog` com 2 perfis adicionais (RTX 3060 12GB, Fallback CPU/FFmpeg).

**Arquivos:**
- `app/domain/render_plan.py` — GpuProfile, GpuProfileCatalog, resolution per quality/profile
- `tests/test_render_plan.py` — 22 testes novos (40 total)

### RND-603 — Registrar Wan VACE 1.3B como futuro opcional

**Status:** Pendente  
**Estimativa:** 2 SP  
**Épico:** EPIC-700 Render e performance  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#rnd-603`  
**Testes:** `08_PLANO_DE_TESTES.md#rnd-603`  

Documentar Wan VACE 1.3B como futuro adapter opcional. Não implementar agora — apenas registrar arquitetura, requisitos de GPU e critérios para ativação futura.

### QA-1003 — Criar teste E2E WanGP falha → FFmpeg

**Status:** Pendente  
**Estimativa:** 5 SP  
**Épico:** EPIC-1100 QA contínuo  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#qa-1003`  
**Testes:** `08_PLANO_DE_TESTES.md#qa-1003`  

Teste end-to-end que valida: quando WanGP falha, o pipeline faz fallback para FFmpeg e entrega MP4 válido.

## Arquitetura / Decisões

### Pipeline de render
SceneContract → PromptCompiler → RenderPlan → EngineRouter → Engine (WanGP|FFmpeg|VACE)

### EngineRouter
Seleciona engine por cena baseado no RenderPlan. Ordem de preferência: WanGP > FFmpeg. VACE é futuro.

### FFmpeg como fallback universal
FFmpeg é o único provider de render obrigatório. WanGP e VACE são opcionais. FFmpeg não pode ser removido.

### GPU Budget
Cada perfil de GPU define: resolução máxima, batch size, limites de VRAM. Perfil GTX 1660 Super (6GB) é o mínimo suportado.

## Regras de preservação

1. **FFmpeg é fallback obrigatório** — nunca pode ser removido ou despriorizado
2. **Engine IA é sempre opcional** — pipeline deve funcionar sem GPU
3. **Provider de render novo deve ser opcional** — nunca quebrar fallback FFmpeg
4. **RenderPlan deve registrar motivo da escolha** — para debug e rastreabilidade
5. **Perfil GTX 1660 Super é o mínimo** — resoluções seguras documentadas

## Referências

- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — VIS-502, VIS-503, RND-600..603, QA-1003
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — descrição detalhada (linhas 1220-1494, 2094-2138)
- `docs/project-control/07_CRITERIOS_ACEITE_GHERKIN.md` — critérios Gherkin
- `docs/project-control/08_PLANO_DE_TESTES.md` — plano de testes
- `docs/project-control/11_DECISOES_TECNICAS_ADR.md` — ADRs de render
