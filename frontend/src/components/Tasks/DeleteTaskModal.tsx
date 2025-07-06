/**
 * DeleteTaskModal component - Confirmation dialog for task deletion
 */
import React from 'react';
import { Dialog, Transition } from '@headlessui/react';
import { useTaskStore } from '../../store/taskStore';
import { Task } from '../../types';
import { 
  ExclamationTriangleIcon, 
  XMarkIcon, 
  CalendarIcon,
  TrashIcon,
  QueueListIcon,
  ClockIcon,
  CheckCircleIcon,
  ClipboardDocumentListIcon,
  ChartBarIcon,
  BoltIcon,
  FireIcon
} from '@heroicons/react/24/outline';
import { ExclamationTriangleIcon as ExclamationTriangleIconSolid } from '@heroicons/react/24/solid';

interface DeleteTaskModalProps {
  isOpen: boolean;
  onClose: () => void;
  task: Task;
}

const DeleteTaskModal: React.FC<DeleteTaskModalProps> = ({
  isOpen,
  onClose,
  task,
}) => {
  const { deleteTask, isLoading } = useTaskStore();

  const handleDelete = async () => {
    try {
      await deleteTask(task.id);
      onClose();
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'todo':
        return <QueueListIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
      case 'in_progress':
        return <ClockIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
      case 'done':
        return <CheckCircleIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
      default:
        return <ClipboardDocumentListIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
    }
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'low':
        return <ChartBarIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
      case 'medium':
        return <BoltIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
      case 'high':
        return <FireIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
      default:
        return <QueueListIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />;
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
        
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Transition.Child
            enter="ease-out duration-300"
            enterFrom="opacity-0 scale-95"
            enterTo="opacity-100 scale-100"
            leave="ease-in duration-200"
            leaveFrom="opacity-100 scale-100"
            leaveTo="opacity-0 scale-95"
          >
            <Dialog.Panel className="mx-auto max-w-2xl w-full bg-white rounded-2xl shadow-elegant-lg overflow-hidden">
              {/* Header */}
              <div className="bg-gradient-to-r from-red-50 to-red-100/50 px-6 py-5 border-b border-red-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="p-2 bg-gradient-to-br from-red-500 to-red-600 rounded-xl shadow-lg">
                      <ExclamationTriangleIconSolid className="h-6 w-6 text-white" />
                    </div>
                    <div>
                      <Dialog.Title className="text-2xl font-bold text-gray-900">
                        Delete Task
                      </Dialog.Title>
                      <p className="text-gray-600 text-sm">This action cannot be undone</p>
                    </div>
                  </div>
                  <button
                    onClick={onClose}
                    className="p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 transition-all duration-300"
                  >
                    <XMarkIcon className="h-6 w-6" />
                  </button>
                </div>
              </div>

              {/* Warning Message */}
              <div className="px-6 py-4 bg-red-50/50 border-b border-red-100">
                <div className="flex items-start space-x-3">
                  <ExclamationTriangleIcon className="h-5 w-5 text-red-500 mt-0.5 flex-shrink-0" />
                  <div>
                    <p className="text-sm text-gray-800">
                      Are you sure you want to delete the task{' '}
                      <span className="font-semibold text-red-600">"{task.title}"</span>?
                    </p>
                    <p className="text-xs text-gray-600 mt-1">
                      This will permanently remove all task data and cannot be recovered.
                    </p>
                  </div>
                </div>
              </div>

              {/* Task Preview */}
              <div className="p-6">
                <div className="bg-white border border-gray-200 rounded-xl p-5 shadow-sm">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h4 className="text-lg font-semibold text-gray-900 mb-2">{task.title}</h4>
                      <p className="text-gray-600 text-sm leading-relaxed">
                        {task.description || 'No description provided'}
                      </p>
                    </div>
                  </div>

                  {/* Task Details */}
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t border-gray-100">
                    <div className="text-center">
                      {getStatusIcon(task.status)}
                      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Status</p>
                      <p className="text-sm text-gray-900 capitalize">
                        {task.status.replace('_', ' ')}
                      </p>
                    </div>

                    <div className="text-center">
                      {getPriorityIcon(task.priority)}
                      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Priority</p>
                      <p className="text-sm text-gray-900 capitalize">{task.priority}</p>
                    </div>

                    <div className="text-center">
                      <CalendarIcon className="h-6 w-6 mx-auto mb-1 text-gray-400" />
                      <p className="text-xs font-medium text-gray-500 uppercase tracking-wide">Created</p>
                      <p className="text-sm text-gray-900">
                        {new Date(task.created_at).toLocaleDateString()}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Actions */}
                <div className="flex justify-end space-x-4 pt-6 border-t border-gray-100 mt-6">
                  <button
                    type="button"
                    onClick={onClose}
                    className="btn-secondary"
                  >
                    Cancel
                  </button>
                  <button
                    type="button"
                    onClick={handleDelete}
                    disabled={isLoading}
                    className="bg-gradient-to-r from-red-600 to-red-700 text-white font-medium py-2.5 px-5 rounded-lg transition-all duration-300 transform hover:scale-105 hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none relative overflow-hidden"
                  >
                    <span className="flex items-center">
                      {isLoading ? (
                        <>
                          <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2" />
                          Deleting Task...
                        </>
                      ) : (
                        <>
                          <TrashIcon className="h-4 w-4 mr-2" />
                          Delete Task
                        </>
                      )}
                    </span>
                  </button>
                </div>
              </div>
            </Dialog.Panel>
          </Transition.Child>
        </div>
      </Dialog>
    </Transition>
  );
};

export default DeleteTaskModal;