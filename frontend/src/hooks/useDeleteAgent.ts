import { useState } from 'react';
import { agentService } from '../services/agentService';

export const useDeleteAgent = () => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<Error | null>(null);

  const deleteAgent = async (agentId: string) => {
    setIsDeleting(true);
    setError(null);
    try {
      await agentService.deleteAgent(agentId);
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Failed to delete agent'));
      throw err;
    } finally {
      setIsDeleting(false);
    }
  };

  return {
    deleteAgent,
    isDeleting,
    error
  };
}; 