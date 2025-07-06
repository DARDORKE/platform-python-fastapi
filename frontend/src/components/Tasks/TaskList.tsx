/**
 * TaskList component - Complete task management interface
 */
import React, { useEffect, useState } from 'react';
import { useTaskStore } from '../../store/taskStore';
import { useProjectStore } from '../../store/projectStore';
import { Task } from '../../types';
import CreateTaskModal from './CreateTaskModal';
import EditTaskModal from './EditTaskModal';
import DeleteTaskModal from './DeleteTaskModal';
import {
  PlusIcon,
  PencilIcon,
  TrashIcon,
  MagnifyingGlassIcon,
  CheckCircleIcon,
  ClockIcon,
  ChevronDownIcon,
  CalendarIcon,
  ChartBarIcon,
  FireIcon,
  QueueListIcon,
  ViewColumnsIcon,
  Squares2X2Icon,
  ListBulletIcon,
  AdjustmentsHorizontalIcon,
  SparklesIcon,
} from '@heroicons/react/24/outline';
import {
  CheckCircleIcon as CheckCircleIconSolid,
  ClockIcon as ClockIconSolid,
  ExclamationTriangleIcon as ExclamationTriangleIconSolid,
  QueueListIcon as QueueListIconSolid,
} from '@heroicons/react/24/solid';

const TaskList: React.FC = () => {
  const { tasks, isLoading, error, fetchTasks } = useTaskStore();
  const { projects, fetchProjects } = useProjectStore();
  
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [priorityFilter, setPriorityFilter] = useState<string>('all');
  const [viewMode, setViewMode] = useState<'list' | 'grid' | 'kanban'>('list');
  const [sortBy, setSortBy] = useState('created_at');

  useEffect(() => {
    fetchTasks();
    fetchProjects();
  }, []);

  // Filter tasks based on search and filters
  const filteredTasks = tasks.filter(task => {
    const matchesSearch = task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         task.description?.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus = statusFilter === 'all' || task.status === statusFilter;
    const matchesPriority = priorityFilter === 'all' || task.priority === priorityFilter;
    
    return matchesSearch && matchesStatus && matchesPriority;
  });

  const getStatusConfig = (status: string) => {
    switch (status.toLowerCase()) {
      case 'done':
        return { 
          icon: <CheckCircleIconSolid className="h-5 w-5" />, 
          color: 'text-emerald-600', 
          bg: 'bg-emerald-50',
          badge: 'badge-success',
          emoji: '✅',
          label: 'Completed'
        };
      case 'in_progress':
        return { 
          icon: <ClockIconSolid className="h-5 w-5" />, 
          color: 'text-blue-600', 
          bg: 'bg-blue-50',
          badge: 'badge-info',
          emoji: '🔄',
          label: 'In Progress'
        };
      case 'todo':
        return { 
          icon: <QueueListIconSolid className="h-5 w-5" />, 
          color: 'text-gray-600', 
          bg: 'bg-gray-50',
          badge: 'bg-gray-100 text-gray-800',
          emoji: '📋',
          label: 'To Do'
        };
      default:
        return { 
          icon: <ExclamationTriangleIconSolid className="h-5 w-5" />, 
          color: 'text-gray-600', 
          bg: 'bg-gray-50',
          badge: 'bg-gray-100 text-gray-800',
          emoji: '❓',
          label: status
        };
    }
  };

  const getPriorityConfig = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
        return { 
          badge: 'badge-danger', 
          emoji: '🔥', 
          color: 'text-red-600',
          bg: 'bg-red-50',
          border: 'border-red-200'
        };
      case 'medium':
        return { 
          badge: 'badge-warning', 
          emoji: '⚡', 
          color: 'text-amber-600',
          bg: 'bg-amber-50',
          border: 'border-amber-200'
        };
      case 'low':
        return { 
          badge: 'badge-success', 
          emoji: '🌱', 
          color: 'text-emerald-600',
          bg: 'bg-emerald-50',
          border: 'border-emerald-200'
        };
      default:
        return { 
          badge: 'bg-gray-100 text-gray-800', 
          emoji: '📌', 
          color: 'text-gray-600',
          bg: 'bg-gray-50',
          border: 'border-gray-200'
        };
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200 border-t-primary-600"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <QueueListIcon className="h-6 w-6 text-primary-600 animate-pulse" />
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card-elegant p-6 border-red-200 bg-red-50">
        <div className="flex items-center space-x-3">
          <ExclamationTriangleIconSolid className="h-8 w-8 text-red-500" />
          <div>
            <h3 className="text-lg font-semibold text-red-800">Error loading tasks</h3>
            <p className="text-red-700 mt-1">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl lg:text-4xl font-bold text-gradient flex items-center">
            <QueueListIconSolid className="h-6 w-6 sm:h-8 sm:w-8 lg:h-10 lg:w-10 text-primary-600 mr-2 sm:mr-3" />
            Tasks
          </h1>
          <p className="text-gray-600 mt-1 sm:mt-2 text-sm sm:text-base">
            Organize your work and track progress across all projects
          </p>
          <div className="flex items-center mt-2 sm:mt-3 text-xs sm:text-sm text-gray-500">
            <ChartBarIcon className="h-3 w-3 sm:h-4 sm:w-4 mr-1 sm:mr-2" />
            {filteredTasks.length} of {tasks.length} tasks
          </div>
        </div>
        <button
          onClick={() => setIsCreateModalOpen(true)}
          className="btn-primary flex items-center group w-full sm:w-auto justify-center"
        >
          <PlusIcon className="h-4 w-4 sm:h-5 sm:w-5 mr-2 group-hover:rotate-90 transition-transform duration-300" />
          New Task
        </button>
      </div>

      {/* Filters and Controls */}
      <div className="card-elegant p-4 sm:p-6">
        <div className="flex flex-col gap-4">
          {/* Search */}
          <div className="w-full">
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 sm:h-5 sm:w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search tasks, descriptions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-elegant pl-10 w-full"
              />
            </div>
          </div>
          
          {/* Filters Row */}
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
            {/* Status Filter */}
            <div className="relative">
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="input-elegant pr-8 appearance-none cursor-pointer w-full text-sm"
              >
                <option value="all">All Status</option>
                <option value="todo">📋 To Do</option>
                <option value="in_progress">🔄 In Progress</option>
                <option value="done">✅ Done</option>
              </select>
              <ChevronDownIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
            </div>
            
            {/* Priority Filter */}
            <div className="relative">
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value)}
                className="input-elegant pr-8 appearance-none cursor-pointer w-full text-sm"
              >
                <option value="all">All Priorities</option>
                <option value="high">🔥 High</option>
                <option value="medium">⚡ Medium</option>
                <option value="low">🌱 Low</option>
              </select>
              <ChevronDownIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
            </div>
            
            {/* Sort */}
            <div className="relative">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="input-elegant pr-8 appearance-none cursor-pointer w-full text-sm"
              >
                <option value="created_at">Latest</option>
                <option value="title">Name</option>
                <option value="status">Status</option>
                <option value="priority">Priority</option>
              </select>
              <ChevronDownIcon className="absolute right-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400 pointer-events-none" />
            </div>
          </div>
          
          {/* View Mode Toggle */}
          <div className="w-full sm:w-auto">
            <div className="flex border border-gray-200 rounded-lg p-1 bg-gray-50">
              <button
                onClick={() => setViewMode('list')}
                className={`flex-1 sm:flex-none p-2 rounded-md transition-all duration-300 ${
                  viewMode === 'list'
                    ? 'bg-white shadow-sm text-primary-600'
                    : 'text-gray-400 hover:text-gray-600'
                }`}
                title="List view"
              >
                <ListBulletIcon className="h-4 w-4 sm:h-5 sm:w-5 mx-auto" />
              </button>
              <button
                onClick={() => setViewMode('grid')}
                className={`flex-1 sm:flex-none p-2 rounded-md transition-all duration-300 ${
                  viewMode === 'grid'
                    ? 'bg-white shadow-sm text-primary-600'
                    : 'text-gray-400 hover:text-gray-600'
                }`}
                title="Grid view"
              >
                <Squares2X2Icon className="h-4 w-4 sm:h-5 sm:w-5 mx-auto" />
              </button>
              <button
                onClick={() => setViewMode('kanban')}
                className={`flex-1 sm:flex-none p-2 rounded-md transition-all duration-300 ${
                  viewMode === 'kanban'
                    ? 'bg-white shadow-sm text-primary-600'
                    : 'text-gray-400 hover:text-gray-600'
                }`}
                title="Kanban view"
              >
                <ViewColumnsIcon className="h-4 w-4 sm:h-5 sm:w-5 mx-auto" />
              </button>
            </div>
          </div>
          
          {/* Clear Filters */}
          {(searchTerm || statusFilter !== 'all' || priorityFilter !== 'all') && (
            <button
              onClick={() => {
                setSearchTerm('');
                setStatusFilter('all');
                setPriorityFilter('all');
              }}
              className="btn-secondary flex items-center justify-center w-full sm:w-auto"
            >
              <AdjustmentsHorizontalIcon className="h-4 w-4 mr-2" />
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {/* Task Content */}
      {filteredTasks.length === 0 ? (
        <div className="card-elegant p-12 text-center">
          <div className="w-24 h-24 bg-gradient-to-br from-primary-100 to-accent-purple/20 rounded-full flex items-center justify-center mx-auto mb-6">
            <QueueListIcon className="h-12 w-12 text-primary-500" />
          </div>
          <h3 className="text-2xl font-bold text-gray-900 mb-2">
            {tasks.length === 0 ? 'No tasks yet' : 'No matching tasks'}
          </h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            {tasks.length === 0 
              ? 'Create your first task to start organizing your work and tracking progress.'
              : 'Try adjusting your search terms or filters to find what you\'re looking for.'
            }
          </p>
          {tasks.length === 0 && (
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="btn-primary inline-flex items-center"
            >
              <SparklesIcon className="h-5 w-5 mr-2" />
              Create Your First Task
            </button>
          )}
        </div>
      ) : viewMode === 'list' ? (
        <div className="card-elegant overflow-hidden">
          <div className="divide-y divide-gray-100">
            {filteredTasks.map((task, index) => {
              const statusConfig = getStatusConfig(task.status);
              const priorityConfig = getPriorityConfig(task.priority);
              
              return (
                <div
                  key={task.id}
                  className="p-4 sm:p-6 hover:bg-gradient-to-r hover:from-gray-50 hover:to-transparent transition-all duration-300 group cursor-pointer animate-slide-in-up"
                  style={{ animationDelay: `${index * 0.05}s` }}
                  onClick={() => setEditingTask(task)}
                >
                  <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div className="flex items-start sm:items-center space-x-3 sm:space-x-4 flex-1">
                      {/* Status Indicator */}
                      <div className={`p-1.5 sm:p-2 rounded-lg ${statusConfig.bg} ${statusConfig.color} flex-shrink-0`}>
                        {statusConfig.icon}
                      </div>
                      
                      {/* Task Content */}
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-3 mb-2">
                          <h3 className="text-base sm:text-lg font-bold text-gray-900 group-hover:text-primary-700 transition-colors">
                            {task.title}
                          </h3>
                          <div className="flex items-center gap-2">
                            <span className={`badge ${statusConfig.badge} text-xs`}>
                              <span className="mr-1">{statusConfig.emoji}</span>
                              {statusConfig.label}
                            </span>
                            <span className={`badge ${priorityConfig.badge} text-xs`}>
                              <span className="mr-1">{priorityConfig.emoji}</span>
                              {task.priority}
                            </span>
                          </div>
                        </div>
                        
                        {task.description && (
                          <p className="text-gray-600 text-sm mb-3 line-clamp-2">
                            {task.description}
                          </p>
                        )}
                        
                        <div className="flex items-center space-x-4 text-xs text-gray-500">
                          <div className="flex items-center">
                            <CalendarIcon className="h-3 w-3 mr-1" />
                            {new Date(task.created_at).toLocaleDateString()}
                          </div>
                          {task.is_completed && (
                            <div className="flex items-center text-emerald-600">
                              <CheckCircleIcon className="h-3 w-3 mr-1" />
                              Completed
                            </div>
                          )}
                        </div>
                      </div>
                    </div>
                    
                    {/* Actions */}
                    <div className="flex items-center space-x-2 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity duration-300">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setEditingTask(task);
                        }}
                        className="p-1.5 sm:p-2 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
                        title="Edit task"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setDeletingTask(task);
                        }}
                        className="p-1.5 sm:p-2 rounded-lg hover:bg-red-50 hover:text-red-600 transition-colors"
                        title="Delete task"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ) : viewMode === 'grid' ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {filteredTasks.map((task, index) => {
            const statusConfig = getStatusConfig(task.status);
            const priorityConfig = getPriorityConfig(task.priority);
            
            return (
              <div
                key={task.id}
                className={`card-elegant group hover-lift cursor-pointer relative overflow-hidden animate-slide-in-up ${priorityConfig.border} border-l-4`}
                style={{ animationDelay: `${index * 0.1}s` }}
                onClick={() => setEditingTask(task)}
              >
                <div className="p-4 sm:p-6">
                  {/* Header */}
                  <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-3 sm:gap-4 mb-4">
                    <div className="flex items-center space-x-3">
                      <div className={`p-1.5 sm:p-2 rounded-lg ${statusConfig.bg} ${statusConfig.color}`}>
                        {statusConfig.icon}
                      </div>
                      <span className={`badge ${statusConfig.badge} text-xs`}>
                        {statusConfig.emoji} {statusConfig.label}
                      </span>
                    </div>
                    <span className={`badge ${priorityConfig.badge} text-xs self-start`}>
                      {priorityConfig.emoji}
                    </span>
                  </div>
                  
                  {/* Content */}
                  <h3 className="text-lg sm:text-xl font-bold text-gray-900 group-hover:text-primary-700 transition-colors mb-3 line-clamp-2">
                    {task.title}
                  </h3>
                  
                  {task.description && (
                    <p className="text-gray-600 text-sm mb-4 line-clamp-3">
                      {task.description}
                    </p>
                  )}
                  
                  {/* Footer */}
                  <div className="flex items-center justify-between">
                    <div className="text-xs text-gray-500 flex items-center">
                      <CalendarIcon className="h-3 w-3 mr-1" />
                      {new Date(task.created_at).toLocaleDateString()}
                    </div>
                    
                    <div className="flex items-center space-x-1 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity duration-300">
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setEditingTask(task);
                        }}
                        className="p-1.5 sm:p-2 rounded-lg hover:bg-primary-50 hover:text-primary-600 transition-colors"
                      >
                        <PencilIcon className="h-3 w-3 sm:h-4 sm:w-4" />
                      </button>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setDeletingTask(task);
                        }}
                        className="p-1.5 sm:p-2 rounded-lg hover:bg-red-50 hover:text-red-600 transition-colors"
                      >
                        <TrashIcon className="h-3 w-3 sm:h-4 sm:w-4" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      ) : (
        // Kanban View
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
          {['todo', 'in_progress', 'done'].map((status) => {
            const statusTasks = filteredTasks.filter(task => task.status.toLowerCase() === status);
            const statusConfig = getStatusConfig(status);
            
            return (
              <div key={status} className="card-elegant p-6">
                <div className={`flex items-center space-x-3 mb-6 p-3 rounded-lg ${statusConfig.bg}`}>
                  <div className={statusConfig.color}>
                    {statusConfig.icon}
                  </div>
                  <h3 className={`font-bold ${statusConfig.color}`}>
                    {statusConfig.label} ({statusTasks.length})
                  </h3>
                </div>
                
                <div className="space-y-4">
                  {statusTasks.map((task, index) => {
                    const priorityConfig = getPriorityConfig(task.priority);
                    
                    return (
                      <div
                        key={task.id}
                        className={`p-4 bg-white rounded-lg border-l-4 ${priorityConfig.border} hover:shadow-md transition-all duration-300 cursor-pointer group animate-slide-in-up`}
                        style={{ animationDelay: `${index * 0.1}s` }}
                        onClick={() => setEditingTask(task)}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <h4 className="font-semibold text-gray-900 text-sm group-hover:text-primary-700 transition-colors">
                            {task.title}
                          </h4>
                          <span className={`text-lg ${priorityConfig.color}`}>
                            {priorityConfig.emoji}
                          </span>
                        </div>
                        
                        {task.description && (
                          <p className="text-xs text-gray-600 mb-3 line-clamp-2">
                            {task.description}
                          </p>
                        )}
                        
                        <div className="flex items-center justify-between">
                          <div className="text-xs text-gray-500">
                            {new Date(task.created_at).toLocaleDateString()}
                          </div>
                          <div className="flex space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                setEditingTask(task);
                              }}
                              className="p-1 rounded hover:bg-primary-50 hover:text-primary-600"
                            >
                              <PencilIcon className="h-3 w-3" />
                            </button>
                            <button
                              onClick={(e) => {
                                e.stopPropagation();
                                setDeletingTask(task);
                              }}
                              className="p-1 rounded hover:bg-red-50 hover:text-red-600"
                            >
                              <TrashIcon className="h-3 w-3" />
                            </button>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[
          { 
            label: 'Total Tasks', 
            value: tasks.length, 
            icon: QueueListIcon, 
            color: 'text-blue-600',
            bg: 'bg-blue-50',
            gradient: 'from-blue-500 to-blue-600'
          },
          { 
            label: 'Completed', 
            value: tasks.filter(t => t.status === 'done').length, 
            icon: CheckCircleIcon, 
            color: 'text-emerald-600',
            bg: 'bg-emerald-50',
            gradient: 'from-emerald-500 to-emerald-600'
          },
          { 
            label: 'In Progress', 
            value: tasks.filter(t => t.status === 'in_progress').length, 
            icon: ClockIcon, 
            color: 'text-amber-600',
            bg: 'bg-amber-50',
            gradient: 'from-amber-500 to-amber-600'
          },
          { 
            label: 'High Priority', 
            value: tasks.filter(t => t.priority === 'high').length, 
            icon: FireIcon, 
            color: 'text-red-600',
            bg: 'bg-red-50',
            gradient: 'from-red-500 to-red-600'
          }
        ].map((stat, index) => (
          <div key={stat.label} className="card-elegant p-6 group hover-lift animate-slide-in-up" style={{ animationDelay: `${index * 0.1}s` }}>
            <div className="flex items-center justify-between">
              <div>
                <p className="text-3xl font-bold text-gray-900 mb-1">
                  {stat.value}
                </p>
                <p className="text-sm font-medium text-gray-600">
                  {stat.label}
                </p>
              </div>
              <div className={`p-3 rounded-xl bg-gradient-to-br ${stat.gradient} shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modals */}
      <CreateTaskModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        projects={projects}
      />
      
      {editingTask && (
        <EditTaskModal
          isOpen={!!editingTask}
          onClose={() => setEditingTask(null)}
          task={editingTask}
          projects={projects}
        />
      )}
      
      {deletingTask && (
        <DeleteTaskModal
          isOpen={!!deletingTask}
          onClose={() => setDeletingTask(null)}
          task={deletingTask}
        />
      )}
    </div>
  );
};

export default TaskList;