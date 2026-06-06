import { create } from "zustand";

export type SignalEvent = {
  id?: number | string;
  signal_id?: string;
  type?: string;
  event_type?: string;
  source: string;
  raw_text?: string;
  summary?: string;
  severity: number;
  affected_region?: string;
  region?: string;
  affected_commodities?: string[];
  commodities?: string[];
  timestamp?: string;
  confidence?: number;
};

export type SupplierRiskScore = {
  supplier_id: string;
  supplier_name?: string;
  risk_score: number;
  risk_level?: string;
  reasoning?: string[];
};

export type SupplierProfile = {
  supplier_id: string;
  supplier_name: string;
  tier?: number;
  country?: string;
  region?: string;
  city?: string;
  commodities?: string[];
  primary_commodity?: string;
  lead_time_days?: number;
  risk_score?: number;
  historical_disruptions?: number;
};

export type ImpactedSKU = {
  sku_id?: string;
  sku_name?: string;
  product_name?: string;
  supplier_id?: string;
  supplier_name?: string;
  stockout_days?: number;
  days_to_stockout?: number;
  days_until_stockout?: number;
  revenue_at_risk?: number;
  severity?: string;
  risk_level?: string;
};

export type SupplierSenseState = {
  raw_signals?: SignalEvent[];
  signal_summary?: string;
  disruption_detected?: boolean;
  supplier_risk_scores?: SupplierRiskScore[];
  supplier_profiles?: SupplierProfile[];
  impacted_skus?: ImpactedSKU[];
  total_revenue_at_risk?: number;
  impact_severity?: string;
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