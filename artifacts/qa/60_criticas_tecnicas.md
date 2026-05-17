# 60 Críticas Técnicas — GalFlowAI

> 20 Arquitetura/estrutura + 20 Qualidade de código + 20 UX/desempenho
> Gerado em: 2026-05-17

---

## Bloco A — Arquitetura e Estrutura (20)

### A1. Pipeline não usa JobState
`VideoGenerationPipeline.generate_commercial()` retorna dicts avulsos. `JobState` existe como máquina de estados formal com transições guardadas, mas o pipeline nunca cria ou atualiza um `JobState`. Isso impede rastreabilidade de jobs e integração com `JobLedger`.

### A2. Gatilhos de idempotência existem mas não são chamados
`CheckIdempotencyUseCase` e `RegisterIdempotencyUseCase` estão implementados mas não são invocados em nenhum ponto do pipeline principal. Cada execução de `generate_commercial()` roda do zero mesmo com briefing idêntico.

### A3. Ledger SQLite não integrado ao pipeline
`SQLiteJobLedger` existe com suporte WAL, transações ACID e thread-safety, mas o pipeline não persiste estados intermediários. Se o processo morre na etapa 5, não há como retomar da etapa 4.

### A4. Ausência de checkpoint/retry por etapa
Cada etapa do pipeline executa de forma atômica sem checkpoint. Uma falha no `RenderAllScenesUseCase` faz todo o pipeline falhar, sem possibilidade de retry parcial. Cenas já renderizadas são perdidas.

### A5. Duas UIs concorrentes sem sincronização
`main.py` (Gradio Blocks) e `app/ui/gradio_app.py` (Gradio com tabs) coexistem com lógica de projeto duplicada. Mudanças em uma não refletem na outra. Ex: `main.py` tem aprovação inline, `gradio_app.py` tem stage groups.

### A6. Injeção de dependência manual e rígida
`VideoGenerationPipeline.__init__()` instancia 6 use cases + 3 adapters diretamente. Não há DI container ou factory. Testar com mocks exige monkey-patch de atributos de instância.

### A7. ProviderRouter sem fallback unificado
`ProviderRouter` escolhe provider por mode string, mas o fallback entre providers é feito ad-hoc em cada caller. `script_service.py` tem sua própria lógica de fallback, e `gradio_app.py` trata fallback de forma diferente.

### A8. StageLogger subutilizado
`StageLogger` existe com eventos estruturados mas só é usado no `VideoGenerationPipeline` e `WanGPAdapter`. Use cases individuais (`SplitScenesUseCase`, `BuildPromptsUseCase`) não logam eventos de stage.

### A9. Ausência de timeouts explícitos
Chamadas a LLM providers, WanGP e FFmpeg não têm timeout explícito. Uma chamada bloqueante pode travar o pipeline indefinidamente, especialmente com modelos locais lentos.

### A10. Repositórios sem interface formal
`ScriptRepository`, `SceneRepository`, `PromptRepository` são classes concretas sem ABC/Protocol. Não há como trocar implementação (ex: S3 vs local) sem modificar os callers.

### A11. ErrorCatalogService subutilizado
O catálogo de erros com `ErrorCode`, sugestões e diagnóstico está implementado, mas a UI e o CLI nunca chamam `build_user_message()` ou `build_diagnostic_message()`. Erros são exibidos crus.

### A12. SceneContractService sem validação de domínio
`SceneContractService` aceita qualquer `SceneContract` sem validar consistência entre `prompt_positive`, `duration` e `scene_number`. Contratos inconsistentes passam pela validação.

### A13. MemoryQualityGate isolado
`MemoryQualityGate` (VEC-801) valida ingredientes e BibleEntry para vector store, mas não é chamado por nenhum use case ou pipeline. A validação de qualidade de memória não ocorre em runtime.

### A14. Cache de artefato só no script
`CheckArtifactCacheUseCase`/`StoreArtifactUseCase` só funcionam para geração de roteiro. Cenas, prompts, áudio e vídeo não têm cache de artefato. Cada execução regenera tudo.

### A15. Módulo `app/domain/` com responsabilidades mistas
`scene_contract.py` contém schema (dataclass/Pydantic) + serviço (CRUD) + regras de negócio. Não há separação entre modelo, repositório e serviço de domínio.

### A16. Expansão de provedores exige boilerplate
Adicionar um novo adaptador WanGP/VAce exige implementar ~200 linhas com `_build_command()`, `_check_availability()`, `get_metrics()`, `get_stage_events()`. Sem template ou abstract method para guiar.

### A17. `app/pipeline/__init__.py` vazio
`__init__.py` do pacote pipeline está vazio. Não exporta `VideoGenerationPipeline`, `JobState`, `JobLedger`, `StageGate`. Importar exige caminho completo do módulo.

### A18. Sem observabilidade de latência por etapa
`JobMetrics` coleta duração por stage, mas o pipeline nunca chama `add_stage_event()`. Não há como medir quanto tempo cada etapa leva em produção.

### A19. Gradio `demo.queue()` e `concurrency_count` não configurados
Chamadas longas (render, concat) podem bloquear a UI. `demo.queue(max_size=5)` existe mas sem configuração explícita de `concurrency_count` para múltiplos jobs simultâneos.

### A20. Sem health check unificado
`get_pipeline_status()` em `VideoGenerationPipeline` e `_check_system()` em `ObservabilityUseCases` duplicam lógica de verificação de disponibilidade. Não há um endpoint `/health` que agregue ambos.

---

## Bloco B — Qualidade de Código (20)

### B1. Try/except genérico no pipeline
`generate_commercial()` tem `except Exception as e:` que captura tudo e retorna `{"success": False, "error": str(e)}`. Erros de programação (NameError, TypeError) são silenciados como "falha no pipeline".

### B2. Logs com f-strings em logger
`logger.error(f"Erro no pipeline: {e}")` em vez de `logger.error("Erro no pipeline: %s", e)`. f-strings são avaliadas mesmo quando o nível de log está desligado.

### B3. Módulos com importações pesadas no topo
`app/main.py` importa `pipelines.auto_pipeline` e `app.services.script_service` diretamente. Isso torna o módulo lento para carregar e difícil de testar isoladamente.

### B4. Paths como strings em vez de Path objects
`scene_parser.py:48`: `"prompt_negative": "blurry, low quality, distorted, bad anatomy"`. Constantes de qualidade negativa estão hardcoded em 4 lugares diferentes (prompt_builder_service, scene_parser, prompt_compiler, visual_consistency_use_cases).

### B5. Variáveis mutáveis como default
`generate_commercial()` aceita `keywords: Optional[List[str]] = None`, o que é correto, mas `BuildPromptsUseCase` aceita `scenes: List[Dict]` sem Optional — cenário de lista vazia não é tratado.

### B6. Duplicação de validação de briefing
`main.py:25-27`: valida briefing vazio. `gradio_app.py`: mesma validação em local diferente. `stage_gate.py`: `BriefingNotEmptyGate` repete o mesmo padrão em um terceiro local. Três implementações para a mesma regra.

### B7. Importação circular potencial
`error_jsonl_writer.py` e `app/adapters/wangp_adapter.py` usam lazy import para evitar circular, mas a necessidade de lazy import indica que o acoplamento está alto.

### B8. Retorno inconsistente de use cases
`GenerateScriptUseCase` retorna `Result` (subclasse de dict). `SplitScenesUseCase` retorna `Result`. `RenderAllScenesUseCase` retorna `Dict[str, Any]`. Inconsistência na camada de aplicação.

### B9. Nomes de métodos em português e inglês misturados
`generate_commercial()`, `_report_progress()`, `get_pipeline_status()` ao lado de `on_save()`, `_improve_wrapper()`. Dentro do mesmo arquivo, estilos misturados.

### B10. Comentários TODO sem tracker
Há TODOs como `# TODO(GAL-933, type=completed): Pipeline delega...` (já concluído) e `# TODO(GAL-934, type=debt): Adicionar testes...` (débito real). TODOs concluídos deveriam ser removidos.

### B11. `except Exception: pass` em vários lugares
`app/main.py` tem `except Exception: return []` no carregamento de versões. `script_service.py` tem blocos silenciosos. Erros são engolidos sem log.

### B12. Constantes mágicas em lógicas de negócio
`max_tokens=800` em `gpt4all_provider.py` e `max_tokens=400` anterior (já corrigido) mostram que parâmetros de LLM estão hardcoded em vez de configurados via `app.config`.

### B13. Testes com timeout ausente para I/O real
`test_pipeline_completa.py` e `test_wangp_hardening.py` não têm timeout configurado. Se um mock falha e chama I/O real, o teste pode travar.

### B14. Mocks insuficientes em testes de pipeline
`test_pipeline_structured_errors.py` usa `patch` em targets de string, mas alguns mocks têm `return_value` incompleto (falta `scene_prompts`, `rendered_scenes`), fazendo testes passarem com cobertura baixa.

### B15. Erro JSONL writer com duplicação de método
`error_jsonl_writer.py` parece ter `read_recent` sobrescrevendo `write` — indicando bug de cópia ou método mal nomeado.

### B16. Sem type hints em funções internas
`main.py` define `_improve_wrapper`, `_complement_wrapper` etc. sem type hints para parâmetros ou retorno. Funções aninhadas perdem rastreabilidade.

### B17. Testes com `tmp_path` sem cleanup explícito
Alguns testes criam arquivos em `tmp_path` que persistem além do escopo do teste. O cleanup do pytest é confiável, mas testes podem interferir entre si se reutilizam o mesmo `tmp_path`.

### B18. Sem fixture de escopo para PROJECTS_DIR
Testes que dependem de `PROJECTS_DIR` usam `mock.patch` repetido em cada teste. Falta uma fixture de autouse que configure `PROJECTS_DIR` como temp dir automaticamente.

### B19. Cobertura baixa em módulos de adaptador
`wangp_adapter.py` e `vace_adapter.py` têm testes, mas as branches de `_check_availability()` (Path + import) não são cobertas. Cobertura real < 60% nos módulos de adaptador.

### B20. Sem validação de schema Pydantic em runtime
`SceneContract` usa Pydantic mas `scene_contract_service.py` faz validação manual (description não vazia) em vez de confiar no Pydantic validator.

---

## Bloco C — UX e Desempenho (20)

### C1. Pipeline sem barra de progresso granular
A barra de progresso só tem 5 pontos discretos (10%, 20%, 30%, 50%, 85%). Sub-etapas como "render cena 3/10" não são reportadas. Usuário vê 50% por minutos sem saber o que acontece.

### C2. Sem notificação de conclusão
Quando o pipeline termina (sucesso ou falha), não há notificação visual ou sonora. Usuário precisa ficar olhando a tela.

### C3. Cancelamento de job não implementado
`JobState.cancel()` existe, mas não há botão "Cancelar" na UI e o pipeline não verifica `cancel_requested` entre etapas. Uma vez iniciado, o pipeline roda até o fim.

### C4. Sem cache de modelo local
Modelos GPT4All e WanGP são carregados do zero a cada execução. Não há warm cache ou persistência de modelo em memória entre chamadas.

### C5. FFmpeg concat sem validação prévia
`ConcatVideosUseCase` tenta concatenar sem verificar codecs, resolução ou frame rate dos vídeos de entrada. Se uma cena tem codec diferente, o concat falha com erro obscuro.

### C6. WanGP sem fallback por timeout
`WanGPAdapter.render_scene()` não tem timeout. Se o processo WanGP trava (ex: GPU out-of-memory), o pipeline trava junto. Não há mecanismo de kill por tempo.

### C7. Mensagens de erro em português e inglês misturadas
Pipeline retorna erros como "Roteiro não aprovado" (PT) mas gates retornam "Briefing is empty" (EN). Usuário final vê mensagens em dois idiomas.

### C8. Sem pré-visualização de prompt por cena
A UI mostra o roteiro editável, mas não mostra os prompts individuais que serão usados para cada cena. Usuário não sabe qual imagem/vídeo será gerado.

### C9. Dashboard de projetos sem métricas de qualidade
A aba "Dashboard de Projetos" mostra apenas existência de pastas e status binário. Não exibe: score dos prompts, tempo de render, taxa de fallback, warnings.

### C10. Sem light/dark mode
Gradio UI não tem seletor de tema. Em ambientes com pouca luz (estúdio), o tema claro padrão pode incomodar.

### C11. Formulário de briefing não salva rascunho
Se o usuário fecha o navegador, o briefing é perdido. Não há autosave em `gr.Textbox` ou localStorage.

### C12. Sem lazy loading de logs
A aba de logs carrega ~200 entradas a cada 2 segundos via timer. Em projetos longos, isso gera tráfego desnecessário e pisca a tabela.

### C13. Export path unificado mas sem feedback
O export salva em `projects/{id}/export/`, mas a UI não informa onde o arquivo foi salvo. Usuário precisa navegar manualmente.

### C14. Sem health check visual
Não há indicador visual de "FFmpeg disponível ✅" ou "WanGP offline ❌". Usuário só descobre que WanGP está offline quando o pipeline falha na etapa 5.

### C15. Tempo de carregamento inicial alto
`main.py` importa `pipelines.auto_pipeline` e vários módulos pesados no topo. O carregamento inicial leva ~3-5s antes de mostrar qualquer UI.

### C16. Sem progresso por cena no render
Render de 10 cenas com WanGP pode levar 5+ minutos. A barra mostra 50% durante todo o processo. Cada cena concluída deveria avançar ~5%.

### C17. Gradio Blocks sem `.queue()` para fila de jobs
A UI principal (`main.py`) não chama `demo.queue()`. Se dois usuários (ou duas abas) clicam "Gerar" simultaneamente, as execuções competem sem fila.

### C18. Sem validação de duração vs cenas
Pipeline aceita `duration_seconds=60` mesmo quando tem apenas 2 cenas (30s cada). A duração não é validada contra número de cenas ou conteúdo do script.

### C19. Sem fallback de TTS na UI principal
O pipeline (video_generation_pipeline.py) trata TTS como opcional. A UI principal (`main.py`) não mostra se o áudio foi gerado ou é silêncio.

### C20. CLI sem feedback de progresso
O pipeline via CLI (se chamado diretamente) não tem barra de progresso ou output intermediário. O usuário vê uma pausa silenciosa até o resultado final.

---

## Resumo

| Bloco | Críticas | Severidade média |
|-------|----------|-----------------|
| A — Arquitetura | 20 | Alta |
| B — Qualidade | 20 | Média |
| C — UX/Performance | 20 | Média |
| **Total** | **60** | — |
