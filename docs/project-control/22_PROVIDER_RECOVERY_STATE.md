# 22_PROVIDER_RECOVERY_STATE — GalFlowAI

## Estado atual de recovery
- Data/hora: 2026-05-08 03:30:00 (aproximado)
- História atual: QA-1004 — Criar teste TTS falha → export sem áudio
- Status da história: Concluída ✅
- Modelo que falhou: Nemotron 3 Super Free (recuperado para Big Pickle na próxima sessão)
- Erro detectado: Free usage exceeded (superado após correção de asserts de teste)
- Tipo do erro:
  - [ ] transient_provider_error
  - [ ] timeout
  - [ ] rate_limit
  - [x] free_usage_exceeded, se o erro atual for Free usage exceeded
  - [ ] unknown
- Próximo modelo recomendado:
  - Se falhou Nemotron 3 Super Free: Big Pickle
  - Se falhou Big Pickle: MiniMax M2.5 Free
  - Se falhou MiniMax M2.5 Free: parar e pedir intervenção humana
- Arquivo em edição: tests/test_tts_fallback.py
- Arquivos modificados segundo git status: 
  GalFlowAI_Governance_Backlog_Checkpoint_Pack_v2/
  app/adapters/piper_adapter.py
  app/application/use_cases/generate_audio_use_case.py
  app/application/use_cases/manage_queue_use_case.py
  app/application/use_cases/render_video_use_case.py
  app/pipeline/checkpoint_manager.py
  app/pipeline/filesystem_helper.py
  app/pipeline/job_state.py
  app/pipeline/stages/
  app/pipeline/video_generation_pipeline.py.backup
  app/pipeline/voice_script_optimizer.py
  app/utils/
  opencode.jsonc.example
  temp_commit.patch
  tests/test_tts_fallback.py
  docs/project-control/00_STATUS_EXECUTIVO.md
  docs/project-control/05_BACKLOG_PRIORIZADO.md
  docs/project-control/06_HISTORIAS_REFINADAS.md
  docs/project-control/10_DAILY_LOG.md
- Comando/teste rodado mais recente: pytest tests/test_tts_fallback.py -v
- Resultado real do teste: 5/5 testes passando (ver detalhes abaixo)
- Último passo seguro: Testes corrigidos com base no comportamento real do pipeline (quando WanGP disponível, FFmpeg.create_static_video não é chamado para geração de cena)
- Próximo passo técnico recomendado: Arquivar estado de recovery e avançar para próxima história
- Pode continuar automaticamente?
  - [x] sim
  - [ ] não
- Precisa de intervenção humana?
  - [ ] sim
  - [x] não

## Observação técnica QA-1004
Registrar explicitamente:

No cenário "TTS indisponível com WanGP disponível":
- o pipeline deve continuar;
- WanGP.generate_video deve ser chamado;
- FFmpeg.create_static_video NÃO deve ser exigido;
- FFmpeg.concat_videos pode ser exigido para montagem final;
- narration_path pode ser None se nenhum arquivo de áudio foi gerado.

No cenário "TTS indisponível com WanGP indisponível":
- o pipeline deve continuar se FFmpeg estiver disponível;
- FFmpeg.create_static_video deve ser chamado;
- FFmpeg.concat_videos deve ser chamado;
- WanGP.generate_video não deve ser chamado.

No cenário "TTS disponível":
- o teste só deve exigir narration_path se o mock criar ou simular corretamente a existência do arquivo de áudio esperado pelo pipeline.
- Se o pipeline usa audio_path.exists(), o teste precisa simular/criar o arquivo ou ajustar a expectativa conforme comportamento real.

## Checklist antes de continuar em nova sessão
- [x] git status foi registrado
- [x] branch atual foi registrada
- [x] último commit foi registrado
- [x] arquivos alterados foram listados
- [x] QA-1004 concluída
- [x] teste falho foi registrado e corrigido
- [x] ponto técnico WanGP vs FFmpeg foi registrado
- [x] próximo modelo foi indicado
- [x] commit foi feito nesta etapa

## Evidências
- erro exibido: Free usage exceeded (do provider) - superado após correção de teste
- teste/comando executado: pytest tests/test_tts_fallback.py -v
- resultado final: 
  1. test_tts_adapter_files_exist: PASSED
  2. test_tts_has_silence_fallback: PASSED
  3. test_tts_unavailable_graceful_audio_fallback: PASSED
  4. test_tts_available_normal_operation: PASSED
  5. test_both_wangp_and_tts_unavailable: PASSED
- arquivos modificados: lista acima (inclui arquivos de teste e documentação de status)