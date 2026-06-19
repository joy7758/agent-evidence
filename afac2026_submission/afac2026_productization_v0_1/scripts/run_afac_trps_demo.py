#!/usr/bin/env python3
"""Run the local AFAC2026 TRPS productization demo."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
MODEL_VERSION = "trps_productization_demo_v0.1"
DEMO_TIMESTAMP = "2026-06-20T00:00:00Z"


def load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def stable_hash(value: object, length: int = 24) -> str:
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:length]


def utc_now() -> str:
    return DEMO_TIMESTAMP


def action_map() -> dict[str, dict[str, object]]:
    ontology = load_json(ROOT / "04_action_ontology.json")
    assert isinstance(ontology, dict)
    return {item["action_code"]: item for item in ontology["actions"]}


def policy_constraints() -> dict[str, object]:
    policy = load_json(ROOT / "05_policy_constraints.json")
    assert isinstance(policy, dict)
    return policy


def scenario_pack() -> dict[str, object]:
    pack = load_json(ROOT / "07_demo_scenarios.json")
    assert isinstance(pack, dict)
    return pack


def missing_evidence(scenario: dict[str, object]) -> bool:
    belief_state = scenario["belief_state"]
    assert isinstance(belief_state, dict)
    evidence_status = belief_state["evidence_status"]
    assert isinstance(evidence_status, dict)
    missing_items = evidence_status.get("missing_items", [])
    completeness = float(evidence_status.get("completeness", 0.0))
    return completeness < 1.0 or bool(missing_items)


def triggered_constraints(scenario: dict[str, object], policy: dict[str, object]) -> list[str]:
    risk = scenario["risk_distribution"]
    assert isinstance(risk, dict)
    triggered: list[str] = ["audit_receipt_required"]
    if scenario.get("prohibited_intent"):
        triggered.append("no_autonomous_live_trade")
    if float(risk["aggregate_risk"]) > float(scenario["risk_budget"]):
        triggered.append("max_risk_budget")
    if float(scenario["volatility_index"]) >= float(policy["high_volatility_threshold"]):
        triggered.append("mandatory_review_for_high_volatility")
    if missing_evidence(scenario):
        triggered.append("block_on_missing_evidence")
    if scenario.get("conflicting_signals"):
        triggered.append("degrade_on_conflicting_signals")
    if not scenario.get("kill_switch_available"):
        triggered.append("kill_switch_required")
    return triggered


def select_gate_action(scenario: dict[str, object], triggered: list[str]) -> str:
    if "block_on_missing_evidence" in triggered or "no_autonomous_live_trade" in triggered:
        return "BLOCK"
    if "degrade_on_conflicting_signals" in triggered:
        return "DEGRADE_TO_SAFE_MODE"
    if "max_risk_budget" in triggered and "mandatory_review_for_high_volatility" in triggered:
        return "ESCALATE"
    if "max_risk_budget" in triggered or "mandatory_review_for_high_volatility" in triggered:
        return "REVIEW_REQUIRED"
    risk = scenario["risk_distribution"]
    assert isinstance(risk, dict)
    if float(risk["aggregate_risk"]) >= 0.2:
        return "WARN"
    return "ALLOW"


def allowed_actions_by_constraint(policy: dict[str, object]) -> dict[str, set[str]]:
    result: dict[str, set[str]] = {}
    for item in policy["constraints"]:
        result[item["constraint_id"]] = set(item["allowed_gate_actions"])
    return result


def unhandled_constraints(
    action: str, triggered: list[str], policy: dict[str, object]
) -> list[str]:
    allowed = allowed_actions_by_constraint(policy)
    return [constraint for constraint in triggered if action not in allowed.get(constraint, set())]


def human_review_for(action: str, actions: dict[str, dict[str, object]]) -> dict[str, object]:
    role = str(actions[action]["human_role_required"])
    required = action in {
        "REVIEW_REQUIRED",
        "ESCALATE",
        "BLOCK",
        "DEGRADE_TO_SAFE_MODE",
        "HUMAN_OVERRIDE",
    }
    if action == "ESCALATE":
        status = "required_and_escalated_for_demo"
    elif action == "BLOCK":
        status = "required_for_block_review"
    elif action == "DEGRADE_TO_SAFE_MODE":
        status = "required_for_safe_mode_review"
    elif action == "REVIEW_REQUIRED":
        status = "required_before_next_business_step"
    else:
        status = "desk_acknowledged_for_demo"
    return {
        "required": required,
        "role": role,
        "status": status,
        "approval_scope": "simulation_only",
        "final_external_execution_authorized": False,
    }


def gate_reason(action: str, triggered: list[str]) -> str:
    if action == "BLOCK":
        return "Hard policy stopped the requested action and preserved the review receipt."
    if action == "DEGRADE_TO_SAFE_MODE":
        return "Conflicting signals were converted into a safe offline review artifact."
    if action == "ESCALATE":
        return "Risk budget pressure and high volatility require escalation."
    if action == "REVIEW_REQUIRED":
        return "Material risk pressure requires human review."
    if action == "WARN":
        return "Risk is inside budget, but receipt-level caution is preserved."
    return "No material constraint required review."


def build_receipt(
    decision_id: str,
    scenario: dict[str, object],
    triggered: list[str],
    action: str,
    human_review: dict[str, object],
    policy: dict[str, object],
) -> dict[str, object]:
    scenario_hash = stable_hash(scenario)
    receipt_base = {
        "decision_id": decision_id,
        "scenario_id": scenario["scenario_id"],
        "policy_version": policy["policy_version"],
        "scenario_hash": scenario_hash,
        "final_action": action,
        "triggered_constraints": triggered,
    }
    receipt_id = f"receipt-{stable_hash(receipt_base, 16)}"
    return {
        "receipt_id": receipt_id,
        "decision_id": decision_id,
        "model_version": MODEL_VERSION,
        "policy_version": str(policy["policy_version"]),
        "scenario_hash": scenario_hash,
        "input_summary": {
            "scenario_id": scenario["scenario_id"],
            "name_zh": scenario["name_zh"],
            "requested_operation": scenario["input"]["requested_operation"],
            "intent_class": scenario["belief_state"]["intent_class"],
        },
        "risk_summary": scenario["risk_distribution"],
        "triggered_constraints": triggered,
        "gate_decision": action,
        "human_review_status": str(human_review["status"]),
        "final_action": action,
        "rationale": gate_reason(action, triggered),
        "limitations": [
            "Local synthetic demo only.",
            "No real customer data.",
            "No investment advice.",
            "No external execution connectivity.",
            "No claim of external approval.",
        ],
        "reproducibility_hash": stable_hash(
            {
                "decision_id": decision_id,
                "scenario_hash": scenario_hash,
                "policy_version": policy["policy_version"],
                "triggered_constraints": triggered,
                "final_action": action,
            },
            32,
        ),
    }


def build_decision(
    scenario: dict[str, object],
    index: int,
    policy: dict[str, object],
    actions: dict[str, dict[str, object]],
) -> dict[str, object]:
    scenario_id = str(scenario["scenario_id"])
    decision_id = f"decision-{index + 1:02d}-{stable_hash(scenario_id, 10)}"
    triggered = triggered_constraints(scenario, policy)
    gate_action = select_gate_action(scenario, triggered)
    unhandled = unhandled_constraints(gate_action, triggered, policy)
    human_review = human_review_for(gate_action, actions)
    receipt = build_receipt(decision_id, scenario, triggered, gate_action, human_review, policy)
    deterministic_latency_ms = 12 + index * 7 + len(triggered) * 3
    return {
        "decision_id": decision_id,
        "scenario_id": scenario_id,
        "timestamp": utc_now(),
        "belief_state": scenario["belief_state"],
        "risk_distribution": scenario["risk_distribution"],
        "constrained_policy": {
            "policy_version": policy["policy_version"],
            "triggered_constraints": triggered,
            "unhandled_constraints": unhandled,
        },
        "candidate_action": scenario["candidate_action"],
        "gate_decision": {
            "action_code": gate_action,
            "decision_reason": gate_reason(gate_action, triggered),
            "policy_violation_count": len(unhandled),
            "expected_gate_decision": scenario["expected_gate_decision"],
        },
        "human_review": human_review,
        "simulated_execution": {
            "mode": "offline_synthetic_simulation",
            "executed": True,
            "actual_transaction_generated": False,
            "external_execution_connected": False,
            "execution_note": "The demo records a review outcome only.",
            "latency_ms": deterministic_latency_ms,
        },
        "receipt": receipt,
    }


def receipt_required_fields() -> list[str]:
    schema = load_json(ROOT / "06_receipt_schema.json")
    assert isinstance(schema, dict)
    return list(schema["required"])


def receipt_complete(decision: dict[str, object]) -> bool:
    receipt = decision["receipt"]
    assert isinstance(receipt, dict)
    return all(
        field in receipt and receipt[field] not in (None, "", [])
        for field in receipt_required_fields()
    )


def build_metrics(decisions: list[dict[str, object]]) -> dict[str, object]:
    scenario_count = len(decisions)
    blocked_unsafe_action_count = sum(
        1
        for decision in decisions
        if decision["gate_decision"]["action_code"] in {"BLOCK", "DEGRADE_TO_SAFE_MODE"}
    )
    mandatory_review_count = sum(
        1 for decision in decisions if decision["human_review"]["required"]
    )
    receipt_completeness_rate = (
        sum(1 for decision in decisions if receipt_complete(decision)) / scenario_count
        if scenario_count
        else 0.0
    )
    policy_violation_count = sum(
        int(decision["gate_decision"]["policy_violation_count"]) for decision in decisions
    )
    audit_trace_linkage_rate = (
        sum(
            1
            for decision in decisions
            if decision["receipt"]["decision_id"] == decision["decision_id"]
            and decision["receipt"]["scenario_hash"]
            and decision["receipt"]["reproducibility_hash"]
        )
        / scenario_count
        if scenario_count
        else 0.0
    )
    return {
        "scenario_count": scenario_count,
        "blocked_unsafe_action_count": blocked_unsafe_action_count,
        "mandatory_review_count": mandatory_review_count,
        "receipt_completeness_rate": round(receipt_completeness_rate, 4),
        "policy_violation_count": policy_violation_count,
        "average_decision_latency_ms": round(
            mean(decision["simulated_execution"]["latency_ms"] for decision in decisions), 2
        )
        if decisions
        else 0.0,
        "audit_trace_linkage_rate": round(audit_trace_linkage_rate, 4),
        "actual_transaction_generated_count": sum(
            1
            for decision in decisions
            if decision["simulated_execution"]["actual_transaction_generated"]
        ),
        "external_execution_connected": any(
            decision["simulated_execution"]["external_execution_connected"]
            for decision in decisions
        ),
    }


def build_summary(decisions: list[dict[str, object]], metrics: dict[str, object]) -> str:
    rows = [
        "| Scenario | Gate | Human Review | Receipt |",
        "| --- | --- | --- | --- |",
    ]
    for decision in decisions:
        rows.append(
            "| {scenario} | `{gate}` | `{review}` | `{receipt}` |".format(
                scenario=decision["scenario_id"],
                gate=decision["gate_decision"]["action_code"],
                review=decision["human_review"]["status"],
                receipt=decision["receipt"]["receipt_id"],
            )
        )
    metric_lines = [f"- `{key}`: `{value}`" for key, value in metrics.items()]
    return "\n".join(
        [
            "# AFAC2026 TRPS Demo Summary",
            "",
            "Status: local synthetic demo output.",
            "",
            "No real customer data, investment advice, external execution "
            "connectivity, or actual transactions are used.",
            "",
            "## Decisions",
            "",
            *rows,
            "",
            "## Metrics",
            "",
            *metric_lines,
            "",
            "## EEOAP Notes",
            "",
            "Generated receipts support local review for `EEOAP-001`, "
            "`EEOAP-003`, and `EEOAP-004`.",
            "",
        ]
    )


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    policy = policy_constraints()
    actions = action_map()
    pack = scenario_pack()
    decisions = [
        build_decision(scenario, index, policy, actions)
        for index, scenario in enumerate(pack["scenarios"])
    ]
    metrics = build_metrics(decisions)
    write_json(
        OUTPUT_DIR / "demo_receipts.json",
        {
            "generated_at": utc_now(),
            "model_version": MODEL_VERSION,
            "scenario_pack_id": pack["scenario_pack_id"],
            "decisions": decisions,
        },
    )
    write_json(OUTPUT_DIR / "demo_metrics.json", metrics)
    (OUTPUT_DIR / "demo_summary.md").write_text(build_summary(decisions, metrics), encoding="utf-8")
    print(
        json.dumps(
            {
                "ok": True,
                "scenario_count": len(decisions),
                "policy_violation_count": metrics["policy_violation_count"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
