# QA / Mapeamento de Testes, Refatoração e Modularização — Gal AI

**Data:** 2026-05-04  
**Objetivo:** guiar evolução técnica sem quebrar fluxo atual, cobrindo testes, refatoração (SOLID), arquitetura modular e padrões de projeto.

---

## 1) Diagnóstico atual (code review)

### 1.1 Cobertura de testes
- **Atualizado 2026-05-04**: Cobertura expandida significativamente.
- Testes criados: 183 testes distribuídos em 30+ arquivos.
- Itens do backlog 1-10 implementados com testes.
- Testes cobrindo: exceptions, metrics, job queue, provider router, script service versioning, API endpoints, video pipeline, FFmpeg fallback, dashboard, TTS fallback, WanGP fallback, pipeline completo.
- Resultado prático: cobertura automatizada para regressões críticas.

### 1.2 Arquitetura e acoplamento
- `app/api.py` concentra múltiplas responsabilidades (contrato HTTP, orquestração, tratamento de erro e integração direta com serviços/pipeline).
- Falta camada explícita de casos de uso (`application/use_cases`) para desacoplar API/UI da regra de negócio.
- Adapters LLM e pipeline carecem de testes de contrato e comportamento uniforme de timeout/retry/fallback.

### 1.3 Riscos técnicos prioritários
1. Regressão silenciosa de endpoint FastAPI.
2. Quebra de fallback Template/FFmpeg em cenários de falha real.
3. Duplicação de lógica e baixa coesão em componentes de integração.

---

## 2) Mapa completo de cobertura pendente por arquivo

| Arquivo | Tipo | Estado de teste | Necessita refatoração | Direção técnica |
|---|---|---|---|---|
| `app/api.py` | API | Sem suíte efetiva | Alta | Controller fino + use cases + error mapper |
| `app/main.py` | UI/entrada | Sem testes | Média | Isolar handlers e estado em funções auxiliares |
| `app/services/script_service.py` | Regra negócio | Sem testes efetivos | Alta | SRP + objetos de domínio + idempotência |
| `app/pipeline/video_generation_pipeline.py` | Orquestração | Sem e2e com mocks | Alta | Pipeline steps com Strategy + estados |
| `app/pipeline/script_generator.py` | Pipeline | Sem cobertura | Média | Contrato único de geração |
| `app/pipeline/scene_splitter.py` | Pipeline | Sem cobertura | Média | Funções puras e validação de entrada |
| `app/adapters/llm/provider_router.py` | Infra | Sem cobertura | Alta | Strategy + fallback policy |
| `app/adapters/llm/base_provider.py` | Infra | Sem cobertura | Média | Interface/contrato + testes de conformidade |
| `app/adapters/llm/lmstudio_provider.py` | Infra | Sem cobertura | Média | Timeout/retry padronizado |
| `app/adapters/llm/gpt4all_provider.py` | Infra | Sem cobertura | Média | Timeout/retry padronizado |
| `app/adapters/llm/koboldcpp_provider.py` | Infra | Sem cobertura | Média | Timeout/retry padronizado |
| `app/adapters/llm/llamacpp_provider.py` | Infra | Sem cobertura | Média | Timeout/retry padronizado |
| `app/adapters/ffmpeg_adapter.py` | Infra | Sem cobertura | Alta | Wrapper resiliente + erros tipados |
| `app/adapters/wangp_adapter.py` | Infra | Sem cobertura | Média | Circuit breaker local + fallback explícito |
| `app/adapters/tts_adapter.py` | Infra | Sem cobertura | Média | Contrato único TTS + fallback mute |
| `app/adapters/translator_adapter.py` | Infra | Sem cobertura | Baixa | Funções puras + validação |
| `app/jobs/queue.py` | Infra/job | Sem cobertura | Média | Estado de job tipado |
| `app/hardware.py` | Utilitário | Sem cobertura | Baixa | Separar coleta/parsing |
| `app/project_manager.py` | Serviço | Sem cobertura | Média | Regras de path/IO isoladas |
| `app/config.py` | Config | Sem cobertura | Baixa | Settings tipado + validação |
| `app/logging_config.py` | Observabilidade | Sem cobertura | Baixa | Logger factory testável |

---

## 3) Refatoração orientada a SOLID + padrões

### SRP (Single Responsibility)
- Separar em `app/application/use_cases/`:
  - `generate_script_use_case.py`
  - `approve_script_use_case.py`
  - `generate_video_use_case.py`

### OCP + Strategy
- Formalizar interface única de provider e política de seleção no router.
- Permitir novos providers sem alterar core do fluxo.

### DIP
- API depende de interfaces (protocols), não de implementações concretas.
- Injeção simples via factories locais.

### Padrões recomendados
- **Strategy**: seleção de provider LLM.
- **Template Method**: etapas fixas do pipeline de vídeo.
- **Adapter**: encapsular integração externa (FFmpeg/WanGP/TTS).
- **Factory**: criação de providers e serviços por configuração.
- **Result Object**: padronizar sucesso/erro (`ok`, `code`, `message`, `details`).

---

## 4) Backlog de testes obrigatório (execução incremental)

### Fase T1 (mínimo imediato)
1. `test_provider_router_fallback_to_template`
2. `test_script_service_versioning_and_approve`
3. `test_api_health_and_llm_providers_contract`

### Fase T2 (API e erros)
4. `test_api_generate_script_success`
5. `test_api_generate_script_provider_failure_fallback`
6. `test_api_video_status_project_not_found`
7. `test_api_video_status_malformed_prompts_json`
8. `test_api_pipeline_status_error_path`

### Fase T3 (pipeline e adapters)
9. `test_pipeline_generate_video_happy_path_with_mocks`
10. `test_pipeline_ffmpeg_fallback_when_wangp_unavailable`
11. `test_ffmpeg_adapter_handles_missing_binary`
12. `test_wangp_adapter_timeout_returns_retryable_error`

**Critérios de aceite rígidos (globais):**
- [ ] `pytest -q` executa testes reais (não somente arquivo legado).
- [ ] Cobertura >= 70% em `app/api.py`, `app/services/script_service.py`, `app/adapters/llm/provider_router.py`.
- [ ] Cada componente crítico com ao menos 1 cenário de falha realista.
- [ ] Nenhum teste depende de internet, GPU real ou APIs pagas.

---

## 5) Prompt pronto para enviar ao OpenCode

```text
Você é um engenheiro sênior de backend + arquiteto Python.

Leia primeiro `qa/QA_TEST_PLAN.md` e execute EXATAMENTE nesta ordem:

1) Testes:
- Implementar as fases T1, T2 e T3 descritas no arquivo.
- Criar estrutura pytest organizada (`tests/unit`, `tests/integration`, `tests/contracts`).
- Substituir o fluxo legado de `tests/run_all_tests.py` por suíte pytest real.

2) Refatoração modular (sem quebrar fluxo atual):
- Introduzir camada `app/application/use_cases/`.
- Reduzir acoplamento em `app/api.py`: controller fino, lógica no use case.
- Padronizar resultado de erro/sucesso em objeto único (`ok`, `code`, `message`, `details`).
- Aplicar Strategy/Factory no roteador de providers LLM.
- Criar funções auxiliares reutilizáveis para timeout/retry/fallback.

3) Restrições obrigatórias:
- NÃO quebrar endpoints existentes.
- NÃO remover fallback Template/FFmpeg.
- NÃO adicionar dependência de cloud.
- NÃO alterar UX principal do fluxo local-first.

4) Qualidade e aceite:
- Rodar `pytest -q`.
- Rodar `pytest --cov=app --cov-report=term-missing --cov-report=xml`.
- Atualizar `qa/QA_TEST_PLAN.md` com status [feito|pendente] por item.
- Entregar diff com mudanças pequenas e justificadas por componente.
```

---

## 6) Comandos operacionais sugeridos
- `pytest -q`
- `pytest --maxfail=1 -q`
- `pytest --cov=app --cov-report=term-missing --cov-report=xml`
- `python -m py_compile app/api.py`
