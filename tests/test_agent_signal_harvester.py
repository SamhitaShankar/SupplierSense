import json
import os
import sys

# Add project root to Python path so pytest can import "agents"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents.signal_harvester.agent import signal_harvester_agent


def test_signal_harvester_writes_expected_keys_only():
    initial_state = {
        "raw_signals": [],
        "signal_summary": "",
        "supplier_risk_scores": {},
        "supplier_profiles": {},
        "disruption_detected": False,
        "affected_suppliers": [],
        "impacted_skus": [],
        "total_revenue_at_risk": 0.0,
        "impact_severity": "low",
        "reorder_recommendations": [],
        "safety_stock_adjustments": {},
        "playbook": {
            "run_id": "test-run",
            "severity": "low",
            "executive_summary": "",
            "actions": [],
            "supplier_comms": [],
            "internal_alerts": [],
            "escalate_to": [],
        },
        "escalation_required": False,
        "run_id": "test-run",
        "triggered_at": "2026-04-17T00:00:00Z",
        "status": "running",
        "error_log": [],
    }

    result = signal_harvester_agent(initial_state)

    assert "raw_signals" in result
    assert "signal_summary" in result
    assert isinstance(result["raw_signals"], list)
    assert isinstance(result["signal_summary"], str)
    assert len(result["raw_signals"]) > 0

    first = result["raw_signals"][0]
    required_keys = {
        "id",
        "type",
        "source",
        "raw_text",
        "severity",
        "affected_region",
        "affected_commodities",
        "timestamp",
        "confidence",
    }
    assert required_keys.issubset(first.keys())


def test_signal_harvester_preserves_unrelated_state():
    initial_state = {
        "raw_signals": [],
        "signal_summary": "",
        "supplier_risk_scores": {"SUP-1": 0.3},
        "supplier_profiles": {},
        "disruption_detected": False,
        "affected_suppliers": [],
        "impacted_skus": [],
        "total_revenue_at_risk": 0.0,
        "impact_severity": "low",
        "reorder_recommendations": [],
        "safety_stock_adjustments": {},
        "playbook": {
            "run_id": "test-run",
            "severity": "low",
            "executive_summary": "",
            "actions": [],
            "supplier_comms": [],
            "internal_alerts": [],
            "escalate_to": [],
        },
        "escalation_required": False,
        "run_id": "test-run",
        "triggered_at": "2026-04-17T00:00:00Z",
        "status": "running",
        "error_log": [],
    }

    result = signal_harvester_agent(initial_state)

    assert result["supplier_risk_scores"] == {"SUP-1": 0.3}
    assert result["run_id"] == "test-run"
    assert result["status"] == "running"