import styles from './DotsSpinner.module.css';
import type { FC } from 'react';

export const DotsSpinner: FC = () => {
  return (
    <div className="flex items-center justify-center space-x-2">
      {['•', '•', '•', '•', '•'].map((letter, index) => (
        <span
          key={index}
          className={`text-xl font-bold text-black-500 ${styles.bounce}`}
          style={{
            animationDelay: `${index * 0.1}s`
          }}
        >
          {letter}
        </span>
      ))}
    </div>
  );
};
