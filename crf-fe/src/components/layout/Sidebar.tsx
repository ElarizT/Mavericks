import React from 'react';

interface SidebarProps {
  children: React.ReactNode;
  title?: string;
  className?: string;
}

export const Sidebar: React.FC<SidebarProps> = ({
  children,
  title,
  className = '',
}) => {
  return (
    <aside className={`flex flex-col h-full bg-gray-50 border-r ${className}`}>
      {title && (
        <div className='p-4 border-b bg-white'>
          <h2 className='text-lg font-semibold'>{title}</h2>
        </div>
      )}
      <div className='flex-1 overflow-y-auto'>{children}</div>
    </aside>
  );
};
