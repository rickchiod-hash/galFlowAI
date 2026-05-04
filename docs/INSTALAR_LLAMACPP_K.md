# Instalação Llama.cpp no K:

## O que é Llama.cpp?
Llama.cpp é uma implementação em C++ para rodar modelos Llama (GGUF) com máxima eficiência. Versão avançada para quem quer controle técnico.

## Opção A: Usar Python Bindings

### 1. Instalar Pacote
```bash
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe -m pip install llama-cpp-python
```

### 2. Baixar Modelo GGUF
Crie pasta: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf\`
Baixe modelos de: https://huggingface.co/models?pipeline_tag=text-generation
Procure: Llama 3.2 3B Q4, Phi-3 mini Q4

### 3. Iniciar Servidor (Opcional)
```bash
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
scripts\llm\06_iniciar_llamacpp_exemplo.bat
```

Ou:
```bash
python -m llama_cpp.server ^
  --model "K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/models/gguf/seu_modelo.gguf" ^
  --port 8080 ^
  --n_ctx 2048
```

### 4. Testar
```bash
curl http://localhost:8080/v1/models
```

## Opção B: Compilar do Zero (Avançado)
**NÃO recomendado** para iniciantes. Requer:
- CMake
- Compilador C++
- Conhecimento técnico

Se quiser seguir, veja: https://github.com/ggerganov/llama.cpp

## Usar no Gal AI
1. Instale o pacote (Opção A, passo 1)
2. Baixe um modelo (passo 2)
3. Opcionalmente inicie o servidor (passo 3)
4. Execute: `python app/main.py`
5. Acesse: http://127.0.0.1:7860
6. Verá: "Motor usado: LlamaCppProvider"

## Configuração
No `app\config.py`:
```python
LLAMACPP_BASE_URL = "http://localhost:8080/v1"
GGUF_MODEL_DIR = "K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/models/gguf"
```

## Vantagens
- ✅ Máxima eficiência
- ✅ Controle total do hardware
- ✅ Suporta quantização personalizada
- ✅ Comunidade ativa

## Observações
- Difícil configuração inicial
- Requer conhecimento técnico
- O Gal AI usa **TemplateProvider** se não estiver configurado

---

**Versão:** 1.0
**Data:** 03/05/2026
