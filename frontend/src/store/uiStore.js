import { create } from "zustand";

export const useUiStore = create((set) => ({
  sidebarOpen: true,
  selectedNodeId: null,
  selectedAgentId: null,
  filters: {},
  notifications: [],
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  selectNode: (selectedNodeId) => set({ selectedNodeId }),
  selectAgent: (selectedAgentId) => set({ selectedAgentId }),
  setFilter: (key, value) => set((state) => ({ filters: { ...state.filters, [key]: value } })),
  notify: (notification) =>
    set((state) => ({ notifications: [{ id: crypto.randomUUID(), ...notification }, ...state.notifications].slice(0, 4) })),
  dismissNotification: (id) =>
    set((state) => ({ notifications: state.notifications.filter((notification) => notification.id !== id) }))
}));
