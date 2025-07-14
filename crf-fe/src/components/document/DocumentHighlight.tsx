import React from 'react';

interface DocumentHighlightProps {
  text: string;
  highlights: Array<{
    start: number;
    end: number;
    color?: string;
  }>;
  className?: string;
}

export const DocumentHighlight: React.FC<DocumentHighlightProps> = ({
  text,
  highlights,
  className = '',
}) => {
  const renderHighlightedText = () => {
    if (highlights.length === 0) {
      return <span>{text}</span>;
    }

    const parts: React.ReactNode[] = [];
    let lastIndex = 0;

    highlights.forEach((highlight, index) => {
      // Add text before highlight
      if (highlight.start > lastIndex) {
        parts.push(
          <span key={`text-${index}`}>
            {text.slice(lastIndex, highlight.start)}
          </span>
        );
      }

      // Add highlighted text
      parts.push(
        <span
          key={`highlight-${index}`}
          className={`bg-yellow-200 px-1 rounded ${highlight.color || ''}`}
        >
          {text.slice(highlight.start, highlight.end)}
        </span>
      );

      lastIndex = highlight.end;
    });

    // Add remaining text
    if (lastIndex < text.length) {
      parts.push(<span key='text-end'>{text.slice(lastIndex)}</span>);
    }

    return parts;
  };

  return (
    <div className={`text-sm leading-relaxed ${className}`}>
      {renderHighlightedText()}
    </div>
  );
};
