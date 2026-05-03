# Motores de Roteiro - Gal AI

## Visão Geral

O Gal AI suporta múltiplos motores de roteiro, todos **locais** e **sem API key**.

## Motores Disponíveis

### 1. TemplateProvider (Obrigatório)
- ✅ **Sempre funciona**
- ✅ **Zero instalação**
- ✅ **Zero internet**
- ✅ Gera roteiros comerciais decentes
- ✅ Suporta fantasias/cosplay/geek/3D
- ⚠️ Qualidade menor que LLMs reais

**Templates disponíveis:**
- `viral` - Chamativo, viral
- `fantasia` - Medieval, cosplay, personagem
- `futurista` - Cyberpunk, neon, tech
- `geek` - Colecionável, action figure
- `impressao3d` - Impressão 3D personalizada
- `premium` - Luxo, sofisticado
- `servico_local` - Loja, bastidores

### 2. LM Studio (Opcional, Recomendado)
- Baixe: https://lmstudio.ai
- Ative: Developer → Local Server → Porta 1234
- Modelos: Llama 3.2 3B, Phi-3 mini (leves para 6GB VRAM)
- ✅ Melhor qualidade
- ✅ Interface amigável
- ✅ Fácil de usar

### 3. KoboldCpp (Opcional, Portátil)
- Baixe executável: https://github.com/LostRuins/KoboldCpp/releases
- Salve em: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\llm_engines\koboldcpp`
- Modelos GGUF em: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf`
- ✅ Portátil (um exe)
- ✅ Não instala nada no C:
- ✅ Rápido

### 4. GPT4All (Opcional, SDK Python)
- Instale: `pip install gpt4all`
- Modelos em: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gpt4all`
- ✅ Integração Python direta
- ✅ Não precisa de servidor

### 5. Llama.cpp (Opcional, Avançado)
- Instale: `pip install llama-cpp-python`
- Ou use servidor: http://localhost:8080
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
- Avalia qualidade
- Ideal para roteiro final.

### Modo Seguro (`safe`)
- Tenta um por vez
- Garantido funciona
- Ideal para debug.

## Fallback Garantido

```
LM Studio (se ativo) → KoboldCpp (se ativo) → Llama.cpp (se ativo) → 
GPT4All (se ativo) → TemplateProvider (SEMPRE)
```

**O app NUNCA quebra por falta de LLM!**

## Configuração no `app/config.py`

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
3. Verá: "Motor usado: TemplateProvider"

### Com LM Studio:
1. Abra LM Studio → Developer → Local Server
2. Carregue um modelo → Start Server
3. Teste: `curl http://localhost:1234/v1/models`
4. No Gal AI verá: "Motor usado: LMStudioProvider"

### Com outros providers:
- Execute: `scripts\llm\01_detectar_llms_locais.bat`
- Siga as instruções nas docs criadas

## Mensagens na UI (Português)

- "Motor usado: LM Studio local (2.34s)"
- "Motor usado: Template local (0.01s)"
- "LM Studio não encontrado. Usando próximo motor."
- "KoboldCpp não encontrado. Usando próximo motor."
- "Nenhum LLM local ativo. Usando Template local."

## Documentação Criada

- `docs/LLM_LOCAL_SEM_API_KEY.md` - Visão geral
- `docs/INSTALAR_LM_STUDIO_K.md` - LM Studio
- `docs/INSTALAR_KOBOLDCPP_K.md` - KoboldCpp
- `docs/INSTALAR_GPT4ALL_K.md` - GPT4All
- `docs/INSTALAR_LLAMACPP_K.md` - Llama.cpp
- `docs/ROTEIROS_COM_FANTASIA.md` - Exemplos de fantasia

## Por que Ollama não é obrigatório?

1. **Pesado**: Baixa modelos grandes por padrão
2. **Difícil controle**: Não deixa escolher fácilmente a pasta K:
3. **Depende de internet**: Precisa baixar modelos na primeira vez
4. **TemplateProvider é suficiente**: Para quem não quer instalar nada

---

**Versão:** 1.0  
**Data:** 03/05/2026  
**Status:** Implementado, documentado, testável
