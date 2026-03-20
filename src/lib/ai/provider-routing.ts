import type { CapabilityClass, CapabilityRouting, ProviderId, ProviderPreset, RoutingPolicy, RoutingPresetConfig } from "./provider-types";
import { isAvailable } from "./provider-health";

export const DEFAULT_ROUTING_POLICY: RoutingPolicy = {
  presets: {
    fast: {
      preferredProviders: ["groq", "gemini", "openai"],
      description: "Fastest inference speed, lower cost",
    },
    low_cost: {
      preferredProviders: ["groq", "gemini", "openai"],
      description: "Lowest cost per token",
    },
    balanced: {
      preferredProviders: ["openai", "anthropic", "gemini"],
      description: "Balance of quality, speed, and cost",
    },
    premium_reasoning: {
      preferredProviders: ["anthropic", "openai", "gemini"],
      description: "Highest quality reasoning and analysis",
    },
    multimodal_ready: {
      preferredProviders: ["gemini", "openai", "anthropic"],
      description: "Multimodal input support scaffold",
    },
  } satisfies Record<ProviderPreset, RoutingPresetConfig>,

  capabilityMap: {
    detail_explainer: { preferredProvider: "anthropic", fallbacks: ["openai", "gemini"], preset: "balanced" },
    observation_classifier: { preferredProvider: "groq", fallbacks: ["openai", "gemini"], preset: "fast" },
    related_detail_suggester: { preferredProvider: "openai", fallbacks: ["anthropic", "gemini"], preset: "balanced" },
    manufacturer_note_drafter: { preferredProvider: "anthropic", fallbacks: ["openai", "gemini"], preset: "balanced" },
    assembly_summarizer: { preferredProvider: "openai", fallbacks: ["anthropic", "gemini"], preset: "balanced" },
    field_note_cleaner: { preferredProvider: "groq", fallbacks: ["openai", "gemini"], preset: "fast" },
    artifact_summary: { preferredProvider: "openai", fallbacks: ["anthropic", "groq"], preset: "low_cost" },
    premium_reasoning: { preferredProvider: "anthropic", fallbacks: ["openai", "gemini"], preset: "premium_reasoning" },
    fast_classification: { preferredProvider: "groq", fallbacks: ["gemini", "openai"], preset: "fast" },
  } satisfies Record<CapabilityClass, CapabilityRouting>,

  fallbackChain: ["openai", "anthropic", "gemini", "groq"],
};

export interface RoutingDecision {
  provider: ProviderId;
  reason: string;
  isFallback: boolean;
  originalProvider?: ProviderId;
}

export function resolveProvider(
  capability: CapabilityClass | undefined,
  preset: ProviderPreset | undefined,
  explicitProvider: ProviderId | undefined,
  enabledProviders: Set<ProviderId>,
  policy: RoutingPolicy = DEFAULT_ROUTING_POLICY
): RoutingDecision {
  // Explicit provider takes priority
  if (explicitProvider && enabledProviders.has(explicitProvider) && isAvailable(explicitProvider)) {
    return { provider: explicitProvider, reason: "Explicit provider selection", isFallback: false };
  }

  // Capability-based routing
  if (capability && policy.capabilityMap[capability]) {
    const cap = policy.capabilityMap[capability];
    if (enabledProviders.has(cap.preferredProvider) && isAvailable(cap.preferredProvider)) {
      return { provider: cap.preferredProvider, reason: `Preferred for capability: ${capability}`, isFallback: false };
    }
    for (const fb of cap.fallbacks) {
      if (enabledProviders.has(fb) && isAvailable(fb)) {
        return {
          provider: fb,
          reason: `Fallback for capability: ${capability} (preferred ${cap.preferredProvider} unavailable)`,
          isFallback: true,
          originalProvider: cap.preferredProvider,
        };
      }
    }
  }

  // Preset-based routing
  if (preset && policy.presets[preset]) {
    for (const p of policy.presets[preset].preferredProviders) {
      if (enabledProviders.has(p) && isAvailable(p)) {
        return { provider: p, reason: `Preset: ${preset}`, isFallback: false };
      }
    }
  }

  // Fallback chain
  for (const p of policy.fallbackChain) {
    if (enabledProviders.has(p) && isAvailable(p)) {
      return { provider: p, reason: "Fallback chain", isFallback: true };
    }
  }

  // Last resort: return first enabled
  const first = Array.from(enabledProviders)[0];
  if (first) {
    return { provider: first, reason: "Last resort — no available preferred providers", isFallback: true };
  }

  throw new Error("No AI providers are enabled or available");
}
