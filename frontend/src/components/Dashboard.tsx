import { useRunStore } from "../store/runStore";

export const Dashboard = () => {
  const state = useRunStore((s) => s.state);

  if (!state) return <div>Waiting for data...</div>;

  return (
    <div>
      <h2>SupplierSense Dashboard</h2>

      <pre style={{ textAlign: "left" }}>
        {JSON.stringify(state, null, 2)}
      </pre>
    </div>
  );
};