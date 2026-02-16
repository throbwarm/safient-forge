# Safient Forge

Laboratorio de criacao e evolucao de packs verticais (core + templates + skills) para o ecossistema Safient.

## Objetivo

- Desenvolver e testar componentes reutilizaveis para verticais (ex.: realestate, travel, education, legal).
- Preparar artefatos para promocao controlada ao runtime (`openclaw-main`).
- Evitar acoplamento entre laboratorio e ambiente operacional.

## Regras

1. Este repositorio nao faz deploy direto em BETA.
2. Promocao para runtime so via PR no `openclaw-main`.
3. Sem sync manual de producao (`scp`/`rsync`) para deploy regular.
4. Toda skill nova entra em `skills/incoming/` e passa por gate.

## Estrutura

- `templates/` - core e packs verticais
- `skills/` - pipeline incoming/approved/rejected
- `registry/` - mapas de packs e contratos
- `scripts/` - automacao local do laboratorio
- `docs/` - runbooks e ponte de release

## Ponte Oficial de Release

Ver `docs/RELEASE-BRIDGE.md`.
