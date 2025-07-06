import { useEffect, useState } from 'react';
import { X } from 'lucide-react';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface ToastProps {
  id: string;
  title: string;
  message?: string;
  type: ToastType;
  duration?: number;
  onClose: (id: string) => void;
}

export const Toast: React.FC<ToastProps> = ({
  id,
  title,
  message,
  type,
  duration = 5000,
  onClose,
}) => {
  const [isVisible, setIsVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsVisible(false);
      setTimeout(() => onClose(id), 300);
    }, duration);

    return () => clearTimeout(timer);
  }, [id, duration, onClose]);

  const getTypeStyles = () => {
    switch (type) {
      case 'success':
        return 'bg-gradient-to-r from-success-50 to-success-100 border-success-300 text-success-800 shadow-success';
      case 'error':
        return 'bg-gradient-to-r from-danger-50 to-danger-100 border-danger-300 text-danger-800 shadow-danger';
      case 'warning':
        return 'bg-gradient-to-r from-warning-50 to-warning-100 border-warning-300 text-warning-800 shadow-warning';
      case 'info':
        return 'bg-gradient-to-r from-primary-50 to-primary-100 border-primary-300 text-primary-800 shadow-colorful';
      default:
        return 'bg-gradient-to-r from-gray-50 to-gray-100 border-gray-300 text-gray-800 shadow-md';
    }
  };

  return (
    <div
      className={`
        fixed top-4 right-4 z-50 max-w-md p-4 border-2 rounded-2xl backdrop-blur-xl
        transition-all duration-500 ease-in-out
        ${isVisible ? 'translate-x-0 opacity-100' : 'translate-x-full opacity-0'}
        ${getTypeStyles()}
      `}
    >
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <h4 className="font-semibold text-sm">{title}</h4>
          {message && (
            <p className="mt-1 text-sm opacity-90">{message}</p>
          )}
        </div>
        <button
          onClick={() => {
            setIsVisible(false);
            setTimeout(() => onClose(id), 300);
          }}
          className="ml-3 text-gray-400 hover:text-gray-600 transition-all duration-300 hover:scale-110 hover:bg-white/50 rounded-lg p-1"
        >
          <X size={16} />
        </button>
      </div>
    </div>
  );
};

export interface ToastContextType {
  showToast: (toast: Omit<ToastProps, 'id' | 'onClose'>) => void;
  showSuccess: (title: string, message?: string) => void;
  showError: (title: string, message?: string) => void;
  showWarning: (title: string, message?: string) => void;
  showInfo: (title: string, message?: string) => void;
}

export const ToastContainer: React.FC = () => {
  const [toasts, setToasts] = useState<ToastProps[]>([]);

  const removeToast = (id: string) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  };

  const showToast = (toast: Omit<ToastProps, 'id' | 'onClose'>) => {
    const id = Date.now().toString();
    setToasts(prev => [...prev, { ...toast, id, onClose: removeToast }]);
  };

  const showSuccess = (title: string, message?: string) => {
    showToast({ title, message, type: 'success' });
  };

  const showError = (title: string, message?: string) => {
    showToast({ title, message, type: 'error' });
  };

  const showWarning = (title: string, message?: string) => {
    showToast({ title, message, type: 'warning' });
  };

  const showInfo = (title: string, message?: string) => {
    showToast({ title, message, type: 'info' });
  };

  // Expose toast functions globally
  useEffect(() => {
    (window as any).toast = {
      showToast,
      showSuccess,
      showError,
      showWarning,
      showInfo,
    };
  }, []);

  return (
    <div className="toast-container">
      {toasts.map(toast => (
        <Toast key={toast.id} {...toast} />
      ))}
    </div>
  );
};