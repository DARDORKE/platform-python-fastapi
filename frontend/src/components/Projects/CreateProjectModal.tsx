/**
 * Create project modal component
 */
import React, { useState } from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { XMarkIcon, RocketLaunchIcon, CalendarIcon, CurrencyEuroIcon, FlagIcon } from '@heroicons/react/24/outline';
import { useProjectStore } from '../../store/projectStore';
import { CreateProjectData } from '../../types';

interface CreateProjectModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const CreateProjectModal: React.FC<CreateProjectModalProps> = ({
  isOpen,
  onClose,
}) => {
  const { createProject, isLoading } = useProjectStore();
  
  const [formData, setFormData] = useState<CreateProjectData>({
    name: '',
    description: '',
    status: 'planning',
    priority: 'medium',
    start_date: '',
    end_date: '',
    budget: undefined,
  });

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'budget' ? (value ? parseInt(value) : undefined) : value,
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createProject(formData);
      handleClose();
    } catch (error) {
      // Error is handled by the store
    }
  };

  const handleClose = () => {
    setFormData({
      name: '',
      description: '',
      status: 'planning',
      priority: 'medium',
      start_date: '',
      end_date: '',
      budget: undefined,
    });
    onClose();
  };

  return (
    <Transition show={isOpen} as={React.Fragment}>
      <Dialog onClose={handleClose} className="relative z-50">
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
        
        <div className="fixed inset-0 flex items-center justify-center p-4 sm:p-6">
          <Transition.Child
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
          >
            <Dialog.Panel className="mx-auto max-w-2xl w-full max-h-[90vh] overflow-y-auto bg-white/95 backdrop-blur-xl rounded-2xl shadow-colorful border border-white/20">
              {/* Header */}
              <div className="bg-gradient-to-r from-primary-100 to-secondary-100 px-4 sm:px-6 py-4 sm:py-5 border-b border-primary-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2 sm:space-x-3">
                    <div className="p-1.5 sm:p-2 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-xl shadow-colorful">
                      <RocketLaunchIcon className="h-5 w-5 sm:h-6 sm:w-6 text-white" />
                    </div>
                    <Dialog.Title className="text-lg sm:text-2xl font-bold text-gray-900">
                      Create New Project
                    </Dialog.Title>
                  </div>
                  <button
                    onClick={handleClose}
                    className="p-1.5 sm:p-2 rounded-xl text-gray-400 hover:text-danger-600 hover:bg-danger-50 transition-all duration-300 hover:scale-110"
                  >
                    <XMarkIcon className="h-5 w-5 sm:h-6 sm:w-6" />
                  </button>
                </div>
                <p className="text-gray-600 mt-2 text-sm sm:text-base">🚀 Fill in the details to create your new project</p>
              </div>

              {/* Form */}
              <form onSubmit={handleSubmit} className="p-4 sm:p-6 space-y-4 sm:space-y-6">
                {/* Project Name */}
                <div className="space-y-2">
                  <label htmlFor="name" className="block text-sm font-semibold text-gray-700">
                    Project Name *
                  </label>
                  <input
                    type="text"
                    id="name"
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="input-elegant"
                    placeholder="Enter a descriptive project name..."
                  />
                </div>

                {/* Description */}
                <div className="space-y-2">
                  <label htmlFor="description" className="block text-sm font-semibold text-gray-700">
                    Description
                  </label>
                  <textarea
                    id="description"
                    name="description"
                    rows={4}
                    value={formData.description}
                    onChange={handleChange}
                    className="input-elegant resize-none"
                    placeholder="Describe your project goals and objectives..."
                  />
                </div>

                {/* Status and Priority */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                  <div className="space-y-2">
                    <label htmlFor="status" className="block text-sm font-semibold text-gray-700 flex items-center">
                      <FlagIcon className="h-4 w-4 mr-2 text-secondary-500" />
                      Status
                    </label>
                    <select
                      id="status"
                      name="status"
                      value={formData.status}
                      onChange={handleChange}
                      className="input-elegant appearance-none cursor-pointer"
                    >
                      <option value="planning">📋 Planning</option>
                      <option value="active">🚀 Active</option>
                      <option value="on_hold">⏸️ On Hold</option>
                      <option value="completed">✅ Completed</option>
                      <option value="cancelled">❌ Cancelled</option>
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
                      <option value="urgent">🚨 Urgent</option>
                    </select>
                  </div>
                </div>

                {/* Dates */}
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-6">
                  <div className="space-y-2">
                    <label htmlFor="start_date" className="block text-sm font-semibold text-gray-700 flex items-center">
                      <CalendarIcon className="h-4 w-4 mr-2 text-primary-500" />
                      Start Date
                    </label>
                    <input
                      type="date"
                      id="start_date"
                      name="start_date"
                      value={formData.start_date}
                      onChange={handleChange}
                      className="input-elegant"
                    />
                  </div>

                  <div className="space-y-2">
                    <label htmlFor="end_date" className="block text-sm font-semibold text-gray-700 flex items-center">
                      <CalendarIcon className="h-4 w-4 mr-2 text-danger-500" />
                      End Date
                    </label>
                    <input
                      type="date"
                      id="end_date"
                      name="end_date"
                      value={formData.end_date}
                      onChange={handleChange}
                      className="input-elegant"
                    />
                  </div>
                </div>

                {/* Budget */}
                <div className="space-y-2">
                  <label htmlFor="budget" className="block text-sm font-semibold text-gray-700 flex items-center">
                    <CurrencyEuroIcon className="h-4 w-4 mr-2 text-success-500" />
                    Budget ($)
                  </label>
                  <div className="relative">
                    <CurrencyEuroIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
                    <input
                      type="number"
                      id="budget"
                      name="budget"
                      min="0"
                      step="100"
                      value={formData.budget || ''}
                      onChange={handleChange}
                      className="input-elegant pl-11"
                      placeholder="10,000"
                    />
                  </div>
                </div>

                {/* Actions */}
                <div className="flex flex-col sm:flex-row justify-end space-y-3 sm:space-y-0 sm:space-x-4 pt-4 sm:pt-6 border-t border-gradient-to-r from-primary-200 to-secondary-200">
                  <button
                    type="button"
                    onClick={handleClose}
                    className="w-full sm:w-auto order-2 sm:order-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2.5 px-6 rounded-xl transition-all duration-300 hover:scale-105"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={isLoading || !formData.name.trim()}
                    className="btn-primary relative overflow-hidden w-full sm:w-auto order-1 sm:order-2"
                  >
                    <span className="flex items-center">
                      {isLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2" />
                          Creating...
                        </>
                      ) : (
                        <>
                          <RocketLaunchIcon className="h-4 w-4 mr-2" />
                          Create Project
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

export default CreateProjectModal;