# Relatório de Auditoria do Ambiente — GalFlowAI

Data: 01/05/2026  
Autor: Agente OpenCode  

---

## 1. Espaço Livre em K:
- **Total usado**: 299.25 GB  
- **Espaço livre**: 632.26 GB  
- **Status**: ✅ Suficiente para MVP e gerações de cenas 480p

---

## 2. Existência de `envs\studio`
- Caminho: `K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio`  
- **Status**: ✅ Existe

---

## 3. Versão do Python (no ambiente studio)
- **Versão**: Python 3.10.20  
- **Executável**: `K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\python.exe`  
- **Status**: ✅ Compatível (conforme AGENTS.md)

---

## 4. Existência de FFmpeg e Git
### Git
- Caminho: `K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\Library\bin\git.exe`  
- Versão: git version 2.53.0.windows.1  
- **Status**: ✅ Existe

### FFmpeg
- Caminho: `K:\AI_VIDEO_COMMERCIAL_STUDIO\envs\studio\Library\bin\ffmpeg.exe`  
- **Status**: ✅ Existe no ambiente studio

---

## 5. Existência de Wan2GP e FramePack
- Wan2GP: `K:\AI_VIDEO_COMMERCIAL_STUDIO\engines\Wan2GP` → ✅ Existe  
- FramePack: `K:\AI_VIDEO_COMMERCIAL_STUDIO\engines\FramePack` → ✅ Existe

---

## 6. Existência das Pastas Obrigatórias
| Pasta               | Existe? |
|---------------------|---------|
| assets              | ✅ Sim  |
| cache               | ✅ Sim  |
| logs                | ✅ Sim  |
| models              | ✅ Sim  |
| projects            | ✅ Sim  |
| temp                | ✅ Sim  |

---

## 7. Variáveis de Ambiente Necessárias
| Variável                     | Valor Atual                                 | Status |
|------------------------------|---------------------------------------------|--------|
| PIP_CACHE_DIR                | K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\pip     | ✅ OK  |
| HF_HOME                      | K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\hf      | ✅ OK  |
| TORCH_HOME                   | K:\AI_VIDEO_COMMERCIAL_STUDIO\cache\torch   | ✅ OK  |
| XDG_CACHE_HOME               | K:\AI_VIDEO_COMMERCIAL_STUDIO\cache         | ✅ OK  |
| OLLAMA_MODELS                | K:\AI_VIDEO_COMMERCIAL_STUDIO\models\ollama | ✅ OK  |
| TEMP                         | C:\Users\PCGAME~1\AppData\Local\Temp        | ⚠️ Risco (aponta para C:) |
| TMP                          | C:\Users\PCGAME~1\AppData\Local\Temp        | ⚠️ Risco (aponta para C:) |
| GIT_PYTHON_GIT_EXECUTABLE    | (não definida)                              | ⚠️ Risco (deve apontar para git.exe do studio) |

> **Mitigação**: O arquivo `app/config.py` configura essas variáveis automaticamente ao iniciar a aplicação, sobrescrevendo valores incorretos.

---

## 8. Riscos de Uso do C:
1. **TEMP/TMP apontando para C:**: Se scripts forem executados sem carregar as variáveis do `config.py`, arquivos temporários serão gravados em C:.  
2. **GIT_PYTHON_GIT_EXECUTABLE não definida**: Pode causar erro em operações Git que dependam dessa variável.  
3. **Caches padrão**: Se as variáveis `PIP_CACHE_DIR` etc. não forem setadas, o Python usará pastas padrão em C:.  

> **Mitigação já implementada**: O módulo `app/config.py` define todas as variáveis obrigatórias ao iniciar o GalFlowAI.

---

## 9. Conclusão
O ambiente está **pronto para iniciar o MVP** com as seguintes ressalvas:
- Executar sempre via `app/config.py` para garantir variáveis K-only.  
- Não rodar scripts Python soltos sem configurar as variáveis de ambiente.  
- Nenhuma alteração em engines, envs ou projetos existentes foi feita.

---

## 10. Arquivos Alterados/Criados
- `docs/RELATORIO_ANALISE_AMBIENTE.md` (novo relatório, conforme solicitado)
