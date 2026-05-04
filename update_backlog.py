#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to update BACKLOG.md with all missing sections.
All text in Portuguese Brazilian, no 'prompts visuais em inglês'.
"""
from pathlib import Path

# Read current BACKLOG.md
backlog_path = Path("BACKLOG.md")
with open(backlog_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Define ALL missing sections (in Portuguese Brazilian)
missing = """

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

"""

# Check if sections are missing and append
sections_to_check = ["P1-SCRIPT-01", "P1-SCRIPT-02", "P1-SCRIPT-03"]
missing_count = 0
for section in sections_to_check:
    if section not in content:
        missing_count += 1

if missing_count > 0:
    with open(backlog_path, 'a', encoding='utf-8') as f:
        f.write(missing)
    print(f"Missing sections appended successfully ({missing_count} sections checked)")
else:
    print("All main sections already present")

print(f"Total length: {len(content) + len(missing)} chars")
