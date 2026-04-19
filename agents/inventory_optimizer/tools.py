import math
from typing import List, Dict
from langchain_core.tools import tool


ALTERNATE_SUPPLIERS = [
    {
        "supplier_id": "ALT001",
        "lead_time": 10,
        "reliability": 0.9,
        "price": 100,
    },
    {
        "supplier_id": "ALT002",
        "lead_time": 7,
        "reliability": 0.8,
        "price": 110,
    },
]


@tool
def find_alternate_suppliers(supplier_id: str) -> List[Dict]:
    """Find alternate suppliers for a disrupted supplier."""
    return ALTERNATE_SUPPLIERS


@tool
def calculate_reorder_quantity(
    demand: float,
    ordering_cost: float,
    holding_cost: float,
) -> float:
    """Calculate reorder quantity using the EOQ formula."""
    if holding_cost == 0:
        return 0.0
    return math.sqrt((2 * demand * ordering_cost) / holding_cost)


@tool
def calculate_safety_stock(
    z: float,
    lead_time: float,
    demand_std_dev: float,
) -> float:
    """Calculate safety stock using z * sqrt(lead_time) * demand_std_dev."""
    return z * math.sqrt(lead_time) * demand_std_dev


@tool
def check_budget_availability(amount: float) -> bool:
    """Mock finance check for whether emergency procurement budget is available."""
    return amount < 1_000_000


@tool
def rank_alternate_suppliers(suppliers: List[Dict]) -> List[Dict]:
    """Rank alternate suppliers using weighted score: 40% lead time, 40% reliability, 20% price."""
    ranked = []

    for supplier in suppliers:
        lead_time_score = 1 / supplier["lead_time"] if supplier["lead_time"] > 0 else 0
        reliability_score = supplier["reliability"]
        price_score = 1 / supplier["price"] if supplier["price"] > 0 else 0

        total_score = (
            0.4 * lead_time_score
            + 0.4 * reliability_score
            + 0.2 * price_score
        )

        ranked.append(
            {
                **supplier,
                "score": total_score,
            }
        )

    return sorted(ranked, key=lambda x: x["score"], reverse=True)


@tool
def generate_emergency_po_draft(supplier_id: str, quantity: float) -> Dict:
    """Generate a mock emergency purchase order draft."""
    return {
        "supplier_id": supplier_id,
        "quantity": quantity,
        "status": "draft",
    }