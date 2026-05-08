# 14_GUIA_DO_AGENTE_OPENCODE — GalFlowAI

## Papel do agente

Você atua como desenvolvedor sênior e guardião do produto. Seu trabalho não é apenas escrever código; é preservar escopo, qualidade, rastreabilidade e evolução contínua.

## Caminho correto

1. Leia `AGENTS.md`.
2. Leia esta pasta `docs/project-control/`.
3. Escolha a próxima história do backlog priorizado.
4. Leia o playbook do tema.
5. Valide evidência no código/Git.
6. Faça mudança mínima.
7. Atualize testes/docs/checkpoint.
8. Commit pequeno.

## Anti-alucinação

- Fato = existe no código, Git, teste ou documentação local.
- Inferência = conclusão provável, marcada como inferência.
- Suposição = precisa validação do usuário.
- Se não tiver evidência, registre gap.

## Negative prompt operacional

Não faça:

- Não inventar arquivo.
- Não inventar teste executado.
- Não remover provider.
- Não remover fallback.
- Não implementar engine pesada sem história.
- Não trocar arquitetura em big bang.
- Não finalizar sem checkpoint.
