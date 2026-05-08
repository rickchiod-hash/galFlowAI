# Contributing to GalFlowAI

**Última atualização:** 06/05/2026

## Definition of Done (DoD) por tipo de mudança

### Para mudanças de código (Use Cases, Services, Adapters)
- [ ] Código segue padrão 3 pontos: Validate → Execute → Return
- [ ] Testes unitários criados/atualizados (100% passando)
- [ ] Logs com formato padrão: `CAUSA: ... | CORREÇÃO: ...`
- [ ] Sem caminhos C: (apenas K: ou relativos)
- [ ] Documentação da API atualizada (se houver novos endpoints)
- [ ] Commit atômico com mensagem clara

### Para mudanças de documentação (README, BACKLOG, ROADMAP, docs/)
- [ ] Documento reflete estado real da implementação
- [ ] Distingue claramente **implementado** vs **planejado**
- [ ] Inclui evidência (teste, log, endpoint ou artefato)
- [ ] Naming oficial **GalFlowAI** usado (nunca GalFlowAI)
- [ ] Logos oficiais referenciadas (`galflowai_logo_master.png`, `galflowai_app_icon.png`)
- [ ] Template de critérios de aceite aplicado (Contexto, Objetivo, 3 pontos, Evidência)

### Para mudanças de testes
- [ ] Testes cobrem cenários felizes e de erro
- [ ] Seguem padrão 3 pontos (Validate → Execute → Return)
- [ ] Incluem mocks para dependências externas
- [ ] 100% passando (`pytest -q`)

---

## Gates de Qualidade (DOC-20)

### Obrigatório para todo PR:
1. **Docs-sync:** Documentação atualizada no mesmo PR
2. **Evidência:** Teste, log, endpoint ou artefato que comprove a mudança
3. **Testes mínimos:** Pelo menos 1 teste para cada nova funcionalidade
4. **Naming:** Uso de **GalFlowAI** (nunca GalFlowAI)
5. **Logos:** Referência a `galflowai_logo_master.png` e `galflowai_app_icon.png` onde aplicável

---

## Checklist de coerência com princípio offline-first (DOC-18)

### Para toda nova feature, verificar:
- [ ] Não depende de API paga obrigatória
- [ ] Funciona sem internet (fallback local disponível)
- [ ] Fallback documentado (ex.: TemplateProvider → FFmpeg)
- [ ] Caminhos usam K: ou variáveis de ambiente (nunca C:)
- [ ] Variáveis obrigatórias configuradas (PIP_CACHE_DIR, HF_HOME, etc.)

---

## Padrão de Commits

### Formato:
```
<Tipo>: <Descrição curta>

- <Detalhe 1>
- <Detalhe 2>
```

### Tipos:
- `REF`: Refatoração (rename, padronização)
- `DOC`: Documentação (README, BACKLOG, ROADMAP, docs/)
- `Hxx`: História de usuário (H11-H20)
- `RC-xx`: Correção crítica (RC-01 a RC-07)
- `FIX`: Correção de bug
- `FEAT`: Nova funcionalidade

---

## Como executar testes
```bash
# Todos os testes
pytest -q

# Testes específicos
pytest tests/test_h16_*.py -v

# Total atual: 314 testes coletados
```

---

## Ambiente de desenvolvimento
- **Python:** K:\AI_VIDEO_COMERCIAL_STUDIO\envs\studio\Scripts\python.exe
- **Variáveis obrigatórias:** Ver `scripts/start_GalFlowAI_standard.bat`
- **IDE recomendada:** VS Code com Python extension
- **Lint:** `python -m py_compile <file>`

---

## Contato
- Issues: https://github.com/rickchiod-hash/galFlowAI/issues
- Repository: https://github.com/rickchiod-hash/galFlowAI
