import { useRunStore } from "../store/runStore";

const getStockoutColor = (days: number) => {
  if (days <= 3) return "text-red-600";
  if (days <= 7) return "text-amber-600";
  return "text-green-600";
};

const getSeverityLabel = (value?: string) => {
  if (!value) return "Medium"; // fallback
  return value;
};

export default function SKUImpactGrid() {
  const state = useRunStore((s) => s.state);

  const impactedSKUs = state?.impacted_skus ?? [];

  if (!impactedSKUs.length) {
    return (
      <div className="bg-white rounded-2xl shadow p-4 mt-4">
        <h2 className="text-xl font-semibold mb-4">SKU Impact Grid</h2>
        <p className="text-gray-500 text-sm">No impacted SKUs detected.</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl shadow p-4 mt-4">
      <h2 className="text-xl font-semibold mb-4">SKU Impact Grid</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {impactedSKUs.map((sku, index) => {
          const skuName =
            sku.product_name ||
            sku.sku_name ||
            sku.sku_id ||
            `SKU-${index + 1}`;

          const stockoutDays =
            sku.stockout_days ??
            sku.days_to_stockout ??
            sku.days_until_stockout ??
            null;

          const revenueAtRisk = Number(sku.revenue_at_risk ?? 0);

          const severity =
            sku.severity ||
            sku.risk_level ||
            (stockoutDays && stockoutDays <= 5
              ? "High"
              : stockoutDays && stockoutDays <= 10
              ? "Medium"
              : "Low");

          return (
            <div
              key={sku.sku_id || index}
              className="border rounded-xl p-4 shadow-sm bg-gray-50"
            >
              <h3 className="text-lg font-semibold mb-2">{skuName}</h3>

              <div className="text-sm space-y-2">
                <p>
                  <span className="font-medium">Risk Level:</span>{" "}
                  {getSeverityLabel(severity)}
                </p>

                <p>
                  <span className="font-medium">Days Until Stockout:</span>{" "}
                  <span
                    className={
                      stockoutDays !== null
                        ? getStockoutColor(stockoutDays)
                        : ""
                    }
                  >
                    {stockoutDays ?? "N/A"}
                  </span>
                </p>

                <p>
                  <span className="font-medium">Revenue at Risk:</span>{" "}
                  ₹{revenueAtRisk.toLocaleString("en-IN")}
                </p>

                <p>
                  <span className="font-medium">Supplier:</span>{" "}
                  {sku.supplier_name || sku.supplier_id || "N/A"}
                </p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}