# Golden Template Checklist

- [ ] `pack.json` updated with final `id`, `name`, `version`
- [ ] `tool_policy.deny` contains `exec`, `browser`, `apply_patch`
- [ ] `operational-policy.json` uses `default_mode = safe`
- [ ] `external_auto_send` remains `false` in early phases
- [ ] Lead schema blocks sensitive fields in chat
- [ ] Mock dataset contains only fake records
- [ ] Scenarios exist for intake/search/schedule/proposal/followup
- [ ] `scripts/validate_golden_pack.py` passes
- [ ] Evidence generated in `evidence/phase2-golden-pack/`
