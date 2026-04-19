from agents.interfaces import SupplierSenseState
from agents.inventory_optimizer.tools import (
    find_alternate_suppliers,
    calculate_reorder_quantity,
    calculate_safety_stock,
    check_budget_availability,
    rank_alternate_suppliers,
    generate_emergency_po_draft,
)


def inventory_optimizer_agent(state: SupplierSenseState) -> SupplierSenseState:
    print("Running Inventory Optimizer")

    impacted_skus = state.get("impacted_skus", [])

    reorder_recommendations = []
    safety_stock_adjustments = []

    for sku in impacted_skus:
        demand = sku.get("avg_daily_demand", 100)
        ordering_cost = 50
        holding_cost = 5
        lead_time = sku.get("stockout_days", 10)
        demand_std_dev = 5

        reorder_qty = calculate_reorder_quantity.invoke(
            {
                "demand": demand,
                "ordering_cost": ordering_cost,
                "holding_cost": holding_cost,
            }
        )

        safety_stock = calculate_safety_stock.invoke(
            {
                "z": 1.65,
                "lead_time": lead_time,
                "demand_std_dev": demand_std_dev,
            }
        )

        alternates = find_alternate_suppliers.invoke(
            {"supplier_id": sku.get("supplier_id", "SUP001")}
        )

        ranked = rank_alternate_suppliers.invoke({"suppliers": alternates})
        best_supplier = ranked[0] if ranked else None

        if best_supplier:
            budget_ok = check_budget_availability.invoke(
                {"amount": reorder_qty * best_supplier["price"]}
            )

            if budget_ok:
                po = generate_emergency_po_draft.invoke(
                    {
                        "supplier_id": best_supplier["supplier_id"],
                        "quantity": reorder_qty,
                    }
                )
                reorder_recommendations.append(po)

        safety_stock_adjustments.append(
            {
                "sku_id": sku.get("sku_id"),
                "recommended_safety_stock": safety_stock,
            }
        )

    state["reorder_recommendations"] = reorder_recommendations
    state["safety_stock_adjustments"] = safety_stock_adjustments

    return state