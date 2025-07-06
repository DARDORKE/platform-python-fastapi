/**
 * Project list component
 */
import React, { useEffect, useState } from 'react';
import { useProjectStore } from '../../store/projectStore';
import { Project } from '../../types';
import { PlusIcon, FolderIcon, PencilIcon, TrashIcon, EyeIcon } from '@heroicons/react/24/outline';
import CreateProjectModal from './CreateProjectModal';
import EditProjectModal from './EditProjectModal';
import DeleteProjectModal from './DeleteProjectModal';
import ViewProjectModal from './ViewProjectModal';

const ProjectList: React.FC = () => {
  const { projects, fetchProjects, isLoading } = useProjectStore();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [editingProject, setEditingProject] = useState<Project | null>(null);
  const [deletingProject, setDeletingProject] = useState<Project | null>(null);
  const [viewingProject, setViewingProject] = useState<Project | null>(null);

  useEffect(() => {
    fetchProjects();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status.toUpperCase()) {
      case 'ACTIVE':
        return 'bg-gradient-to-r from-success-100 to-success-200 text-success-800 ring-2 ring-success-300/50';
      case 'PLANNING':
        return 'bg-gradient-to-r from-warning-100 to-warning-200 text-warning-800 ring-2 ring-warning-300/50';
      case 'COMPLETED':
        return 'bg-gradient-to-r from-primary-100 to-primary-200 text-primary-800 ring-2 ring-primary-300/50';
      case 'ON_HOLD':
        return 'bg-gradient-to-r from-secondary-100 to-secondary-200 text-secondary-800 ring-2 ring-secondary-300/50';
      case 'CANCELLED':
        return 'bg-gradient-to-r from-danger-100 to-danger-200 text-danger-800 ring-2 ring-danger-300/50';
      default:
        return 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 ring-2 ring-gray-300/50';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toUpperCase()) {
      case 'CRITICAL':
        return 'bg-gradient-to-r from-danger-100 to-danger-200 text-danger-800 ring-2 ring-danger-300/50';
      case 'HIGH':
        return 'bg-gradient-to-r from-warning-100 to-warning-200 text-warning-800 ring-2 ring-warning-300/50';
      case 'MEDIUM':
        return 'bg-gradient-to-r from-secondary-100 to-secondary-200 text-secondary-800 ring-2 ring-secondary-300/50';
      case 'LOW':
        return 'bg-gradient-to-r from-success-100 to-success-200 text-success-800 ring-2 ring-success-300/50';
      default:
        return 'bg-gradient-to-r from-gray-100 to-gray-200 text-gray-800 ring-2 ring-gray-300/50';
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary-200 border-t-primary-600 shadow-colorful"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gradient-primary">Projects</h1>
        <button
          onClick={() => setIsCreateModalOpen(true)}
          className="btn-primary flex items-center"
        >
          <PlusIcon className="h-4 w-4 mr-2" />
          New Project
        </button>
      </div>

      {/* Projects Grid */}
      {projects.length === 0 ? (
        <div className="text-center py-12">
          <FolderIcon className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No projects</h3>
          <p className="mt-1 text-sm text-gray-500">
            Get started by creating a new project.
          </p>
          <div className="mt-6">
            <button
              onClick={() => setIsCreateModalOpen(true)}
              className="btn-primary flex items-center"
            >
              <PlusIcon className="h-4 w-4 mr-2" />
              New Project
            </button>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <div
              key={project.id}
              className="card-colorful overflow-hidden hover-lift group"
            >
              <div className="p-6">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-700 transition-colors truncate">
                    {project.name}
                  </h3>
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(
                      project.status
                    )}`}
                  >
                    {project.status.replace('_', ' ')}
                  </span>
                </div>
                
                <p className="text-sm text-gray-500 mb-4 line-clamp-2">
                  {project.description || 'No description provided'}
                </p>
                
                <div className="flex items-center justify-between mb-4">
                  <span
                    className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getPriorityColor(
                      project.priority
                    )}`}
                  >
                    {project.priority} priority
                  </span>
                  
                  <span className="text-xs text-gray-500">
                    {new Date(project.created_at).toLocaleDateString()}
                  </span>
                </div>

                {/* Budget */}
                {project.budget && (
                  <div className="mb-4">
                    <span className="text-sm text-gray-600">
                      Budget: <span className="font-medium">${project.budget.toLocaleString()}</span>
                    </span>
                  </div>
                )}
                
                {/* Actions */}
                <div className="flex justify-end space-x-2">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setViewingProject(project);
                    }}
                    className="p-2 text-gray-400 hover:text-primary-600 transition-all duration-300 hover:scale-110 hover:bg-primary-50 rounded-lg"
                    title="View project"
                  >
                    <EyeIcon className="h-5 w-5" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setEditingProject(project);
                    }}
                    className="p-2 text-gray-400 hover:text-secondary-600 transition-all duration-300 hover:scale-110 hover:bg-secondary-50 rounded-lg"
                    title="Edit project"
                  >
                    <PencilIcon className="h-5 w-5" />
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setDeletingProject(project);
                    }}
                    className="p-2 text-gray-400 hover:text-danger-600 transition-all duration-300 hover:scale-110 hover:bg-danger-50 rounded-lg"
                    title="Delete project"
                  >
                    <TrashIcon className="h-5 w-5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modals */}
      <CreateProjectModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
      />
      
      {editingProject && (
        <EditProjectModal
          isOpen={!!editingProject}
          onClose={() => setEditingProject(null)}
          project={editingProject}
        />
      )}
      
      {deletingProject && (
        <DeleteProjectModal
          isOpen={!!deletingProject}
          onClose={() => setDeletingProject(null)}
          project={deletingProject}
        />
      )}
      
      {viewingProject && (
        <ViewProjectModal
          isOpen={!!viewingProject}
          onClose={() => setViewingProject(null)}
          project={viewingProject}
        />
      )}
    </div>
  );
};

export default ProjectList;