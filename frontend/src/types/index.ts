/**
 * TypeScript type definitions
 */

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  is_active: boolean;
  role: 'admin' | 'manager' | 'user';
  created_at: string;
  updated_at: string;
  last_login?: string;
}

export interface UserWithStats extends User {
  total_tasks: number;
  completed_tasks: number;
  total_projects: number;
}

export interface Project {
  id: number;
  name: string;
  description?: string;
  status: 'planning' | 'active' | 'on_hold' | 'completed' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  start_date?: string;
  end_date?: string;
  budget?: number;
  owner_id: number;
  created_at: string;
  updated_at: string;
}

export interface ProjectWithStats extends Project {
  total_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
  completion_percentage: number;
}

export interface Task {
  id: number;
  title: string;
  description?: string;
  status: 'todo' | 'in_progress' | 'review' | 'done' | 'cancelled';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  due_date?: string;
  estimated_hours?: number;
  actual_hours?: number;
  is_completed: boolean;
  completion_date?: string;
  owner_id: number;
  project_id?: number;
  created_at: string;
  updated_at: string;
}

export interface TaskWithProject extends Task {
  project_name?: string;
  project_status?: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  email: string;
  username: string;
  full_name: string;
  password: string;
  role?: 'admin' | 'manager' | 'user';
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface ApiError {
  detail: string;
  status_code: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

export interface CreateProjectData {
  name: string;
  description?: string;
  status?: Project['status'];
  priority?: Project['priority'];
  start_date?: string;
  end_date?: string;
  budget?: number;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  status?: Task['status'];
  priority?: Task['priority'];
  due_date?: string;
  estimated_hours?: number;
  project_id?: number;
}