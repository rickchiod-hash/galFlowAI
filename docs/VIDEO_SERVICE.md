# VideoService - Documentação

## Visão Geral

O `VideoService` é o serviço responsável por orquestrar a geração de vídeos comerciais no GalFlowAI. Ele integra os adaptadores WanGP (vídeo real) e FFmpeg (fallback estático).

## Localização

- **Arquivo**: `app/services/video_service.py`
- **Testes**: `test_video_service.py`

## Funcionalidades

### 1. Geração de Cena Individual
```python
from app.services.video_service import VideoService

service = VideoService()
result = service.generate_scene_video(
    scene_id="scene_001",
    prompt="Um produto incrível em ação",
    output_path="output.mp4",
    negative_prompt="borrado, embaçado",
    duration_seconds=5
)
```

### 2. Geração de Comercial Completo
```python
result = service.generate_commercial(
    project_id="20260505_120000_meuproduto",
    product="Meu Produto Incrível",
    target_audience="Jovens adultos, entusiastas de tecnologia",
    duration_seconds=30,
    style="viral"
)
```

### 3. Verificação de Status
```python
status = service.get_status()
# Retorna:
# {
#     "available": True/False,
#     "wangp_available": True/False,
#     "ffmpeg_available": True/False,
#     "preferred_provider": "WanGP" ou "FFmpeg" ou "None"
# }
```

## Fluxo de Geração

1. **Roteiro**: Gera texto usando LLM local (via pipeline)
2. **Cenas**: Divide o roteiro em cenas usando `scene_splitter`
3. **Prompts**: Cria prompts de vídeo para cada cena usando `prompt_builder`
4. **Vídeos**: Gera vídeo para cada cena (WanGP ou FFmpeg fallback)
5. **Montagem**: Concatena todos os vídeos usando FFmpeg

## Fallback Automático

O serviço tenta usar WanGP primeiro. Se falhar ou não estiver disponível, usa FFmpeg automaticamente:

- **WanGP disponível**: Gera vídeos reais com IA
- **WanGP indisponível**: Gera vídeos estáticos com texto (FFmpeg)
- **Nenhum motor**: Retorna erro

## Hardware Aware

O WanGP adapter já configura automaticamente:
- **Modelo**: 1.3B (ideal para GTX 1660 Super 6GB)
- **Resolução**: 480p (seguro para 6GB VRAM)
- **Cenas**: Uma por vez (evita estouro de VRAM)

## Testes

```bash
cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe -m pytest test_video_service.py -v
```

**Cobertura**:
- Inicialização do serviço
- Geração de cena (WanGP e FFmpeg)
- Fallback automático
- Status do serviço

## Exemplo de Uso

Veja `example_video_generation.py` para um exemplo completo com progress callback.

## Dependências

- `app.adapters.wangp_adapter.WanGPAdapter`
- `app.adapters.ffmpeg_adapter.FFmpegAdapter`
- `app.pipeline.script_generator`
- `app.pipeline.scene_splitter`
- `app.pipeline.prompt_builder`

## Limitações Conhecidas

1. **WanGP real**: Precisa de PyTorch e WanGP instalados corretamente
2. **FFmpeg fallback**: Gera vídeos estáticos (sem animação real)
3. **LLM**: Precisa de pelo menos um provedor LLM configurado para roteiro

## Próximos Passos

- [ ] Integrar com UI Gradio
- [ ] Adicionar suporte a áudio/narração
- [ ] Implementar fila de jobs para múltiplos vídeos
- [ ] Adicionar métricas de progresso detalhadas
