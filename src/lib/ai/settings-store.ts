import type { AISettings, ProviderId, ProviderSettings } from "./provider-types";
import { DEFAULT_ROUTING_POLICY } from "./provider-routing";

const KEYS_ENV_PREFIX = "AI_PROVIDER_KEY_";

// In-memory settings store (replaces filesystem for Vercel compatibility)
let inMemorySettings: AISettings | null = null;

const DEFAULT_SETTINGS: AISettings = {
  defaultProvider: "anthropic",
  fallbackProvider: "groq",
  activePreset: "balanced",
  defaultTemperature: 0.7,
  defaultMaxTokens: 2048,
  timeoutMs: 30000,
  streamingEnabled: false,
  providers: {
    openai: { enabled: false, defaultModel: "gpt-4o-mini" },
    anthropic: { enabled: false, defaultModel: "claude-sonnet-4-6" },
    gemini: { enabled: false, defaultModel: "gemini-2.5-flash" },
    groq: { enabled: false, defaultModel: "llama-3.3-70b-versatile" },
  },
  routing: DEFAULT_ROUTING_POLICY,
};

// Auto-enable providers that have env keys configured
function autoEnableFromEnv(settings: AISettings): AISettings {
  const providers: ProviderId[] = ["openai", "anthropic", "gemini", "groq"];
  for (const p of providers) {
    if (hasKey(p) && !settings.providers[p].enabled) {
      settings.providers[p] = { ...settings.providers[p], enabled: true };
    }
  }
  return settings;
}

export function loadSettings(): AISettings {
  if (inMemorySettings) {
    return autoEnableFromEnv({ ...inMemorySettings, routing: DEFAULT_ROUTING_POLICY });
  }
  const settings = { ...DEFAULT_SETTINGS, providers: { ...DEFAULT_SETTINGS.providers } };
  return autoEnableFromEnv(settings);
}

export function saveSettings(updates: Partial<Omit<AISettings, "routing">>): AISettings {
  const current = loadSettings();

  // Deep-merge providers: preserve existing fields, only override what's provided
  let mergedProviders = current.providers;
  if (updates.providers) {
    mergedProviders = { ...current.providers };
    for (const [id, partial] of Object.entries(updates.providers)) {
      const pid = id as ProviderId;
      if (mergedProviders[pid] && partial) {
        mergedProviders[pid] = { ...mergedProviders[pid] };
        if (typeof partial.enabled === "boolean") mergedProviders[pid].enabled = partial.enabled;
        if (typeof partial.defaultModel === "string") mergedProviders[pid].defaultModel = partial.defaultModel;
        if (partial.baseUrl !== undefined) mergedProviders[pid].baseUrl = partial.baseUrl || undefined;
      }
    }
  }

  const merged: AISettings = {
    defaultProvider: updates.defaultProvider ?? current.defaultProvider,
    fallbackProvider: updates.fallbackProvider ?? current.fallbackProvider,
    activePreset: updates.activePreset ?? current.activePreset,
    defaultTemperature: updates.defaultTemperature ?? current.defaultTemperature,
    defaultMaxTokens: updates.defaultMaxTokens ?? current.defaultMaxTokens,
    timeoutMs: updates.timeoutMs ?? current.timeoutMs,
    streamingEnabled: updates.streamingEnabled ?? current.streamingEnabled,
    providers: mergedProviders,
    routing: current.routing,
  };

  inMemorySettings = merged;
  return merged;
}

// ─── API Key Management (Server-Side Only) ──────────

const keyStore: Map<ProviderId, string> = new Map();
let keysLoaded = false;

function loadKeys(): void {
  if (keysLoaded) return;

  // Load from env vars
  const providers: ProviderId[] = ["openai", "anthropic", "gemini", "groq"];
  for (const p of providers) {
    const envKey = process.env[`${KEYS_ENV_PREFIX}${p.toUpperCase()}`];
    if (envKey) keyStore.set(p, envKey);
  }

  // Also check common env var names
  if (process.env.OPENAI_API_KEY) keyStore.set("openai", process.env.OPENAI_API_KEY);
  if (process.env.ANTHROPIC_API_KEY) keyStore.set("anthropic", process.env.ANTHROPIC_API_KEY);
  if (process.env.GOOGLE_API_KEY) keyStore.set("gemini", process.env.GOOGLE_API_KEY);
  if (process.env.GROQ_API_KEY) keyStore.set("groq", process.env.GROQ_API_KEY);

  keysLoaded = true;
}

export function getProviderKey(provider: ProviderId): string | undefined {
  loadKeys();
  return keyStore.get(provider);
}

export function setProviderKey(provider: ProviderId, key: string): void {
  loadKeys();
  keyStore.set(provider, key);
}

export function clearProviderKey(provider: ProviderId): void {
  loadKeys();
  keyStore.delete(provider);
}

export function getMaskedKey(provider: ProviderId): string {
  const key = getProviderKey(provider);
  if (!key) return "";
  if (key.length <= 8) return "••••••••";
  return key.slice(0, 4) + "••••••••" + key.slice(-4);
}

export function hasKey(provider: ProviderId): boolean {
  return !!getProviderKey(provider);
}
