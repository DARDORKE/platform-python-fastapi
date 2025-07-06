/**
 * Login form component
 */
import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';
import { LoginCredentials } from '../../types';
import { 
  EyeIcon, 
  EyeSlashIcon, 
  EnvelopeIcon, 
  LockClosedIcon,
  SparklesIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/outline';

const LoginForm: React.FC = () => {
  const navigate = useNavigate();
  const { login, isLoading, error, clearError } = useAuthStore();
  const [showPassword, setShowPassword] = useState(false);
  const [focusedField, setFocusedField] = useState<string | null>(null);
  
  const [formData, setFormData] = useState<LoginCredentials>({
    email: '',
    password: '',
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (error) clearError();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(formData);
      navigate('/');
    } catch (error) {
      // Error is handled by the store
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-100 via-white to-secondary-100 py-12 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Background decorations */}
      <div className="absolute top-0 left-0 w-72 h-72 bg-gradient-to-br from-primary-300/40 to-secondary-300/30 rounded-full -translate-x-1/2 -translate-y-1/2 blur-3xl" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-gradient-to-tl from-secondary-200/30 to-warning-200/20 rounded-full translate-x-1/2 translate-y-1/2 blur-3xl" />
      
      <div className="max-w-md w-full space-y-8 relative z-10">
        {/* Header */}
        <div className="text-center animate-slide-in-up">
          <div className="mx-auto w-16 h-16 bg-gradient-to-br from-primary-500 to-secondary-500 rounded-2xl shadow-colorful flex items-center justify-center mb-6 transform hover:scale-105 transition-transform duration-300">
            <SparklesIcon className="h-8 w-8 text-white" />
          </div>
          <h2 className="text-4xl font-bold text-gradient-rainbow mb-2">
            Welcome Back
          </h2>
          <p className="text-gray-600">
            Sign in to continue to your dashboard
          </p>
          <p className="mt-4 text-sm text-gray-500">
            Don't have an account?{' '}
            <Link
              to="/register"
              className="font-semibold text-primary-600 hover:text-secondary-600 transition-colors duration-300 hover:underline"
            >
              Create one here
            </Link>
          </p>
        </div>
        
        {/* Login Card */}
        <div className="card-colorful p-8 animate-slide-in-up" style={{ animationDelay: '0.1s' }}>
          <form className="space-y-6" onSubmit={handleSubmit}>
            {/* Error Message */}
            {error && (
              <div className="bg-gradient-to-r from-danger-50 to-danger-100 border border-danger-200 text-danger-700 px-4 py-3 rounded-xl flex items-center space-x-3 animate-slide-in-up shadow-danger">
                <ExclamationTriangleIcon className="h-5 w-5 text-danger-500 flex-shrink-0" />
                <span className="text-sm">{error}</span>
              </div>
            )}
            
            <div className="space-y-5">
              {/* Email Field */}
              <div className="space-y-2">
                <label htmlFor="email" className="block text-sm font-semibold text-gray-700">
                  Email Address
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <EnvelopeIcon className={`h-5 w-5 transition-colors duration-300 ${
                      focusedField === 'email' ? 'text-primary-500' : 'text-gray-400'
                    }`} />
                  </div>
                  <input
                    id="email"
                    name="email"
                    type="email"
                    autoComplete="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    onFocus={() => setFocusedField('email')}
                    onBlur={() => setFocusedField(null)}
                    className="input-elegant pl-11 transition-all duration-300"
                    placeholder="Enter your email"
                  />
                </div>
              </div>
              
              {/* Password Field */}
              <div className="space-y-2">
                <label htmlFor="password" className="block text-sm font-semibold text-gray-700">
                  Password
                </label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <LockClosedIcon className={`h-5 w-5 transition-colors duration-300 ${
                      focusedField === 'password' ? 'text-primary-500' : 'text-gray-400'
                    }`} />
                  </div>
                  <input
                    id="password"
                    name="password"
                    type={showPassword ? 'text' : 'password'}
                    autoComplete="current-password"
                    required
                    value={formData.password}
                    onChange={handleChange}
                    onFocus={() => setFocusedField('password')}
                    onBlur={() => setFocusedField(null)}
                    className="input-elegant pl-11 pr-11 transition-all duration-300"
                    placeholder="Enter your password"
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute inset-y-0 right-0 pr-3 flex items-center hover:text-primary-600 transition-colors duration-300"
                  >
                    {showPassword ? (
                      <EyeSlashIcon className="h-5 w-5 text-gray-400" />
                    ) : (
                      <EyeIcon className="h-5 w-5 text-gray-400" />
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Demo Accounts */}
            <div className="bg-gradient-to-r from-primary-100 to-secondary-100 rounded-xl p-4 border border-primary-200 shadow-md">
              <p className="text-xs font-semibold text-gray-700 mb-2">Demo Accounts:</p>
              <div className="grid grid-cols-1 gap-1 text-xs text-gray-600">
                <div>Admin: admin@example.com / admin123</div>
                <div>Manager: manager@example.com / manager123</div>
                <div>User: john.doe@example.com / user123</div>
              </div>
            </div>

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="btn-primary w-full relative overflow-hidden group disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
            >
              <span className="relative z-10 flex items-center justify-center">
                {isLoading ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent mr-2" />
                    Signing you in...
                  </>
                ) : (
                  'Sign In'
                )}
              </span>
              {!isLoading && (
                <div className="absolute inset-0 bg-gradient-to-r from-secondary-500 to-primary-600 translate-x-full group-hover:translate-x-0 transition-transform duration-500" />
              )}
            </button>
            
            {/* Additional Options */}
            <div className="text-center">
              <Link
                to="/forgot-password"
                className="text-sm text-gray-500 hover:text-primary-600 transition-colors duration-300"
              >
                Forgot your password?
              </Link>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;