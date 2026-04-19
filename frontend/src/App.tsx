import { useState } from "react";
import "./dashboard.css";
import { startRun } from "./api/client";
import { TopNav } from "./components/layout/TopNav";
import { SignalFeed } from "./components/signals/SignalFeed";
import { useRunSocket } from "./hooks/useRunSocket";
import { useRunStore } from "./store/runStore";

type TabKey = "overview" | "suppliers" | "playbook";

function App() {
  const [activeTab, setActiveTab] = useState<TabKey>("overview");

  const runId = useRunStore((s) => s.runId);
  const status = useRunStore((s) => s.status);
  const state = useRunStore((s) => s.state);
  const error = useRunStore((s) => s.error);

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
              <div className="content-card">
                <h2>Suppliers</h2>
                <p>Supplier analysis components will go here next.</p>
              </div>
            )}

            {activeTab === "playbook" && (
              <div className="content-card">
                <h2>Playbook</h2>
                <p>Response planning and mitigation steps will go here later.</p>
              </div>
            )}

            {error && (
              <div className="error-box">
                {error}
              </div>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}

export default App;