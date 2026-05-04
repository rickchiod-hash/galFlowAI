# QA Test Plan — Gal AI Studio

## Status Geral
- **Data:** 2026-05-03
- **Branch:** master
- **Último commit:** P1-GRADIO-13: Modo Simples e Avançado

## Fases de Testes (T1/T2/T3)

### T1 — Testes Unitários (Mínimos)
| Teste | Arquivo | Status | Cobertura |
|---|---|---|---|
| Geração com TemplateProvider | `tests/test_script_generator.py` | [feito] | Script generation |
| Fallback sem LLM | `tests/test_script_generator.py` | [feito] | Fallback behavior |
| FFmpeg adapter init | `tests/test_ffmpeg_adapter.py` | [feito] | Adapter status |
| Parser de logs (INFO/WARN/ERROR) | `tests/test_log_service.py` | [feito] | Log parsing |
| Eliminação de UNKNOWN | `tests/test_log_service.py` | [feito] | Log quality |

### T2 — Testes de API e E2E
| Teste | Arquivo | Status | Cobertura |
|---|---|---|---|
| Endpoints FastAPI | `tests/test_api_endpoints.py` | [feito] | API coverage |
| Pipeline E2E completo | `tests/test_pipeline_e2e.py` | [feito] | End-to-end |
| Fallback behavior E2E | `tests/test_pipeline_e2e.py` | [feito] | Fallback |
| Múltiplas cenas E2E | `tests/test_pipeline_e2e.py` | [feito] | Scene generation |

### T3 — Gaps e Melhorias (Pós-P1)
| Item | Descrição | Status | Prioridade |
|---|---|---|---|
| Contratos de erro | `app/exceptions.py` | [pendente] | Alta |
| Concorrência e fila de jobs | `app/jobs/queue.py` | [pendente] | Alta |
| Timeout/Retry/Backoff | `app/adapters/*.py` | [pendente] | Média |
| Métricas | `app/services/metrics_service.py` | [pendente] | Média |
| Validação de arquivos | `app/services/*.py` | [pendente] | Baixa |

## Cenários de Automação e Chamadas de API
1. **Criar projeto via API**: `POST /api/project/create`
2. **Gerar roteiro via API**: `POST /api/script/generate`
3. **Fluxo completo E2E**: Briefing → Roteiro → Cenas → Preview
4. **Fallback TemplateProvider**: Verificar se usa template quando LLM ausente
5. **Modo Simples vs Avançado**: Alternar via UI e verificar campos

## Cobertura Obtida
- **Testes unitários:** 5 arquivos criados (`test_script_generator.py`, `test_ffmpeg_adapter.py`, `test_log_service.py`, `test_api_endpoints.py`, `test_pipeline_e2e.py`)
- **Cenários principais:** Cobertos (geração, fallback, parser de logs)
- **Cenários de falha:** Cobertos (briefing vazio, LLM ausente, FFmpeg ausente)

## Gaps Remanescentes
1. **React V2.5**: Aguardar estabilidade FastAPI (não iniciado)
2. **Chatbot lateral (V2.3)**: Futuro, não implementado
3. **Dashboard de projetos (P2-GRADIO-16)**: Não iniciado
4. **Integração WanGP real**: Dependente de instalação local

## Como Rodar os Testes
```bash
# Todos os testes
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest tests/ -v

# Teste específico
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest tests/test_script_generator.py -v
```

## Histórico de Execução
- **2026-05-03**: Criação de 5 arquivos de teste (item 5 do plano)
- **Próximo**: Executar testes e verificar cobertura real
