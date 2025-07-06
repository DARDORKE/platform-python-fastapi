/**
 * Project store using Zustand
 */
import { create } from 'zustand';
import { Project, ProjectWithStats, CreateProjectData } from '@/types';
import api from '@/lib/api.ts';

interface ProjectState {
  projects: Project[];
  currentProject: ProjectWithStats | null;
  isLoading: boolean;
  error: string | null;
  fetchProjects: () => Promise<void>;
  fetchProject: (id: number) => Promise<void>;
  createProject: (data: CreateProjectData) => Promise<Project>;
  updateProject: (id: number, data: Partial<CreateProjectData>) => Promise<Project>;
  deleteProject: (id: number) => Promise<void>;
  clearError: () => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  projects: [],
  currentProject: null,
  isLoading: false,
  error: null,

  fetchProjects: async () => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get<Project[]>('/projects');
      set({ projects: response.data, isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch projects', 
        isLoading: false 
      });
    }
  },

  fetchProject: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.get<ProjectWithStats>(`/projects/${id}`);
      set({ currentProject: response.data, isLoading: false });
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to fetch project', 
        isLoading: false 
      });
    }
  },

  createProject: async (data: CreateProjectData) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.post<Project>('/projects/', data);
      const newProject = response.data;
      
      set(state => ({
        projects: [...state.projects, newProject],
        isLoading: false
      }));
      
      return newProject;
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to create project', 
        isLoading: false 
      });
      throw error;
    }
  },

  updateProject: async (id: number, data: Partial<CreateProjectData>) => {
    set({ isLoading: true, error: null });
    try {
      const response = await api.put<Project>(`/projects/${id}`, data);
      const updatedProject = response.data;
      
      set(state => ({
        projects: state.projects.map(p => p.id === id ? updatedProject : p),
        currentProject: state.currentProject?.id === id 
          ? { ...state.currentProject, ...updatedProject }
          : state.currentProject,
        isLoading: false
      }));
      
      return updatedProject;
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to update project', 
        isLoading: false 
      });
      throw error;
    }
  },

  deleteProject: async (id: number) => {
    set({ isLoading: true, error: null });
    try {
      await api.delete(`/projects/${id}`);
      
      set(state => ({
        projects: state.projects.filter(p => p.id !== id),
        currentProject: state.currentProject?.id === id ? null : state.currentProject,
        isLoading: false
      }));
    } catch (error: any) {
      set({ 
        error: error.response?.data?.detail || 'Failed to delete project', 
        isLoading: false 
      });
      throw error;
    }
  },

  clearError: () => set({ error: null }),
}));