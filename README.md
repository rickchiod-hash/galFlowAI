# Gal AI — Estúdio Local para Comerciais Curtos com IA

## Sobre o Projeto
O **Gal AI** é uma plataforma local-first para criação automática de comerciais, propagandas e vídeos curtos para redes sociais, rodando em Windows no disco K:, sem dependências pagas ou serviços em nuvem.

## Requisitos
- Windows 10/11
- Disco K: com pelo menos 100 GB livres
- Python 3.10+ (ambiente `K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio`)
- Gradio (instalado no ambiente)
- FFmpeg (em `K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Library\bin\ffmpeg.exe`)
- WanGP/Wan2GP (opcional, em `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP`)
- GPU NVIDIA com 6 GB VRAM (GTX 1660 Super recomendada)

## Como Iniciar
1. Abra o terminal (PowerShell) no diretório:
   ```
   cd K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta
   ```

2. Execute o script de inicialização:
   ```
   scripts\start_app.bat
   ```
   Ou manualmente:
   ```
   $env:PIP_CACHE_DIR="K:\AI_VIDEO_COMERCIAL_STUDIO\cache\pip"
   $env:HF_HOME="K:\AI_VIDEO_COMERCIAL_STUDIO\cache\huggingface"
   $env:TORCH_HOME="K:\AI_VIDEO_COMERCIAL_STUDIO\cache\torch"
   $env:XDG_CACHE_HOME="K:\AI_VIDEO_COMERCIAL_STUDIO\cache"
   $env:TEMP="K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
   $env:TMP="K:\AI_VIDEO_COMERCIAL_STUDIO\temp"
   $env:OLLAMA_MODELS="K:\AI_VIDEO_COMERCIAL_STUDIO\models\ollama"
   $env:PYTHONPATH="K:\AI_VIDEO_COMERCIAL_STUDIO\opencodegalpasta"
   K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\python.exe -m app.main
   ```

3. Acesse no navegador:
   ```
   http://127.0.0.1:7860
   ```

## Fluxo de Uso (MVP)
1. **Briefing**: Descreva o comercial (ex: "Quero vender um boneco colecionável impresso em 3D...")
2. **Criar**: Clique em "Criar comercial automaticamente"
3. **Roteiro**: Revise o roteiro gerado (pode editar)
4. **Cenas**: A Gal AI divide em cenas com prompts
5. **Geração**: Storyboard FFmpeg criado automaticamente
6. **Montagem**: Vídeo final montado em 30 FPS
7. **Resultado**: Vídeo MP4 salvo em `projects/<ID>/final/`

## Estrutura do Projeto
```
opencodegalpasta/
  app/
    main.py              # Interface Gradio (Gal AI)
    config.py            # Caminhos K-only
    hardware.py          # Detecção GPU/RAM/disco
    logging_config.py    # Logs em português
    project_manager.py   # Criação de projetos
    safety.py            # Backup antes de sobrescrever
    adapters/
      ffmpeg_adapter.py   # Montagem FFmpeg
      wangp_adapter.py   # Integração WanGP (opcional)
      tts_adapter.py      # Narração offline
    pipelines/
      auto_pipeline.py    # Automação completa
      script_generator.py  # Geração de roteiro
      scene_splitter.py   # Divisão em cenas
      prompt_builder.py   # Criação de prompts
    jobs/
      queue.py            # Fila de jobs local
  scripts/
    start_app.bat         # Inicia a aplicação
    check_environment.bat  # Verifica ambiente
  static/
    gal_ai.css           # Tema escuro premium
  tests/
    test_project.py      # Testes de projeto
    test_hardware.py     # Testes de hardware
    test_pipeline.py     # Testes de pipeline
    run_all_tests.py     # Executa todos os testes
  docs/
    RELATORIO_ANALISE_AMBIENTE.md  # Relatório de auditoria
  projects/                 # Projetos criados (K:)
  logs/                     # Logs do sistema
```

## Regras Absolutas
- ✅ Nada é salvo no C: (apenas K:)
- ✅ Não usa RunPod ou APIs pagas
- ✅ Não quebra WanGP/FramePack existentes
- ✅ Modelo 1.3B como padrão (seguro para 6 GB VRAM)
- ✅ 14B bloqueado no modo seguro
- ✅ Fallback FFmpeg se WanGP falhar

## Status Atual (MVP)
- ✅ Interface Gal AI 100% em português brasileiro
- ✅ Criação automática de comercial
- ✅ Roteiro, cenas, prompts
- ✅ Storyboard FFmpeg funcionando
- ✅ Montagem de vídeo final
- ✅ Logs em português
- ✅ Job queue local implementada

## Próximos Passos
- 🔄 Integração WanGP real (1.3B)
- 🔄 Narração TTS (pyttsx3/Kokoro)
- 🔄 Testes automatizados
- 🔄 Melhoria de UX

---
**Gal AI** — Crie comerciais profissionais sem sair do seu PC.
