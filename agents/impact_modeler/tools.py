from __future__ import annotations

from typing import Any, List, Dict
from datetime import datetime, timedelta
import random

# If you already have a DB helper, import it:
# from core.db import get_db_connection

# -----------------------------
# STUB / DB-LIKE HELPERS
# -----------------------------

def get_skus_for_supplier(supplier_id: str) -> List[Dict[str, Any]]:
    """
    Return SKUs supplied by a supplier.
    Replace with DB query later.
    """
    # stub
    return [
        {"sku_id": f"{supplier_id}-SKU1", "name": "Microcontroller Unit", "unit_price": 1200},
        {"sku_id": f"{supplier_id}-SKU2", "name": "PCB Board", "unit_price": 800},
    ]


def get_current_inventory(sku_id: str) -> Dict[str, Any]:
    """
    Return current stock and 30-day demand history.
    """
    # stub realistic numbers
    daily_history = [random.randint(5, 20) for _ in range(30)]
    return {
        "sku_id": sku_id,
        "current_stock": random.randint(50, 200),
        "demand_history": daily_history,
    }


def forecast_demand(demand_history: List[int]) -> float:
    """
    Simple average demand (replace with Prophet later if needed).
    """
    if not demand_history:
        return 0.0
    return sum(demand_history) / len(demand_history)


def calculate_stockout_days(stock: int, avg_daily_demand: float) -> float:
    """
    Days before stockout.
    """
    if avg_daily_demand <= 0:
        return float("inf")
    return stock / avg_daily_demand


def calculate_revenue_at_risk(
    avg_daily_demand: float,
    unit_price: float,
    disruption_days: int = 7,
) -> float:
    """
    Revenue lost during disruption window.
    """
    return avg_daily_demand * unit_price * disruption_days


def classify_severity(total_revenue_at_risk: float) -> str:
    """
    Deterministic severity classification.
    """
    if total_revenue_at_risk > 500000:
        return "high"
    elif total_revenue_at_risk > 100000:
        return "medium"
    else:
        return "low"


def run_impact_simulation(supplier_id: str) -> Dict[str, Any]:
    """
    Full simulation for a supplier.
    """
    skus = get_skus_for_supplier(supplier_id)

    impacted_skus = []
    total_revenue = 0.0

    for sku in skus:
        inv = get_current_inventory(sku["sku_id"])
        avg_demand = forecast_demand(inv["demand_history"])
        stockout_days = calculate_stockout_days(inv["current_stock"], avg_demand)

        revenue_risk = calculate_revenue_at_risk(avg_demand, sku["unit_price"])

        impacted_skus.append({
            "sku_id": sku["sku_id"],
            "stock": inv["current_stock"],
            "avg_daily_demand": round(avg_demand, 2),
            "stockout_days": round(stockout_days, 2),
            "revenue_at_risk": round(revenue_risk, 2),
        })

        total_revenue += revenue_risk

    severity = classify_severity(total_revenue)

    return {
        "supplier_id": supplier_id,
        "impacted_skus": impacted_skus,
        "total_revenue_at_risk": round(total_revenue, 2),
        "impact_severity": severity,
    }