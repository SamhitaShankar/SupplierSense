import json
from agents.impact_modeler.agent import impact_modeler_agent


def test_impact_modeler():
    with open("data/fixtures/mock_state.json") as f:
        state = json.load(f)

    # ensure there is at least one affected supplier
    state["affected_suppliers"] = ["SUP001"]

    result = impact_modeler_agent(state)

    assert "impacted_skus" in result
    assert "total_revenue_at_risk" in result
    assert "impact_severity" in result