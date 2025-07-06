/**
 * EditTaskModal component
 */
import React, { useState, useEffect } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { useTaskStore } from '../../store/taskStore';
import { Task, Project } from '../../types';
import { 
  XMarkIcon, 
  CalendarIcon, 
  FlagIcon,
  FolderIcon,
  ExclamationCircleIcon,
  PencilIcon
} from '@heroicons/react/24/outline';
import { PencilIcon as PencilIconSolid } from '@heroicons/react/24/solid';

interface EditTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  task: Task;
  projects: Project[];
}

const EditTaskModal: React.FC<EditTaskModalProps> = ({
  isOpen,
  onClose,
  task,
  projects,
}) => {
  const { updateTask, isLoading } = useTaskStore();
  
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    status: 'todo',
    priority: 'medium',
    project_id: '',
  });

  const [errors, setErrors] = useState<Record<string, string>>({});

  // Initialize form data when task changes
  useEffect(() => {
    if (task) {
      setFormData({
        title: task.title,
        description: task.description || '',
        status: task.status,
        priority: task.priority,
        project_id: task.project_id ? task.project_id.toString() : '',
      });
    }
  }, [task]);

  const validateForm = () => {
    const newErrors: Record<string, string> = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }

    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    try {
      await updateTask(task.id, {
        title: formData.title,
        description: formData.description,
        status: formData.status as any,
        priority: formData.priority as any,
        project_id: formData.project_id ? parseInt(formData.project_id) : undefined,
      });
      
      setErrors({});
      onClose();
    } catch (error) {
      console.error('Failed to update task:', error);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  return (
    <Transition show={isOpen} as={React.Fragment}>
      <Dialog onClose={onClose} className="relative z-50">
        <Transition.Child
          enter="ease-out duration-300"
          enterFrom="opacity-0"
          enterTo="opacity-100"
          leave="ease-in duration-200"
          leaveFrom="opacity-100"
          leaveTo="opacity-0"
        >
          <div className="modal-backdrop fixed inset-0" aria-hidden="true" />
        </Transition.Child>
        
        <div className="fixed inset-0 flex items-end sm:items-center justify-center p-0 sm:p-4">
          <Transition.Child
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-95 translate-y-full sm:translate-y-0"
            enterTo="opacity-100 scale-100 translate-y-0"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100 translate-y-0"
            leaveTo="opacity-0 scale-95 translate-y-full sm:translate-y-0"
          >
            <Dialog.Panel className="mx-auto max-w-2xl w-full max-h-screen sm:max-h-[90vh] overflow-y-auto bg-white rounded-t-2xl sm:rounded-2xl shadow-elegant-lg">
              {/* Header */}
              <div className="bg-gradient-to-r from-blue-50 to-blue-100/50 px-4 sm:px-6 py-4 sm:py-5 border-b border-blue-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 sm:space-x-3">
                    <div className="p-1.5 sm:p-2 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl shadow-lg">
                      <PencilIconSolid className="h-5 w-5 sm:h-6 sm:w-6 text-white" />
                    </div>
                    <div>
                      <Dialog.Title className="text-lg sm:text-2xl font-bold text-gray-900">
                        Edit Task
                      </Dialog.Title>
                      <p className="text-gray-600 text-xs sm:text-sm">Update task details and settings</p>
                    </div>
                  </div>
                  <button
                    onClick={onClose}
                    className="p-1.5 sm:p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-all duration-300"
                  >
                    <XMarkIcon className="h-5 w-5 sm:h-6 sm:w-6" />
                  </button>
                </div>
              </div>
              
              {/* Task Info */}
              <div className="px-4 sm:px-6 py-3 sm:py-4 bg-gray-50 border-b border-gray-200">
                <div className="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 text-xs sm:text-sm text-gray-600">
                  <div className="flex items-center">
                    <CalendarIcon className="h-4 w-4 mr-1" />
                    Created: {new Date(task.created_at).toLocaleDateString()}
                  </div>
                  {task.updated_at && task.updated_at !== task.created_at && (
                    <div className="flex items-center">
                      <PencilIcon className="h-4 w-4 mr-1" />
                      Updated: {new Date(task.updated_at).toLocaleDateString()}
                    </div>
                  )}
                </div>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="p-4 sm:p-6 space-y-4 sm:space-y-6">
                {/* Task Title */}
                <div className="space-y-2">
                  <label htmlFor="title" className="block text-sm font-semibold text-gray-700">
                    Task Title *
                  </label>
                  <input
                    type="text"
                    id="title"
                    name="title"
                    value={formData.title}
                    onChange={handleChange}
                    className={`input-elegant ${
                      errors.title ? 'border-red-300 bg-red-50/50' : ''
                    }`}
                    placeholder="Enter a clear, descriptive task title..."
                  />
                  {errors.title && (
                    <div className="flex items-center space-x-2 text-red-600">
                      <ExclamationCircleIcon className="h-4 w-4" />
                      <p className="text-sm">{errors.title}</p>
                    </div>
                  )}
                </div>

                {/* Description */}
                <div className="space-y-2">
                  <label htmlFor="description" className="block text-sm font-semibold text-gray-700">
                    Description *
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    rows={4}
                    value={formData.description}
                    onChange={handleChange}
                    className={`input-elegant resize-none ${
                      errors.description ? 'border-red-300 bg-red-50/50' : ''
                    }`}
                    placeholder="Describe what needs to be done, include any important details..."
                  />
                  {errors.description && (
                    <div className="flex items-center space-x-2 text-red-600">
                      <ExclamationCircleIcon className="h-4 w-4" />
                      <p className="text-sm">{errors.description}</p>
                    </div>
                  )}
                </div>

                {/* Status and Priority */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                  <div className="space-y-2">
                    <label htmlFor="status" className="block text-sm font-semibold text-gray-700 flex items-center">
                      <FlagIcon className="h-4 w-4 mr-2 text-blue-500" />
                      Status
                    </label>
                    <select
                      id="status"
                      name="status"
                      value={formData.status}
                      onChange={handleChange}
                      className="input-elegant appearance-none cursor-pointer"
                    >
                      <option value="todo">📋 To Do</option>
                      <option value="in_progress">🔄 In Progress</option>
                      <option value="done">✅ Done</option>
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="priority" className="block text-sm font-semibold text-gray-700">
                      Priority
                    </label>
                    <select
                      id="priority"
                      name="priority"
                      value={formData.priority}
                      onChange={handleChange}
                      className="input-elegant appearance-none cursor-pointer"
                    >
                      <option value="low">🌱 Low</option>
                      <option value="medium">⚡ Medium</option>
                      <option value="high">🔥 High</option>
                    </select>
                  </div>
                </div>

                {/* Project Assignment */}
                <div className="space-y-2">
                  <label htmlFor="project_id" className="block text-sm font-semibold text-gray-700 flex items-center">
                    <FolderIcon className="h-4 w-4 mr-2 text-primary-500" />
                    Assign to Project (Optional)
                  </label>
                  <select
                    id="project_id"
                    name="project_id"
                    value={formData.project_id}
                    onChange={handleChange}
                    className="input-elegant appearance-none cursor-pointer"
                  >
                    <option value="">📁 No project - Standalone task</option>
                    {projects.map((project) => (
                      <option key={project.id} value={project.id}>
                        📂 {project.name}
                      </option>
                    ))}
                  </select>
                  <p className="text-xs text-gray-500">
                    Choose a project to organize this task, or leave it as a standalone task
                  </p>
                </div>

                {/* Actions */}
                <div className="flex flex-col-reverse sm:flex-row justify-end gap-3 sm:gap-4 pt-4 sm:pt-6 border-t border-gray-100">
                  <button
                    type="button"
                    onClick={onClose}
                    className="btn-secondary w-full sm:w-auto"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading || !formData.title.trim() || !formData.description.trim()}
                    className="btn-primary relative overflow-hidden w-full sm:w-auto"
                  >
                    <span className="flex items-center">
                      {isLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2" />
                          Updating Task...
                        </>
                      ) : (
                        <>
                          <PencilIcon className="h-4 w-4 mr-2" />
                          Update Task
                        </>
                      )}
                    </span>
                  </button>
                </div>
              </form>
            </Dialog.Panel>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition>
  );
};

export default EditTaskModal;