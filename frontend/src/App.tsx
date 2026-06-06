import { useState } from "react";
import "./dashboard.css";
import { startRun } from "./api/client";
import { TopNav } from "./components/layout/TopNav";
import { SignalFeed } from "./components/signals/SignalFeed";
import SupplierRiskTable from "./components/SupplierRiskTable";
import SKUImpactGrid from "./components/SKUImpactGrid";
import { useRunSocket } from "./hooks/useRunSocket";
import { useRunStore } from "./store/runStore";

type TabKey = "overview" | "suppliers" | "playbook";

function App() {
  const [activeTab, setActiveTab] = useState<TabKey>("overview");

  const runId = useRunStore((s) => s.runId);
  const status = useRunStore((s) => s.status);
  const state = useRunStore((s) => s.state);
  const error = useRunStore((s) => s.error);

  console.log("FULL STATE:", state);
  console.log("supplier_profiles raw:", state?.supplier_profiles);
  console.log("supplier_profiles isArray:", Array.isArray(state?.supplier_profiles));
  console.log("supplier_profiles values:", Object.values(state?.supplier_profiles ?? {}));

  console.log("supplier_risk_scores raw:", state?.supplier_risk_scores);
  console.log("supplier_risk_scores isArray:", Array.isArray(state?.supplier_risk_scores));
  console.log("supplier_risk_scores values:", Object.values(state?.supplier_risk_scores ?? {}));

  console.log("impacted_skus raw:", state?.impacted_skus);
  console.log("impacted_skus isArray:", Array.isArray(state?.impacted_skus));

  const setRunId = useRunStore((s) => s.setRunId);
  const setStatus = useRunStore((s) => s.setStatus);
  const setError = useRunStore((s) => s.setError);

  useRunSocket(runId);

  const handleRun = async () => {
    try {
      setError(null);
      setStatus("queued");

      const res = await startRun();
      setRunId(res.run_id);
      setStatus(res.status as "queued");
    } catch (err) {
      console.error(err);
      setStatus("failed");
      setError("Could not start analysis run");
    }
  };

  return (
    <div className="app-shell">
      <TopNav onStartRun={handleRun} status={status} runId={runId} />

      <div className="dashboard-layout">
        <aside className="left-panel">
          <SignalFeed />
        </aside>

        <main className="main-panel">
          <div className="tabs-row">
            <button
              className={activeTab === "overview" ? "tab active-tab" : "tab"}
              onClick={() => setActiveTab("overview")}
            >
              Overview
            </button>

            <button
              className={activeTab === "suppliers" ? "tab active-tab" : "tab"}
              onClick={() => setActiveTab("suppliers")}
            >
              Suppliers
            </button>

            <button
              className={activeTab === "playbook" ? "tab active-tab" : "tab"}
              onClick={() => setActiveTab("playbook")}
            >
              Playbook
            </button>
          </div>

          <section className="tab-content">
            {activeTab === "overview" && (
              <div className="content-card">
                <h2>Overview</h2>
                <p>
                  {state?.signal_summary ??
                    "Signal summary will appear here after analysis."}
                </p>
                <p>
                  <strong>Disruption detected:</strong>{" "}
                  {String(state?.disruption_detected ?? false)}
                </p>
              </div>
            )}

            {activeTab === "suppliers" && (
              <div className="suppliers-tab-layout">
                <div className="content-card">
                  <h2>Supplier Risk Table</h2>
                  <SupplierRiskTable />
                </div>

                <div className="content-card">
                  <h2>SKU Impact Grid</h2>
                  <SKUImpactGrid />
                </div>
              </div>
            )}

            {activeTab === "playbook" && (
              <div className="content-card">
                <h2>Playbook</h2>
                <p>Response planning and mitigation steps will go here later.</p>
              </div>
            )}

            {error && <div className="error-box">{error}</div>}
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;