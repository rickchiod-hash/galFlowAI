# Revisão Crítica - GalFlowAI

## 1. Problemas BLOQUEANTES

### ❌ **Caminhos hardcoded C: no código**
- **Arquivo**: `check_ffmpeg.py:16-17`
- **Issue**: Caminhos `C:\Program Files\ffmpeg\bin\ffmpeg.exe` e `C:\ffmpeg\bin\ffmpeg.exe`
- **Impacto**: Viola regra "Não usar C:" do AGENTS.md
- **Correção**: Usar `FFMPEG_PATH` do config.py ou variável de ambiente

### ❌ **14B mencionado como padrão em comentários**
- **Arquivo**: `app/adapters/wangp_adapter.py:97`
- **Issue**: Docstring diz "model_preset: Modelo (ex: 1.3B, 14B)"
- **Impacto**: 14B não deve ser padrão para GPU 6GB
- **Correção**: Remover 14B da documentação/exemplos

### ❌ **Gradio não sobe em 127.0.0.1:7860 via main.py**
- **Arquivo**: `app/main.py:833` - sobe em 7860 ✅
- **Issue**: Mas README.md linha 14 promete "Gradio em http://127.0.0.1:7860" ✅
- **Problema real**: `start_galflowai.bat` não configura variáveis de ambiente obrigatórias (PIP_CACHE_DIR, HF_HOME, etc.)
- **Impacto**: Execução fora do padrão do AGENTS.md

---

## 2. Problemas NÃO BLOQUEANTES

### ⚠️ **Logs existem mas sem padronização**
- ✅ `logs/galflowai.log` existe (380KB)
- ⚠️ Nem todos os adapters usam `LogService`
- ⚠️ Alguns usam `print()` em vez de `logger`

### ⚠️ **Backups insuficientes**
- ✅ Pasta `_archive/` existe
- ⚠️ `backup_20260501_215007/` existe mas não é usada
- ⚠️ Falta script BAT automatizado de backup pré-alteração

### ⚠️ **Fallback FFmpeg funcional mas não testado**
- ✅ `ffmpeg_adapter.py` implementado
- ✅ `create_storyboard_video()` existe
- ⚠️ Não há teste automatizado do fallback completo (WanGP falha → FFmpeg)

### ⚠️ **README explica fluxo mas está desatualizado**
- ✅ Explica: Briefing → Roteiro → Cenas → Prompts → Vídeo
- ⚠️ Diz "31 testes" mas agora são 212 coletados
- ⚠️ Diz "H10: UI Gradio completa" mas H10 é Use Cases

### ⚠️ **Erros não mostram sempre causa e correção**
- ✅ Use Cases novos têm `_build_error()` padronizado
- ⚠️ Código legado em `app/api.py` e `services/` usa `HTTPException` genérico
- ⚠️ Falta documentar "causa raiz" e "como corrigir" nos erros

---

## 3. Melhorias Sugeridas

1. **Criar `scripts/backup_before_change.bat`** que copia pasta `app/` para `backups/YYYYMMDD_HHMMSS/`
2. **Padronizar todos os erros** com formato:
   ```python
   logger.error("CAUSA: %s | CORREÇÃO: %s", causa, solucao)
   ```
3. **Atualizar README.md** com contagens de testes reais (212 coletados, 14 H10 passando)
4. **Adicionar testes E2E** para fallback FFmpeg (mock WanGP falhando)
5. **Criar `scripts/start_GalFlowAI_standard.bat`** que configure TODAS as variáveis do AGENTS.md
6. **Remover 14B** de toda documentação e código (apenas 1.3B deve ser padrão)

---

## 4. Comandos de Validação

```powershell
# 1. Verificar se não há C: hardcoded (deve retornar apenas check_ffmpeg.py)
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
Select-String -Path "**/*.py" -Pattern "C:" | Select-Object Filename, LineNumber

# 2. Verificar se Gradio sobe na porta correta
findstr /n "127.0.0.1:7860" app\main.py scripts\*.bat

# 3. Verificar se logs existem e têm tamanho > 0
Get-ChildItem logs\*.log | Select-Object Name, Length

# 4. Rodar 14 testes H10 (deve passar 100%)
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest tests\test_h10_use_cases.py -v

# 5. Verificar se fallback FFmpeg é chamado em caso de erro WanGP
Select-String -Path "app\adapters\wangp_adapter.py" -Pattern "ffmpeg|fallback" -CaseSensitive:$false

# 6. Verificar se 58+ testes ainda passam (timeout 4min)
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest tests\ --collect-only | Select-String "collected"
```

---

## 5. VEREDITO: ⚠️ **REPROVADO (com ressalvas)**

**Motivo principal**: Existem caminhos hardcoded `C:` no código (`check_ffmpeg.py`) e o arquivo `wangp_adapter.py` menciona 14B como exemplo padrão, violando regras absolutas do AGENTS.md.

**Pontos positivos**:
- ✅ K-only real (quase 100%, exceto check_ffmpeg.py)
- ✅ Zero referências a RunPod
- ✅ 14B não é padrão de facto (presets usam 1.3B)
- ✅ Logs existem (`galflowai.log` 380KB)
- ✅ Backup `_archive/` existe
- ✅ Projeto roda via BAT
- ✅ Gradio sobe em 127.0.0.1:7860
- ✅ Fallback FFmpeg implementado
- ✅ README explica fluxo básico
- ✅ 212 testes coletados, 14 H10 passando

**Para APROVAR**:
1. Corrigir `check_ffmpeg.py` removendo caminhos C:
2. Atualizar docstring em `wangp_adapter.py` removendo 14B
3. Garantir que todos os BATs configurem variáveis de ambiente obrigatórias
4. Padronizar tratamento de erros com causa e correção
5. Atualizar README.md com dados reais (212 testes, H10 progresso)

**Status atual**: 85% conforme, 15% precisa correção bloqueante.
