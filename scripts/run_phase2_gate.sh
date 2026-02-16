#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
EVIDENCE_DIR="$ROOT/evidence/phase2-golden-pack"
LOG_FILE="$EVIDENCE_DIR/validator.log"
REPORT_FILE="$EVIDENCE_DIR/report.md"
TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

mkdir -p "$EVIDENCE_DIR"

STATUS="PASS"
if python3 "$ROOT/scripts/validate_golden_pack.py" | tee "$LOG_FILE"; then
  STATUS="PASS"
else
  STATUS="FAIL"
fi

ERROR_COUNT="$(grep -c '^ERROR:' "$LOG_FILE" || true)"
WARN_COUNT="$(grep -c '^WARN:' "$LOG_FILE" || true)"

cat > "$REPORT_FILE" <<REPORT
# Phase 2 Golden Pack Gate Report

- Timestamp (UTC): $TIMESTAMP
- Status: $STATUS
- Error count: $ERROR_COUNT
- Warning count: $WARN_COUNT
- Validator script: \`scripts/validate_golden_pack.py\`
- Scope: \`templates/packs/realestate\` + \`templates/packs/_golden-template\`

## Validator Output

\`\`\`text
$(cat "$LOG_FILE")
\`\`\`
REPORT

if [[ "$STATUS" != "PASS" ]]; then
  echo "Gate failed. See $REPORT_FILE"
  exit 1
fi

echo "Gate passed. Report generated at $REPORT_FILE"
