export const startRun = async () => {
  const res = await fetch("http://127.0.0.1:8000/run", {
    method: "POST",
  });
  return res.json();
};

export const getRun = async (runId: string) => {
  const res = await fetch(`http://127.0.0.1:8000/run/${runId}`);
  return res.json();
};