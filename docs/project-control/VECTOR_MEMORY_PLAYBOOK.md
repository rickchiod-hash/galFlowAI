# VECTOR_MEMORY_PLAYBOOK — GalFlowAI

## Visão geral

Este playbook documenta os componentes de memória vetorial e consistência visual do GalFlowAI. A camada de memória é totalmente opcional — o pipeline funciona sem ela. Quando ativa, permite retrieval semântico e consistência visual entre sessões.

Componentes:
- **Ingredient Registry** — catálogo de produtos/personagens/cenários
- **Visual Bible** — referências visuais aprovadas para consistência
- **VectorStoreAdapter** — porta de abstração para backend vetorial
- **MemoryQualityGate** — barreira de qualidade antes de indexação
- **Qdrant** — backend alvo para produção (opcional)
- **Chroma** — backend para protótipo (opcional)

## Stories mapeadas

| Story ID | Título | Status | SP | Prioridade | DoR completo |
|----------|--------|--------|----|-----------|-------------|
| VIS-500 | Criar schema Ingredient Registry | Pendente | 5 | Alta | Não |
| VIS-501 | Criar schema Visual Bible | Pendente | 5 | Alta | Não |
| VEC-800 | Criar VectorStoreAdapter sem runtime obrigatório | Concluída | 3 | Média | Sim |
| VEC-801 | Criar MemoryQualityGate | Concluída | 5 | Média | Sim |
| VEC-802 | Planejar Qdrant local opcional | Pendente | 3 | Baixa | Não |
| VEC-803 | Planejar Chroma como protótipo opcional | Pendente | 2 | Baixa | Não |

### VIS-500 — Criar schema Ingredient Registry

**Status:** Pendente  
**Estimativa:** 5 SP  
**Épico:** EPIC-600 Consistência visual  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vis-500`  
**Testes:** `08_PLANO_DE_TESTES.md#vis-500`  

Schema que define o registro de ingredientes: produtos, personagens, cenários, objetos de cena. Cada ingrediente tem nome, descrição, referências visuais e metadados. Garante consistência entre cenas e sessões.

### VIS-501 — Criar schema Visual Bible

**Status:** Pendente  
**Estimativa:** 5 SP  
**Épico:** EPIC-600 Consistência visual  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vis-501`  
**Testes:** `08_PLANO_DE_TESTES.md#vis-501`  

Schema que fixa referências visuais aprovadas por ingrediente. Reduz drift visual entre gerações. A Visual Bible é consultada pelo Prompt Compiler para incluir referências nos prompts.

### VEC-800 — Criar VectorStoreAdapter sem runtime obrigatório

**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Épico:** EPIC-900 IA vetorial futura  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vec-800`  
**Testes:** `08_PLANO_DE_TESTES.md#vec-800`  

Adapter que abstrai o backend vetorial. Interface comum para Chroma, Qdrant ou qualquer store futura. Não aciona runtime — apenas define o contrato. O pipeline funciona sem vector store.

**Arquivos:**
- `app/adapters/vector_store.py` — VectorStoreAdapter (ABC), InMemoryVectorStore, cosine_similarity
- `tests/test_vector_store.py` — 25 testes (CRUD, search, similarity, edge cases)

### VEC-801 — Criar MemoryQualityGate

**Status:** Concluída ✅  
**Estimativa:** 5 SP  
**Épico:** EPIC-900 IA vetorial futura  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vec-801`  
**Testes:** `08_PLANO_DE_TESTES.md#vec-801`  

Barreira de qualidade que impede indexação de rascunhos ruins. Critérios: completude mínima do ingrediente, presença de referência visual, validação de schema.

**Arquivos:**
- `app/domain/memory_quality_gate.py` — MemoryQualityGate, QualityGateResult
- `tests/test_memory_quality_gate.py` — 13 testes (ingredient/bible validation)

### VEC-802 — Planejar Qdrant local opcional

**Status:** Pendente  
**Estimativa:** 3 SP  
**Épico:** EPIC-900 IA vetorial futura  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vec-802`  
**Testes:** `08_PLANO_DE_TESTES.md#vec-802`  

Planejar integração com Qdrant como backend alvo de produção. Qdrant suporta payload filtering, multi-tenancy e busca híbrida. Deve ser opcional e local-first.

### VEC-803 — Planejar Chroma como protótipo opcional

**Status:** Pendente  
**Estimativa:** 2 SP  
**Épico:** EPIC-900 IA vetorial futura  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vec-803`  
**Testes:** `08_PLANO_DE_TESTES.md#vec-803`  

Planejar integração com Chroma como backend rápido para prototipagem. Ideal para testes de retrieval textual com baixo atrito. Opcional e local-first.

## Arquitetura / Decisões

### Camada de memória opcional
Vector store nunca é obrigatório. O pipeline funciona sem ele. A ativação é via configuração.

### Adapter pattern
VectorStoreAdapter define interface. Implementações concretas (Chroma, Qdrant) são injetadas. O sistema não conhece o backend específico.

### Quality Gate antes de indexar
MemoryQualityGate impede que dados de baixa qualidade contaminem o espaço vetorial. Executa validação de schema e completude.

### Ingredient Registry + Visual Bible
Schemas que vivem na camada de domínio. Alimentam o VectorStoreAdapter quando a memória está ativa.

## Regras de preservação

1. **Vector store é sempre opcional** — pipeline principal não depende dele
2. **Adapter define interface** — implementações são plugáveis
3. **Quality Gate é obrigatório quando memória está ativa** — sem ele, não indexar
4. **Ingredient Registry é o schema base** — Visual Bible é derivação
5. **Nenhum backend vetorial é obrigatório** — Chroma (protótipo), Qdrant (produção), ambos opcionais
6. **Backend existente não pode ser removido sem ADR** — documentar motivo

## Referências

- `docs/project-control/05_BACKLOG_PRIORIZADO.md` — VIS-500, VIS-501, VEC-800..803
- `docs/project-control/06_HISTORIAS_REFINADAS.md` — descrição detalhada (linhas 1128-1218, 1680-1862)
- `docs/project-control/07_CRITERIOS_ACEITE_GHERKIN.md` — critérios Gherkin
- `docs/project-control/08_PLANO_DE_TESTES.md` — plano de testes
- `docs/project-control/11_DECISOES_TECNICAS_ADR.md` — ADRs de memória vetorial
