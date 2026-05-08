# PROMPT_ROTEIRO_V2 - Planejamento (NÃO IMPLEMENTAR AGORA)

**Status:** Planejamento - NÃO implementar agora.
**Objetivo:** Melhorar profundamente o motor de geração de roteiro do GalFlowAI.

---

## Problema Atual
O roteiro ainda pode sair genérico, fraco, robótico ou pouco viral.

Exemplos ruins que devem ser evitados:
- "Apresentamos..."
- "Solução completa para suas necessidades."
- "Adquira agora."
- "Pessoas que têm interesse..."
- roteiro sem gancho;
- cenas sem visual claro;
- CTA genérico;
- narração sem ritmo;
- prompts visuais vagos;
- ausência de negative prompt;
- ausência de estrutura para TikTok, Reels e Shorts.

## Objeto Futuro
Criar uma arquitetura de prompt para roteiro que gere comerciais curtos mais fortes, com:
- gancho;
- retenção;
- narrativa curta;
- CTA;
- cena visual;
- narração;
- texto na tela;
- prompt visual em português brasileiro;
- negative prompt em português brasileiro;
- JSON estruturado;
- Markdown legível.

**IMPORTANTE:** Tudo em português brasileiro. Remova qualquer exigência de "prompts visuais em inglês".

## Estrutura Planejada

### 1. Prompt Base de Roteiro
- Template reutilizável para todos os providers
- Regras fixas do GalFlowAI
- Tudo em português brasileiro

### 2. Separação de Prompt
- Prompt Base (regras fixas)
- Prompt do Briefing (dados específicos)
- Contrato de Saída (JSON + Markdown)

### 3. Quality Gate
- Rejeitar roteiros genéricos automaticamente
- Score de 0 a 100
- Tudo em português brasileiro

### 4. Estruturas por Tipo
- Produto físico, Serviço, Geek, 3D, Fantasia, etc.
- Cada tipo tem estrutura própria
- Tudo em português brasileiro

### 5. Biblioteca de Ganchos
- Frases de abertura fortes
- Categorias: curiosidade, dor, desejo, surpresa, etc.
- Tudo em português brasileiro

### 6. Enriquecimento de Briefing
- Completar briefing curto com suposições seguras
- Nunca inventar dados críticos
- Tudo em português brasileiro

### 7. Geração de Cenas por Duração
- 15s: 4 cenas, 30s: 6 cenas, etc.
- Cada cena tem ação visual clara
- Tudo em português brasileiro

### 8. Contrato de Saída
- JSON estruturado (chaves em português brasileiro)
- Markdown legível para revisão humana

## Critérios de Aceite (quando implementar no futuro)
- Tudo em português brasileiro (sem "prompts visuais em inglês")
- Templates funcionam com TemplateProvider e providers externos
- Quality Gate bloqueia roteiro genérico
- Cada tipo de comercial tem estrutura própria
- Score de roteiro aparece na UI/logs
- Versões salvas no project/roteiro_versions.json

## Status de Implementação
- [ ] Criar app/templates/script_prompt_base.py
- [ ] Implementar validate_script_quality() mais rigorosa
- [ ] Criar enrich_briefing()
- [ ] Criar templates por tipo de comercial
- [ ] Criar biblioteca de ganchos
- [ ] Implementar generate_script_v2()
- [ ] Criar score de roteiro
- [ ] Atualizar ProviderRouter para usar novo prompt
- [ ] Atualizar TemplateProvider
- [ ] Documentar em docs/PROMPT_ROTEIRO_V2.md (já feito - planejamento)

**NÃO IMPLEMENTAR AGORA. Apenas planejamento.**
