/**
 * Task store using Zustand
 */
import { create } from 'zustand';
import { Task, CreateTaskData } from '~/types';
import api from '~/lib/api';

interface TaskState {
  tasks: Task[];
  isLoading: boolean;
  error: string | null;
  fetchTasks: (projectId?: number) => Promise<void>;
  fetchTask: (id: number) => Promise<Task>;
  createTask: (data: CreateTaskData) => Promise<Task>;
  updateTask: (id: number, data: Partial<CreateTaskData>) => Promise<Task>;
  deleteTask: (id: number) => Promise<void>;
  getTaskStats: () => Promise<any>;
  clearError: () => void;
}

export const useTaskStore = create<TaskState>((set) => ({
  tasks: [],
  isLoading: false,
  error: null,

  fetchTasks: async (projectId?: number) => {
    set({ isLoading: true, error: null });
    try {
      const params = projectId ? { project_id: projectId } : {};
      const response = await api.get<Task[]>('/tasks', { params });
      set({ tasks: response.data, isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch tasks', 
        isLoading: false 
      });
    }
  },

  fetchTask: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get<Task>(`/tasks/${id}`);
      set({ isLoading: false });
      return response.data;
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch task', 
        isLoading: false 
      });
      throw error;
    }
  },

  createTask: async (data: CreateTaskData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post<Task>('/tasks/', data);
      const newTask = response.data;
      
      set(state => ({
        tasks: [...state.tasks, newTask],
        isLoading: false
      }));
      
      return newTask;
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to create task', 
        isLoading: false 
      });
      throw error;
    }
  },

  updateTask: async (id: number, data: Partial<CreateTaskData>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.put<Task>(`/tasks/${id}`, data);
      const updatedTask = response.data;
      
      set(state => ({
        tasks: state.tasks.map(t => t.id === id ? updatedTask : t),
        isLoading: false
      }));
      
      return updatedTask;
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to update task', 
        isLoading: false 
      });
      throw error;
    }
  },

  deleteTask: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      await api.delete(`/tasks/${id}`);
      
      set(state => ({
        tasks: state.tasks.filter(t => t.id !== id),
        isLoading: false
      }));
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to delete task', 
        isLoading: false 
      });
      throw error;
    }
  },

  getTaskStats: async () => {
    try {
      const response = await api.get('/tasks/stats/me');
      return response.data;
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch task stats'
      });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));