import { create } from "zustand";

export type SignalEvent = {
  id: number | string;
  type: string;
  source: string;
  raw_text: string;
  severity: number;
  affected_region: string;
  affected_commodities: string[];
  timestamp: string;
  confidence: number;
};

export type SupplierSenseState = {
  raw_signals: SignalEvent[];
  signal_summary?: string;
  disruption_detected?: boolean;
  [key: string]: unknown;
};

export type RunStatus = "idle" | "queued" | "running" | "completed" | "failed";

type RunStore = {
  runId: string | null;
  status: RunStatus;
  state: SupplierSenseState | null;
  error: string | null;

  setRunId: (runId: string | null) => void;
  setStatus: (status: RunStatus) => void;
  setState: (state: SupplierSenseState | null) => void;
  setError: (error: string | null) => void;

  updateFromRunPayload: (payload: {
    run_id?: string;
    status?: string;
    state?: SupplierSenseState;
    error?: string | null;
  }) => void;

  reset: () => void;
};

export const useRunStore = create<RunStore>((set) => ({
  runId: null,
  status: "idle",
  state: null,
  error: null,

  setRunId: (runId) => set({ runId }),
  setStatus: (status) => set({ status }),
  setState: (state) => set({ state }),
  setError: (error) => set({ error }),

  updateFromRunPayload: (payload) =>
    set((current) => ({
      runId: payload.run_id ?? current.runId,
      status: (payload.status as RunStatus) ?? current.status,
      state: payload.state ?? current.state,
      error: payload.error ?? null,
    })),

  reset: () =>
    set({
      runId: null,
      status: "idle",
      state: null,
      error: null,
    }),
}));