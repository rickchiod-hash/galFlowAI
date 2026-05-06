# BACKLOG TÉCNICO (Code Review) — Gal AI / galFlowAI

**Última atualização:** 03/05/2026  
**Objetivo:** Evoluir a base atual sem quebrar o fluxo local-first existente (Gradio + FastAPI + fallback Template/FFmpeg).

---

## Resumo executivo (sem viés)

### Pontos fortes atuais
- Arquitetura já separa UI/API de serviços e adapters, o que facilita evolução incremental.
- Fallbacks centrais (TemplateProvider e FFmpeg) preservam continuidade operacional.
- Existe documentação base para operação local e setup de providers.

### Pontos críticos atuais
- Backlog anterior estava desatualizado e continha diagnósticos incorretos (ex.: sintaxe de `app/api.py` já está válida).
- Há risco de divergência entre comportamento real e documentação em endpoints/fluxos.
- Ausência de suíte de testes de contrato para API e de testes de regressão para fluxo fim-a-fim.

---

## Critérios para aceitar melhorias
1. **Não quebrar fluxo vigente** (gerar roteiro → editar/aprovar → cenas → preview → MP4).
2. **Melhorar observabilidade** (logs, erro claro, rastreabilidade por `project_id`/`job_id`).
3. **Aumentar robustez** sem impor dependências cloud ou lock-in externo.
4. **Permitir rollback fácil** (mudanças pequenas, feature flags quando aplicável).

---

## Backlog priorizado (crítico e coerente)

## P0 — Confiabilidade e risco imediato

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P0-01 | Documentação e estado do código divergentes geram retrabalho | Criar checklist de release técnico (README/docs/endpoints/scripts) antes de merge | Evita drift entre docs e código | Exige disciplina por PR | **Sim (alto impacto, baixo custo)** |
| P0-02 | API sem testes de contrato tende a quebrar silenciosamente | Adicionar testes de contrato FastAPI para rotas críticas (`/api/health`, `/api/llm/*`, `/api/projects/*/script/*`) | Reduz regressão em endpoint | Setup inicial de fixtures | **Sim** |
| P0-03 | Falhas de provider podem degradar UX sem diagnóstico claro | Padronizar envelope de erro (`code`, `message`, `details`, `retryable`) e mapear exceptions por adapter | Debug mais rápido, UX previsível | Refatoração moderada nas rotas | **Sim** |

## P1 — Robustez de arquitetura sem ruptura

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P1-01 | Regras de negócio podem se espalhar entre API/UI | Consolidar casos de uso em camada `application` (use-cases) mantendo adapters em `infrastructure` | Reduz acoplamento e facilita testes | Refatoração gradual, demanda convenção | **Sim, incremental** |
| P1-02 | Pipeline de vídeo pode bloquear requisição síncrona | Introduzir executor assíncrono local com fila leve (`sqlite` + worker já existente em Go/Python) | Melhor responsividade e retomada | Mais componentes operacionais | **Sim, faseado** |
| P1-03 | Configuração local extensa e sujeita a erro | Adotar validação central de config (`pydantic-settings`) com mensagem de erro acionável | Menos erro de ambiente | Migração de config existente | **Sim** |
| P1-04 | Falta de idempotência em ações de roteiro pode duplicar estado | Definir idempotency key por operação de escrita em script/versionamento | Evita versões fantasmas | Requer armazenamento de chave/estado | **Sim, para estabilidade** |

## P2 — Eficiência e qualidade de código

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P2-01 | Providers diferentes podem repetir lógica de timeout/retry | Criar utilitário comum de execução (`retry`, `timeout`, `circuit breaker` simples local) | Menos duplicação, comportamento homogêneo | Ajuste em todos adapters | **Sim** |
| P2-02 | Logs atuais dificultam correlação ponta-a-ponta | Estruturar logs JSON com `project_id`, `provider`, `latency_ms`, `fallback_used` | Observabilidade real | Requer adaptação de leitura manual | **Sim** |
| P2-03 | Sem métricas mínimas, tuning fica subjetivo | Instrumentar métricas locais (tempo de geração, taxa fallback, erro por provider) | Decisão baseada em dado | Pequeno overhead | **Sim** |
| P2-04 | Testes lentos/instáveis por dependência de LLM local | Criar modo de teste com fakes determinísticos para providers | CI estável e rápida | Necessário manter fakes | **Sim** |

## P3 — Modernização arquitetural (sem “big bang”)

| ID | Contexto da melhoria | Sugestão objetiva | Prós | Contras / custo | Vale a pena agora? |
|---|---|---|---|---|---|
| P3-01 | Evolução de frontend pode exigir API mais formal | Versionar API (`/api/v1`) e publicar schema OpenAPI versionado | Permite evolução sem quebrar clientes | Trabalho de governança | **Sim, antes da UI nova** |
| P3-02 | Operações longas sem estado formal de job | Padronizar máquina de estados (`queued/running/succeeded/failed/canceled`) | Controle operacional e UX melhor | Implementação moderada | **Sim** |
| P3-03 | Crescimento de features sem limites claros | Definir ADRs curtas (Architecture Decision Records) para decisões críticas | Histórico técnico rastreável | Custo de documentação contínua | **Sim** |

---

## Plano de execução recomendado (sem quebrar fluxo)

### Sprint A (1–2 semanas)
- P0-01, P0-02, P0-03
- P1-03
- P2-02

### Sprint B (2 semanas)
- P1-01 (apenas casos de uso de roteiro)
- P2-01, P2-04
- P3-02 (estado de job mínimo)

### Sprint C (2+ semanas)
- P1-02 (fila local faseada)
- P2-03
- P3-01, P3-03

---

## Itens congelados (não fazer agora)
- Reescrita completa da UI em React sem estabilizar contratos da API.
- Dependência obrigatória de cloud/API paga.
- Troca massiva de stack sem baseline de performance/confiabilidade.

---

## Checklist de revisão por PR
- [ ] Mudança preserva fallback Template + FFmpeg.
- [ ] Existe teste automatizado para rota/caso alterado.
- [ ] Logs incluem contexto mínimo (`project_id`/`provider`).
- [ ] Documentação atualizada no mesmo PR.
- [ ] Sem promessa de funcionalidade não implementada.

---

## Refinamento de histórias (correções pontuais com economia de tokens)

> Objetivo: executar correções pequenas, verificáveis e com baixa ambiguidade.

### H1 — Padronizar identidade e metadados da API
**Contexto:** ainda havia strings legadas no `app/api.py` (nome antigo do produto).  
**Implementação sugerida:** manter docstring, título da API e payload de health coerentes com Gal AI.

**Critérios de aceite (rígidos):**
- [ ] `app/api.py` compila com `python -m py_compile app/api.py`.
- [ ] `FastAPI(title=...)` usa nome atual do projeto.
- [ ] `GET /api/health` retorna `app` coerente com branding atual.

**Prompt enxuto (engenharia de prompt):**
```text
Corrija somente metadados de identidade em app/api.py sem alterar contratos de endpoint.
Restrições: não criar novos endpoints, não alterar schemas de request/response.
Entrega: patch mínimo + validação por py_compile.
```

### H2 — Endurecer tratamento de exceção sem mudar comportamento funcional
**Contexto:** havia `except:` genérico em leitura de status de projeto.  
**Implementação sugerida:** trocar por `except Exception` mantendo fallback atual.

**Critérios de aceite (rígidos):**
- [ ] Não existir `except:` nu em `app/api.py`.
- [ ] Endpoint `/api/video-status/{project_id}` continua retornando status mesmo quando `prompts.json` estiver malformado.
- [ ] `python -m py_compile app/api.py` permanece OK.

**Prompt enxuto (engenharia de prompt):**
```text
Refatore apenas blocos `except:` nus em app/api.py para `except Exception`.
Não mude regras de negócio, payload ou fluxo de fallback.
Valide compilação no final.
```

### H3 — Execução local previsível do módulo API
**Contexto:** execução `__main__` deve ser explícita e estável para ambiente local.  
**Implementação sugerida:** manter host local e explicitar parâmetros de `uvicorn.run` sem mudar porta/API.

**Critérios de aceite (rígidos):**
- [ ] Bloco `if __name__ == "__main__":` inicia API em `host=127.0.0.1` e `port=8000`.
- [ ] Não importar variáveis não usadas de `config.py`.
- [ ] Compilação sintática sem erro.

**Prompt enxuto (engenharia de prompt):**
```text
Ajuste somente o bloco __main__ de app/api.py para inicialização local determinística.
Não alterar rotas, modelos Pydantic ou middlewares.
```


## QA obrigatório (referência cruzada)
- Plano oficial de QA e mapeamento de pendências: `qa/QA_TEST_PLAN.md`.
- Regra: após cada história P0/P1 concluída, criar/ajustar ao menos 3 testes unitários cobrindo sucesso, falha e fallback.
- Regra: incluir cenários de automação/API e simulação de condições reais para capturar gaps antes de release.

---

## GAPs faltantes (análise profunda adicional)

### Gaps técnicos não cobertos ainda
1. **Ausência de contratos tipados de erro** entre API e serviços (risco de payload inconsistente).
2. **Acoplamento forte de IO com regra de negócio** em serviços/pipeline (dificulta testes e rollback).
3. **Sem testes de concorrência/reentrância** para versionamento de roteiro (risco de corrida em gravação).
4. **Sem política central de timeout/retry/backoff** para adapters (comportamento heterogêneo).
5. **Sem métricas operacionais mínimas** (latência por provider, taxa de fallback, taxa de erro por etapa).
6. **Sem validação de contrato de arquivos do projeto** (`script`, `prompts`, `storyboard`, `final`) antes/apos cada etapa.
7. **Sem testes de compatibilidade de backward endpoints** para preservar clientes locais existentes.

### Gaps de engenharia de qualidade
1. **Sem cobertura de cenários negativos realistas** (JSON corrompido, diretório ausente, permissão negada, timeout).
2. **Sem testes de smoke do fluxo completo local-first** (com mocks determinísticos).
3. **Sem baseline de cobertura por módulo crítico** com gate de falha.

### Decisão
- Estes ajustes **não serão executados agora**; entram na fila de backlog para execução incremental guiada por `qa/QA_TEST_PLAN.md`.

### P0-LOG-01 — Central de Logs na UI
Descrição:
Criar aba/painel visual com INFO, WARN e ERROR, filtros, busca, últimas linhas e diagnóstico copiável.

Critério de aceite:
- Gradio mostra Central de Logs;
- DEBUG não aparece;
- filtros funcionam;
- busca funciona;
- últimas linhas aparecem;
- diagnóstico copiável existe.

### P0-LOG-02 — LogService central
Descrição:
Criar serviço único para leitura, resumo e formatação de logs.

Critério de aceite:
- UI e FastAPI usam o mesmo serviço;
- leitura limitada a N linhas;
- erro de log não quebra app.

### P1-LOG-03 — Endpoints FastAPI para logs
Descrição:
Expor logs via API local.

Critério de aceite:
- /api/logs/recent;
- /api/logs/summary;
- /api/logs/last-error;
- testes de contrato.

### P2-LOG-04 — WebSocket de logs
Descrição:
Streaming opcional de logs via FastAPI WebSocket.

Critério de aceite:
- não obrigatório;
- testado;
- fallback por polling continua funcionando.

### P2-LOG-05 — Logs estruturados JSON futuramente
Descrição:
Planejar logs JSON com project_id, provider, latency_ms, fallback_used.

Critério de aceite:
- documentado;
- não quebrar leitura atual.

## Backlog — Motor de Roteiro V2

Criar os cards abaixo.

-------------------------------------------------------------------------------

### P1-SCRIPT-01 — Criar Prompt Base de Roteiro do Gal AI

Contexto:
Hoje os providers podem gerar roteiro sem um contrato suficiente forte. O modelo precisa receber um prompt base padronizado com regras fixas do Gal AI.

Objetivo:
Criar um Prompt Base reutilizável para todos os providers de roteiro.

O prompt base deve orientar o modelo a gerar:
- roteiro para comerciais curtos;
- linguagem em português brasileiro;
- estrutura para Reels, TikTok, Shorts e anúncios verticais;
- gancho nos primeiros 1 a 3 segundos;
- proposta clara;
- benefício;
- prova visual;
- CTA;
- narração;
- texto na tela;
- cenas;
- prompts visuais em português brasileiro;
- negative prompts em português brasileiro;
- JSON estruturado;
- Markdown legível.

Critério de aceite:
- criar template futuro em app/templates/script_prompt_base.py ou equivalente;
- todos os providers devem usar esse prompt base no futuro;
- TemplateProvider também deve seguir a mesma estrutura;
- documentar em docs/PROMPT_ROTEIRO_V2.md;
- não implementar agora se houver tarefa atual em andamento.

-------------------------------------------------------------------------------

### P1-SCRIPT-02 — Separar Prompt Base, Briefing e Instruções de Saída

Contexto:
Não devemos "aquecer" a IA com uma chamada anterior e esperar que ela lembre. A maioria dos providers funcionam de forma stateless. O contexto importante precisa ir junto com o briefing em cada chamada.

Objetivo:
Separar o prompt em três partes:

1. Prompt Base:
Regras fixas do Gal AI.

2. Prompt do Briefing:
Dados específicos do usuário.

3. Contrato de Saída:
Formato obrigatório em JSON + Markdown.

Critério de aceite:
- criar estrutura documentada:
  - system_prompt;
  - user_prompt;
  - output_contract;
- garantir que a chamada final envie tudo junto;
- evitar dependência de memória entre chamadas;
- todas as instruções e respostas devem ser em português brasileiro;
- documentar por que não usar chamada prévia de aquecimento como requisito.

-------------------------------------------------------------------------------

### P1-SCRIPT-03 — Criar Quality Gate para Roteiros Genéricos

Contexto:
Roteiros genéricos prejudicam o produto. O sistema precisa rejeitar automaticamente roteiros fracos.

Objetivo:
Criar uma validação futura chamada validate_script_quality() mais rigorosa.

Deve bloquear:
- "Apresentamos";
- "Solução completa para suas necessidades";
- "Adquira agora";
- "Pessoas que têm interesse";
- ausência de gancho;
- ausência de CTA;
- ausência de cenas;
- ausência de narração;
- ausência de texto na tela;
- ausência de prompt visual;
- ausência de negative prompt;
- texto institucional frio;
- cenas sem ação visual.

Critério de aceite:
- se falhar, gerar nova versão com prompt mais forte;
- registrar log WARN:
  "Roteiro genérico detectado. Gerando versão melhorada.";
- nunca deixar roteiro genérico passar direto para cenas.

-------------------------------------------------------------------------------

### P1-SCRIPT-04 — Criar Estruturas de Roteiro por Tipo de Comercial

Contexto:
Produto físico, serviço local, UGC, oferta e fantasia/cosplay não devem usar a mesma estrutura.

Objetivo:
Criar templates estratégicos por tipo.

Tipos mínimos:
- Produto físico;
- Serviço local;
- Produto geek ou colecionável;
- Impressão 3D;
- Fantasia/cosplay;
- UGC natural;
- Depoimento;
- Oferta relâmpago;
- Bastidores/artesanal;
- Lançamento;
- Antes e depois;
- Demonstração de produto;
- Prova social;
- Luxo/premium;
- Direto para venda.

Critério de aceite:
- cada tipo tem estrutura própria;
- cada estrutura tem gancho, desenvolvimento e CTA;
- TemplateProvider consegue usar essas estruturas;
- providers externos recebem o tipo como variável;
- tudo em português brasileiro.

-------------------------------------------------------------------------------

### P1-SCRIPT-05 — Criar Biblioteca de Ganchos

Contexto:
O começo do vídeo decide retenção. O roteiro precisa começar com uma frase visual ou emocional forte.

Objetivo:
Criar uma biblioteca de ganchos por intenção.

Categorias:
- curiosidade;
- dor;
- desejo;
- surpresa;
- comparação;
- transformação;
- prova visual;
- exclusividade;
- urgência leve;
- bastidor;
- antes/depois;
- pergunta direta;
- desafio;
- objeto incomum.

Exemplos:
- "Isso aqui não veio de loja."
- "Você não percebe o detalhe até a luz bater."
- "Olhe o que uma impressora 3D consegue fazer."
- "Esse detalhe muda tudo."
- "Parece peça de coleção, mas foi feito sob demanda."
- "Se você curte peças únicas, presta atenção nisso."

Critério de aceite:
- ganchos devem ser naturais;
- evitar clickbait vazio;
- evitar frases institucionais;
- escolher gancho com base no briefing, estilo e tipo de comercial;
- tudo em português brasileiro.

-------------------------------------------------------------------------------

### P1-SCRIPT-06 — Criar Geração de Cenas por Duração

Contexto:
O roteiro precisa respeitar duração e ritmo de rede social.

Objetivo:
Padronizar quantidade de cenas por duração.

Regra:
- 15 segundos: 4 cenas;
- 20 segundos: 5 cenas;
- 30 segundos: 6 cenas;
- 45 segundos: 8 cenas;
- 60 segundos: 10 cenas.

Cada cena deve conter:
- scene_id;
- início;
- fim;
- duração;
- objetivo;
- texto na tela;
- narração;
- descrição visual;
- movimento de câmera;
- emoção principal;
- energia;
- prompt visual em português brasileiro;
- negative prompt em português brasileiro.

Critério de aceite:
- cenas não podem ser genéricas;
- cada cena deve ter uma ação visual clara;
- cada cena deve ser renderizável;
- nada em inglês deve aparecer para o usuário.

-------------------------------------------------------------------------------

### P1-SCRIPT-07 — Criar Enriquecimento de Briefing Fraco

Contexto:
Usuários escrevem briefing curto ou mal estruturado. O sistema precisa completar com suposições seguras.

Exemplo de entrada:
"pessoas que têm interesse em impressões 3D"

O sistema deve inferir:
- produto provável: peças, bonecos ou objetos personalizados em impressão 3D;
- público: colecionadores, fãs de action figures, decoração geek e presentes personalizados;
- desejo: peça única, personalizada e visualmente marcante;
- ângulo comercial: exclusividade, personalização e acabamento artesanal;
- CTA provável: chamar no direct ou WhatsApp.

Critério de aceite:
- criar enrich_briefing();
- mostrar ao usuário:
  "Briefing curto detectado. A Gal AI completou algumas informações com suposições seguras.";
- nunca inventar dados críticos como preço, garantia, marca ou disponibilidade;
- tudo em português brasileiro.

-------------------------------------------------------------------------------

### P1-SCRIPT-08 — Criar Score de Roteiro

Contexto:
Sem métrica, a melhoria de roteiro vira chute.

Objetivo:
Criar um score de 0 a 100.

Critérios:
- força do gancho;
- clareza;
- força visual;
- CTA;
- retenção;
- especificidade;
- adequação à plataforma;
- prontidão para virar cena.

Regras:
- abaixo de 60: rejeitar;
- 60 a 74: aceitar com aviso;
- 75 a 89: bom;
- 90+: excelente.

Critério de aceite:
- score aparece na UI/logs no futuro;
- score aparece no retorno da API;
- score é salvo na versão do roteiro;
- nomes dos critérios em português brasileiro.

-------------------------------------------------------------------------------

### P1-SCRIPT-09 — Melhorar Contrato de Saída em JSON + Markdown

Contexto:
O pipeline precisa de JSON; o usuário precisa de Markdown legível.

Objetivo:
Garantir duas saídas:

1. Markdown para revisão humana.
2. JSON para pipeline.

JSON mínimo:
{
  "titulo": "",
  "conceito": "",
  "publico_alvo": "",
  "gancho_principal": "",
  "estrategia_criativa": "",
  "duracao_segundos": 30,
  "formato": "9:16",
  "estilo": "",
  "status": "rascunho",
  "score": 0,
  "cenas": [],
  "narrarao_completa": "",
  "cta": "",
  "observacoes": ""
}

Critério de aceite:
- JSON validável;
- chaves em português brasileiro;
- Markdown legível;
- erro de JSON gera fallback;
- saída compatível com cenas e pipeline.

-------------------------------------------------------------------------------

### P1-SCRIPT-10 — Criar Prompt de Melhoria de Roteiro

Contexto:
O usuário pode editar, melhorar, complementar e pedir variações. O prompt precisa preservar o que já foi aprovado.

Objetivo:
Criar prompts especializados para:
- Melhorar roteiro;
- Complementar roteiro;
- Deixar mais viral;
- Deixar mais premium;
- Deixar mais direto;
- Gerar nova versão;
- Restaurar versão anterior;
- Aprovar roteiro.

Critério de aceite:
- cada ação tem prompt próprio;
- cada melhoria salva nova versão;
- nenhuma melhoria apaga versão anterior;
- a versão aprovada é usada para cenas;
- tudo em português brasileiro.

-------------------------------------------------------------------------------

### P2-SCRIPT-11 — Criar Prompt Pack de Roteiro por Plataforma

Contexto:
TikTok, Reels e Shorts têm comportamento parecido, mas não idêntico.

Objetivo:
Criar variações por plataforma:
- Reels;
- TikTok;
- Shorts;
- YouTube horizontal;
- Feed quadrado.

Critério de aceite:
- formato 9:16 padrão para Reels/TikTok/Shorts;
- roteiro usa texto na tela e narração;
- CTA adaptado;
- considerar safe zone em etapa futura;
- tudo em português brasileiro;
- não implementar agora.

-------------------------------------------------------------------------------

### P2-SCRIPT-12 — Criar Exemplos Internos de Roteiros Bons

Contexto:
Exemplos internos podem melhorar consistência de saída.

Objetivo:
Criar biblioteca de exemplos bons para:
- impressão 3D;
- fantasia/cosplay;
- produto premium;
- serviço local;
- UGC;
- oferta.

Critério de aceite:
- exemplos ficam em docs ou templates;
- exemplos não são copiados literalmente;
- usados como referência de estrutura, não como resposta fixa;
- todos os exemplos em português brasileiro.

## Itens identificados na Revisão Crítica (H10)

| ID | Contexto da melhoria | Sugestão objetiva | Prioridade |
|---|---|---|---|
| RC-01 | Caminhos C: hardcoded em `check_ffmpeg.py` | Substituir por caminhos relativos ou variáveis de ambiente (K:) | P0 (Bloqueante) |
| RC-02 | 14B mencionado como exemplo em `wangp_adapter.py` | Remover 14B da docstring, manter apenas 1.3B como padrão seguro | P0 (Bloqueante) |
| RC-03 | BATs não configuram variáveis obrigatórias | Criar BAT padrão que configure TODAS as variáveis do AGENTS.md | P0 (Bloqueante) |
| RC-04 | Erros sem causa e correção clara | Padronizar: `logger.error("CAUSA: %s | CORREÇÃO: %s", causa, solucao)` | P1 |
| RC-05 | README desatualizado | Atualizar: 212 testes coletados, progresso H10, status de use cases | P1 |
| RC-06 | Falta teste E2E para fallback FFmpeg | Criar teste: mock WanGP falha → verificar se FFmpeg é chamado | P1 |
| RC-07 | Backups não sistêmicos | Criar `scripts/backup_before_change.bat` automatizado | P2 |

## Item obrigatório de backlog (solicitação direta)
 
Após a etapa atual (`[Pasted ~5 lines]`), executar obrigatoriamente:
- Criar **3 testes unitários** que validem cenários principais e de falha.
- Criar cenários de **testes de automação e chamadas de API**.
- Aumentar cobertura com cenários que simulem a realidade para capturar gaps.
- Ler `qa/QA_TEST_PLAN.md` e mapear todos os testes implementados até o presente momento.
- Colocar itens pendentes na fila de revisão/criação/melhoria antes de novas features.


---

## Histórias de excelência documental (refinadas e pendentes)

> Escopo desta seção: **apenas histórias pendentes**. Itens já implementados ficam fora do backlog para evitar ruído.

> Objetivo: transformar gaps de qualidade documental em entregas pequenas, auditáveis e com valor direto para operação.

| ID | Prioridade | História | Critérios de aceite objetivos |
|---|---|---|---|
| DOC-06 | P1 | Criar seção fixa de riscos técnicos ativos por release | README possui "Riscos Ativos" com top-5; cada risco tem impacto + mitigação + owner. |
| DOC-07 | P1 | Separar trilha de documentação por persona (operar vs evoluir) | README traz índice "Operação" e "Arquitetura" com links diretos para docs de cada trilha. |
| DOC-08 | P2 | Quebrar épicos de documentação em histórias executáveis de sprint | 100% dos itens documentais novos têm escopo ≤ 1 sprint e dependências explícitas. |
| DOC-09 | P1 | Padronizar template de critérios de aceite no backlog | Todas as histórias novas usam padrão: Contexto, Objetivo, Critérios, Evidência. |
| DOC-10 | P1 | Definir baseline de cobertura por módulo crítico | `qa/QA_TEST_PLAN.md` inclui tabela por módulo com baseline e meta mínima. |
| DOC-11 | P2 | Implantar ADR leve para decisões arquiteturais | Existe diretório ADR e ao menos 1 ADR para cada mudança estrutural futura. |
| DOC-12 | P1 | Clarificar prioridades H11-H14 por impacto/risco | `ROADMAP.md` traz ordenação explícita com racional técnico. |
| DOC-13 | P2 | Criar rastreabilidade roadmap → entrega | Release notes incluem tabela de vínculo entre item planejado e evidência entregue. |
| DOC-14 | P2 | Definir política de depreciação documental | Docs legadas possuem banner de status: ativa/legada/arquivada + data. |
| DOC-15 | P1 | Consolidar onboarding em trilha única de quickstart | README oferece quickstart validado em ambiente limpo com no máximo 3 comandos. |
| DOC-16 | P1 | Formalizar Definition of Done por tipo de mudança | Template de PR com DoD obrigatório para docs, código e testes. |
| DOC-17 | P2 | Definir SLO/SLA local para operação offline-first | Documento técnico com metas mínimas de disponibilidade e latência local. |
| DOC-18 | P1 | Adotar checklist de coerência com princípio offline-first | Toda feature nova passa por checklist de dependência externa e fallback. |
| DOC-19 | P2 | Padronizar playbook de rollback por feature | Existe runbook com passos de rollback e validação pós-reversão. |
| DOC-20 | P1 | Evoluir guia de contribuição com gates de qualidade | README/CONTRIBUTING exigem docs-sync, evidência e testes mínimos por PR. |

### Sequenciamento recomendado
1. **Sprint A (P1 crítico):** DOC-06, DOC-07, DOC-09, DOC-12, DOC-15, DOC-16, DOC-18, DOC-20.
2. **Sprint B (governança):** DOC-10, DOC-11, DOC-13, DOC-14.
3. **Sprint C (maturidade operacional):** DOC-17, DOC-19.
