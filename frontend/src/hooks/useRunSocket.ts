import { useEffect } from "react";
import { useRunStore } from "../store/runStore";

export const useRunSocket = (runId: string | null) => {
  const setState = useRunStore((s) => s.setState);

  useEffect(() => {
    if (!runId) return;

    const ws = new WebSocket(`ws://127.0.0.1:8000/ws/${runId}`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setState(data.state);
    };

    ws.onerror = (err) => {
      console.error("WebSocket error:", err);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
    };

    return () => ws.close();
  }, [runId]);
};