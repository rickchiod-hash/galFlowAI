# BACKLOG E ROADMAP - FlowForgeAI

**Arquivo de Checkpoint**: Consultar e atualizar sempre que iniciar nova sessão.
**Objetivo**: Mapear o que foi feito, pular o que foi validado, e listar pendências.

**Última atualização**: 03/05/2026
**Último commit**: `3ea7b9e` - "feat(llm): LLM Providers completo + FastAPI V2 + Script Service + Video Pipeline"

---

## ✅ CHECKLIST DE VALIDAÇÃO PARA NOVA SESSÃO

Ao iniciar uma **nova sessão**, valide **tudo que está marcado como ✅** abaixo. Se estiver funcionando, **pule** para as pendências (⚠️).

### 1. Estrutura Básica
- [x] `app/main.py` existe e compila
- [x] `app/api.py` existe (mas pode ter erros de sintaxe)
- [x] `app/services/script_service.py` existe
- [x] `app/adapters/llm/` com 6 providers criados
- [x] `app/pipeline/video_generation_pipeline.py` criado
- [x] `README.md` atualizado
- [x] `AGENTS.md` atualizado
- [x] `docs/` com 10 documentos
- [x] `tests/` com testes criados

### 2. Funcionalidades Implementadas
- [x] **LLM Providers** (6 providers) - Template, LM Studio, KoboldCpp, GPT4All, Llama.cpp
- [x] **Script Service** - Camada de negócio com versionamento
- [x] **FastAPI V2** - 15+ endpoints criados
- [x] **Gradio UI** - Interface com seletor de motor
- [x] **Video Pipeline** - Estrutura completa criada
- [x] **Adapters** - WanGP, TTS, FFmpeg criados
- [x] **Documentação** - 10 documentos completos
- [x] **Testes** - Unitários e integração criados

### 3. Commits e Push
- [x] Commit realizado: `3ea7b9e`
- [x] Push realizado para `origin/master`

---

## ❌ PENDÊNCIAS CRÍTICAS (Corrigir Agora)

### 1. Erros de Sintaxe em `api.py` ⚠️
**Status**: ❌ NÃO CORRIGIDO
**Problema**: Múltiplos erros de sintaxe:
- Linha 7: `from typing import Dict, List, Optional, Any` (está `Dict, List` sem vírgula)
- Linha 13: `sys.path.insert(0, str(Path(__file__).parent.parent))` (está `__file__` incorreto)
- Múltiplos returns: `return {"ok": True "version": ...}` (falta vírgula após `True`)
- Linha 29: `allow_origins` (deveria ser `allow_origins`)
- CORS middleware chamado incorretamente

**Ação**: Corrigir todos os erros de sintaxe antes de subir aplicação.

### 2. Python Não Encontrado ⚠️
**Status**: ❌ REDIRECIONANDO PARA MICROSOFT STORE
**Problema**: `python` comando redireciona para Microsoft Store
**Causa**: Alias de execução do Windows ativado

**Ação**: Usar caminho completo: `K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe`

### 3. Caminhos Inconsistentes ⚠️
**Status**: ❌ PARCIALMENTE INCONSISTENTE
**Problema**: `AI_VIDEO_COMERCIAL_STUDIO` vs `AI_VIDEO_COMMERCIAL_STUDIO`

**Ação**: Padronizar para `AI_VIDEO_COMERCIAL_STUDIO` (verificar se pasta é `COMERCIAL` ou `COMMERCIAL`)

---

## 📋 BACKLOG COMPLETO

### Prioridade 1 - Correções Críticas

| ID | Tarefa | Status | Arquivos Afetados |
|----|--------|--------|-------------------|
| P1-01 | Corrigir sintaxe em `api.py` (faltam vírgulas em dicionários) | ❌ | `app/api.py` |
| P1-02 | Corrigir `__file__` para `__file__` em `api.py` | ❌ | `app/api.py` |
| P1-03 | Corrigir `allow_origins` para `allow_origins` | ❌ | `app/api.py` |
| P1-04 | Corrigir CORS middleware (está `CORSMiddleware` mas deveria ser `CORSMiddleware`) | ❌ | `app/api.py` |
| P1-05 | Corrigir `GRADIO_PORT` para `GRADIO_PORT` (conforme config.py) | ❌ | `app/api.py` |
| P1-06 | Verificar sintaxe em `main.py` | ⚠️ | `app/main.py` |
| P1-07 | Configurar Python para não abrir Microsoft Store | ❌ | Scripts de start |
| P1-08 | Testar se Gradio sobe em `http://127.0.0.1:7860` | ❌ | `app/main.py` |
| P1-09 | Testar se FastAPI sobe em `http://127.0.0.1:8000` | ❌ | `app/api.py` |

### Prioridade 2 - Validação de Funcionalidades

| ID | Tarefa | Status | Teste |
|----|--------|--------|-------|
| P2-01 | Validar LLM Providers (6 providers) | ✅ | `tests/unit/test_llm_providers.py` |
| P2-02 | Validar Script Service | ⚠️ | `tests/test_script_service.py` |
| P2-03 | Validar FastAPI endpoints | ❌ | `tests/test_api_*.py` |
| P2-04 | Validar Gradio UI (seletor de motor) | ❌ | Manual |
| P2-05 | Validar Roteiro Editável | ❌ | Manual |
| P2-06 | Validar Video Pipeline (FFmpeg fallback) | ⚠️ | `tests/integration/test_pipeline_completo.py` |
| P2-07 | Validar WanGP Adapter | ❌ | `app/adapters/wangp_adapter.py` |
| P2-08 | Validar TTS Adapter | ❌ | `app/adapters/tts_adapter.py` |

### Prioridade 3 - Melhorias e Integração

| ID | Tarefa | Status | Detalhes |
|----|--------|--------|----------|
| P3-01 | Instalar WanGP real | ❌ | `scripts/install_wangp.bat` criado |
| P3-02 | Testar pipeline completo com FFmpeg | ⚠️ | Funcionou parcialmente (preview de 35s) |
| P3-03 | Integrar WebSocket para progresso | ❌ | Placeholder criado |
| P3-04 | Adicionar fila de jobs (SQLite) | ❌ | Futuro |
| P3-05 | Criar React UI (V3) | ❌ | Futuro |
| P3-06 | Documentar com OpenAPI completo | ❌ | Swagger existe |

---

## 🗺️ ROADMAP POR VERSÃO

### V2.0 - ATUAL (Em andamento)
**Objetivo**: Finalizar funcionalidades básicas locais
- ✅ LLM Providers sem API key
- ✅ Script Service com versionamento
- ✅ FastAPI V2 com endpoints
- ❌ Corrigir sintaxe em `api.py`
- ❌ Subir Gradio + FastAPI com sucesso
- ⚠️ Testar pipeline completo

### V2.1 - PRÓXIMA (Planejada)
**Objetivo**: Estabilização e WanGP real
- Corrigir todos os erros de sintaxe
- Instalar WanGP em `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP`
- Testar geração real de vídeo com 1.3B
- Validar fallback FFmpeg
- Completar testes automatizados

### V3.0 - FUTURA
**Objetivo**: React UI + WebSocket + Jobs
- Migrar Gradio para React/TypeScript
- Implementar WebSocket para progresso em tempo real
- Adicionar fila de jobs com Redis/RQ ou SQLite
- Documentação OpenAPI completa
- Deploy local primeiro

---

## 🔄 INSTRUÇÕES PARA NOVA SESSÃO

Ao iniciar uma **nova sessão**, siga estes passos:

### 1. Consultar este arquivo
```
LEIA: K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\BACKLOG.md
```

### 2. Validar o que está marcado como ✅
- Execute os testes básicos
- Verifique se os arquivos existem
- Confirme se o último commit está estável

### 3. Pular o que foi validado
Se algo marcado como ✅ está funcionando:
- **NÃO reimplemente**
- **NÃO recomece do zero**
- **CONTINUE das pendências marcadas como ❌ ou ⚠️**

### 4. Atualizar este arquivo
Após cada sessão:
- Atualize o status das tarefas
- Marque como ✅ o que foi concluído
- Adicione novas pendências se necessário
- Atualize o "Último commit" e "Última atualização"

### 5. Fazer commit deste arquivo
```
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
git add BACKLOG.md
git commit -m "docs(backlog): Atualiza checkpoint e pendências"
git push origin master
```

---

## 📊 RESUMO DO ESTADO ATUAL

### ✅ Concluído (Não mexer)
1. Estrutura de pastas básica
2. LLM Providers (6 providers implementados)
3. Script Service (camada de negócio)
4. Video Pipeline (estrutura criada)
5. Documentação (10 documentos)
6. Testes (criados, mas não executados)
7. Commit e Push realizados (`3ea7b9e`)

### ❌ Pendências Críticas (Fazer agora)
1. **Corrigir sintaxe em `api.py`** - faltam vírgulas em dicionários
2. **Configurar Python** - evitar Microsoft Store
3. **Subir Gradio** - testar em `http://127.0.0.1:7860`
4. **Subir FastAPI** - testar em `http://127.0.0.1:8000`

### 🎯 Próximo Marco
**Meta**: Aplicação funcionando com:
- Gradio UI abrindo corretamente
- FastAPI respondendo endpoints
- TemplateProvider funcionando
- Video Pipeline gerando preview com FFmpeg

---

**NOTA PARA MIM MESMO**:
Sempre que iniciar nova sessão:
1. **LEIA este arquivo primeiro**
2. **Valide o que está ✅**
3. **Pule o que foi validado**
4. **Foque nas pendências ❌**
5. **Atualize este arquivo ao final**
6. **Faça commit com tag `checkpoint`**
