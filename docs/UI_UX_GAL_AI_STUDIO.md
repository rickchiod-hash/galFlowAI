# UI/UX Gal AI Studio — Diagnóstico e Objetivos

## Diagnóstico do Visual Atual
1. UI funcional, mas ainda com cara de formulário técnico.
2. Nome FlowForgeAI ainda presente na interface.
3. Preview vazio sem orientação ao usuário.
4. Central de Logs ausente na UI principal.
5. Sem hierarquia visual de botões.
6. Cenas não têm representação visual (cards/gallery).
7. Estado da sessão não mantido com gr.State.

## Objetivo do Gal AI Studio
Transformar a interface atual em um produto premium que pareça um estúdio de IA para criação de comerciais, mantendo a simplicidade do Gradio e a estabilidade do pipeline local.

## Inspiração
- Estúdios de geração de vídeo/imagem (ex: Runway, MidJourney).
- Ferramentas locais com UI premium (ex: Stable Diffusion WebUI).
- Foco em clareza de fluxo e feedback visual imediato.

## Design System
- **Paleta:** Fundo #08080B, Cards #18181F, Laranja #FF5A00.
- **Tipografia:** Sans-serif legível, tamanhos hierárquicos.
- **Botões:** Primário (laranja), Secundário (cinza), Perigo (vermelho).
- **Estados:** Verde (sucesso), Amarelo (aviso), Vermelho (erro), Azul (info).

## Componentes Principais
- **Blocks:** Base da UI com abas para cada etapa.
- **Video:** Preview e vídeo final.
- **Gallery:** Cenas, frames e assets.
- **Dataframe:** Central de Logs e fila de jobs.
- **State:** Contexto da sessão (project_id, roteiro, cenas).
- **Timer:** Atualização controlada de logs/status.

## Fluxo de Navegação
1. **Briefing:** Input de texto simples.
2. **Roteiro:** Edição e ações (Melhorar, Complementar, etc.).
3. **Cenas:** Cards/Gallery com status e ações.
4. **Preview:** Vídeo gerado com detalhes técnicos.
5. **Resultado:** Download e metadados.
6. **Logs e Diagnóstico:** Central de Logs estruturada.

## Central de Logs
- Gr.Dataframe com colunas fixas.
- Filtros por nível e busca por texto.
- Cores por nível (Verde/Amarelo/Vermelho).
- Botões: Copiar diagnóstico, Atualizar, Pausar/Retomar.

## Preview
- Gr.Video com estado vazio elegante.
- Diferenciação entre FFmpeg fallback, IA real e vídeo final.
- Metadados: duração, resolução, engine, fallback.

## Cards de Cenas
- Cada cena como card com número, duração, status, miniatura.
- Botões: Editar, Ver Prompt, Regenerar, Aprovar.
- Estados visuais: Pendente, Gerada, Concluída, Falhou.

## Modo Simples vs Modo Avançado
- **Simples:** Apenas briefing, duração, estilo e botão criar.
- **Avançado:** Motores de roteiro, endpoints, logs, presets.
- Valor padrão: Modo Simples.

## Por que não React agora?
- Gradio já atende ao MVP com baixo esforço.
- React exigiria API estável e testes de contrato.
- Migração precoce pode quebrar o fluxo atual.

## Quando considerar React?
- V2.5, após:
  - FastAPI estável.
  - Endpoints versionados.
  - Testes automatizados.
  - Fluxo Gradio validado.

## Checklist de Aceite
- [ ] Branding Gal AI aplicado.
- [ ] UI em Blocks com abas claras.
- [ ] Central de Logs legível sem UNKNOWN.
- [ ] Preview com estado vazio orientativo.
- [ ] Cenas como cards/gallery.
- [ ] Design System consistente.
- [ ] Tudo em português brasileiro.
