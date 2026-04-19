import type { RunStatus } from "../../store/runStore";

type TopNavProps = {
  onStartRun: () => Promise<void>;
  status: RunStatus;
  runId: string | null;
};

const getStatusColor = (status: RunStatus) => {
  switch (status) {
    case "queued":
      return "#f59e0b";
    case "running":
      return "#2563eb";
    case "completed":
      return "#16a34a";
    case "failed":
      return "#dc2626";
    default:
      return "#6b7280";
  }
};

export const TopNav = ({ onStartRun, status, runId }: TopNavProps) => {
  return (
    <header className="top-nav">
      <div>
        <h1 className="app-title">SupplierSense</h1>
        <p className="app-subtitle">Supply chain intelligence dashboard</p>
      </div>

      <div className="top-nav-actions">
        <div
          className="status-badge"
          style={{ backgroundColor: getStatusColor(status) }}
        >
          {status.toUpperCase()}
        </div>

        <button className="start-button" onClick={onStartRun}>
          Start Analysis
        </button>
      </div>

      <div className="run-id-text">
        {runId ? `Run ID: ${runId}` : "No run started yet"}
      </div>
    </header>
  );
};