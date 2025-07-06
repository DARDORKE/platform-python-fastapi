/**
 * Dashboard component
 */
import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { useProjectStore } from '../../store/projectStore';
import { useTaskStore } from '../../store/taskStore';
import { useDashboardStore } from '../../store/dashboardStore';
import CreateProjectModal from '../Projects/CreateProjectModal';
import CreateTaskModal from '../Tasks/CreateTaskModal';
import {
  FolderIcon,
  ClipboardDocumentListIcon,
  CheckCircleIcon,
  ClockIcon,
  CalendarDaysIcon,
  RocketLaunchIcon,
  ChartBarIcon,
  BoltIcon,
  StarIcon,
  ArrowRightIcon,
} from '@heroicons/react/24/outline';
import {
  FolderIcon as FolderIconSolid,
  ClipboardDocumentListIcon as ClipboardIconSolid,
  CheckCircleIcon as CheckCircleIconSolid,
  ClockIcon as ClockIconSolid,
} from '@heroicons/react/24/solid';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const { projects, fetchProjects } = useProjectStore();
  const { tasks, fetchTasks } = useTaskStore();
  const { stats: dashboardStats, fetchStats } = useDashboardStore();
  
  const [isCreateProjectModalOpen, setIsCreateProjectModalOpen] = useState(false);
  const [isCreateTaskModalOpen, setIsCreateTaskModalOpen] = useState(false);

  useEffect(() => {
    fetchProjects();
    fetchTasks();
    fetchStats();
  }, []);

  const stats = [
    {
      name: 'Total Projects',
      value: dashboardStats?.projects_count || 0,
      icon: FolderIcon,
      iconSolid: FolderIconSolid,
      gradient: 'from-blue-500 to-blue-600',
      bgColor: 'bg-blue-50',
      textColor: 'text-blue-700',
      change: '+12%',
      trend: 'up',
    },
    {
      name: 'Total Tasks',
      value: dashboardStats?.tasks_count || 0,
      icon: ClipboardDocumentListIcon,
      iconSolid: ClipboardIconSolid,
      gradient: 'from-emerald-500 to-emerald-600',
      bgColor: 'bg-emerald-50',
      textColor: 'text-emerald-700',
      change: '+18%',
      trend: 'up',
    },
    {
      name: 'Completed Tasks',
      value: dashboardStats?.completed_tasks || 0,
      icon: CheckCircleIcon,
      iconSolid: CheckCircleIconSolid,
      gradient: 'from-purple-500 to-purple-600',
      bgColor: 'bg-purple-50',
      textColor: 'text-purple-700',
      change: '+23%',
      trend: 'up',
    },
    {
      name: 'Active Projects',
      value: dashboardStats?.active_projects || 0,
      icon: ClockIcon,
      iconSolid: ClockIconSolid,
      gradient: 'from-amber-500 to-amber-600',
      bgColor: 'bg-amber-50',
      textColor: 'text-amber-700',
      change: '+8%',
      trend: 'up',
    },
  ];

  const recentTasks = tasks.slice(0, 5);
  const recentProjects = projects.slice(0, 5);

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div className="relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-primary-100/50 to-accent-purple/20 rounded-full -translate-y-1/2 translate-x-1/4 blur-3xl opacity-60" />
        <div className="relative z-10">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-4xl font-bold text-gradient mb-2">
                Welcome back, {user?.full_name?.split(' ')[0] || 'User'}! 👋
              </h1>
              <p className="text-lg text-gray-600">
                Here's your productivity overview for today
              </p>
              <div className="flex items-center mt-3 text-sm text-gray-500">
                <CalendarDaysIcon className="h-4 w-4 mr-2" />
                {new Date().toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </div>
            </div>
            <div className="hidden lg:flex items-center space-x-4">
              <div className="text-right">
                <p className="text-2xl font-bold text-gray-900">98%</p>
                <p className="text-sm text-gray-500">Productivity</p>
              </div>
              <div className="w-16 h-16 rounded-full bg-gradient-to-br from-emerald-400 to-emerald-600 flex items-center justify-center shadow-lg shadow-emerald-200">
                <ChartBarIcon className="h-8 w-8 text-white" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat, index) => (
          <div
            key={stat.name}
            className="card-elegant p-6 hover-lift group relative overflow-hidden animate-slide-in-up"
            style={{ animationDelay: `${index * 0.1}s` }}
          >
            {/* Background Pattern */}
            <div className="absolute top-0 right-0 w-20 h-20 opacity-5 transform rotate-12 translate-x-4 -translate-y-4">
              <stat.iconSolid className="w-full h-full text-current" />
            </div>
            
            <div className="relative z-10">
              <div className="flex items-center justify-between mb-4">
                <div className={`p-3 rounded-xl bg-gradient-to-br ${stat.gradient} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                  <stat.icon className="h-6 w-6 text-white" />
                </div>
                <div className={`px-2 py-1 rounded-full text-xs font-semibold ${
                  stat.trend === 'up' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'
                }`}>
                  {stat.change}
                </div>
              </div>
              
              <div>
                <p className="text-3xl font-bold text-gray-900 mb-1">
                  {stat.value.toLocaleString()}
                </p>
                <p className="text-sm font-medium text-gray-600">
                  {stat.name}
                </p>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
        {/* Recent Projects */}
        <div className="xl:col-span-2">
          <div className="card-elegant overflow-hidden animate-slide-in-up" style={{ animationDelay: '0.4s' }}>
            <div className="bg-gradient-to-r from-primary-50 to-accent-purple/10 px-6 py-4 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="p-2 bg-gradient-to-br from-primary-500 to-accent-purple rounded-lg shadow-md">
                    <RocketLaunchIcon className="h-5 w-5 text-white" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900">Recent Projects</h3>
                </div>
                <button 
                  onClick={() => navigate('/projects')}
                  className="text-primary-600 hover:text-accent-purple transition-colors duration-300 flex items-center text-sm font-medium"
                >
                  View all
                  <ArrowRightIcon className="h-4 w-4 ml-1" />
                </button>
              </div>
            </div>
            <div className="p-6">
              {recentProjects.length === 0 ? (
                <div className="text-center py-12">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
                    <FolderIcon className="h-8 w-8 text-gray-400" />
                  </div>
                  <p className="text-gray-500 text-lg font-medium mb-2">
                    No projects yet
                  </p>
                  <p className="text-gray-400 text-sm mb-4">
                    Create your first project to get started
                  </p>
                  <button 
                    onClick={() => setIsCreateProjectModalOpen(true)}
                    className="btn-primary text-sm px-4 py-2"
                  >
                    Create Project
                  </button>
                </div>
              ) : (
                <div className="space-y-4">
                  {recentProjects.map((project, index) => (
                    <div
                      key={project.id}
                      onClick={() => navigate('/projects')}
                      className="group p-4 rounded-xl border border-gray-100 hover:border-primary-200 hover:bg-gradient-to-r hover:from-primary-50/30 hover:to-transparent transition-all duration-300 hover:shadow-md cursor-pointer"
                      style={{ animationDelay: `${0.5 + index * 0.1}s` }}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="flex items-center space-x-3 mb-2">
                            <h4 className="font-bold text-gray-900 group-hover:text-primary-700 transition-colors">
                              {project.name}
                            </h4>
                            <span className={`badge ${
                              project.status === 'active'
                                ? 'badge-success'
                                : project.status === 'planning'
                                ? 'badge-warning'
                                : project.status === 'completed'
                                ? 'badge-info'
                                : 'badge-danger'
                            }`}>
                              {project.status}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 line-clamp-2">
                            {project.description}
                          </p>
                        </div>
                        <ArrowRightIcon className="h-5 w-5 text-gray-400 group-hover:text-primary-500 group-hover:translate-x-1 transition-all duration-300" />
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Recent Tasks */}
          <div className="card-elegant overflow-hidden animate-slide-in-up" style={{ animationDelay: '0.6s' }}>
            <div className="bg-gradient-to-r from-emerald-50 to-emerald-100/50 px-6 py-4 border-b border-gray-100">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-br from-emerald-500 to-emerald-600 rounded-lg shadow-md">
                  <BoltIcon className="h-5 w-5 text-white" />
                </div>
                <h3 className="text-lg font-bold text-gray-900">Recent Tasks</h3>
              </div>
            </div>
            <div className="p-6">
              {recentTasks.length === 0 ? (
                <div className="text-center py-8">
                  <ClipboardDocumentListIcon className="h-12 w-12 text-gray-300 mx-auto mb-3" />
                  <p className="text-gray-500 text-sm">
                    No tasks yet
                  </p>
                </div>
              ) : (
                <div className="space-y-3">
                  {recentTasks.map((task, index) => (
                    <div
                      key={task.id}
                      onClick={() => navigate('/tasks')}
                      className="group p-3 rounded-lg hover:bg-gray-50 transition-colors duration-300 animate-fade-in cursor-pointer"
                      style={{ animationDelay: `${0.7 + index * 0.1}s` }}
                    >
                      <div className="flex items-start space-x-3">
                        <div className={`w-2 h-2 rounded-full mt-2 ${
                          task.status === 'done'
                            ? 'bg-emerald-500'
                            : task.status === 'in_progress'
                            ? 'bg-blue-500'
                            : task.status === 'review'
                            ? 'bg-amber-500'
                            : 'bg-gray-400'
                        }`} />
                        <div className="flex-1 min-w-0">
                          <p className="font-medium text-gray-900 text-sm group-hover:text-primary-700 transition-colors">
                            {task.title}
                          </p>
                          <p className="text-xs text-gray-500 mt-1 line-clamp-2">
                            {task.description}
                          </p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="card-elegant animate-slide-in-up" style={{ animationDelay: '0.8s' }}>
            <div className="p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <StarIcon className="h-5 w-5 text-amber-500 mr-2" />
                Quick Actions
              </h3>
              <div className="space-y-3">
                <button 
                  onClick={() => setIsCreateProjectModalOpen(true)}
                  className="w-full btn-primary text-sm py-2.5"
                >
                  Create New Project
                </button>
                <button 
                  onClick={() => setIsCreateTaskModalOpen(true)}
                  className="w-full btn-secondary text-sm py-2.5"
                >
                  Add Task
                </button>
                <button 
                  onClick={() => navigate('/tasks')}
                  className="w-full text-gray-600 hover:text-primary-600 transition-colors text-sm py-2"
                >
                  View Reports
                </button>
              </div>
            </div>
          </div>

          {/* Progress Summary */}
          <div className="card-elegant animate-slide-in-up" style={{ animationDelay: '1s' }}>
            <div className="p-6">
              <h3 className="text-lg font-bold text-gray-900 mb-4 flex items-center">
                <ChartBarIcon className="h-5 w-5 text-primary-500 mr-2" />
                This Week
              </h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">Tasks Completed</span>
                    <span className="font-medium text-gray-900">8/12</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-2 rounded-full" style={{ width: '67%' }} />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span className="text-gray-600">Project Progress</span>
                    <span className="font-medium text-gray-900">75%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-gradient-to-r from-primary-500 to-primary-600 h-2 rounded-full" style={{ width: '75%' }} />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Modals */}
      <CreateProjectModal
        isOpen={isCreateProjectModalOpen}
        onClose={() => setIsCreateProjectModalOpen(false)}
      />
      
      <CreateTaskModal
        isOpen={isCreateTaskModalOpen}
        onClose={() => setIsCreateTaskModalOpen(false)}
        projects={projects}
      />
    </div>
  );
};

export default Dashboard;