# QA_AUDITORIA_UNIFICADA — Guia Único de Revisão Técnica (GalFlowAI)

> **Documento único, completo e auxiliar** para revisão rigorosa de histórias marcadas como concluídas/validadas.
> 
> **Uso:** orientar revisão de código, testes, arquitetura e histórico Git sem interromper o fluxo de desenvolvimento.
> 
> **Regra operacional:** este arquivo não executa mudanças automaticamente; ele orienta o revisor a validar evidências e abrir correções com critério.

---

## 1) Objetivo

Garantir que qualquer item marcado como **IMPLEMENTADO / CONCLUÍDO / VALIDADO** no projeto GalFlowAI esteja comprovado por:

1. Código real versionado;
2. Testes relevantes e suficientes;
3. Integração no fluxo principal;
4. Evidência no histórico Git (commit/PR);
5. Coerência arquitetural e ausência de regressão.

Se não houver comprovação objetiva, o status deve ser tratado como:

> **EVIDÊNCIA INSUFICIENTE**

---

## 2) Mandato do revisor

Você atua como:
- Staff Engineer
- QA Architect
- Software Architect
- Revisor técnico de qualidade e confiabilidade

### Postura obrigatória
- Não aceitar documentação como prova final.
- Não aceitar checklist/status/roadmap como evidência suficiente.
- Não aceitar mock fraco como validação de regra de negócio.
- Não elogiar sem evidência.
- Não inferir comportamento não provado.

---

## 3) Regras obrigatórias do GalFlowAI (gate de validação)

Todos os itens concluídos devem respeitar:

1. FFmpeg é fallback obrigatório.
2. WanGP é opcional.
3. TTS falhando não pode quebrar exportação.
4. UI/API não devem chamar adapters diretamente.
5. Use cases coordenam responsabilidades.
6. Pipeline deve orquestrar, não concentrar regra de domínio.
7. Nenhum provider/fallback/log/métrica/checkpoint pode ser removido silenciosamente.

---

## 4) Pré-check obrigatório antes da revisão

Execute e registre saída:

1. `git status --short`
2. `git branch --show-current`
3. `git fetch --all --prune`
4. `git pull --rebase` (quando permitido)
5. `git log --oneline --decorate -n 50`
6. `git rev-list --count HEAD`
7. `git log --oneline origin/<branch>..HEAD` (se remoto existir)

### Interpretação
- Se houver alterações locais não commitadas: registrar risco de análise contaminada.
- Se houver commits locais não enviados: registrar risco de divergência com remoto.

---

## 5) Escopo mínimo de leitura documental

Revisar e cruzar com código:

- `README.md`
- `ROADMAP.md`
- `BACKLOG.md`
- `state/FLUXO_STATUS.md`
- `CHECKPOINT_H10.md`
- `ETAPA_H4A_H8.md`
- `ETAPA_H4A_H8_COMPLETA.md`
- `qa/QA_TEST_PLAN.md`

Se houver arquivos adicionais de controle (ex.: `docs/project-control/*`), incluir no escopo.

---

## 6) Escopo mínimo técnico (código/testes)

Revisar implementação real em:

- `app/main.py`
- `app/pipeline/video_generation_pipeline.py`
- `app/application/use_cases/*.py`
- `app/services/*.py`
- `app/adapters/*.py`
- `tests/` (unit, integration, e2e relevantes)

---

## 7) Método de auditoria por história

Para cada história marcada como concluída:

1. Capturar declaração documental (onde foi marcada como concluída).
2. Encontrar implementação real no código (arquivo, função, classe, endpoint, stage).
3. Verificar teste que comprova regra principal e falhas críticas.
4. Verificar integração no fluxo principal:
   `briefing -> roteiro -> aprovação -> cenas -> prompts -> render -> composição -> export`
5. Verificar histórico Git (commit que introduziu, ajustes, regressões).
6. Classificar status real:
   - IMPLEMENTADA
   - PARCIAL
   - NÃO IMPLEMENTADA
   - EVIDÊNCIA INSUFICIENTE

---

## 8) Matriz obrigatória de validação

Use esta estrutura:

| História | Status declarado | Status real | Evidência objetiva | Divergência doc vs código | Risco | Correção recomendada |
|---|---|---|---|---|---|---|

### Critério mínimo de “Evidência objetiva”
- Arquivo + símbolo (função/classe/use case/endpoint);
- Teste(s) associado(s) e o que provam;
- Commit(s) relevantes.

---

## 9) Matriz de GAPs priorizados (TODO)

Registrar lacunas encontradas em formato acionável:

| GAP ID | Tema | Gravidade | Evidência | Impacto | Próxima ação | Critério de aceite |
|---|---|---|---|---|---|---|

### Prioridade
- **P0:** quebra fluxo principal ou regra mandatória.
- **P1:** risco arquitetural/regr. relevante.
- **P2:** melhoria de robustez/governança.

---

## 10) Separação por commit (anti-perda de contexto)

Para cada gap/história:

- **Commit com evidência suficiente** (o que realmente entrega).
- **Commit com lacuna** (faltou teste, faltou integração, faltou fallback, etc.).

Exemplo:
- `abc123`: introduz use case base ✅
- `def456`: faltou teste de fallback TTS ❌

---

## 11) Regras para não impactar fluxo de trabalho

Este arquivo é **auxiliar**. Portanto:

- Não iniciar refactor durante auditoria.
- Não iniciar feature nova durante auditoria.
- Não alterar vários `.md` por impulso.
- Só mover status para **“em andamento”** quando gap estiver comprovado e a correção for iniciada.
- Toda correção aberta deve nascer com:
  - critério de aceite,
  - evidência esperada,
  - vínculo com GAP ID,
  - validação de regressão.

---

## 12) Entrega esperada da revisão

A revisão deve sair com:

1. Veredito geral do pacote: CONFIÁVEL / PARCIAL / NÃO CONFIÁVEL.
2. Lista de histórias declaradas como concluídas.
3. Matriz de validação por história.
4. Falsos positivos (docs disseram concluído, código não comprovou).
5. Bloqueadores para considerar o pacote realmente concluído.
6. Riscos técnicos e de regressão.
7. Testes faltantes.
8. Próximo passo exato sem quebra de fluxo.

---

## 13) Prompt pronto para usar no OpenCode

Copie e cole exatamente:

```txt
Leia o arquivo `docs/QA_AUDITORIA_UNIFICADA.md` e execute a auditoria completa exatamente conforme as regras dele.

Objetivo:
Validar todas as histórias marcadas como concluídas/validadas usando código, testes, integração real e histórico Git.

Regras mandatórias:
- Não alterar código nesta etapa.
- Não aceitar documentação como prova suficiente.
- Não inferir sem evidência.
- Se não conseguir comprovar, responder literalmente: EVIDÊNCIA INSUFICIENTE.
- Validar as regras obrigatórias do GalFlowAI (fallback FFmpeg, WanGP opcional, TTS não quebrar exportação, separação UI/API/adapters, use cases coordenando, pipeline orquestrador).

Passos obrigatórios:
1) Rodar pré-check Git listado no documento.
2) Ler docs do escopo mínimo.
3) Validar implementação no escopo técnico (app/, tests/).
4) Montar matriz por história com status real + evidência.
5) Montar matriz de GAPs com prioridade P0/P1/P2.
6) Separar achados por commit: evidência suficiente vs lacuna.
7) Entregar veredito final e próximo passo exato.

Formato de saída obrigatório:
1. Veredito geral do pacote
2. Histórias declaradas como concluídas
3. Matriz de validação
4. Falsos positivos
5. Bloqueadores
6. Riscos
7. Testes faltantes
8. Próximo passo exato
```

---

## 14) Fechamento

Se um item foi marcado como validado sem prova técnica objetiva, o revisor deve questionar explicitamente:

- Qual arquivo/função comprova?
- Qual teste prova a regra de negócio?
- Qual commit integrou sem regressão?

Sem essas respostas: **EVIDÊNCIA INSUFICIENTE**.
