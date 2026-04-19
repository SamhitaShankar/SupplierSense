export type StartRunResponse = {
  run_id: string;
  status: string;
  celery_task_id: string;
};

export const startRun = async (): Promise<StartRunResponse> => {
  const res = await fetch("http://127.0.0.1:8000/run", {
    method: "POST",
  });

  if (!res.ok) {
    throw new Error(`Failed to start run: ${res.status}`);
  }

  return res.json();
};

export const getRun = async (runId: string) => {
  const res = await fetch(`http://127.0.0.1:8000/run/${runId}`);

  if (!res.ok) {
    throw new Error(`Failed to fetch run ${runId}: ${res.status}`);
  }

  return res.json();
};