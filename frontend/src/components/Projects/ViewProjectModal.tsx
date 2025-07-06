/**
 * ViewProjectModal component
 */
import React, { useState, useEffect } from 'react';
import { Project, Task } from '../../types';
import { XMarkIcon, CalendarIcon, CurrencyEuroIcon } from '@heroicons/react/24/outline';
import { useTaskStore } from '../../store/taskStore';

interface ViewProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
  project: Project;
}

const ViewProjectModal: React.FC<ViewProjectModalProps> = ({
  isOpen,
  onClose,
  project,
}) => {
  const { tasks, fetchTasks, isLoading } = useTaskStore();
  const [projectTasks, setProjectTasks] = useState<Task[]>([]);

  // Fetch tasks when modal opens
  useEffect(() => {
    if (isOpen && project) {
      fetchTasks();
    }
  }, [isOpen, project, fetchTasks]);

  // Filter tasks for this project
  useEffect(() => {
    if (tasks && project) {
      const filteredTasks = tasks.filter(task => task.project_id === project.id);
      setProjectTasks(filteredTasks);
    }
  }, [tasks, project]);

  const getStatusBadgeColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'planning':
        return 'bg-gradient-to-r from-warning-100 to-warning-200 text-warning-800 ring-2 ring-warning-300/50';
      case 'active':
        return 'bg-gradient-to-r from-success-100 to-success-200 text-success-800 ring-2 ring-success-300/50';
      case 'on_hold':
        return 'bg-gradient-to-r from-secondary-100 to-secondary-200 text-secondary-800 ring-2 ring-secondary-300/50';
      case 'completed':
        return 'bg-gradient-to-r from-primary-100 to-primary-200 text-primary-800 ring-2 ring-primary-300/50';
      case 'cancelled':
        return 'bg-gradient-to-r from-danger-100 to-danger-200 text-danger-800 ring-2 ring-danger-300/50';
      default:
        return 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 ring-2 ring-gray-300/50';
    }
  };

  const getPriorityBadgeColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'low':
        return 'bg-gradient-to-r from-success-100 to-success-200 text-success-800 ring-2 ring-success-300/50';
      case 'medium':
        return 'bg-gradient-to-r from-warning-100 to-warning-200 text-warning-800 ring-2 ring-warning-300/50';
      case 'high':
        return 'bg-gradient-to-r from-secondary-100 to-secondary-200 text-secondary-800 ring-2 ring-secondary-300/50';
      case 'urgent':
        return 'bg-gradient-to-r from-danger-100 to-danger-200 text-danger-800 ring-2 ring-danger-300/50';
      default:
        return 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 ring-2 ring-gray-300/50';
    }
  };

  const getTaskStatusBadgeColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'todo':
        return 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 ring-2 ring-gray-300/50';
      case 'in_progress':
        return 'bg-gradient-to-r from-primary-100 to-primary-200 text-primary-800 ring-2 ring-primary-300/50';
      case 'review':
        return 'bg-gradient-to-r from-secondary-100 to-secondary-200 text-secondary-800 ring-2 ring-secondary-300/50';
      case 'done':
        return 'bg-gradient-to-r from-success-100 to-success-200 text-success-800 ring-2 ring-success-300/50';
      case 'cancelled':
        return 'bg-gradient-to-r from-danger-100 to-danger-200 text-danger-800 ring-2 ring-danger-300/50';
      default:
        return 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 ring-2 ring-gray-300/50';
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm transition-opacity" onClick={onClose}></div>

        <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>

        <div className="relative inline-block align-bottom bg-white/95 backdrop-blur-xl rounded-2xl px-4 pt-5 pb-4 text-left overflow-hidden shadow-colorful transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full sm:p-6 border border-white/20">
          <div className="absolute top-0 right-0 pt-4 pr-4">
            <button
              type="button"
              className="bg-white/90 rounded-xl text-gray-400 hover:text-danger-600 hover:bg-danger-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-danger-500 transition-all duration-300 hover:scale-110"
              onClick={onClose}
            >
              <XMarkIcon className="h-6 w-6" />
            </button>
          </div>

          <div className="sm:flex sm:items-start">
            <div className="mt-3 text-center sm:mt-0 sm:text-left w-full">
              <h3 className="text-lg leading-6 font-medium text-gray-900 mb-6">
                Project Details
              </h3>

              {/* Project Information */}
              <div className="bg-white shadow rounded-lg mb-6">
                <div className="px-6 py-4 border-b border-gray-200">
                  <div className="flex items-center justify-between">
                    <h4 className="text-xl font-semibold text-gray-900">{project.name}</h4>
                    <div className="flex space-x-2">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusBadgeColor(project.status)}`}>
                        {project.status.charAt(0).toUpperCase() + project.status.slice(1).replace('_', ' ')}
                      </span>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityBadgeColor(project.priority)}`}>
                        {project.priority.charAt(0).toUpperCase() + project.priority.slice(1)}
                      </span>
                    </div>
                  </div>
                </div>

                <div className="px-6 py-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div>
                      <h5 className="text-sm font-medium text-gray-900 mb-2">Description</h5>
                      <p className="text-sm text-gray-600">{project.description || 'No description provided'}</p>
                    </div>

                    <div className="space-y-4">
                      {project.budget && (
                        <div className="flex items-center">
                          <CurrencyEuroIcon className="h-5 w-5 text-gray-400 mr-2" />
                          <span className="text-sm text-gray-600">Budget: ${project.budget.toLocaleString()}</span>
                        </div>
                      )}

                      <div className="flex items-center">
                        <CalendarIcon className="h-5 w-5 text-gray-400 mr-2" />
                        <span className="text-sm text-gray-600">
                          Created: {new Date(project.created_at).toLocaleDateString()}
                        </span>
                      </div>

                      {project.start_date && (
                        <div className="flex items-center">
                          <CalendarIcon className="h-5 w-5 text-gray-400 mr-2" />
                          <span className="text-sm text-gray-600">
                            Start Date: {new Date(project.start_date).toLocaleDateString()}
                          </span>
                        </div>
                      )}

                      {project.end_date && (
                        <div className="flex items-center">
                          <CalendarIcon className="h-5 w-5 text-gray-400 mr-2" />
                          <span className="text-sm text-gray-600">
                            End Date: {new Date(project.end_date).toLocaleDateString()}
                          </span>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Project Tasks */}
              <div className="bg-white shadow rounded-lg">
                <div className="px-6 py-4 border-b border-gray-200">
                  <h4 className="text-lg font-medium text-gray-900">
                    Associated Tasks ({projectTasks.length})
                  </h4>
                </div>

                <div className="px-6 py-4">
                  {isLoading ? (
                    <div className="text-center py-4">
                      <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
                      <p className="mt-2 text-sm text-gray-600">Loading tasks...</p>
                    </div>
                  ) : projectTasks.length === 0 ? (
                    <div className="text-center py-8">
                      <p className="text-sm text-gray-500">No tasks associated with this project yet.</p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {projectTasks.map((task) => (
                        <div key={task.id} className="border border-gray-200 rounded-lg p-4">
                          <div className="flex items-center justify-between mb-2">
                            <h5 className="text-sm font-medium text-gray-900">{task.title}</h5>
                            <div className="flex space-x-2">
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getTaskStatusBadgeColor(task.status)}`}>
                                {task.status.charAt(0).toUpperCase() + task.status.slice(1).replace('_', ' ')}
                              </span>
                              <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getPriorityBadgeColor(task.priority)}`}>
                                {task.priority.charAt(0).toUpperCase() + task.priority.slice(1)}
                              </span>
                            </div>
                          </div>
                          
                          {task.description && (
                            <p className="text-sm text-gray-600 mb-2">{task.description}</p>
                          )}
                          
                          <div className="flex items-center justify-between text-xs text-gray-500">
                            <span>Created: {new Date(task.created_at).toLocaleDateString()}</span>
                            {task.is_completed && (
                              <span className="text-green-600 font-medium">✓ Completed</span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* Actions */}
              <div className="mt-6 flex justify-end">
                <button
                  type="button"
                  onClick={onClose}
                  className="inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:text-sm"
                >
                  Close
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ViewProjectModal;