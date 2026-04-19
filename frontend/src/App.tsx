import { useState } from "react";
import { startRun } from "./api/client";
import { useRunSocket } from "./hooks/useRunSocket";
import { Dashboard } from "./components/Dashboard";

function App() {
  const [runId, setRunId] = useState<string | null>(null);

  useRunSocket(runId);

  const handleRun = async () => {
    const res = await startRun();
    setRunId(res.run_id);
  };

  return (
    <div>
      <h1>SupplierSense</h1>

      <button onClick={handleRun}>
        Start Analysis
      </button>

      <Dashboard />
    </div>
  );
}

export default App;