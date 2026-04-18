from typing import TypedDict
from langgraph.graph import StateGraph, END
from agents.signal_harvester.agent import signal_harvester_agent
# Import your shared contract
from agents.interfaces import SupplierSenseState


# =========================
# STUB NODE FUNCTIONS
# =========================

def signal_harvester(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Signal Harvester")
    return state


def supplier_analyzer(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Supplier Analyzer")
    return state


def impact_modeler(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Impact Modeler")
    return state


def inventory_optimizer(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Inventory Optimizer")
    return state


def response_planner(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Response Planner")
    return state


def orchestrator(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Orchestrator")
    return state


# =========================
# CONDITIONAL LOGIC
# =========================

def check_disruption(state: SupplierSenseState) -> str:
    if state["disruption_detected"]:
        return "disruption"
    else:
        return "no_disruption"


# =========================
# BUILD GRAPH
# =========================

builder = StateGraph(SupplierSenseState)

# Add nodes
builder.add_node("signal_harvester", signal_harvester_agent)
builder.add_node("supplier_analyzer", supplier_analyzer)
builder.add_node("impact_modeler", impact_modeler)
builder.add_node("inventory_optimizer", inventory_optimizer)
builder.add_node("response_planner", response_planner)
builder.add_node("orchestrator", orchestrator)

# Define flow
builder.set_entry_point("signal_harvester")

builder.add_edge("signal_harvester", "supplier_analyzer")

# Conditional branching
builder.add_conditional_edges(
    "supplier_analyzer",
    check_disruption,
    {
        "disruption": "impact_modeler",
        "no_disruption": "orchestrator"
    }
)

builder.add_edge("impact_modeler", "inventory_optimizer")
builder.add_edge("inventory_optimizer", "response_planner")
builder.add_edge("response_planner", "orchestrator")

builder.add_edge("orchestrator", END)

# Compile graph
graph = builder.compile()


# =========================
# TEST RUN WITH MOCK STATE
# =========================

if __name__ == "__main__":
    import json

    with open("data/fixtures/mock_state.json") as f:
        state = json.load(f)

    result = graph.invoke(state)

    print("\nPipeline completed successfully!")