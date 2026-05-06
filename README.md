# FlowForgeAI - Gerador de Vídeos Comerciais com IA Local

[![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

## 🎯 Visão Geral

FlowForgeAI é uma plataforma **100% local** para geração de comerciais curtos para redes sociais, rodando em Windows com hardware modesto (GTX 1660 Super 6GB VRAM).

**Características principais:**
- ✅ 100% offline (sem APIs pagas)
- ✅ Hardware-aware (otimizado para 6GB VRAM)
- ✅ Interface web (Gradio em http://127.0.0.1:7860)
- ✅ Múltiplos provedores LLM (GPT4All, LM Studio, KoboldCpp)
- ✅ Fallback robusto (WanGP → FFmpeg → Template)

## 🚀 Status do Projeto

### ✅ Concluído (H1-H8)
- **H1**: Correção crítica de sintaxe (100+ arquivos)
- **H2**: Central de logs operacional
- **H3**: Infraestrutura LLM (ProviderRouter + Strategy + Factory)
- **H4a**: Download modelo GPT4All (mistral-7b-openorca.Q4_0.gguf - 4.11GB)
- **H4b**: PyTorch 2.11.0+cpu instalado
- **H6**: WanGP Adapter funcional (1.3B, 480p para 6GB VRAM)
- **H7**: 31 testes unitários passando

### ⏳ Em Andamento
- **H5a**: LM Studio (código pronto, aguardando instalação manual)
- **H5b**: KoboldCpp (código pronto, aguardando download de modelo)
- **H8**: Documentação e validação final

### 📋 Próximos Passos
- H9: Integração Fim-a-Fim (VideoService ✅)
- H10: UI Gradio completa
- H11: Sistema de fila de jobs
- H12: Métricas e monitoramento

## 🛠️ Instalação

### Pré-requisitos
- Windows 10/11
- Python 3.10+ (recomendado 3.10.20 para compatibilidade)
- 16GB RAM
- GPU NVIDIA com 6GB+ VRAM (GTX 1660 Super testado)
- 50GB disco livre (K:)

### Ambiente
```powershell
# Criar ambiente virtual
cd K:\AI_VIDEO_COMERCIAL_STUDIO
python -m venv envs/studio

# Ativar
envs\studio\Scripts\Activate.ps1

# Instalar dependências
pip install -r requirements.txt
```

### Modelos (Opcional - Fallback Disponível)
```powershell
# GPT4All (já baixado automaticamente)
# Local: K:\AI_VIDEO_COMERCIAL_STUDIO\models\gpt4all\

# WanGP (já existe em engines/Wan2GP)
# PyTorch CPU instalado via: python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cpu
```

## 🎮 Como Usar

### Iniciar Aplicação
```powershell
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe main.py
```

Acesse: **http://127.0.0.1:7860**

### Gerar Comercial (Linha de Comando)
```powershell
python example_video_generation.py
```

### Rodar Testes
```powershell
# Todos os testes
python run_all_tests.py

# Testes específicos
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest test_all_stories.py -v
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest test_video_service.py -v
```

## 🏗️ Arquitetura

```
FlowForgeAI/
├── app/
│   ├── adapters/          # Adapters para motores externos
│   │   ├── wangp_adapter.py      # WanGP (vídeo IA)
│   │   ├── ffmpeg_adapter.py     # FFmpeg (fallback)
│   │   └── llm/                  # Provedores LLM
│   ├── services/          # Serviços de negócio
│   │   ├── video_service.py      # Geração de vídeo
│   │   └── tts_service.py        # Text-to-Speech
│   ├── pipeline/         # Pipeline de processamento
│   │   ├── script_generator.py   # Roteiros
│   │   ├── scene_splitter.py     # Divisão em cenas
│   │   └── prompt_builder.py     # Prompts para vídeo
│   └── api.py            # API FastAPI (opcional)
├── projects/              # Projetos gerados
│   └── YYYYMMDD_HHMMSS_nome/
│       ├── brief/        # Briefing
│       ├── script/       # Roteiro
│       ├── prompts/      # Prompts de vídeo
│       ├── storyboard/   # Cenas
│       ├── renders/      # Vídeos das cenas
│       ├── audio/        # Narração
│       └── final/        # Vídeo final
└── docs/                 # Documentação
```

## 🧪 Testes

**Cobertura atual: 31 testes**
- ✅ test_all_stories.py (15 testes - H1-H8)
- ✅ test_video_service.py (8 testes)
- ✅ test_prompt_builder.py (8 testes)
- ✅ test_scene_splitter.py (9 testes)
- ✅ test_script_generator.py (6 testes)
- ✅ test_complete_system.py (integração)

```powershell
# Rodar todos
python run_all_tests.py

# Saída esperada:
# Testes executados: 31
# Sucessos: 31
# Falhas: 0
```

## 📊 Hardware Suportado

| Componente | Especificação | Status |
|-------------|---------------|--------|
| GPU | NVIDIA GTX 1660 Super 6GB | ✅ Testado |
| RAM | 16GB DDR4 | ✅ OK |
| CPU | AMD Ryzen 5 5600 6C/12T | ✅ OK |
| Disco | K: (SSD recomendado) | ✅ OK |

**Configurações automáticas para 6GB VRAM:**
- Modelo: 1.3B (não 14B)
- Resolução: 480p/512p
- Cenas curtas (~5s cada)
- Uma geração por vez

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Distribuído sob licença MIT. Veja `LICENSE` para mais informações.

## 🆘 Suporte

- **Issues**: https://github.com/rickchiod-hash/galFlowAI/issues
- **Docs**: [docs/VIDEO_SERVICE.md](docs/VIDEO_SERVICE.md)
- **Logs**: Verifique `projects/*/logs/` para diagnósticos

---

**Desenvolvido com ❤️ para criação local de conteúdo.**
