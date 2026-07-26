import { create } from "zustand";

export const useUiStore = create((set) => ({
  sidebarOpen: true,
  selectedNodeId: null,
  selectedAgentId: null,
  filters: {},
  notifications: [],
  // Execution state slices
  simulationState: { events: [], finalResponse: null, rawState: null, sampleId: "" },
  liveState: { events: [], finalResponse: null, rawState: null, sampleId: "" },
  // Update execution state (patch) for simulation or live
  setExecutionState: (isSimulation, patch) =>
    set((state) => {
      const key = isSimulation ? "simulationState" : "liveState";
      return { [key]: { ...state[key], ...patch } };
    }),
  // Reset execution state to initial values
  resetExecutionState: (isSimulation) =>
    set((state) => {
      const key = isSimulation ? "simulationState" : "liveState";
      return { [key]: { events: [], finalResponse: null, rawState: null, sampleId: "" } };
    }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  selectNode: (selectedNodeId) => set({ selectedNodeId }),
  selectAgent: (selectedAgentId) => set({ selectedAgentId }),
  setFilter: (key, value) => set((state) => ({ filters: { ...state.filters, [key]: value } })),
  notify: (notification) =>
    set((state) => ({ notifications: [{ id: crypto.randomUUID(), ...notification }, ...state.notifications].slice(0, 4) })),
  dismissNotification: (id) =>
    set((state) => ({ notifications: state.notifications.filter((notification) => notification.id !== id) })),
}));
