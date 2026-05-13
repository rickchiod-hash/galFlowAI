# 18_IMPLEMENTATION_ORDER — GalFlowAI

## Ordem que o OpenCode deve seguir

### Fase 0 — Importação e auditoria

1. Copiar este pack.
2. Ler `AGENTS.md`.
3. Rodar comandos Git.
4. Atualizar `00_STATUS_EXECUTIVO.md`.
5. Commit `docs(governance): import v2 control pack`.

### Fase 1 — Antirregressão documental

1. GOV-001.
2. GOV-002.
3. GOV-003.
4. GOV-004.
5. GOV-005.
6. GOV-006.

### Fase 2 — Diagnóstico real

1. CORE-100.
2. CORE-101.
3. CORE-102.

### Fase 3 — Testes base

1. QA-1000.
2. QA-1001.
3. QA-1002.

### Fase 4 — Refatoração segura

1. ARCH-300.
2. ARCH-301.
3. ARCH-302.
4. PROV-300.
5. PROV-301.

### Fase 5 — Pipeline e produto

1. UI-201.
2. UI-202.
3. PIPE-400.
4. PIPE-401.
5. RND-600.
6. AUD-700.

### Fase 6A — Structural Stabilization (anti-break order)

1. ARCH-320 ✅
2. API-210
3. API-211
4. LOG-100

### Fase 6B — Mandatory Functional Integration

1. UI-205
2. RND-610
3. RND-611
4. RND-612

### Fase 6C — Complete Platform

1. VEC-810
2. VEC-811
3. DOC-120

## Regra

1. Não pular fases sem registrar motivo no Status Executivo.
2. **Nunca inverter anti-break order**: 6A → 6B → 6C obrigatório.
