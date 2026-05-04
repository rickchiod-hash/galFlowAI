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
