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

    seen_supplier_ids = set()
    seen_score_pairs = set()

    for signal in raw_signals:
        region = signal.get("affected_region")
        commodities = signal.get("affected_commodities", []) or []

        matched_suppliers = []

        if commodities:
            for commodity in commodities:
                matched_suppliers.extend(
                    lookup_supplier_by_region(region, commodity)
                )

        if not matched_suppliers:
            matched_suppliers = lookup_supplier_by_region(region, None)

        unique_suppliers = {}
        for supplier in matched_suppliers:
            unique_suppliers[supplier["supplier_id"]] = supplier

        for supplier in unique_suppliers.values():
            supplier_id = supplier["supplier_id"]

            profile = enrich_supplier_profile(supplier_id, 5)

            if supplier_id not in seen_supplier_ids:
                supplier_profiles.append(profile["supplier"])
                seen_supplier_ids.add(supplier_id)

            score_obj = calculate_risk_score.invoke(
                {
                    "signal_event": signal,
                    "supplier_profile": profile,
                }
            )

            score_key = (
                score_obj["supplier_id"],
                signal.get("id") or signal.get("signal_id") or signal.get("timestamp"),
            )

            if score_key not in seen_score_pairs:
                supplier_scores.append(score_obj)
                seen_score_pairs.add(score_key)

            is_disrupted = flag_disruption.invoke(
                {
                    "risk_score": score_obj["risk_score"],
                    "threshold": 0.5,
                }
            )

            if is_disrupted:
                disruption_detected = True
                affected_suppliers.append(supplier_id)

    state["supplier_risk_scores"] = supplier_scores
    state["supplier_profiles"] = supplier_profiles
    state["disruption_detected"] = disruption_detected
    state["affected_suppliers"] = sorted(list(set(affected_suppliers)))

    return state