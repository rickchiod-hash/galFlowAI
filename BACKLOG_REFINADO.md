# Backlog Refinado - FlowForgeAI

## Histórias de Usuário (Atualizado)

### História 6 (Nova)

#### Título ####
Integrar WanGP/Wan2GP como motor opcional de geração de vídeo

#### História de Usuário ####
Como usuário da aplicação,  
quero ter a opção de usar WanGP/Wan2GP para geração avançada de vídeo (opcional),  
para produzir vídeos de maior qualidade quando disponível, mantendo FFmpeg como fallback obrigatório.

#### Contexto ####
- Adapter WanGP já existe em `app/adapters/wangp_adapter.py`
- Pipeline já tenta WanGP primeiro em `video_generation_pipeline.py` (linha 164)
- Fallback para FFmpeg está implementado (linha 179)
- **SUPOSIÇÃO**: WanGP está em `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP`
- **SUPOSIÇÃO**: Preset seguro para 6GB VRAM está implementado (1.3B, 480p)

#### Objetivo ####
Garantir que WanGP integrate opcionalmente ao FlowForgeAI, com fallback transparente para FFmpeg, mantendo a aplicação funcional mesmo sem WanGP instalado.

#### Escopo ####
##### Dentro do escopo #####
- Testar detecção de disponibilidade WanGP (`WanGPAdapter.disponivel()`)
- Criar teste de integração: `test_wangp_adapter_fallback_to_ffmpeg()`
- Validar que fallback para FFmpeg funciona quando WanGP indisponível
- Validar que preset seguro (1.3B, 480p) é usado para 6GB VRAM
- Atualizar README com seção "Motores Avançados de Vídeo"
- Documentar URLs: https://github.com/lostruins/koboldcpp (WanGP relacionado)

##### Fora do escopo #####
- Instalação automática do WanGP
- Download automático de modelos
- FramePack adapter (separado, Story 7)
- Otimizações de performance para GPUs mais fortes

#### Regras de negócio ####
- **SUPOSIÇÃO**: WanGP é opcional - aplicação funciona sem ele
- **SUPOSIÇÃO**: FFmpeg é fallback obrigatório (nunca falha o fluxo)
- **SUPOSIÇÃO**: Preset seguro para 6GB VRAM: 1.3B, 480p/512p, cenas curtas

#### Critérios de aceite ####
##### Cenário 1: WanGP disponível gera vídeo #####
Dado que WanGP está instalado em `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP`,  
quando chamo `pipeline.generate_commercial()`,  
então deve tentar usar WanGP para geração de cenas antes do FFmpeg.

##### Cenário 2: Fallback para FFmpeg quando WanGP indisponível #####
Dado que WanGP não está instalado,  
quando chamo `pipeline.generate_commercial()`,  
então deve usar FFmpeg automaticamente (fallback transparente).

##### Cenário 3: Preset seguro para 6GB VRAM #####
Dado que GPU tem 6GB VRAM,  
quando configuro WanGP adapter,  
então deve usar preset "1.3B" e resolução "480p" por padrão.

##### Cenário 4: Teste de integração fallback #####
Dado que todos os motores avançados estão indisponíveis,  
quando executo `test_wangp_adapter_fallback_to_ffmpeg()`,  
então deve passar confirmando que FFmpeg produz vídeo válido.

#### Critérios não funcionais ####
- **Resiliência**: Aplicação não quebra se WanGP falha
- **Compatibilidade**: Funciona com Wan2GP ou FramePack se disponíveis

#### Dependências ####
- `app/adapters/wangp_adapter.py` (já existe)
- `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\Wan2GP` (opcional)
- FFmpeg (obrigatório, já configurado)

#### Impactos esperados ####
##### Impacto técnico #####
- Adição de opção de alta qualidade para usuários com WanGP
- Mantém compatibilidade com hardware limitado via FFmpeg

##### Impacto de negócio #####
- Diferencial competitivo: opção de vídeo de alta qualidade
- Inclusivo: funciona com hardware básico ou avançado

##### Impacto em outros fluxos #####
- Nenhum impacto negativo
- Positivo: fluxo principal usa mesma interface, apenas motor muda

#### Validações técnicas ####
- **Testes unitários**: `test_wangp_adapter_disponivel()`
- **Testes integrados**: `test_wangp_adapter_fallback_to_ffmpeg()`
- **Testes manuais**: Testar com WanGP instalado e sem instalado
- **Evidências esperadas**: Vídeos gerados com WanGP e FFmpeg

#### Definition of Done ####
- [ ] `WanGPAdapter.disponivel()` testado e funcionando
- [ ] Teste `test_wangp_adapter_fallback_to_ffmpeg()` criado e passando
- [ ] README atualizado com seção "Motores Avançados"
- [ ] Preset seguro documentado para 6GB VRAM
- [ ] Código revisado e aprovado
- [ ] Commit realizado

#### Pontos de Planejamento (Planning Poker): **5 pontos**
*Justificativa: Tarefa média, envolve validação de fallback, criação de testes de integração e documentação. Crítica para MVP completo opcional.*

---

### História 7 (Nova)

#### Título ####
Implementar FramePack adapter como motor opcional secundário

#### História de Usuário ####
Como usuário da aplicação,  
quero ter a opção de usar FramePack para geração de vídeo (opcional),  
para ter alternativa ao WanGP com diferentes características de estilo.

#### Contexto ####
- FramePack mencionado no AGENTS.md como engine opcional
- Adapter não implementado ainda
- **SUPOSIÇÃO**: FramePack está em `K:\AI_VIDEO_COMERCIAL_STUDIO\engines\FramePack`

#### Objetivo ####
Criar adapter FramePack opcional com fallback para FFmpeg, similar ao WanGP.

#### Escopo ####
##### Dentro do escopo #####
- Criar `app/adapters/framepack_adapter.py`
- Implementar detecção de disponibilidade
- Integrar ao pipeline como terceira opção (após WanGP, antes FFmpeg)
- Criar teste de integração

##### Fora do escopo #####
- Instalação automática
- Download de modelos

#### Critérios de aceite ####
##### Cenário 1: FramePack disponível #####
Dado que FramePack está instalado,  
quando chamo pipeline,  
então deve tentar usar FramePack como opção.

##### Cenário 2: Fallback para FFmpeg #####
Dado que FramePack não está disponível,  
quando chamo pipeline,  
então deve usar FFmpeg (fallback).

#### Definition of Done ####
- [ ] `FramePackAdapter` criado
- [ ] Integração no pipeline testada
- [ ] Testes criados e passando

#### Pontos de Planejamento (Planning Poker): **8 pontos**
*Justificativa: Tarefa grande, envolve criação de novo adapter do zero, testes e integração.*

---

### História 8 (Atualizada da UI)

#### Título ####
Refinar interface Gradio com indicadores visuais completos

#### História de Usuário ####
Como usuário da aplicação,  
quero uma interface Gradio com feedback visual claro de progresso e status,  
para acompanhar o processamento de forma intuitiva e sem confusão.

#### Contexto ####
- Interface Gradio (http://127.0.0.1:7860) está funcional (90% completa)
- `gr.Progress()` foi adicionado em Story 5
- Melhorias visuais de erro ainda podem ser feitas

#### Objetivo ####
Melhorar a experiência do usuário na interface Gradio, adicionando indicadores visuais de progresso, melhorando feedback de erros e ajustando layout para melhor legibilidade.

#### Escopo ####
##### Dentro do escopo #####
- Validar se `gr.Progress()` está funcionando corretamente
- Melhorar exibição de erros (cores, ícones)
- Ajustar layout para melhor legibilidade
- Testar manualmente em navegador

##### Fora do escopo #####
- Redesign completo da interface
- Migração para React/TypeScript (V2.5)
- Funcionalidades novas de negócio

#### Critérios de aceite ####
##### Cenário 1: Indicador de progresso aparece #####
Dado que inicio geração de vídeo,  
quando processo está rodando,  
então devo ver barra de progresso ou texto de status atualizado.

##### Cenário 2: Erros são exibidos claramente #####
Dado que ocorre erro na geração,  
quando erro é capturado,  
então deve ser exibido com cor de destaque e mensagem clara.

##### Cenário 3: Layout é legível #####
Dado que abro a interface,  
quando visualizo as abas,  
então texto deve ser legível e elementos bem espaçados.

#### Definition of Done ####
- [ ] `gr.Progress()` testado manualmente
- [ ] Feedback de erro melhorado (cores/ícones)
- [ ] Layout ajustado para melhor legibilidade
- [ ] Testado manualmente em navegador
- [ ] Commit realizado

#### Pontos de Planejamento (Planning Poker): **3 pontos**
*Justificativa: Alterações na interface, envolvem HTML/CSS do Gradio e possível aprendizado de gr.Progress(). Já parcialmente feito em Story 5.*

---

## Status de Desenvolvimento (Porcentagem Atualizada)

| Componente | Status Atual | Percentual | Próxima Etapa |
|------------|---------------|------------|----------------|
| **Core Pipeline** (Briefing→Roteiro→Cenas→Vídeo) | Funcional com FFmpeg | **85%** | Testes E2E completos |
| **LLM Providers** (Template+Locais) | Implementado com fallback | **90%** | Completar Strategy+Factory (História 2) ✅ |
| **Script Management** (Versão+Aprovação) | Completo | **100%** | ✅ Concluído |
| **FastAPI** (Envelope padronizado) | Implementado, testes criados | **95%** | ✅ Concluído (11 testes) |
| **UI Gradio** (http://127.0.0.1:7860) | Funcional, melhorias visuais | **95%** | História 8 (3 pts) |
| **WanGP Integration** (Opcional) | Adapter existe, falta testar | **60%** | História 6 (5 pts) |
| **FramePack Integration** (Opcional) | Planejado, não iniciado | **20%** | História 7 (8 pts) |
| **Documentação** (README + Docs) | Atualizada com links | **85%** | História 6 (seção WanGP) |
| **Testes** (Unitários + Integration) | 50+ testes passando | **85%** | História 6 e 7 (testes) |

**MVP Completo**: **90%** (faltam ajustes finais de UI e testes WanGP/FramPack opcionais)

---

## Ordem de Execução Recomendada

1. **História 6** (5 pts) - WanGP integration com testes de fallback
2. **História 8** (3 pts) - Finalizar ajustes UI (pendências da Story 5)
3. **História 7** (8 pts) - FramePack adapter (se desejar expandir)

**Total de pontos restantes**: **16 pontos** (ideal para 2-3 sprints de 1 semana cada, considerando 1 desenvolvedor)

---

## Botões da Interface - Validação

Todos os botões devem estar funcionais:
- [x] Gerar Roteiro (com progresso)
- [x] Salvar Edição
- [x] Nova Versão
- [x] Restaurar Anterior
- [x] Aprovar Roteiro
- [x] Gerar Comercial (com progresso)
- [x] Melhorar Roteiro
- [x] Tornar mais Viral
- [x] Tornar mais Premium
- [x] Tornar mais Direto
- [x] Abrir Pasta do Projeto

**Status**: Todos os botões estão implementados e devem funcionar conforme testado.
