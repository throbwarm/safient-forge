# Phase 3 Runtime Bridge Plan (Forge -> openclaw-main)

## Objective

Promote validated Golden Pack artifacts from Safient Forge to runtime without drift.

## Bridge Principle

- Forge is lab-only.
- Runtime receives artifacts only through PR in `openclaw-main`.
- No direct server sync (`scp`/`rsync`) for normal promotion.

## Artifacts to bridge

1. `templates/packs/realestate/pack.json`
2. `templates/packs/realestate/operational-policy.json`
3. `templates/packs/realestate/schemas/lead-card.schema.json`
4. `templates/packs/realestate/data/properties.mock.json`
5. `templates/packs/realestate/scenarios/*.json`
6. Optional gate script subset adapted for runtime CI

## PR Order

1. PR-A (contracts only): pack + policy + schema.
2. PR-B (mock data + scenarios): functional fixtures.
3. PR-C (runtime wiring): init/apply/render integration and tests.

## Minimum DEV validations before RC

- Import and schema checks pass.
- Behavior checks for 5 required scenarios pass.
- Policy guardrail checks pass (no external auto-send).
- Health checks remain green.

## RC gate before BETA

- DEV -> RC promotion completed.
- Evidence Pack attached.
- ByteRover sync complete (`query`, `curate`, `push --headless -y`).
- CTO + CEO approval logged.

## Out of scope for Phase 3

- Real external CRM integration.
- Multi-tenant workspace migration.
- Outbound client automation without confirmation.
