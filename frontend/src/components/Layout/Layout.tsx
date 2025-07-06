/**
 * Main layout component
 */
import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate, useNavigate, useLocation } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { useTaskStore } from '../../store/taskStore';
import Dashboard from '../Dashboard/Dashboard';
import ProjectList from '../Projects/ProjectList';
import TaskList from '../Tasks/TaskList';
import {
  HomeIcon,
  FolderIcon,
  ClipboardDocumentListIcon,
  UserIcon,
  ArrowRightOnRectangleIcon,
  Bars3Icon,
  XMarkIcon,
  ChartBarIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';
import {
  HomeIcon as HomeIconSolid,
  FolderIcon as FolderIconSolid,
  ClipboardDocumentListIcon as ClipboardIconSolid,
} from '@heroicons/react/24/solid';

const Layout: React.FC = () => {
  const { user, logout } = useAuthStore();
  const { tasks, fetchTasks } = useTaskStore();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);

  // Fetch tasks for the sidebar stats
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Calculate completed tasks
  const completedTasksCount = tasks.filter(task => task.status === 'done').length;

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navigation = [
    { name: 'Dashboard', href: '/', icon: HomeIcon, iconSolid: HomeIconSolid },
    { name: 'Projects', href: '/projects', icon: FolderIcon, iconSolid: FolderIconSolid },
    { name: 'Tasks', href: '/tasks', icon: ClipboardDocumentListIcon, iconSolid: ClipboardIconSolid },
  ];

  const isActive = (path: string) => location.pathname === path;

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-secondary-50">
      {/* Mobile sidebar backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/30 backdrop-blur-sm z-40 lg:hidden" 
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 w-72 bg-white/90 backdrop-blur-xl shadow-colorful transform transition-transform duration-300 ease-in-out lg:translate-x-0 ${
        sidebarOpen ? 'translate-x-0' : '-translate-x-full'
      }`}>
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-20 items-center justify-between px-6 border-b border-gray-100">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl shadow-colorful">
                <SparklesIcon className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gradient-rainbow">Platform</h1>
                <p className="text-xs text-gray-500">Project Management</p>
              </div>
            </div>
            <button
              onClick={() => setSidebarOpen(false)}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <XMarkIcon className="h-5 w-5 text-gray-500" />
            </button>
          </div>

          {/* Navigation */}
          <nav className="flex-1 px-4 py-6 space-y-2 overflow-y-auto">
            {navigation.map((item) => {
              const active = isActive(item.href);
              const Icon = active ? item.iconSolid : item.icon;
              
              return (
                <a
                  key={item.name}
                  href={item.href}
                  className={`group flex items-center px-4 py-3 text-sm font-medium rounded-xl transition-all duration-300 ${
                    active
                      ? 'bg-gradient-to-r from-primary-100 to-secondary-100 text-primary-700 shadow-colorful border-l-4 border-primary-500'
                      : 'text-gray-600 hover:bg-gradient-to-r hover:from-primary-50 hover:to-secondary-50 hover:text-gray-900 hover:translate-x-1 hover:shadow-md'
                  }`}
                >
                  <Icon className={`mr-3 h-5 w-5 transition-colors ${
                    active ? 'text-primary-600' : 'text-gray-400 group-hover:text-gray-600'
                  }`} />
                  <span className="flex-1">{item.name}</span>
                  {active && (
                    <div className="ml-auto h-2 w-2 rounded-full bg-primary-500 animate-pulse" />
                  )}
                </a>
              );
            })}
          </nav>

          {/* Stats Summary */}
          <div className="px-4 py-4 border-t border-gray-100">
            <div className="bg-gradient-to-r from-primary-100 to-secondary-100 rounded-xl p-4 shadow-colorful">
              <div className="flex items-center justify-between mb-2">
                <ChartBarIcon className="h-5 w-5 text-primary-600" />
                <span className="text-xs text-gray-500">This week</span>
              </div>
              <p className="text-2xl font-bold text-gray-900">{completedTasksCount}</p>
              <p className="text-xs text-gray-600">Tasks completed</p>
            </div>
          </div>

          {/* User section */}
          <div className="border-t border-gray-100 p-4">
            <div className="flex items-center space-x-3 p-3 rounded-xl bg-gradient-to-r from-primary-50 to-secondary-50 mb-3 shadow-md">
              <div className="flex-shrink-0">
                <div className="h-10 w-10 rounded-full bg-gradient-to-br from-primary-500 to-secondary-500 flex items-center justify-center shadow-colorful">
                  <UserIcon className="h-6 w-6 text-white" />
                </div>
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-semibold text-gray-900 truncate">
                  {user?.full_name}
                </p>
                <p className="text-xs text-gray-500 truncate">
                  {user?.email}
                </p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="w-full flex items-center justify-center px-4 py-2.5 text-sm font-medium text-gray-700 rounded-xl hover:bg-gradient-to-r hover:from-danger-50 hover:to-danger-100 hover:text-danger-600 transition-all duration-300 group hover:shadow-danger"
            >
              <ArrowRightOnRectangleIcon className="mr-2 h-5 w-5 text-gray-400 group-hover:text-red-500 transition-colors" />
              Logout
            </button>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:ml-72">
        {/* Mobile header */}
        <div className="sticky top-0 z-30 lg:hidden bg-white/90 backdrop-blur-xl shadow-colorful">
          <div className="flex items-center justify-between px-4 py-4">
            <button
              onClick={() => setSidebarOpen(true)}
              className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <Bars3Icon className="h-6 w-6 text-gray-600" />
            </button>
            <div className="flex items-center space-x-2">
              <div className="p-2 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-lg shadow-colorful">
                <SparklesIcon className="h-5 w-5 text-white" />
              </div>
              <h1 className="text-lg font-bold text-gradient-rainbow">Platform</h1>
            </div>
            <div className="w-10" /> {/* Spacer for balance */}
          </div>
        </div>
        
        {/* Page content */}
        <main className="min-h-screen">
          <div className="py-8 px-4 sm:px-6 lg:px-8 max-w-7xl mx-auto animate-fade-in">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/projects" element={<ProjectList />} />
              <Route path="/tasks" element={<TaskList />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;