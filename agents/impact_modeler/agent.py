from agents.interfaces import SupplierSenseState
from agents.impact_modeler.tools import run_impact_simulation


def impact_modeler_agent(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Impact Modeler")

    affected_suppliers = state.get("affected_suppliers", [])

    all_impacted_skus = []
    total_revenue = 0.0
    severities = []

    for supplier_id in affected_suppliers:
        result = run_impact_simulation(supplier_id)

        all_impacted_skus.extend(result["impacted_skus"])
        total_revenue += result["total_revenue_at_risk"]
        severities.append(result["impact_severity"])

    # overall severity (simple rule)
    if "high" in severities:
        overall = "high"
    elif "medium" in severities:
        overall = "medium"
    else:
        overall = "low"

    state["impacted_skus"] = all_impacted_skus
    state["total_revenue_at_risk"] = round(total_revenue, 2)
    state["impact_severity"] = overall

    return state