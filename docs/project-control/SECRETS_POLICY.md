# Politica de Secrets e Arquivos Sensiveis — GalFlowAI

## Objetivo

Evitar commit de chaves, tokens, paths pessoais e informacoes sensiveis
no repositorio Git.

## Regras

1. **Nunca commitar:**
   - `.env` ou `.env.*` contendo chaves reais
   - `credentials.json`, `credentials.*`, `*.key`, `*.pem`
   - Paths absolutos com drive letter ou nome de usuario
   - Tokens de API, senhas, ou secrets em texto plano
   - Arquivos de configuracao local (`local_settings.*`, `*.local.*`)

2. **Paths pessoais:**
   - Paths como `K:\...`, `C:\Users\<username>\...` nunca devem aparecer
     em arquivos rastreados pelo Git
   - Usar variaveis de ambiente ou `app/config.py` com `BASE_DIR`

3. **.gitignore:**
   - Manter entradas para: `*.env`, `credentials.*`, `*.key`, `*.pem`,
     `__pycache__/`, `*.pyc`, `.DS_Store`

4. **Excecoes documentadas:**
   - Se um path absoluto for necessario para documentacao, usar
     `<BASE_DIR>` ou `$PROJECT_ROOT` como placeholder
   - Excecoes devem ser aprovadas por ADR

## Verificacao

O teste `test_sec_1101_secrets_policy.py` verifica automaticamente:
- Ausencia de `.env` com tokens no repo
- Ausencia de paths com `K:\` ou `C:\Users\` em arquivos `.py` rastreaveis
- Presenca de `.gitignore` com entradas basicas de seguranca

## Referencias

- `docs/project-control/12_DEPENDENCIAS_E_BLOQUEIOS.md` — Dependencias bloqueantes
