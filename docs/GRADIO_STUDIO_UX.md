# Gradio Studio UX — Guia de Implementação

## Por que manter Gradio agora?
- Gradio já está funcionando em 127.0.0.1:7860.
- Permite iteração rápida de UI sem backend separado.
- Blocks oferece controle suficiente para fluxos personalizados.
- Migração para React só é recomendada após API estável (V2.5).

## Por que usar Blocks?
- Controle total sobre layout, eventos e fluxo de dados.
- Suporte a abas, gr.State, gr.Timer e componentes aninhados.
- Melhor para fluxos multi-etapas (Briefing → Roteiro → Cenas → Preview).

## Quando usar Interface?
- Apenas para protótipos rápidos de funções únicas.
- Não recomendado para fluxos complexos como o Gal AI Studio.

## Como usar Theme/CSS
- Usar `gr.theme` base + CSS customizado centralizado em `app/static/gal_ai_theme.css`.
- Não espalhar CSS inline em componentes.
- Paleta Gal AI Studio:
  - Fundo principal: #08080B
  - Fundo secundário: #111116
  - Card: #18181F
  - Borda: #343442
  - Texto principal: #F7F7FA
  - Laranja Gal AI: #FF5A00

## Como usar Video
- Usar `gr.Video` para preview e vídeo final.
- Garantir saída MP4 compatível com navegadores.
- Estado vazio: exibir mensagem orientativa, não placeholder quebrado.

## Como usar Gallery
- Para grid de cenas, frames e assets de referência.
- Cada item com caption (ex: "Cena 1 | 0–5s | Concluída").
- Clicável para expandir detalhes da cena.

## Como usar Dataframe
- Para logs estruturados (Central de Logs) e fila de jobs.
- Colunas fixas: Horário, Nível, Módulo, Projeto, Mensagem, Sugestão.
- Não exibir DEBUG na UI.

## Como usar Timer
- Atualização controlada de logs/status (intervalo 2-5s).
- Botões para pausar/retomar atualização automática.
- Não usar polling agressivo.

## Como usar State
- Manter contexto entre eventos: project_id, roteiro, cenas, status, motor selecionado.
- Evitar perda de estado ao clicar em ações diferentes.

## Por que WebSocket não é obrigatório agora?
- Timer resolve atualização periódica de logs/status.
- WebSocket adiciona complexidade desnecessária no MVP.
- Futuro: considerar apenas após FastAPI estável.

## Quando considerar Chatbot lateral
- V2.3: assistente para explicar erros, sugerir melhorias, orientar próximos passos.
- Não substituir Central de Logs.
- Tudo em português brasileiro.

## Quando considerar React
- V2.5, apenas se:
  - FastAPI estável com endpoints versionados.
  - Testes de contrato implementados.
  - Fluxo Gradio validado.
  - Pipeline fim a fim estável.

## Checklist de Aceite da UI
- [ ] Branding Gal AI (sem GalFlowAI na UI).
- [ ] Layout em Blocks com abas claras.
- [ ] Preview com gr.Video e estado vazio elegante.
- [ ] Central de Logs com gr.Dataframe legível.
- [ ] Uso de gr.State para contexto da sessão.
- [ ] Design System aplicado (cores, botões, cards).
- [ ] Tudo em português brasileiro.
