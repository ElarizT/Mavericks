import React, { useState } from 'react';

interface SplitPaneLayoutProps {
  leftPanel: React.ReactNode;
  rightPanel: React.ReactNode;
  leftPanelWidth?: number;
  minLeftWidth?: number;
  maxLeftWidth?: number;
  className?: string;
}

export const SplitPaneLayout: React.FC<SplitPaneLayoutProps> = ({
  leftPanel,
  rightPanel,
  leftPanelWidth = 300,
  minLeftWidth = 200,
  maxLeftWidth = 500,
  className = '',
}) => {
  const [leftWidth, setLeftWidth] = useState(leftPanelWidth);
  const [isDragging, setIsDragging] = useState(false);

  const handleMouseDown = (e: React.MouseEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleMouseMove = (e: MouseEvent) => {
    if (!isDragging) return;

    const container = e.currentTarget as HTMLElement;
    const rect = container.getBoundingClientRect();
    const newWidth = e.clientX - rect.left;

    if (newWidth >= minLeftWidth && newWidth <= maxLeftWidth) {
      setLeftWidth(newWidth);
    }
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  React.useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDragging, handleMouseMove]);

  return (
    <div className={`flex h-full ${className}`}>
      <div
        className='flex-shrink-0 overflow-hidden'
        style={{ width: leftWidth }}
      >
        {leftPanel}
      </div>

      <div
        className='w-1 bg-gray-200 cursor-col-resize hover:bg-gray-300 transition-colors'
        onMouseDown={handleMouseDown}
      />

      <div className='flex-1 overflow-hidden'>{rightPanel}</div>
    </div>
  );
};
