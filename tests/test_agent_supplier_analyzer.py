import json
from agents.supplier_analyzer.agent import supplier_analyzer_agent


def test_supplier_analyzer():
    with open("data/fixtures/mock_state.json") as f:
        state = json.load(f)

    result = supplier_analyzer_agent(state)

    assert "supplier_risk_scores" in result
    assert "supplier_profiles" in result
    assert "disruption_detected" in result