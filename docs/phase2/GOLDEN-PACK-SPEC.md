# Phase 2 Spec - RealEstate Golden Pack (Mock-first)

## Objective

Define RealEstate as the canonical Golden Pack for future vertical replication.

## Scope

- Full pack contract (`pack.json`, `operational-policy.json`, lead schema)
- Mock data source (`properties.mock.json`)
- Functional scenarios for intake/search/schedule/proposal/followup
- Reusable `_golden-template`
- Automatic gate validation scripts

## Contract Summary

### Pack contract

File: `templates/packs/realestate/pack.json`

Required sections:

- `id`, `name`, `version`
- `workspace_overlays`
- `tool_policy.allow`, `tool_policy.deny`
- `entrypoints` for: intake/search/schedule/proposal/followup
- `compliance` with forbidden fields and safe-chat rules

### Operational policy

File: `templates/packs/realestate/operational-policy.json`

Hard rules:

- `default_mode = safe`
- `external_auto_send = false`
- assisted automation is internal-only for phase 2
- critical actions always require explicit confirmation

### Lead card schema

File: `templates/packs/realestate/schemas/lead-card.schema.json`

Hard rules:

- No sensitive document fields in chat payload
- `additionalProperties = false`
- Required operational fields only

## Scenario Set (mock-first)

Files:

- `intake_valid.json`
- `search_results_3_to_5.json`
- `schedule_requires_confirmation.json`
- `proposal_template_output.json`
- `followup_internal_only.json`

Expected behavior:

1. Intake creates a valid lead card.
2. Search returns 3 to 5 options when dataset supports it.
3. Schedule creates draft + confirmation request (no auto external action).
4. Proposal returns standard draft template.
5. Followup automation generates internal alert only.

## Compliance

Forbidden sensitive collection in chat examples:

- cpf
- renda and income proof fields
- identity document fields

## Gate Command

Run from repo root:

```bash
scripts/run_phase2_gate.sh
```

Outputs:

- `evidence/phase2-golden-pack/validator.log`
- `evidence/phase2-golden-pack/report.md`
