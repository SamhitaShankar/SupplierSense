import json
from graph.pipeline import graph

def test_pipeline_runs():
    with open("data/fixtures/mock_state.json") as f:
        state = json.load(f)

    result = graph.invoke(state)

    assert result is not None
    assert "status" in result