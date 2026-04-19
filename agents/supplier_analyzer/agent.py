from agents.interfaces import SupplierSenseState
from agents.supplier_analyzer.tools import (
    calculate_risk_score,
    flag_disruption,
)
from agents.shared_tools.supplier_tools import (
    lookup_supplier_by_region,
    enrich_supplier_profile,
)


def supplier_analyzer_agent(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Supplier Analyzer")

    raw_signals = state.get("raw_signals", [])

    supplier_scores = []
    supplier_profiles = []
    affected_suppliers = []
    disruption_detected = False

    for signal in raw_signals:
        region = signal.get("affected_region")
        commodities = signal.get("affected_commodities", [])

        suppliers = lookup_supplier_by_region(region, None)

        for supplier in suppliers:
            supplier_id = supplier["supplier_id"]

            profile = enrich_supplier_profile(supplier_id, 5)

            supplier_profiles.append(profile)

            score_obj = calculate_risk_score(signal, profile)

            supplier_scores.append(score_obj)

            if flag_disruption(score_obj["risk_score"], 0.65):
                disruption_detected = True
                affected_suppliers.append(supplier_id)

    state["supplier_risk_scores"] = supplier_scores
    state["supplier_profiles"] = supplier_profiles
    state["disruption_detected"] = disruption_detected
    state["affected_suppliers"] = list(set(affected_suppliers))

    return state