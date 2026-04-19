from langchain_core.tools import tool

from agents.shared_tools.supplier_tools import (
    lookup_supplier_by_region,
    query_supplier_history,
    enrich_supplier_profile,
)
from agents.shared_tools.rag import rag_similarity_search


@tool
def calculate_risk_score(signal_event: dict, supplier_profile: dict) -> dict:
    """
    Calculate a supplier risk score using signal severity, confidence,
    supplier match, and disruption history.
    """
    supplier = supplier_profile["supplier"]
    history = supplier_profile["recent_disruptions"]

    score = float(signal_event.get("severity", 0.0)) * 0.4

    if supplier.get("region") == signal_event.get("affected_region"):
        score += 0.2

    if supplier.get("primary_commodity") in signal_event.get("affected_commodities", []):
        score += 0.15

    if len(history) > 0:
        score += 0.1

    if float(signal_event.get("confidence", 0.0)) > 0.8:
        score += 0.1

    score = min(score, 1.0)

    return {
        "supplier_id": supplier["supplier_id"],
        "supplier_name": supplier["supplier_name"],
        "risk_score": round(score, 3),
    }


@tool
def flag_disruption(risk_score: float, threshold: float = 0.65) -> bool:
    """
    Return True if the supplier risk score crosses the disruption threshold.
    """
    return risk_score >= threshold