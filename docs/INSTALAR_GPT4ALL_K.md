# Instalação GPT4All no K:

## O que é GPT4All?
GPT4All é um SDK Python que permite rodar modelos GGUF localmente com integração direta em Python.

## Passo a Passo

### 1. Instalar SDK Python
Abra o terminal e execute (usando o Python do projeto):
```bash
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe -m pip install gpt4all
```

### 2. Criar Pasta de Modelos
Crie a pasta: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gpt4all\`

### 3. Baixar Modelo
Acesse: https://gpt4all.io/index.html
Procure modelos leves:
- **orca-mini-3.7-8b-q4** (~2GB)
- **gpt4all-falcon-newbpe-q4** (~2GB)

Baixe e salve em: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gpt4all\`

### 4. Testar
Crie um script de teste:
```python
from gpt4all import GPT4All
model = GPT4All("nome_do_modelo.gguf", model_path="K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/models/gpt4all")
response = model.generate("Crie um roteiro para comercial de 30s", max_tokens=500)
print(response)
```

### 5. Usar no FlowForgeAI
1. Instale o SDK (passo 1)
2. Baixe um modelo (passo 3)
3. Execute: `python app/main.py`
4. Acesse: http://127.0.0.1:7860
5. Verá: "Motor usado: GPT4AllProvider"

## Configuração
No `app\config.py`:
```python
GPT4ALL_MODEL_DIR = "K:/AI_VIDEO_COMERCIAL_STUDIO/opencodegalpasta/models/gpt4all"
```

## Vantagens
- ✅ Integração Python direta
- ✅ Não precisa de servidor separado
- ✅ Vários modelos disponíveis
- ✅ Fácil de usar

## Observações
- Só carrega o modelo quando necessário (pode demorar na primeira vez)
- O FlowForgeAI usa **TemplateProvider** se o GPT4All não estiver disponível

---

**Versão:** 1.0
**Data:** 03/05/2026
