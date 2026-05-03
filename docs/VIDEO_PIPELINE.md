# Pipeline de Geração de Vídeo - FlowForgeAI

## Visão Geral

O FlowForgeAI agora possui um pipeline completo de geração de vídeo comercial, integrando:
- **LLM Providers** para roteiro
- **WanGP 1.3B** para geração de vídeo (ou FFmpeg como fallback)
- **TTS** para narração
- **FFmpeg** para montagem final

## Fluxo Completo

```
Briefing → Roteiro (LLM) → Cenas → Prompts → Vídeo por Cena → Narração (TTS) → Montagem FFmpeg → MP4 Final
```

## Componentes

### 1. VideoGenerationPipeline (`app/pipeline/video_generation_pipeline.py`)

Pipeline principal que orquestra todo o processo:

```python
pipeline = VideoGenerationPipeline()
result = pipeline.generate_commercial(
    project_id="20260503_120000_CursoPython",
    product="Curso de Python",
    target_audience="Iniciantes",
    duration_seconds=30,
    style="viral"
)
```

**Passos executados:**
1. Gera roteiro (via LLM Provider)
2. Divide em cenas (`SceneSplitter`)
3. Gera prompts de vídeo (`PromptBuilder`)
4. Gera narração (TTS Adapter)
5. Gera vídeos das cenas (WanGP ou FFmpeg)
6. Monta vídeo final (FFmpeg)

### 2. WanGP Adapter (`app/adapters/wangp_adapter.py`)

Adapter para integrar WanGP/Wan2GP:

- **Status**: Detecta automaticamente se WanGP está instalado
- **Configuração**: Usa 1.3B + 480p para GTX 1660 Super (6GB VRAM)
- **Fallback**: Se falhar, usa FFmpeg para vídeo estático

```python
wangp = WanGPAdapter()
if wangp.is_available():
    result = wangp.generate_video(
        prompt="Um profissional programando...",
        output_path="scene_001.mp4"
    )
```

### 3. TTS Adapter (`app/adapters/tts_adapter.py`)

Gera narração com múltiplos motores:

| Motor | Prioridade | Requer Instalação? |
|-------|-----------|-------------------|
| Kokoro | 1 | Sim (pip install kokoro) |
| pyttsx3 | 2 | Sim (pip install pyttsx3) |
| Windows SAPI | 3 | Não (nativo) |
| Silence | 4 | Não (fallback) |

```python
tts = TTSAdapter()
result = tts.generate_audio(
    text="Aprenda Python em 30 dias...",
    output_path="narration.wav"
)
```

### 4. FastAPI Endpoints

#### POST /api/generate-video
Gera um comercial completo:

```bash
curl -X POST http://127.0.0.1:8000/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{
    "product": "Curso de Python",
    "target_audience": "Iniciantes",
    "duration_seconds": 30,
    "style": "viral"
  }'
```

#### GET /api/video-status/{project_id}
Consulta status do projeto:

```bash
curl http://127.0.0.1:8000/api/video-status/20260503_120000_CursoPython
```

#### GET /api/pipeline/status
Status de todos os componentes:

```bash
curl http://127.0.0.1:8000/api/pipeline/status
```

### 5. Gradio UI - Tab "Gerar Vídeo"

Nova aba na interface web (`http://127.0.0.1:7860`):

1. Preencha: Produto, Público-alvo, Duração, Estilo, Palavras-chave
2. Clique em "Gerar Comercial"
3. Acompanhe progresso em tempo real
4. Visualize o vídeo gerado

## Estrutura de Pastas do Projeto

```
projects/YYYYMMDD_HHMMSS_Nome/
├── brief/              # Dados do briefing
├── script/             # Roteiro aprovado
│   ├── script_approved.md
│   └── script_versions.json
├── storyboard/         # Cenas
│   └── scenes.json
├── prompts/            # Prompts para vídeo
│   └── prompts.json
├── renders/            # Vídeos das cenas
│   ├── scene_000.mp4
│   ├── scene_001.mp4
│   └── ...
├── audio/              # Narração
│   └── narration.wav
├── final/              # Vídeo final
│   └── commercial.mp4
└── logs/               # Logs da geração
```

## Hardware Target

Para **GTX 1660 Super (6GB VRAM)**:
- Modelo: **1.3B** (nunca 14B)
- Resolução: **480p** ou **512p**
- Cenas curtas: **5 segundos** cada
- Uma geração por vez

## Fallbacks Implementados

1. **LLM**: TemplateProvider sempre funciona
2. **Vídeo**: WanGP → FFmpeg (vídeo estático com texto)
3. **TTS**: Kokoro → pyttsx3 → Windows SAPI → Silence
4. **Montagem**: Sempre FFmpeg (obrigatório)

## Scripts Disponíveis

| Script | Função |
|--------|---------|
| `scripts\test_video_pipeline.bat` | Testa imports do pipeline |
| `scripts\start_fastapi.bat` | Inicia FastAPI |
| `scripts\start_app_debug.bat` | Inicia Gradio UI |

## Como Testar

### 1. Verificar Imports
```cmd
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
python -c "from app.pipeline.video_generation_pipeline import VideoGenerationPipeline; print('OK')"
```

### 2. Iniciar FastAPI
```cmd
scripts\start_fastapi.bat
```
Acesse: http://127.0.0.1:8000/docs

### 3. Iniciar Gradio UI
```cmd
scripts\start_app_debug.bat
```
Acesse: http://127.0.0.1:7860 → Tab "Gerar Vídeo"

### 4. Teste Completo via API
```bash
curl -X POST http://127.0.0.1:8000/api/generate-video \
  -H "Content-Type: application/json" \
  -d '{"product": "Teste", "target_audience": "Todos", "duration_seconds": 15}'
```

## Status Atual

| Componente | Status | Notas |
|-----------|--------|-------|
| LLM Providers | ✅ Completo | 6 providers + fallback |
| Script Service | ✅ Completo | Edição + versionamento |
| WanGP Adapter | ✅ Criado | Aguarda WanGP real |
| TTS Adapter | ✅ Criado | 4 motores + fallback |
| Video Pipeline | ✅ Criado | Integra tudo |
| FastAPI V2 | ✅ Atualizado | + endpoints vídeo |
| Gradio UI | ✅ Atualizado | + tab vídeo |
| Testes | ⚠️ Parcial | Aguarda Python |

## Próximos Passos

1. **Instalar/Configurar WanGP** em `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP`
2. **Testar pipeline completo** com WanGP real
3. **Integrar WebSocket** para progresso em tempo real
4. **Adicionar fila de jobs** (Redis/RQ ou SQLite)
5. **Criar React UI** (V3)

## Configuração WanGP

Quando WanGP estiver disponível:

1. Clone: `git clone https://github.com/yourusername/Wan2GP.git`
2. Instale deps: `pip install -r requirements.txt`
3. Baixe modelo 1.3B para `K:\AI_VIDEO_COMERCIAL_STUDIO\models\wan`
4. Teste: `python main.py --help`

O adapter já está configurado para:
- Detectar WanGP automaticamente
- Usar preset 1.3B + 480p (seguro para 6GB VRAM)
- Fazer fallback para FFmpeg se falhar

---

**Nota**: Todos os componentes foram criados seguindo as restrições:
- ✅ Nada no C: (excepto ambiente virtual)
- ✅ Fallback gracioso em todos os adapters
- ✅ Logs em português
- ✅ Sem APIs pagas
- ✅ Compatível com 6GB VRAM
