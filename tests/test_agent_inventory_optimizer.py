import json
from agents.inventory_optimizer.agent import inventory_optimizer_agent


def test_inventory_optimizer():
    with open("data/fixtures/mock_state.json") as f:
        state = json.load(f)

    result = inventory_optimizer_agent(state)

    assert "reorder_recommendations" in result
    assert "safety_stock_adjustments" in result