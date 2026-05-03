# BACKLOG TÉCNICO (Code Review) — Gal AI / galFlowAI

**Última atualização:** 03/05/2026  
**Objetivo:** Evoluir a base atual sem quebrar o fluxo local-first existente (Gradio + FastAPI + fallback Template/FFmpeg).

---

## Resumo executivo (sem viés)

### Pontos fortes atuais
- Arquitetura já separa UI/API de serviços e adapters, o que facilita evolução incremental.
- Fallbacks centrais (TemplateProvider e FFmpeg) preservam continuidade operacional.
- Existe documentação base para operação local e setup de providers.

### Pontos críticos atuais
- Backlog anterior estava desatualizado e continha diagnósticos incorretos (ex.: sintaxe de `app/api.py` já está válida).
- Há risco de divergência entre comportamento real e documentação em endpoints/fluxos.
- Ausência de suíte de testes de contrato para API e de testes de regressão para fluxo fim-a-fim.

---

## Critérios para aceitar melhorias
1. **Não quebrar fluxo vigente** (gerar roteiro → editar/aprovar → cenas → preview → MP4).
2. **Melhorar observabilidade** (logs, erro claro, rastreabilidade por `project_id`/`job_id`).
3. **Aumentar robustez** sem impor dependências cloud ou lock-in externo.
4. **Permitir rollback fácil** (mudanças pequenas, feature flags quando aplicável).

---

## Backlog priorizado (crítico e coerente)

## Status Atual (03/05/2026 - Sessão Resumida)

### ✅ Concluído Nesta Sessão
1. **Correção de Sintaxe**: `app/logging_config.py` tinha backticks inválidos em todas as linhas
2. **Ambiente Python**: Criado `K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio` (venv Python 3.12.4)
3. **Dependências**: Instalados fastapi, uvicorn, gradio, pydantic, httpx no ambiente studio
4. **Validação**: `api.py` compila e importa com sucesso
5. **Teste FastAPI**: Servidor sobe e responde em `http://127.0.0.1:8000/api/health`
6. **Correção de Imports**:
   - `provider_router.py`: Corrigido import de `TemplateProvider` (estava em `base_provider.py`)
   - `auto_pipeline.py`: Corrigido import `generate_script_from_brief` → `generate_script`
   - `main.py`: Corrigido import `create_new_script_version` → `create_new_version`
7. **Criação de Módulos Faltantes**:
   - Criado `app/pipeline/prompt_builder.py` com funções necessárias
8. **Teste Gradio UI**: Servidor sobe e responde em `http://127.0.0.1:7860` (Status 200)

### ⚠️ Pendências Imediatas
1. Testar Gradio UI em `http://127.0.0.1:7860`
2. Validar se `auto_pipeline.py` executa sem erros
3. Commit das correções realizadas

---

## P0 — Confiabilidade e risco imediato

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P0-01 | Documentação e estado do código divergentes geram retrabalho | Criar checklist de release técnico (README/docs/endpoints/scripts) antes de merge | Evita drift entre docs e código | Exige disciplina por PR | **Sim (alto impacto, baixo custo)** |
| P0-02 | API sem testes de contrato tende a quebrar silenciosamente | Adicionar testes de contrato FastAPI para rotas críticas (`/api/health`, `/api/llm/*`, `/api/projects/*/script/*`) | Reduz regressão em endpoint | Setup inicial de fixtures | **Sim** |
| P0-03 | Falhas de provider podem degradar UX sem diagnóstico claro | Padronizar envelope de erro (`code`, `message`, `details`, `retryable`) e mapear exceptions por adapter | Debug mais rápido, UX previsível | Refatoração moderada nas rotas | **Sim** |

## P1 — Robustez de arquitetura sem ruptura

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P1-01 | Regras de negócio podem se espalhar entre API/UI | Consolidar casos de uso em camada `application` (use-cases) mantendo adapters em `infrastructure` | Reduz acoplamento e facilita testes | Refatoração gradual, demanda convenção | **Sim, incremental** |
| P1-02 | Pipeline de vídeo pode bloquear requisição síncrona | Introduzir executor assíncrono local com fila leve (`sqlite` + worker já existente em Go/Python) | Melhor responsividade e retomada | Mais componentes operacionais | **Sim, faseado** |
| P1-03 | Configuração local extensa e sujeita a erro | Adotar validação central de config (`pydantic-settings`) com mensagem de erro acionável | Menos erro de ambiente | Migração de config existente | **Sim** |
| P1-04 | Falta de idempotência em ações de roteiro pode duplicar estado | Definir idempotency key por operação de escrita em script/versionamento | Evita versões fantasmas | Requer armazenamento de chave/estado | **Sim, para estabilidade** |

## P2 — Eficiência e qualidade de código

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P2-01 | Providers diferentes podem repetir lógica de timeout/retry | Criar utilitário comum de execução (`retry`, `timeout`, `circuit breaker` simples local) | Menos duplicação, comportamento homogêneo | Ajuste em todos adapters | **Sim** |
| P2-02 | Logs atuais dificultam correlação ponta-a-ponta | Estruturar logs JSON com `project_id`, `provider`, `latency_ms`, `fallback_used` | Observabilidade real | Requer adaptação de leitura manual | **Sim** |
| P2-03 | Sem métricas mínimas, tuning fica subjetivo | Instrumentar métricas locais (tempo de geração, taxa fallback, erro por provider) | Decisão baseada em dado | Pequeno overhead | **Sim** |
| P2-04 | Testes lentos/instáveis por dependência de LLM local | Criar modo de teste com fakes determinísticos para providers | CI estável e rápida | Necessário manter fakes | **Sim** |

## P3 — Modernização arquitetural (sem “big bang”)

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P3-01 | Evolução de frontend pode exigir API mais formal | Versionar API (`/api/v1`) e publicar schema OpenAPI versionado | Permite evolução sem quebrar clientes | Trabalho de governança | **Sim, antes da UI nova** |
| P3-02 | Operações longas sem estado formal de job | Padronizar máquina de estados (`queued/running/succeeded/failed/canceled`) | Controle operacional e UX melhor | Implementação moderada | **Sim** |
| P3-03 | Crescimento de features sem limites claros | Definir ADRs curtas (Architecture Decision Records) para decisões críticas | Histórico técnico rastreável | Custo de documentação contínua | **Sim** |

---

## Plano de execução recomendado (sem quebrar fluxo)

### Sprint A (1–2 semanas)
- P0-01, P0-02, P0-03
- P1-03
- P2-02

### Sprint B (2 semanas)
- P1-01 (apenas casos de uso de roteiro)
- P2-01, P2-04
- P3-02 (estado de job mínimo)

### Sprint C (2+ semanas)
- P1-02 (fila local faseada)
- P2-03
- P3-01, P3-03

---

## Itens congelados (não fazer agora)
- Reescrita completa da UI em React sem estabilizar contratos da API.
- Dependência obrigatória de cloud/API paga.
- Troca massiva de stack sem baseline de performance/confiabilidade.

---

## Checklist de revisão por PR
- [ ] Mudança preserva fallback Template + FFmpeg.
- [ ] Existe teste automatizado para rota/caso alterado.
- [ ] Logs incluem contexto mínimo (`project_id`/`provider`).
- [ ] Documentação atualizada no mesmo PR.
- [ ] Sem promessa de funcionalidade não implementada.

---

## Refinamento de histórias (correções pontuais com economia de tokens)

> Objetivo: executar correções pequenas, verificáveis e com baixa ambiguidade.

### H1 — Padronizar identidade e metadados da API
**Contexto:** ainda havia strings legadas no `app/api.py` (nome antigo do produto).  
**Implementação sugerida:** manter docstring, título da API e payload de health coerentes com Gal AI.

**Critérios de aceite (rígidos):**
- [ ] `app/api.py` compila com `python -m py_compile app/api.py`.
- [ ] `FastAPI(title=...)` usa nome atual do projeto.
- [ ] `GET /api/health` retorna `app` coerente com branding atual.

**Prompt enxuto (engenharia de prompt):**
```text
Corrija somente metadados de identidade em app/api.py sem alterar contratos de endpoint.
Restrições: não criar novos endpoints, não alterar schemas de request/response.
Entrega: patch mínimo + validação por py_compile.
```

### H2 — Endurecer tratamento de exceção sem mudar comportamento funcional
**Contexto:** havia `except:` genérico em leitura de status de projeto.  
**Implementação sugerida:** trocar por `except Exception` mantendo fallback atual.

**Critérios de aceite (rígidos):**
- [ ] Não existir `except:` nu em `app/api.py`.
- [ ] Endpoint `/api/video-status/{project_id}` continua retornando status mesmo quando `prompts.json` estiver malformado.
- [ ] `python -m py_compile app/api.py` permanece OK.

**Prompt enxuto (engenharia de prompt):**
```text
Refatore apenas blocos `except:` nus em app/api.py para `except Exception`.
Não mude regras de negócio, payload ou fluxo de fallback.
Valide compilação no final.
```

### H3 — Execução local previsível do módulo API
**Contexto:** execução `__main__` deve ser explícita e estável para ambiente local.  
**Implementação sugerida:** manter host local e explicitar parâmetros de `uvicorn.run` sem mudar porta/API.

**Critérios de aceite (rígidos):**
- [ ] Bloco `if __name__ == "__main__":` inicia API em `host=127.0.0.1` e `port=8000`.
- [ ] Não importar variáveis não usadas de `config.py`.
- [ ] Compilação sintática sem erro.

**Prompt enxuto (engenharia de prompt):**
```text
Ajuste somente o bloco __main__ de app/api.py para inicialização local determinística.
Não alterar rotas, modelos Pydantic ou middlewares.
```
