import React from 'react';
import { Button } from '../ui/button';

interface HeaderProps {
  title?: string;
  onLogout?: () => void;
  className?: string;
}

export const Header: React.FC<HeaderProps> = ({
  title = 'Document Chat',
  onLogout,
  className = '',
}) => {
  return (
    <header
      className={`flex items-center justify-between p-4 border-b bg-white ${className}`}
    >
      <div className='flex items-center space-x-2'>
        <h1 className='text-xl font-semibold'>{title}</h1>
      </div>

      <div className='flex items-center space-x-2'>
        {onLogout && (
          <Button variant='outline' size='sm' onClick={onLogout}>
            Logout
          </Button>
        )}
      </div>
    </header>
  );
};
