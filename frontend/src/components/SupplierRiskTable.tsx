import { useRunStore } from "../store/runStore";

const getRiskColor = (score: number) => {
  if (score < 0.4) return "bg-green-500";
  if (score <= 0.65) return "bg-amber-500";
  return "bg-red-500";
};

const getRiskLabel = (score: number) => {
  if (score < 0.4) return "Low";
  if (score <= 0.65) return "Medium";
  return "High";
};

export default function SupplierRiskTable() {
  const state = useRunStore((s) => s.state);

  const supplierProfiles = state?.supplier_profiles ?? [];
  const supplierRiskScores = state?.supplier_risk_scores ?? [];

  const mergedRows = supplierProfiles.map((profile) => {
    const scoreEntry = supplierRiskScores.find(
      (item) => item.supplier_id === profile.supplier_id
    );

    return {
      supplier_id: profile.supplier_id,
      supplier_name: profile.supplier_name,
      tier: profile.tier ?? "--",
      commodities: profile.commodities ?? [],
      risk_score: Number(scoreEntry?.risk_score ?? profile.risk_score ?? 0),
    };
  });

  const sortedRows = [...mergedRows].sort((a, b) => b.risk_score - a.risk_score);

  return (
    <div className="bg-white rounded-2xl shadow p-4">
      <h2 className="text-xl font-semibold mb-4">Supplier Risk Table</h2>

      <div className="overflow-x-auto">
        <table className="w-full border-collapse text-sm">
          <thead>
            <tr className="text-left border-b">
              <th className="py-3 px-2">Supplier</th>
              <th className="py-3 px-2">Tier</th>
              <th className="py-3 px-2">Risk Score</th>
              <th className="py-3 px-2">Affected Commodities</th>
            </tr>
          </thead>

          <tbody>
            {sortedRows.length === 0 ? (
              <tr>
                <td colSpan={4} className="py-4 px-2 text-gray-500">
                  No supplier risk data available.
                </td>
              </tr>
            ) : (
              sortedRows.map((row) => (
                <tr key={row.supplier_id} className="border-b align-top">
                  <td className="py-3 px-2 font-medium">{row.supplier_name}</td>
                  <td className="py-3 px-2">{row.tier}</td>

                  <td className="py-3 px-2 min-w-[240px]">
                    <div className="flex items-center gap-3">
                      <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                        <div
                          className={`h-3 ${getRiskColor(row.risk_score)}`}
                          style={{
                            width: `${Math.min(row.risk_score * 100, 100)}%`,
                          }}
                        />
                      </div>

                      <span className="w-24 text-xs font-medium">
                        {row.risk_score.toFixed(2)} ({getRiskLabel(row.risk_score)})
                      </span>
                    </div>
                  </td>

                  <td className="py-3 px-2">
                    {row.commodities.length === 0 ? (
                      <span className="text-gray-400 text-xs">No commodities</span>
                    ) : (
                      <span className="text-gray-700 text-sm">
                        {row.commodities.join(", ")}
                      </span>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}