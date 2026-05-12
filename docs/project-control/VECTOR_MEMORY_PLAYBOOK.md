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
| VIS-500 | Criar schema Ingredient Registry | Concluída | 5 | Alta | Sim |
| VIS-501 | Criar schema Visual Bible | Concluída | 5 | Alta | Sim |
| VEC-800 | Criar VectorStoreAdapter sem runtime obrigatório | Concluída | 3 | Média | Sim |
| VEC-801 | Criar MemoryQualityGate | Concluída | 5 | Média | Sim |
| VEC-802 | Planejar Qdrant local opcional | Concluída | 3 | Baixa | Sim |
| VEC-803 | Planejar Chroma como protótipo opcional | Concluída | 2 | Baixa | Sim |

### VIS-500 — Criar schema Ingredient Registry

**Status:** Concluída ✅  
**Estimativa:** 5 SP  
**Épico:** EPIC-600 Consistência visual  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vis-500`  
**Testes:** `tests/test_ingredient_registry.py` — 27 testes

Schema que define o registro de ingredientes: produtos, personagens, cenários, objetos de cena. Cada ingrediente tem nome, descrição, referências visuais e metadados. Garante consistência entre cenas e sessões.

**Arquivos:**
- `app/domain/ingredient_registry.py` — IngredientRegistry com CRUD versionado
- `tests/test_ingredient_registry.py` — 27 testes (schemas, CRUD, search, versioning, negative)

### VIS-501 — Criar schema Visual Bible

**Status:** Concluída ✅  
**Estimativa:** 5 SP  
**Épico:** EPIC-600 Consistência visual  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vis-501`  
**Testes:** `tests/test_visual_bible.py`

Schema que fixa referências visuais aprovadas por ingrediente. Reduz drift visual entre gerações. A Visual Bible é consultada pelo Prompt Compiler para incluir referências nos prompts.

**Arquivos:**
- `app/domain/visual_bible.py` — VisualBible schema
- `tests/test_visual_bible.py`

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

**Status:** Concluída ✅  
**Estimativa:** 3 SP  
**Épico:** EPIC-900 IA vetorial futura  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vec-802`  
**Testes:** `08_PLANO_DE_TESTES.md#vec-802`  

Planejar integração com Qdrant como backend alvo de produção. Qdrant suporta payload filtering, multi-tenancy e busca híbrida. Deve ser opcional e local-first.

#### Plano de integração

**Arquitetura:**
```
VectorStoreAdapter (ABC)
  └── QdrantStore
        ├── Client gRPC (qdrant-client Python)
        ├── Collection por project_id (multi-tenancy)
        └── Payload: {ingredient_id, ingredient_name, type, source}
```

**Pré-requisitos:**
- Dependência Python: `qdrant-client` (opcional, importada apenas quando ativo)
- Qdrant local via Docker: `docker run -p 6333:6333 qdrant/qdrant`
- Modo embedded (sem Docker): `from qdrant_client import QdrantClient` com `:memory:` ou caminho local
- Vector dimension: 384 (default para all-MiniLM-L6-v2) ou configurável

**Recursos:**
- RAM: ~2GB para Qdrant local (depende do volume de dados)
- CPU: qualquer CPU moderna
- GPU: não obrigatório (Qdrant é CPU-only)
- Disco: persistência opcional em `local_data/qdrant/`

**Critérios para ativação:**
1. Implementar `QdrantStore(VectorStoreAdapter)` em `app/adapters/vector_store_qdrant.py`
2. Registrar na configuração como store ativo: `vector_store.type = "qdrant"`
3. MemoryQualityGate deve executar antes de upsert (regra #3)
4. Pipeline funciona sem Qdrant — import falha silenciosa
5. NUNCA remover InMemoryVectorStore (fallback para teste)

**Plano de implementação (futuro):**
1. Adicionar `qdrant-client` como dependência opcional em `pyproject.toml`
2. Criar `QdrantStore` com métodos: search, upsert, delete, list_collections
3. Config: host, port, collection_prefix, embedding_dim
4. Testes com Qdrant `:memory:` mode (sem Docker necessário)
5. Atualizar `MemoryQualityGate` para usar QdrantStore quando ativo

### VEC-803 — Planejar Chroma como protótipo opcional

**Status:** Concluída ✅  
**Estimativa:** 2 SP  
**Épico:** EPIC-900 IA vetorial futura  
**Gherkin:** `07_CRITERIOS_ACEITE_GHERKIN.md#vec-803`  
**Testes:** `08_PLANO_DE_TESTES.md#vec-803`  

Planejar integração com Chroma como backend rápido para prototipagem. Ideal para testes de retrieval textual com baixo atrito. Opcional e local-first.

#### Plano de integração

**Arquitetura:**
```
VectorStoreAdapter (ABC)
  └── ChromaStore
        ├── Client HTTP (chromadb Python)
        ├── Collection por projeto (tenant/namespace)
        └── Metadata: {ingredient_id, ingredient_name, source}
```

**Pré-requisitos:**
- Dependência Python: `chromadb` (opcional, import lazy)
- Chroma embedded (in-process, sem servidor externo): `chromadb.Client()` com `PersistentClient` ou `EphemeralClient`
- Modo servidor opcional: `chromadb run --path ./chroma_data`
- Vector dimension: 384 (default) ou configurável via embedding function

**Recursos:**
- RAM: ~500MB-1GB (depende do volume)
- CPU: qualquer CPU moderna
- GPU: não obrigatório
- Disco: persistência opcional em `local_data/chroma/`

**Critérios para ativação:**
1. Implementar `ChromaStore(VectorStoreAdapter)` em `app/adapters/vector_store_chroma.py`
2. Registrar na configuração: `vector_store.type = "chroma"`
3. MemoryQualityGate executa antes de upsert (regra #3 compartilhada)
4. Pipeline funciona sem Chroma — import falha silenciosa
5. InMemoryVectorStore mantido como fallback para teste

**Comparação Qdrant vs Chroma:**

| Aspecto | Qdrant | Chroma |
|---------|--------|--------|
| Uso | Produção | Protótipo |
| API | gRPC | HTTP/Embedded |
| Payload filtering | Sim (nativo) | Limitado |
| Multi-tenancy | Sim (coleções) | Sim (tenant/namespace) |
| Busca híbrida | Sim | Limitado |
| Setup | Docker ou embedded | Embedded direto |
| RAM estimada | ~2GB | ~500MB-1GB |
| Maturidade | Alta | Média |

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
