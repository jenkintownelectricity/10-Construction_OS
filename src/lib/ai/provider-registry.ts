import type { ModelInfo, ProviderId } from "./provider-types";
import { OPENAI_MODELS } from "./providers/openai";
import { ANTHROPIC_MODELS } from "./providers/anthropic";
import { GEMINI_MODELS } from "./providers/gemini";
import { GROQ_MODELS } from "./providers/groq";

export interface ProviderRegistryEntry {
  id: ProviderId;
  name: string;
  description: string;
  defaultModel: string;
  models: ModelInfo[];
  supportsBaseUrl: boolean;
  icon: string;
}

export const PROVIDER_REGISTRY: Record<ProviderId, ProviderRegistryEntry> = {
  openai: {
    id: "openai",
    name: "OpenAI",
    description: "GPT-4o, GPT-4 Turbo, and o1 reasoning models",
    defaultModel: "gpt-4o-mini",
    models: OPENAI_MODELS,
    supportsBaseUrl: true,
    icon: "OpenAI",
  },
  anthropic: {
    id: "anthropic",
    name: "Anthropic",
    description: "Claude Opus, Sonnet, and Haiku models",
    defaultModel: "claude-sonnet-4-6",
    models: ANTHROPIC_MODELS,
    supportsBaseUrl: false,
    icon: "Anthropic",
  },
  gemini: {
    id: "gemini",
    name: "Google Gemini",
    description: "Gemini 2.5 Pro, Flash, and multimodal models",
    defaultModel: "gemini-2.5-flash",
    models: GEMINI_MODELS,
    supportsBaseUrl: false,
    icon: "Gemini",
  },
  groq: {
    id: "groq",
    name: "Groq",
    description: "Ultra-fast inference with Llama and Mixtral models",
    defaultModel: "llama-3.3-70b-versatile",
    models: GROQ_MODELS,
    supportsBaseUrl: false,
    icon: "Groq",
  },
};

export function getProvider(id: ProviderId): ProviderRegistryEntry {
  return PROVIDER_REGISTRY[id];
}

export function getAllProviders(): ProviderRegistryEntry[] {
  return Object.values(PROVIDER_REGISTRY);
}

export function getModelsForProvider(id: ProviderId): ModelInfo[] {
  return PROVIDER_REGISTRY[id].models;
}
