import type { FC, ReactNode } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
const ProtectedRoute: FC<{
  children: ReactNode;
}> = ({
  children
}) => {
  const {
    user,
    isLoading
  } = useAuth();
  if (isLoading) {
    return <div className="flex items-center justify-center h-screen">
        Loading...
      </div>;
  }
  if (!user) {
    return <Navigate to="/login" />;
  }
  return <>{children}</>;
};
export default ProtectedRoute;