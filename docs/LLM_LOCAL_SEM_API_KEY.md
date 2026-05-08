# LLMs Locais Sem API Key

O GalFlowAI (galFlowAI) foi redesenhado para funcionar **100% sem API key** e **100% offline**.

## Arquitetura de Providers

```
briefing → ProviderRouter → LLM Local (opcional) → TemplateProvider (obrigatório)
```

### Ordem de Fallback (modo seguro):
1. **LMStudioProvider** (opcional) - http://localhost:1234
2. **KoboldCppProvider** (opcional) - http://localhost:5001
3. **LlamaCppProvider** (opcional) - http://localhost:8080
4. **GPT4AllProvider** (opcional) - Python package
5. **TemplateProvider** (obrigatório) - sempre funciona

## Opções de Uso

### 1. Apenas Template (Sem instalação)
- ✅ Funciona imediatamente
- ✅ Zero instalação
- ✅ Gera roteiros com templates inteligentes
- ⚠️ Qualidade menor que LLMs reais

### 2. Com LM Studio (Recomendado)
- Baixe: https://lmstudio.ai
- Ative: Developer → Local Server → Porta 1234
- Modelos leves: Llama 3.2 3B, Phi-3 mini
- ✅ Melhor qualidade
- ✅ Fácil de usar

### 3. Com KoboldCpp (Portátil)
- Baixe executável para K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\llm_engines\koboldcpp
- Use modelos GGUF leves (2-3GB)
- ✅ Não instala nada no C:
- ✅ Rápido

### 4. Com GPT4All (SDK Python)
- Instale: `pip install gpt4all`
- Baixe modelos para K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gpt4all
- ✅ Integração Python direta
- ✅ Modelos variados

### 5. Com Llama.cpp (Avançado)
- Instale: `pip install llama-cpp-python`
- Ou use servidor local
- ✅ Controle total
- ✅ Melhor para hardware específico

## Modos de Geração

### Modo Rápido (`fast`)
- Dispara providers em paralelo
- Usa primeiro válido
- Timeout curto (5s)
- Ideal para prévias

### Modo Qualidade (`quality`)
- Espera resposta melhor
- Timeout maior (15s)
- Valida qualidade
- Ideal para roteiro final

### Modo Seguro (`safe`)
- Tenta um por um
- Garantido funciona
- Ideal para debug

## Por que Ollama não é obrigatório?

1. **Pesado**: Ollama baixa modelos grandes por padrão
2. **Difícil controle**: Não deixa escolher facilmente a pasta K:
3. **Depende de internet**: Precisa baixar modelos na primeira vez
4. **TemplateProvider é suficiente**: Para quem não quer instalar nada

## Configuração no `config.py`

```python
LLM_PROVIDER_MODE = "auto"  # auto, fast, quality, safe
LLM_FAST_TIMEOUT_SECONDS = 5
LLM_QUALITY_TIMEOUT_SECONDS = 15

LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
KOBOLDCPP_BASE_URL = "http://localhost:5001"
LLAMACPP_BASE_URL = "http://localhost:8080/v1"
GPT4ALL_MODEL_DIR = "K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/models/gpt4all"
GGUF_MODEL_DIR = "K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/models/gguf"
```

## Como Testar

### Sem nenhum LLM:
1. Execute: `python app/main.py`
2. Acesse: http://127.0.0.1:7860
3. Digite briefing e clique "Criar comercial"
4. Verá: "Motor usado: TemplateProvider"

### Com LM Studio:
1. Abra LM Studio
2. Vá em Developer → Local Server
3. Carregue um modelo
4. Clique "Start Server"
5. Teste: `curl http://localhost:1234/v1/models`
6. No GalFlowAI, verá: "Motor usado: LMStudioProvider"

### Com outros providers:
- Execute: `scripts\llm\01_detectar_llms_locais.bat`
- Siga as instruções nas docs criadas

## Mensagens na UI (Português)

- "Motor usado: LM Studio local"
- "Motor usado: Template local"
- "LM Studio não encontrado. Usando próximo motor."
- "KoboldCpp não encontrado. Usando próximo motor."
- "Nenhum LLM local ativo. Usando Template local."

## Fallback Garantido

Mesmo que:
- ❌ LM Studio não esteja instalado
- ❌ KoboldCpp não esteja rodando
- ❌ Llama.cpp não esteja configurado
- ❌ GPT4All não esteja instalado

O **TemplateProvider SEMPRE FUNCIONA** e gera roteiros aceitáveis.

## Próximos Passos

1. **Teste sem nada**: Veja o TemplateProvider funcionando
2. **Instale LM Studio**: Melhor qualidade com menor esforço
3. **Ou teste KoboldCpp**: Se quiser portabilidade no K:
4. **Nunca quebre o app**: Fallback sempre funciona

---

**Documentação criada em:** 03/05/2026
**Versão:** GalFlowAI 1.0 - Local-First Architecture
