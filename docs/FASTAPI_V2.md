# FastAPI V2 - GalFlowAI

## Visao Geral

A API FastAPI V2 é a camada pública/local preparada para:
- Automação
- Testes
- Futuro React/TypeScript
- Integração externa local
- Documentação OpenAPI

## Endpoints

### Health Check
```
GET /api/health
```

Retorno:
```json
{
  "status": "ok",
  "app": "GalFlowAI",
  "mode": "local",
  "ui": "gradio",
  "fastapi": true,
  "version": "2.0"
}
```

### LLM Providers
```
GET /api/llm/providers
```

Retorno:
```json
{
  "template": true,
  "lmstudio": false,
  "koboldcpp": false,
  "gpt4all": false,
  "llamacpp": false,
  "openai_compatible_local": false
}
```

### Generate Script
```
POST /api/llm/script
```

Entrada:
```json
{
  "briefing": "Quero vender...",
  "project_id": "opcional",
  "provider": "auto|template|lmstudio|koboldcpp|gpt4all|llamacpp",
  "mode": "first_valid|quality|safe",
  "timeout_seconds": 10,
  "endpoint": "opcional"
}
```

Saída:
```json
{
  "ok": true,
  "provider_used": "TemplateProvider",
  "fallback_used": false,
  "response_time_seconds": 1.23,
  "quality_score": 0,
  "script_markdown": "...",
  "script_json": {},
  "logs": []
}
```

### Script Editing
```
POST /api/projects/{project_id}/script/save-manual-edit
POST /api/projects/{project_id}/script/improve
POST /api/projects/{project_id}/script/more-viral
POST /api/projects/{project_id}/script/more-premium
POST /api/projects/{project_id}/script/more-direct
POST /api/projects/{project_id}/script/new-version
POST /api/projects/{project_id}/script/restore-previous
POST /api/projects/{project_id}/script/approve
GET /api/projects/{project_id}/script/current
GET /api/projects/{project_id}/script/versions
```

### Hardware
```
GET /api/hardware
```

### Jobs (Placeholder)
```
GET /api/jobs/{job_id}
POST /api/jobs/{job_id}/cancel
WS /ws/jobs/{job_id}
```

## Como Subir

### Opção 1: Script
```bash
scripts/start_fastapi.bat
```

### Opção 2: Manual
```bash
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe -m uvicorn ^
  app.api:app ^
  --host 127.0.0.1 ^
  --port 8000 ^
  --reload
```

## Testar

### Health Check
```bash
curl http://127.0.0.1:8000/api/health
```

### Testar Providers
```bash
curl http://127.0.0.1:8000/api/llm/providers
```

### Documentação Automática
Abra: http://127.0.0.1:8000/docs

## Regras

1. **Gradio continua sendo a UI principal**
2. **FastAPI é complementar**, não substituta
3. **Todos os endpoints usam `services/`**
4. **Não duplicar lógica** entre Gradio e FastAPI
5. **CORS configurado** apenas para localhost
6. **Sem dependência de cloud**
7. **TemplateProvider sempre disponível**

## Próximos Passos

1. Integrar React/TypeScript na V3 (usando FastAPI)
2. Adicionar WebSocket real para progresso
3. Implementar jobs reais com Redis/RQ (opcional)
4. Documentar com OpenAPI completo

---

**Versão:** 2.0  
**Data:** 03/05/2026  
**Status:** Implementado, testável
