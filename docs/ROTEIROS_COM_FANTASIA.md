# Roteiros com Fantasia

O GalFlowAI agora suporta **briefings de fantasia** com templates especializados que geram roteiros comerciais (não narrativas de RPG).

## Exemplos de Briefings de Fantasia

### 1. Fantasia Medieval Artesanal
```
"Quero vender uma fantasia medieval artesanal para eventos, com capa preta, detalhes dourados e aparência de nobre sombrio."
```
**Template usado:** `fantasia`
**Resultado esperado:** Roteiro com ambiente medieval, close-ups de detalhes, narração épica.

### 2. Fantasia Futurista / Cyberpunk
```
"Quero criar um comercial para uma fantasia futurista com armadura leve, visor neon verde e estética cyberpunk."
```
**Template usado:** `futurista`
**Resultado esperado:** Roteiro com neon, tecnologia, movimentos rápidos.

### 3. Boneco Colecionável 3D
```
"Quero vender um boneco colecionável impresso em 3D, amarelo e dourado, com visor verde, estilo premium, para fãs de action figures."
```
**Template usado:** `geek`
**Resultado esperado:** Roteiro com macro shots, detalhes de pintura, unboxing.

### 4. Loja de Acessórios de Cosplay
```
"Quero divulgar uma loja que cria acessórios de cosplay personalizados sob encomenda."
```
**Template usado:** `servico_local`
**Resultado esperado:** Roteiro com bastidores, processo de criação, depoimentos.

### 5. Decoração Geek 3D
```
"Quero criar um anúncio viral para uma peça de decoração geek feita em impressão 3D."
```
**Template usado:** `impressao3d`
**Resultado esperado:** Roteiro com timelapse de impressão, personalização, aplicação.

## Estrutura do Roteiro Gerado

Cada roteiro contém:
1. **Conceito** - O que está sendo vendido
2. **Público-alvo** - Para quem é
3. **Hook** - Primeiros 1-3 segundos (fundamental)
4. **Cenas com tempo** - 5-6 cenas com durações exatas
5. **Texto na tela** - Call-to-action visual
6. **Narração** - Audio script completo
7. **Descrição visual** - O que a câmera mostra
8. **Movimento de câmera** - Zoom, orbit, etc.
9. **Prompt visual** - Em inglês para IA de vídeo
10. **Negative prompt** - O que evitar
11. **CTA** - Chamada para ação final

## Diferença: Comercial vs RPG

| Característica | Comercial (Template) | RPG (Não usar) |
|--------------|----------------------|----------------|
| Foco | Venda/projeto | História |
| Tempo | 30-40 segundos | Ilimitado |
| Cenas | 5-6 cenas curtas | Longas |
| Narração | Direta e persuasiva | Descritiva |
| CTA | "Adquira já!" | "O que você faz?" |
| Prompt visual | Para vídeo IA | Para imagem |

## Validação de Qualidade

O GalFlowAI rejeita roteiros que contenham:
- "Apresentamos" (robótico)
- "Solução completa" (genérico)
- "Adquira agora" (sem contexto)
- Ausência de hook
- Ausência de CTA
- Sem descrição visual

## Testando

Execute no GalFlowAI:
1. Cole um dos briefings acima
2. Clique "Criar comercial"
3. Verá o roteiro gerado com todas as seções
4. O vídeo de preview será criado com base nas cenas

## Templates Disponíveis

| Estilo | Palavras-chave | Melhor para |
|--------|----------------|-------------|
| Viral | "viral", "chamativo" | Redes sociais, jovens |
| Premium | "luxo", "sofisticado" | Produtos de alto padrão |
| UGC | "depimento", "cliente" | Prova social |
| Cinematográfico | "cinema", "épico" | Filmes, trailers |
| Bastidores | "artesanal", "processo" | Produtos feitos à mão |
| Geek | "colecionável", "action figure" | Nerd culture |
| Fantasia Medieval | "medieval", "fantasia" | RPG, cosplay |
| Fantasia Futurista | "futurista", "cyberpunk" | Sci-fi, tech |
| Fantasia Sombria | "sombrio", "noite" | Terror, mistério |
| Luxo | "luxo", "premium" | Joias, acessórios |
| Direto para Venda | "compre", "oferta" | E-commerce |

---

**Documentação criada em:** 03/05/2026
**Versão:** GalFlowAI 1.0
