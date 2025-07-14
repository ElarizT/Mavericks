// Simple toast hook for error handling
// TODO: Replace with proper toast library like react-hot-toast or react-toastify
export const useToast = () => {
  const showSuccess = (message: string) => {
    console.log('✅ Success:', message);
    // TODO: Replace with proper toast notification
    alert(`Success: ${message}`);
  };

  const showError = (message: string) => {
    console.error('❌ Error:', message);
    // TODO: Replace with proper toast notification
    alert(`Error: ${message}`);
  };

  return { showSuccess, showError };
};
