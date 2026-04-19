import { useEffect } from "react";
import { useRunStore } from "../store/runStore";

export const useRunSocket = (runId: string | null) => {
  const updateFromRunPayload = useRunStore((s) => s.updateFromRunPayload);

  useEffect(() => {
    if (!runId) return;

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${runId}`);

    ws.onopen = () => {
      console.log("WebSocket connected");
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      updateFromRunPayload(data);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    return () => ws.close();
  }, [runId, updateFromRunPayload]);
};