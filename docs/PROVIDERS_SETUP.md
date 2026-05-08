# Provedores LLM - Guia de Configuração

## Visão Geral

O GalFlowAI suporta múltiplos provedores LLM locais. Este guia explica como configurar cada um.

## Provedores Suportados

### 1. GPT4All (Recomendado para iniciantes)
**Status**: ✅ Configurado e testado

**O que é**: Pacote Python que roda modelos GGUF localmente.

**Modelo atual**: `mistral-7b-openorca.Q4_0.gguf` (4.11 GB)

**Localização do modelo**:
```
K:\AI_VIDEO_COMERCIAL_STUDIO\models\gpt4all\mistral-7b-openorca.Q4_0.gguf
```

**Como usar**:
```python
from app.adapters.llm.gpt4all_provider import GPT4AllProvider

provider = GPT4AllProvider()
if provider.is_available():
    result = provider.generate("Crie um roteiro para...")
    print(result)
```

**Sem configuração adicional necessária** - já está pronto para uso.

---

### 2. LM Studio
**Status**: ⏳ Código pronto, instalação manual necessária

**O que é**: Aplicativo desktop para rodar LLMs localmente com interface gráfica.

**Download**: https://lmstudio.ai/

**Instalação**:
1. Baixe e instale o LM Studio
2. Abra o programa e carregue um modelo (ex: Mistral 7B Q4)
3. Vá em "Local Server" e inicie o servidor (porta 1234)

**Teste se está rodando**:
```powershell
try {
    Invoke-WebRequest -Uri "http://localhost:1234/v1/models" -TimeoutSec 5
    Write-Host "✅ LM Studio rodando!"
} catch {
    Write-Host "❌ LM Studio não está rodando"
}
```

**Configuração no GalFlowAI**:
O `lmstudio_provider.py` já está implementado. O sistema detectará automaticamente se o LM Studio estiver rodando.

---

### 3. KoboldCpp
**Status**: ⏳ Código pronto, download de modelo necessário

**O que é**: Interface web para rodar modelos GGUF via navegador.

**Download recomendado**: TinyLlama 1.1B Q4 (~600MB)
```powershell
# Baixar modelo
$url = "https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF/resolve/main/tinyllama-1.1b-chat-v1.0.q4_k_m.gguf"
$output = "K:\AI_VIDEO_COMERCIAL_STUDIO\models\koboldcpp\tinyllama-1.1b-chat-v1.0.q4_k_m.gguf"
Invoke-WebRequest -Uri $url -OutFile $output
```

**Uso**:
1. Execute o KoboldCpp
2. Carregue o modelo baixado
3. O GalFlowAI detectará automaticamente na porta 5001

**Teste**:
```powershell
try {
    Invoke-WebRequest -Uri "http://localhost:5001/api/v1/models" -TimeoutSec 5
    Write-Host "✅ KoboldCpp rodando!"
} catch {
    Write-Host "❌ KoboldCpp não está rodando"
}
```

---

### 4. TemplateProvider (Fallback)
**Status**: ✅ Sempre disponível

**O que é**: Gerador de roteiros baseado em templates fixos. Usado quando nenhum LLM está disponível.

**Vantagens**:
- Funciona 100% offline
- Não precisa de modelos baixados
- Resposta instantânea

**Uso**: Automático - o sistema usa quando LLMs falham.

---

## Como o Sistema Seleciona o Provedor

O `ProviderRouter` (em `app/adapters/llm/provider_router.py`) seleciona automaticamente:

1. **Modo 'auto'**: Tenta GPT4All → LM Studio → KoboldCpp → Template
2. **Modo 'fast'**: Prefere modelos menores/mais rápidos
3. **Modo 'quality'**: Prefere modelos maiores/melhores
4. **Modo 'safe'**: Evita modelos que podem travar em 6GB VRAM
5. **Modo 'template'**: Força uso de TemplateProvider

**Exemplo**:
```python
from app.services.script_service import generate_script_with_llm

# Automático (recomendado)
result = generate_script_with_llm("Briefing aqui", mode="auto")

# Forçar Template (sem LLM)
result = generate_script_with_llm("Briefing aqui", mode="template")
```

---

## Resolução de Problemas

### Erro: "Nenhum provedor LLM disponível"
**Causa**: Nenhum dos provedores está rodando.

**Solução**:
1. Verifique se GPT4All model existe em `K:\AI_VIDEO_COMERCIAL_STUDIO\models\gpt4all\`
2. Ou inicie LM Studio / KoboldCpp
3. Ou use modo 'template' (não precisa LLM)

### Erro: "PyTorch not found" (WanGP)
**Causa**: PyTorch não instalado.

**Solução**:
```powershell
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Erro: "VRAM insuficiente"
**Causa**: Modelo muito grande para sua GPU.

**Solução**:
- Use modelos Q4 (quantizados) em vez de FP16
- O sistema já configura 1.3B e 480p para GTX 1660 Super
- Evite rodar outros programas pesados enquanto gera vídeo

---

## Próximos Passos

1. ✅ GPT4All já configurado
2. ⏳ Configure LM Studio se desejar interface gráfica
3. ⏳ Configure KoboldCpp se preferir interface web
4. ✅ TemplateProvider sempre disponível como fallback

**Documentação relacionada**:
- [VideoService.md](VIDEO_SERVICE.md)
- [README.md](../README.md)
