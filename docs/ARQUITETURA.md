# Arquitetura

O Gal AI possui duas entradas principais (Gradio e FastAPI), reutilizando a mesma camada de serviços.

```mermaid
flowchart LR
    UI[Gradio] --> S[Services]
    API[FastAPI] --> S
    S --> R[ProviderRouter]
    R --> T[Template]
    R --> L[LLMs locais]
    S --> F[FFmpeg]
    S --> W[WanGP opcional]
```

## Camadas
- **Entrada:** `app/main.py` e `app/api.py`
- **Serviços:** `app/services/`
- **Adapters:** `app/adapters/`
- **Pipeline:** `app/pipeline/`
