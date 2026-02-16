# Release Bridge: Safient Forge -> openclaw-main

## Objetivo

Definir como artefatos do laboratorio (`safient-forge`) sao promovidos para o runtime (`openclaw-main`) sem drift.

## Fluxo Oficial

1. Desenvolver e validar artefato no `safient-forge`.
2. Abrir PR no `safient-forge` e aprovar mudanca.
3. Portar mudanca para `openclaw-main` via PR dedicado.
4. Validar no runtime:
   - DEV
   - RC
   - BETA
5. Executar gate final com Evidence Pack + ByteRover sync.

## Proibicoes

- Proibido deploy direto de `safient-forge` para BETA.
- Proibido `scp`/`rsync` como mecanismo regular de promocao.
- Proibido editar runtime em servidor fora de fluxo Git.

## Gate Minimo para Promocao no Runtime

- [ ] Task List
- [ ] Implementation Plan
- [ ] Walkthrough
- [ ] Evidence Pack
- [ ] `brv query`, `brv curate`, `brv push --headless -y`
- [ ] isolamento DEV/BETA confirmado
- [ ] health checks em estado OK
