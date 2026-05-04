# Instalação KoboldCpp no K:

## O que é KoboldCpp?
KoboldCpp é um programa portátil (executável único) que roda modelos GGUF localmente. Ideal para quem quer evitar instalações complexas.

## Passo a Passo

### 1. Baixar KoboldCpp
1. Acesse: https://github.com/LostRuins/KoboldCpp/releases
2. Procure a versão mais recente
3. Baixe o arquivo: `koboldcpp.exe` (Windows)
4. Salve em: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\llm_engines\koboldcpp\`

### 2. Criar Pasta de Modelos
Crie a pasta: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf\`

### 3. Baixar Modelo GGUF Leve
Para GTX 1660 Super (6GB VRAM), recomendamos:
- **Llama 3.2 3B Q4** (~2GB)
- **Phi-3 mini Q4** (~2GB)
- **Gemma 2 2B Q4** (~1.5GB)

Links:
- Hugging Face: https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads
- Procure por arquivos `.gguf`

Salve o modelo baixado em: `K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf\`

### 4. Iniciar Servidor
Abra o terminal e execute:
```bash
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
scripts\llm\05_iniciar_koboldcpp_exemplo.bat
```

Ou manualmente:
```bash
K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\llm_engines\koboldcpp\koboldcpp.exe ^
  --model "K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta\models\gguf\seu_modelo.gguf" ^
  --port 5001 ^
  --threads 6
```

### 5. Testar
Abra outro terminal:
```bash
curl http://localhost:5001/api/v1/models
```

### 6. Usar no Gal AI
1. Mantenha o KoboldCpp rodando
2. Execute: `python app/main.py`
3. Acesse: http://127.0.0.1:7860
4. Verá: "Motor usado: KoboldCppProvider"

## Vantagens
- ✅ Portátil (um único exe)
- ✅ Nada instalado no C:
- ✅ Rápido e eficiente
- ✅ Suporta vários modelos GGUF

## Observações
- Onde diz "seu_modelo.gguf", substitua pelo nome real do arquivo
- Feche a janela do KoboldCpp para parar o servidor
- O Gal AI fará fallback para **TemplateProvider** se o servidor não estiver ativo

---

**Versão:** 1.0
**Data:** 03/05/2026
