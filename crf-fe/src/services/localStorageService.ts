const localStorageService = {
  set<T>(key: string, value: T) {
    if (typeof window === 'undefined') {
      console.warn('localStorage not available in SSR environment');
      return;
    }

    try {
      const serialized = JSON.stringify(value);
      localStorage.setItem(key, serialized);
    } catch (error) {
      console.error(`localStorage set error for key "${key}":`, error);
    }
  },

  get<T>(key: string): T | null {
    if (typeof window === 'undefined') {
      console.warn('localStorage not available in SSR environment');
      return null;
    }

    try {
      const item = localStorage.getItem(key);
      return item ? (JSON.parse(item) as T) : null;
    } catch (error) {
      console.error(`localStorage get error for key "${key}":`, error);
      return null;
    }
  },

  remove(key: string) {
    if (typeof window === 'undefined') {
      console.warn('localStorage not available in SSR environment');
      return;
    }

    try {
      localStorage.removeItem(key);
    } catch (error) {
      console.error(`localStorage remove error for key "${key}":`, error);
    }
  },

  clear() {
    if (typeof window === 'undefined') {
      console.warn('localStorage not available in SSR environment');
      return;
    }

    try {
      localStorage.clear();
    } catch (error) {
      console.error('localStorage clear error:', error);
    }
  },
};

export default localStorageService;
