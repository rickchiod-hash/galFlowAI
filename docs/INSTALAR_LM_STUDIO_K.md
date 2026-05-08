# Instalação LM Studio no K:

## Passo a Passo

### 1. Baixar LM Studio
- Acesse: https://lmstudio.ai
- Baixe a versão para Windows
- **Importante**: Pode instalar no C: (o executável), mas os **modelos ficam no K:**

### 2. Configurar Pasta de Modelos
1. Abra o LM Studio
2. Vá em **Settings** (ícone de engrenagem)
3. Procure **Models Directory**
4. Altere para: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\lmstudio`
5. Salve

### 3. Baixar Modelo Leve
Recomendados para GTX 1660 Super (6GB VRAM):
- **Llama 3.2 3B** (2GB) - Rápido e eficiente
- **Phi-3 mini** (2GB) - Excelente para texto
- **Gemma 2 2B** (1.5GB) - Muito leve

No LM Studio:
1. Vá em **Discover**
2. Procure um dos modelos acima
3. Clique **Download**
4. Aguarde o download (única vez que precisa de internet)

### 4. Ativar Servidor Local
1. Vá em **Developer** (ícone de código)
2. Clique em **Local Server**
3. Selecione o modelo baixado
4. Confira: Porta: `1234`
5. Clique **Start Server**

### 5. Testar
Abra o terminal e execute:
```bash
curl http://localhost:1234/v1/models
```

Deve retornar um JSON com o modelo carregado.

### 6. Usar no GalFlowAI
1. Mantenha o LM Studio aberto com servidor ativo
2. Execute: `python app/main.py`
3. Acesse: http://127.0.0.1:7860
4. Crie um comercial
5. Verá: "Motor usado: LMStudioProvider"

## Configuração no GalFlowAI

Ou vá até: `app\config.py` e confira:
```python
LMSTUDIO_BASE_URL = "http://localhost:1234/v1"
```

## Vantagens do LM Studio
- ✅ Interface amigável
- ✅ Gerencia modelos facilmente
- ✅ Servidor compatível com OpenAI
- ✅ Não precisa de API key
- ✅ Modelos leves rodam bem na GTX 1660

## Observações
- O LM Studio **não precisa** ficar aberto o tempo todo
- Quando fechar, o GalFlowAI usará automaticamente o **TemplateProvider**
- Reabra o LM Studio e inicie o servidor quando quiser melhor qualidade

---

**Versão:** 1.0
**Data:** 03/05/2026
