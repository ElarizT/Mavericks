import { Theme } from '../contexts/ThemeContext';

export const getThemeColors = (theme: Theme) => {
  return {
    // Background colors
    bg: theme === 'light' ? 'bg-light-bg' : 'bg-dark-bg',
    bgAlt: theme === 'light' ? 'bg-light-bgAlt' : 'bg-dark-bgAlt',
    
    // Text colors
    text: theme === 'light' ? 'text-light-text' : 'text-dark-text',
    textSecondary: theme === 'light' ? 'text-light-secondary-secondary' : 'text-dark-secondary-secondary',
    
    // Border colors
    border: theme === 'light' ? 'border-light-secondary-secondary' : 'border-dark-secondary-secondary',
    
    // Button colors
    buttonPrimary: theme === 'light'
      ? 'bg-light-secondary-primary text-light-bg hover:bg-light-secondary-secondary'
      : 'bg-dark-secondary-primary text-dark-bg hover:bg-dark-secondary-secondary',
    
    // Input colors
    input: theme === 'light'
      ? 'border-light-secondary-secondary text-light-text placeholder-light-secondary-secondary focus:ring-light-secondary-primary focus:border-light-secondary-primary'
      : 'border-dark-secondary-secondary text-dark-text placeholder-dark-secondary-secondary focus:ring-dark-secondary-primary focus:border-dark-secondary-primary',
    
    // Focus ring colors
    focusRing: theme === 'light'
      ? 'focus:ring-light-secondary-primary focus:ring-offset-light-bg'
      : 'focus:ring-dark-secondary-primary focus:ring-offset-dark-bg',
  };
}; 