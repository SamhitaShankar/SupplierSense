import { create } from "zustand";

type SupplierSenseState = any; // keep loose for now

type RunStore = {
  state: SupplierSenseState | null;
  setState: (data: SupplierSenseState) => void;
};

export const useRunStore = create<RunStore>((set) => ({
  state: null,
  setState: (data) => set({ state: data }),
}));