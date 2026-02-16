# Skills Shortlist - Phase 2 (RealEstate Golden Pack)

| skill_id | fit_realestate | risk | dependencies | decision_next |
|---|---|---|---|---|
| weather-1.0.0 | High for visit-day planning and client context | Low | none | Evaluate in Phase 3 DEV only |
| portuguese-1.0.0 | High for language normalization in BR market | Low | none | Evaluate in Phase 3 DEV only |
| openclaw-safety-coach-1.0.4 | High for policy and guardrail support | Medium | policy prompt integration | Keep as policy reference |
| local-places | Medium for neighborhood context and POI hints | Medium | external maps API if enabled | Keep mock-only until V2 |
| openai-whisper-api | Medium for voice note ingestion | Medium | OpenAI key, audio pipeline | Defer until voice backlog |
| voice-call | Medium for future assisted calling | High | telephony bridge, credentials | Defer to post-Golden Pack |
| session-logs | Medium for audit and troubleshooting | Low | filesystem access | Evaluate for ops-only use |
| memory-manager-1.0.0 | Medium for context retention hygiene | Medium | shell scripts, process policy | Evaluate in controlled sandbox |

## Notes

- No skill outside this shortlist enters the Golden Pack in Phase 2.
- Shortlist is intentionally limited to protect delivery focus.
