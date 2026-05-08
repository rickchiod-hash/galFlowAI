# PROJECT_REFERENCE_CONTEXT — GalFlowAI

Status: **FONTE DE VERDADE DO PRODUTO**  
Última revisão: 2026-05-08  
Alteração permitida somente com ADR explícita.

## Identidade oficial

Nome oficial do produto: **GalFlowAI**  
Nome do repositório: **galFlowAI**  
Tagline: **Roteiro → Cenas → IA → Vídeo**

Nomes legados como `GalFlowAI`, `GalFlowAI`, `AI Video Comercial Studio` ou variações devem aparecer apenas em histórico, auditoria, compatibilidade ou migração. Qualquer novo arquivo, tela, endpoint, teste, commit, documentação ou prompt deve usar **GalFlowAI**.

## Escopo do produto

GalFlowAI é um estúdio **local-first** para criação de comerciais curtos com IA, focado em redes sociais, operação offline, controle por etapas, fallback robusto, validação humana, governança de artefatos e exportação final em MP4.

O produto correto não é uma tela monolítica de “Gerar Comercial”. O produto correto é uma linha de produção modular:

```text
Projeto/Briefing
→ Roteiro
→ Edição
→ Aprovação
→ Cenas
→ SceneContracts
→ Visual Bible
→ Ingredient Registry / Asset Manager
→ Prompt Context Pack
→ Prompts por cena
→ Narração/TTS
→ SFX/Música
→ RenderPlan
→ Render por cena
→ Fallback FFmpeg
→ Legendas/SRT
→ MP4 final
→ Logs
→ Métricas
→ Diagnóstico
```

## Regra de ouro

**Nenhuma etapa pesada deve executar antes da etapa anterior estar validada.**

Consequências:

- Não renderizar vídeo antes de aprovar roteiro.
- Não gerar prompt final antes de existir SceneContract.
- Não indexar memória vetorial antes de artefato aprovado/canônico.
- Não executar engine pesada sem RenderPlan e GPU Budget.
- Não bloquear entrega de MP4 por falha de TTS, SFX, vector store ou engine opcional.

## Fallbacks invioláveis

- `TemplateProvider` como fallback obrigatório de roteiro.
- `FFmpeg` como fallback universal de vídeo, montagem e exportação.
- Fallback de TTS para `silence` ou vídeo sem áudio.
- Render local-first mesmo sem cloud/API paga.
- Logs com padrão `CAUSA | CORREÇÃO`.
- Rastreabilidade por `project_id`, `job_id`, `story_id` e `artifact_id`.

## Providers obrigatórios a preservar

### Roteiro / LLM

- Template local.
- LM Studio.
- GPT4All.
- KoboldCpp.
- llama.cpp.
- GPT-compatible endpoint.
- Ollama opcional, se existir.

### Vídeo

- FFmpeg obrigatório.
- WanGP/Wan2GP 1.3B opcional como engine local.
- Wan VACE 1.3B futuro e opcional para referência, máscara e keyframe.
- RemoteRenderProvider futuro e opcional para cenas aprovadas.

### Áudio

- pyttsx3 fallback.
- Kokoro opcional.
- Piper pt-BR futuro.
- Chatterbox/XTTS/Fish/F5 apenas laboratório opcional.
- Silence fallback obrigatório.

## Itens que não podem ser removidos silenciosamente

- Roteiro editável.
- Aprovação de roteiro antes das cenas.
- Versionamento de roteiro.
- Logs.
- Métricas.
- Diagnóstico copiável.
- Providers locais.
- TemplateProvider.
- FFmpeg fallback.
- Estado de job.
- Visual Bible.
- Ingredient Registry.
- SceneContracts.
- Prompt Context Pack.
- Asset Manager.
- TTS fallback.
- SRT/legendas planejadas.
- Roadmap e backlog sincronizados.

## Política de remoção

Qualquer remoção de feature, provider, fallback, tela, etapa ou teste exige:

1. ADR.
2. Atualização da Feature Preservation Matrix.
3. Testes de regressão ajustados.
4. Justificativa técnica e impacto.
5. Plano de rollback.
6. Atualização do Status Executivo.

## Filosofia de evolução

- Estabilizar antes de expandir.
- Documentar antes de refatorar.
- Testar antes de afirmar.
- Preservar antes de substituir.
- Feature nova nunca pode remover fallback validado.
- Integração pesada deve ser opcional e protegida por feature flag.
