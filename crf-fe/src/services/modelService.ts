import { apiService } from './apiService';

export interface ModelConfig {
  id: string;
  name: string;
  model: string;
  system_prompt: string;
  temperature: number;
  credentials: Record<string, string>;
  max_last_messages: number;
  user_prompt: string;
}

export interface ModelsConfigs {
  api_key: string;
  provider: string;
  configs: ModelConfig[];
  metadata: Record<string, string>;
}

export interface CreateProviderBody {
  name: string;
  api_key: string;
  metadata: Record<string, string>;
}

export interface CreateModelBody {
  name: string;
  model: string;
  system_prompt: string;
  temperature: number;
  user_prompt: string;
  max_last_messages: number;
  provider: string;
  credentials: Record<string, string>;
  id?: string;
}

export interface Provider {
  id: string;
  provider: string;
  api_key: string;
  created_at: string;
  updated_at: string;
  metadata: Record<string, string>;
}

export interface Config {
  provider: string;
  data: Record<string, string>;
}

export interface ActiveModel extends ModelConfig {
  provider: string;
}

export const AI_PROVIDERS = {
  OPENAI: 'openai',
  AZURE_OPENAI: 'azure openai',
  OLLAMA: 'ollama',
  GENAI: 'genai', // remove after hackathon
} as const;

export type AIProvider = (typeof AI_PROVIDERS)[keyof typeof AI_PROVIDERS];

export const TOOLTIP_MESSAGES = {
  openai: 'Provide OpenAI API key for adding a model',
  'azure openai':
    'Provide Azure OpenAI endpoint, API key, API version and Deployment name for adding a model',
  ollama: 'Provide Ollama Base URL for adding a model',
};

export const PROVIDERS_OPTIONS = [
  { value: AI_PROVIDERS.GENAI, label: 'GenAI' }, // remove after hackathon
  { value: AI_PROVIDERS.OPENAI, label: 'OpenAI' },
  { value: AI_PROVIDERS.AZURE_OPENAI, label: 'Azure OpenAI' },
  { value: AI_PROVIDERS.OLLAMA, label: 'Ollama' },
];

export const modelService = {
  async getPrompt() {
    const response = await apiService.get<{ system_prompt: string }>(
      '/api/llm/model/prompt'
    );

    return response.data?.system_prompt;
  },

  async getModels() {
    const response = await apiService.get<ModelsConfigs[]>(
      '/api/llm/model/configs'
    );
    return response.data;
  },

  async getModel(id: string) {
    const response = await apiService.get<ModelConfig>(
      `/api/llm/model/config/${id}`
    );
    return response.data;
  },

  async createProvider(provider: CreateProviderBody) {
    const response = await apiService.post<Provider>(
      '/api/llm/model/provider',
      provider as unknown as Record<string, unknown>
    );
    return response.data;
  },

  async updateProvider(
    provider: string,
    data: { api_key: string; metadata: Record<string, string> }
  ) {
    const response = await apiService.patch<Provider>(
      `/api/llm/model/providers/${provider}`,
      data
    );
    return response.data;
  },

  async createModel(model: CreateModelBody) {
    const response = await apiService.post<ModelsConfigs[]>(
      '/api/llm/model/config',
      model as unknown as Record<string, unknown>
    );
    return response.data;
  },

  async updateModel(id: string, model: Partial<ModelConfig>) {
    const response = await apiService.patch<ModelConfig>(
      `/api/llm/model/config/${id}`,
      model
    );
    return response.data;
  },

  async deleteModel(id: string) {
    await apiService.delete(`/api/llm/model/config/${id}`);
  },
};

// Legacy functions for backward compatibility
export async function getAvailableModels(): Promise<ModelsConfigs[]> {
  return await modelService.getModels();
}

export async function getDefaultModel(): Promise<ModelConfig | null> {
  try {
    const providers = await getAvailableModels();
    console.log('Available providers:', providers);

    // Find the first provider with configs
    for (const provider of providers) {
      if (provider.configs && provider.configs.length > 0) {
        const config = provider.configs[0]; // Take the first config
        return {
          id: config.id,
          name: config.name,
          model: config.model,
          temperature: config.temperature,
          system_prompt: config.system_prompt,
          credentials: config.credentials,
          max_last_messages: config.max_last_messages,
          user_prompt: config.user_prompt,
        };
      }
    }

    console.warn('No model configurations found');
    return null;
  } catch (error) {
    console.error('Error getting default model:', error);
    return null;
  }
}
