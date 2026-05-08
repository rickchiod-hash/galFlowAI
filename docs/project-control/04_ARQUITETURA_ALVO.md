# 04_ARQUITETURA_ALVO — GalFlowAI

## Regra de dependência

```text
UI Gradio
  ↓
API/Handlers
  ↓
Application Use Cases
  ↓
Domain Services
  ↓
Ports/Interfaces
  ↓
Adapters
  ↓
Filesystem / SQLite / FFmpeg / LLM / TTS / WanGP
```

## Regras

- UI não chama adapter diretamente.
- API não chama adapter diretamente.
- UI/API não chamam pipeline bruto diretamente.
- Use case coordena uma intenção de usuário.
- Service contém regra de domínio.
- Adapter integra tecnologia externa/local.
- Pipeline orquestra steps, mas não acumula regra de negócio.
- Domain models não conhecem Gradio, FastAPI, FFmpeg, WanGP ou Qdrant.

## Pastas-alvo futuras

```text
app/domain/
app/application/use_cases/
app/services/
app/adapters/
app/pipeline/steps/
app/storage/
app/observability/
tests/unit/
tests/integration/
tests/contract/
tests/e2e/
tests/regression/
```

## Estratégia de migração

1. Criar testes antirregressão.
2. Extrair use cases pequenos.
3. Criar domain models mínimos.
4. Trocar chamadas diretas por portas/interfaces.
5. Só depois reorganizar pastas.
