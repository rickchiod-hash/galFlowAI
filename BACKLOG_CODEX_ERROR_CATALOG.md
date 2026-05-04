# Backlog Codex — Error Catalog e Logs Estruturados

Status: Planejado  
Escopo: backlog isolado  
Não implementar nesta PR  
Objetivo: evitar conflito com BACKLOG.md principal

> Este arquivo é um backlog isolado criado para evitar conflitos com o BACKLOG.md principal. Agentes futuros devem ler este arquivo e, quando a tarefa atual estiver concluída, podem migrar os cards para BACKLOG.md ou ROADMAP.md com cuidado.

## P0-ERR-01 — Criar ErrorCode enum

**Contexto:**
O projeto precisa parar de depender apenas de mensagens soltas de erro. Códigos de erro estáveis ajudam a Central de Logs, testes, diagnóstico e comunicação com agentes de código.

**Proposta futura:** criar `app/core/error_codes.py` com enum de códigos fixos.

```python
from enum import StrEnum

class ErrorCode(StrEnum):
    UNKNOWN_ERROR = "UNKNOWN_ERROR"
    GRADIO_START_FAILED = "GRADIO_START_FAILED"
    FASTAPI_UNAVAILABLE = "FASTAPI_UNAVAILABLE"
    LLM_PROVIDER_UNAVAILABLE = "LLM_PROVIDER_UNAVAILABLE"
    SCRIPT_VALIDATION_FAILED = "SCRIPT_VALIDATION_FAILED"
    FFMPEG_NOT_FOUND = "FFMPEG_NOT_FOUND"
    FFMPEG_CONCAT_FAILED = "FFMPEG_CONCAT_FAILED"
    WANGP_UNAVAILABLE = "WANGP_UNAVAILABLE"
    TTS_UNAVAILABLE = "TTS_UNAVAILABLE"
    PROJECT_NOT_FOUND = "PROJECT_NOT_FOUND"
    INVALID_PROJECT_STATE = "INVALID_PROJECT_STATE"
```

**Critério de aceite futuro:**
- enum criado em `app/core/error_codes.py`;
- nomes estáveis e claros;
- não criar 200 códigos de uma vez;
- começar com 10 a 20 códigos principais;
- testes garantem que os valores não mudem sem intenção.

**Risco:** overengineering se criar enum gigante cedo demais.  
**Veredito:** fazer leve.

---

## P0-ERR-02 — Criar AppError padronizado

**Contexto:**
A UI precisa mostrar erro humano, sugestão e código técnico sem despejar traceback cru.

**Proposta futura:** criar `app/core/app_error.py`.

```python
@dataclass
class AppError:
    code: str
    severity: str
    message: str
    suggestion: str
    stage: str
    retryable: bool
    project_id: str | None = None
    job_id: str | None = None
    provider: str | None = None
    fallback_used: bool = False
    details: dict | None = None
```

**Critério de aceite futuro:**
- todo erro estruturado tem `code`, `severity`, `message`, `suggestion` e `stage`;
- serialização JSON disponível;
- sem vazamento de segredo/token/path sensível;
- uso comum por API e UI;
- traceback no log técnico, não na mensagem principal do usuário.

---

## P0-ERR-03 — Criar ErrorCatalogService

**Contexto:**
A Central de Logs precisa traduzir código técnico em mensagem útil para usuário.

**Proposta futura:** criar `app/services/error_catalog_service.py` com:
- `get_error_definition(code)`
- `build_user_message(app_error)`
- `build_diagnostic_message(app_error)`
- `is_retryable(code)`
- `get_suggestion(code)`

**Critério de aceite futuro:**
- `FFMPEG_CONCAT_FAILED` sugere validar `inputs.txt`, paths, `-safe 0` e arquivos ausentes;
- `LLM_PROVIDER_UNAVAILABLE` sugere TemplateProvider;
- `WANGP_UNAVAILABLE` sugere FFmpeg preview;
- `FASTAPI_UNAVAILABLE` sugere health check;
- mensagens em português brasileiro.

---

## P0-ERR-04 — Salvar erros estruturados em JSONL isolado

**Contexto:**
Logs textuais são úteis, mas erros estruturados facilitam filtros, UI e diagnóstico.

**Proposta futura:**
- criar pasta: `logs/errors/`
- arquivos: `logs/errors/errors-YYYY-MM-DD.jsonl`

Exemplo por linha JSONL:

```json
{
  "timestamp": "...",
  "code": "FFMPEG_CONCAT_FAILED",
  "severity": "ERROR",
  "stage": "preview",
  "message": "FFmpeg falhou ao montar preview.",
  "suggestion": "Verifique inputs.txt, caminhos e -safe 0.",
  "retryable": true,
  "project_id": "project_123",
  "job_id": "job_456",
  "provider": null,
  "fallback_used": false
}
```

**Critério de aceite futuro:**
- `logs/errors/` criado automaticamente;
- nunca salvar no C:;
- rotação por data;
- Central de Logs lê JSONL;
- falha de escrita JSONL não quebra app;
- evitar duplicação excessiva.

---

## P0-ERR-05 — Integrar ErrorCode com Central de Logs

**Contexto:**
A Central de Logs deve mostrar diagnóstico claro, não só mensagem crua.

**Proposta futura:** exibir:
- horário, nível, código, etapa, projeto, job, mensagem, sugestão, retryable, fallback_used.

**Critério de aceite futuro:**
- INFO/WARN/ERROR legíveis;
- DEBUG oculto na UI;
- códigos filtráveis;
- botão "Copiar diagnóstico" inclui erros estruturados recentes;
- fallback controlado aparece como WARN, não ERROR fatal.

---

## P1-ERR-06 — Criar docs/ERROR_CATALOG.md

**Proposta futura:** criar `docs/ERROR_CATALOG.md` com visão geral, formato de `AppError`, tabela de códigos, severidade, etapa, sugestão, retryable, exemplos e guideline de extensão.

**Critério de aceite futuro:**
- PT-BR;
- não documentar como implementado antes da implementação;
- exemplos práticos (FFmpeg, LLM, FastAPI, Gradio, TTS e WanGP).

---

## P1-ERR-07 — Testes de erro estruturado

**Proposta futura:**
- `tests/test_error_codes.py`
- `tests/test_app_error.py`
- `tests/test_error_catalog_service.py`
- `tests/test_error_jsonl_writer.py`
- `tests/test_log_service_error_integration.py`

**Critério de aceite futuro:**
- ErrorCode com valores estáveis;
- AppError serializa para dict/JSON;
- ErrorCatalog retorna sugestão;
- JSONL gravado no K:;
- Central de Logs ignora DEBUG;
- WARN de fallback não vira ERROR fatal.

---

## P1-ERR-08 — Mapear erros por domínio

**Domínios iniciais:**
- BOOT, GRADIO, FASTAPI, PROJECT, SCRIPT, LLM, VIDEO, FFMPEG, WANGP, TTS, FILESYSTEM, CONFIG, UNKNOWN.

**Critério de aceite futuro:**
- código inclui domínio claro;
- catálogo separa por domínio;
- logs filtráveis por domínio.

---

## P1-ERR-09 — Padronizar severidade e fallback

**Regras futuras:**
- ERROR: fluxo falhou e precisa ação.
- WARN: fluxo continuou com fallback.
- INFO: evento normal.
- DEBUG: não aparece na UI.

**Critério de aceite futuro:**
- severidade coerente;
- fallback controlado não assusta usuário;
- UI mostra WARN em amarelo e ERROR em vermelho.

---

## P2-ERR-10 — Criar diagnóstico técnico copiável

**Proposta futura:** botão "Copiar diagnóstico" contendo commit, Python, cwd, project_id/job_id, último ErrorCode, últimos WARN/ERROR, status FFmpeg/FastAPI/providers, caminho do log e sugestão principal.

**Critério de aceite futuro:**
- sem segredo/API key/token;
- texto em português;
- útil para colar em chat/agente.

---

## O que não fazer agora

- Não implementar nesta PR.
- Não editar BACKLOG.md principal.
- Não criar observabilidade enterprise.
- Não criar OpenTelemetry agora.
- Não criar banco para erros agora.
- Não criar 200 códigos de erro.
- Não transformar todos os erros em exceções customizadas.
- Não fazer tudo async.
- Não mostrar DEBUG na UI.
- Não salvar nada no C:.
- Não quebrar Central de Logs atual.
- Não quebrar Gradio.
- Não quebrar FastAPI.
- Não quebrar FFmpeg fallback.

## Ordem recomendada de implementação futura

1. Criar ErrorCode enum.
2. Criar AppError.
3. Criar ErrorCatalogService.
4. Criar writer JSONL para `logs/errors`.
5. Integrar com LogService.
6. Integrar com Central de Logs.
7. Criar `docs/ERROR_CATALOG.md`.
8. Criar testes.
9. Migrar erros principais do FFmpeg/LLM/FastAPI para o padrão.
10. Só depois expandir domínios.

## Ganho esperado

- Debug mais rápido.
- Central de Logs mais confiável.
- Menos UNKNOWN.
- Menos traceback cru na UI.
- Diagnóstico copiável melhor.
- Fallbacks mais claros.
- Testes de erro mais previsíveis.
- Codex/OpenCode entende falhas com menos contexto.
- Usuário sabe o que fazer quando algo falha.
- Projeto mais robusto sem grande refatoração.
