/**
 * Dashboard component
 */
import React, { useEffect } from 'react';
import { useAuthStore } from '../../store/authStore';
import { useProjectStore } from '../../store/projectStore';
import { useTaskStore } from '../../store/taskStore';
import { useDashboardStore } from '../../store/dashboardStore';
import {
  FolderIcon,
  ClipboardDocumentListIcon,
  CheckCircleIcon,
  ClockIcon,
} from '@heroicons/react/24/outline';

const Dashboard: React.FC = () => {
  const { user } = useAuthStore();
  const { projects, fetchProjects } = useProjectStore();
  const { tasks, fetchTasks } = useTaskStore();
  const { stats: dashboardStats, fetchStats } = useDashboardStore();

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
      color: 'bg-blue-500',
    },
    {
      name: 'Total Tasks',
      value: dashboardStats?.tasks_count || 0,
      icon: ClipboardDocumentListIcon,
      color: 'bg-green-500',
    },
    {
      name: 'Completed Tasks',
      value: dashboardStats?.completed_tasks || 0,
      icon: CheckCircleIcon,
      color: 'bg-purple-500',
    },
    {
      name: 'Active Projects',
      value: dashboardStats?.active_projects || 0,
      icon: ClockIcon,
      color: 'bg-yellow-500',
    },
  ];

  const recentTasks = tasks.slice(0, 5);
  const recentProjects = projects.slice(0, 5);

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">
          Welcome back, {user?.full_name}!
        </h1>
        <p className="mt-2 text-gray-600">
          Here's what's happening with your projects and tasks.
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <div
            key={stat.name}
            className="bg-white overflow-hidden shadow rounded-lg"
          >
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`${stat.color} p-3 rounded-md`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="text-lg font-medium text-gray-900">
                      {stat.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Recent Projects and Tasks */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Projects */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Recent Projects</h3>
          </div>
          <div className="p-6">
            {recentProjects.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                No projects yet. Create your first project!
              </p>
            ) : (
              <div className="space-y-4">
                {recentProjects.map((project) => (
                  <div
                    key={project.id}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
                  >
                    <div>
                      <h4 className="font-medium text-gray-900">{project.name}</h4>
                      <p className="text-sm text-gray-500">{project.description}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          project.status === 'active'
                            ? 'bg-green-100 text-green-800'
                            : project.status === 'planning'
                            ? 'bg-yellow-100 text-yellow-800'
                            : project.status === 'completed'
                            ? 'bg-blue-100 text-blue-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {project.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Recent Tasks */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Recent Tasks</h3>
          </div>
          <div className="p-6">
            {recentTasks.length === 0 ? (
              <p className="text-gray-500 text-center py-4">
                No tasks yet. Create your first task!
              </p>
            ) : (
              <div className="space-y-4">
                {recentTasks.map((task) => (
                  <div
                    key={task.id}
                    className="flex items-center justify-between p-4 border border-gray-200 rounded-lg hover:bg-gray-50"
                  >
                    <div>
                      <h4 className="font-medium text-gray-900">{task.title}</h4>
                      <p className="text-sm text-gray-500">{task.description}</p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span
                        className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          task.status === 'done'
                            ? 'bg-green-100 text-green-800'
                            : task.status === 'in_progress'
                            ? 'bg-blue-100 text-blue-800'
                            : task.status === 'review'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}
                      >
                        {task.status.replace('_', ' ')}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;