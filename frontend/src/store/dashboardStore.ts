/**
 * Dashboard store using Zustand
 */
import { create } from 'zustand';
import api from '../lib/api';

interface DashboardStats {
  users_count: number;
  projects_count: number;
  tasks_count: number;
  completed_tasks: number;
  active_projects: number;
}

interface DashboardState {
  stats: DashboardStats | null;
  isLoading: boolean;
  error: string | null;
  fetchStats: () => Promise<void>;
  clearError: () => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  stats: null,
  isLoading: false,
  error: null,

  fetchStats: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get<DashboardStats>('/dashboard/stats');
      set({ stats: response.data, isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch dashboard stats', 
        isLoading: false 
      });
    }
  },

  clearError: () => set({ error: null }),
}));