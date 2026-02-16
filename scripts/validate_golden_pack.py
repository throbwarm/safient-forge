#!/usr/bin/env python3
"""Validate phase 2 Golden Pack contracts for Safient Forge."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REAL_ESTATE_DIR = ROOT / "templates" / "packs" / "realestate"
TEMPLATE_DIR = ROOT / "templates" / "packs" / "_golden-template"

ERRORS: list[str] = []
WARNINGS: list[str] = []

SENSITIVE_TERMS = [
    "cpf",
    "renda",
    "holerite",
    "documento",
    "rg",
    "cnh",
    "comprovante",
]


def fail(message: str) -> None:
    ERRORS.append(message)


def warn(message: str) -> None:
    WARNINGS.append(message)


def load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"{path.relative_to(ROOT)} invalid JSON: {exc}")
        return None


def ensure_exists(paths: list[Path]) -> None:
    for path in paths:
        if not path.exists():
            fail(f"Missing required file: {path.relative_to(ROOT)}")


def ensure_pack_contract(pack: dict[str, Any]) -> None:
    required_fields = [
        "id",
        "name",
        "version",
        "workspace_overlays",
        "tool_policy",
        "entrypoints",
        "compliance",
    ]
    for field in required_fields:
        if field not in pack:
            fail(f"pack.json missing required field: {field}")

    deny = pack.get("tool_policy", {}).get("deny", [])
    allow = pack.get("tool_policy", {}).get("allow", [])

    if not isinstance(deny, list) or not isinstance(allow, list):
        fail("pack.json tool_policy.allow/deny must be arrays")
    else:
        required_deny = {"exec", "browser", "apply_patch"}
        missing_deny = sorted(required_deny - set(deny))
        if missing_deny:
            fail(f"pack.json deny list missing: {', '.join(missing_deny)}")

    entrypoints = pack.get("entrypoints", {})
    for key in ["intake", "search", "schedule", "proposal", "followup"]:
        if key not in entrypoints:
            fail(f"pack.json entrypoints missing key: {key}")

    compliance = pack.get("compliance", {})
    forbidden = compliance.get("forbidden_chat_fields", [])
    if not isinstance(forbidden, list) or len(forbidden) == 0:
        fail("pack.json compliance.forbidden_chat_fields must be a non-empty array")


def ensure_operational_policy(policy: dict[str, Any]) -> None:
    if policy.get("default_mode") != "safe":
        fail("operational-policy.json default_mode must be 'safe'")

    if policy.get("external_auto_send") is not False:
        fail("operational-policy.json external_auto_send must be false")

    assisted = policy.get("assisted_auto_actions", [])
    if not isinstance(assisted, list) or not assisted:
        fail("operational-policy.json assisted_auto_actions must be a non-empty array")

    required_confirm = policy.get("requires_confirmation_actions", [])
    if not isinstance(required_confirm, list) or not required_confirm:
        fail("operational-policy.json requires_confirmation_actions must be a non-empty array")


def ensure_lead_card_schema(schema: dict[str, Any]) -> None:
    required = set(schema.get("required", []))
    expected = {
        "lead_id",
        "timestamp",
        "client_name",
        "contact_channel",
        "intent",
        "budget_range",
        "preferred_areas",
        "status",
        "next_action",
    }
    missing = sorted(expected - required)
    if missing:
        fail(f"lead-card.schema.json missing required fields: {', '.join(missing)}")

    if schema.get("type") != "object":
        fail("lead-card.schema.json root type must be object")

    if schema.get("additionalProperties") is not False:
        fail("lead-card.schema.json must set additionalProperties=false")

    sensitive_prop_hits = []
    properties = schema.get("properties", {})
    for key in properties:
        key_l = key.lower()
        if any(term == key_l for term in SENSITIVE_TERMS):
            sensitive_prop_hits.append(key)

    if sensitive_prop_hits:
        fail(
            "lead-card.schema.json must not expose sensitive properties: "
            + ", ".join(sorted(sensitive_prop_hits))
        )


def ensure_mock_data(data: dict[str, Any]) -> None:
    props = data.get("properties", [])
    if not isinstance(props, list) or len(props) < 5:
        fail("properties.mock.json must contain at least 5 properties")
        return

    required_fields = {
        "id",
        "title",
        "area",
        "city",
        "state",
        "price_brl",
        "bedrooms",
        "bathrooms",
        "parking",
        "property_type",
        "availability",
        "source",
    }

    for idx, item in enumerate(props, start=1):
        if not isinstance(item, dict):
            fail(f"properties.mock.json property #{idx} must be an object")
            continue
        missing = sorted(required_fields - set(item.keys()))
        if missing:
            fail(f"properties.mock.json property #{idx} missing fields: {', '.join(missing)}")


def scan_strings_for_sensitive_terms(node: Any, path: str = "$") -> None:
    skip_keys = {
        "forbidden_chat_fields",
        "forbidden_fields_absent",
        "rule_summary",
        "description",
    }

    if isinstance(node, dict):
        for key, value in node.items():
            if key in skip_keys:
                continue
            scan_strings_for_sensitive_terms(value, f"{path}.{key}")
        return

    if isinstance(node, list):
        for index, value in enumerate(node):
            scan_strings_for_sensitive_terms(value, f"{path}[{index}]")
        return

    if isinstance(node, str):
        text = node.lower()
        for term in SENSITIVE_TERMS:
            if re.search(rf"\\b{re.escape(term)}\\b", text):
                fail(f"Sensitive term '{term}' found in example value at {path}")


def ensure_scenarios(scenarios_dir: Path) -> None:
    required = [
        "intake_valid.json",
        "search_results_3_to_5.json",
        "schedule_requires_confirmation.json",
        "proposal_template_output.json",
        "followup_internal_only.json",
    ]
    for name in required:
        path = scenarios_dir / name
        if not path.exists():
            fail(f"Missing required scenario: {path.relative_to(ROOT)}")
            continue

        payload = load_json(path)
        if payload is None:
            continue

        if "input" not in payload or "expected_output" not in payload:
            fail(f"{path.relative_to(ROOT)} must contain input and expected_output")

        scan_strings_for_sensitive_terms(payload)

        if name == "search_results_3_to_5.json":
            expected = payload.get("expected_output", {})
            if expected.get("result_count_min") != 3:
                fail("search_results_3_to_5 expected result_count_min must be 3")
            if expected.get("result_count_max") != 5:
                fail("search_results_3_to_5 expected result_count_max must be 5")

        if name == "schedule_requires_confirmation.json":
            expected = payload.get("expected_output", {})
            if expected.get("requires_confirmation") is not True:
                fail("schedule_requires_confirmation must require confirmation")
            if expected.get("external_action_executed") is not False:
                fail("schedule_requires_confirmation cannot auto execute external action")

        if name == "followup_internal_only.json":
            expected = payload.get("expected_output", {})
            if expected.get("outbound_auto_send") is not False:
                fail("followup_internal_only must keep outbound_auto_send=false")
            if expected.get("internal_alert") is not True:
                fail("followup_internal_only must generate internal alert")


def ensure_template_structure(template_dir: Path) -> None:
    required = [
        template_dir / "README.md",
        template_dir / "CHECKLIST.md",
        template_dir / "pack.json",
        template_dir / "operational-policy.json",
        template_dir / "schemas" / "lead-card.schema.json",
        template_dir / "data" / "domain.mock.json",
        template_dir / "scenarios" / "intake_valid.json",
        template_dir / "scenarios" / "search_results_3_to_5.json",
        template_dir / "scenarios" / "schedule_requires_confirmation.json",
        template_dir / "scenarios" / "proposal_template_output.json",
        template_dir / "scenarios" / "followup_internal_only.json",
    ]
    ensure_exists(required)


def main() -> int:
    print("Running Golden Pack validation...")

    required_realestate = [
        REAL_ESTATE_DIR / "pack.json",
        REAL_ESTATE_DIR / "operational-policy.json",
        REAL_ESTATE_DIR / "schemas" / "lead-card.schema.json",
        REAL_ESTATE_DIR / "data" / "properties.mock.json",
        REAL_ESTATE_DIR / "scenarios" / "intake_valid.json",
        REAL_ESTATE_DIR / "scenarios" / "search_results_3_to_5.json",
        REAL_ESTATE_DIR / "scenarios" / "schedule_requires_confirmation.json",
        REAL_ESTATE_DIR / "scenarios" / "proposal_template_output.json",
        REAL_ESTATE_DIR / "scenarios" / "followup_internal_only.json",
    ]
    ensure_exists(required_realestate)

    pack = load_json(REAL_ESTATE_DIR / "pack.json")
    if isinstance(pack, dict):
        ensure_pack_contract(pack)

    operational_policy = load_json(REAL_ESTATE_DIR / "operational-policy.json")
    if isinstance(operational_policy, dict):
        ensure_operational_policy(operational_policy)

    schema = load_json(REAL_ESTATE_DIR / "schemas" / "lead-card.schema.json")
    if isinstance(schema, dict):
        ensure_lead_card_schema(schema)

    mock_data = load_json(REAL_ESTATE_DIR / "data" / "properties.mock.json")
    if isinstance(mock_data, dict):
        ensure_mock_data(mock_data)

    ensure_scenarios(REAL_ESTATE_DIR / "scenarios")
    ensure_template_structure(TEMPLATE_DIR)

    for warning in WARNINGS:
        print(f"WARN: {warning}")
    for error in ERRORS:
        print(f"ERROR: {error}")

    if ERRORS:
        print(f"FAIL: {len(ERRORS)} error(s), {len(WARNINGS)} warning(s)")
        return 1

    print(f"PASS: Golden Pack validation succeeded with {len(WARNINGS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
