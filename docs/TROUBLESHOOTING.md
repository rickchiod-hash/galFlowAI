# Troubleshooting

## Gradio não abre (`127.0.0.1:7860`)
- Verifique processo/porta: `netstat -ano | findstr :7860`
- Reinicie: `scripts\start_app_debug.bat`

## FastAPI não responde (`127.0.0.1:8000`)
- Suba manualmente: `python -m uvicorn app.api:app --host 127.0.0.1 --port 8000`
- Confira docs: `http://127.0.0.1:8000/docs`

## FFmpeg ausente
- Instale FFmpeg e configure o PATH.

## Sem motor LLM local
- Use fallback Template local.
- Ou inicie LM Studio/GPT4All/KoboldCpp/llama.cpp.

## WanGP ausente
- WanGP é opcional; mantenha fluxo com FFmpeg fallback.

## Como usar a Central de Logs

Incluir:
- abrir aba Logs e Diagnóstico;
- filtrar ERROR;
- buscar por FFmpeg, provider ou project_id;
- copiar diagnóstico;
- anexar diagnóstico em issue;
- verificar logs em K:\.

### Status da Central de Logs
- Acesse a aba "📋 Logs e Diagnóstico" na UI.
- Filtre por nível: Todos, INFO, WARN, ERROR.
- Use a busca para encontrar erros específicos.
- Clique em "📋 Copiar diagnóstico" para copiar texto técnico.
- Clique em "📁 Abrir pasta de logs" para ver arquivos.
- Use "⏸ Pausar atualização automática" se necessário.

### Mensagens comuns
- "Logs atualizados." - Tudo OK.
- "Nenhum erro encontrado." - Sem erros recentes.
- "Erro detectado. Veja a sugestão." - Verifique a coluna "Sugestão".
- "Arquivo de log ainda não existe." - Gere um roteiro primeiro.
- "Atualização automática pausada." - Clique em "▶ Retomar atualização automática".

### Diagnóstico copiável
Clique em "📋 Copiar diagnóstico" para gerar:
- Horário atual.
- Commit atual (se disponível).
- Python usado.
- Portas Gradio e FastAPI.
- Últimos 20 WARN/ERROR.
- Status dos providers.
- Status do FFmpeg.
- Caminho dos logs.
- Sugestão de próximo passo.
