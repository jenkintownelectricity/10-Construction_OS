import fs from "node:fs";
import path from "node:path";
import type { AISettings, ProviderId, ProviderSettings } from "./provider-types";
import { DEFAULT_ROUTING_POLICY } from "./provider-routing";

const SETTINGS_PATH = path.join(process.cwd(), "ai-settings.json");
const KEYS_ENV_PREFIX = "AI_PROVIDER_KEY_";

interface PersistedSettings {
  defaultProvider: string;
  fallbackProvider: string;
  activePreset: string;
  defaultTemperature: number;
  defaultMaxTokens: number;
  timeoutMs: number;
  streamingEnabled: boolean;
  providers: Record<string, {
    enabled: boolean;
    defaultModel: string;
    baseUrl?: string;
  }>;
  keys?: Record<string, string>;
}

const DEFAULT_SETTINGS: AISettings = {
  defaultProvider: "openai",
  fallbackProvider: "anthropic",
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

// Always read from disk — no stale cache
export function loadSettings(): AISettings {
  try {
    if (fs.existsSync(SETTINGS_PATH)) {
      const raw = JSON.parse(fs.readFileSync(SETTINGS_PATH, "utf-8")) as PersistedSettings;
      return {
        defaultProvider: (raw.defaultProvider as ProviderId) ?? DEFAULT_SETTINGS.defaultProvider,
        fallbackProvider: (raw.fallbackProvider as ProviderId) ?? DEFAULT_SETTINGS.fallbackProvider,
        activePreset: (raw.activePreset as AISettings["activePreset"]) ?? DEFAULT_SETTINGS.activePreset,
        defaultTemperature: raw.defaultTemperature ?? DEFAULT_SETTINGS.defaultTemperature,
        defaultMaxTokens: raw.defaultMaxTokens ?? DEFAULT_SETTINGS.defaultMaxTokens,
        timeoutMs: raw.timeoutMs ?? DEFAULT_SETTINGS.timeoutMs,
        streamingEnabled: raw.streamingEnabled ?? DEFAULT_SETTINGS.streamingEnabled,
        providers: {
          openai: { ...DEFAULT_SETTINGS.providers.openai, ...raw.providers?.openai },
          anthropic: { ...DEFAULT_SETTINGS.providers.anthropic, ...raw.providers?.anthropic },
          gemini: { ...DEFAULT_SETTINGS.providers.gemini, ...raw.providers?.gemini },
          groq: { ...DEFAULT_SETTINGS.providers.groq, ...raw.providers?.groq },
        },
        routing: DEFAULT_ROUTING_POLICY,
      };
    }
  } catch {
    // Fall through to defaults
  }
  return { ...DEFAULT_SETTINGS, providers: { ...DEFAULT_SETTINGS.providers } };
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

  // Read existing file to preserve keys
  let existingKeys: Record<string, string> | undefined;
  try {
    if (fs.existsSync(SETTINGS_PATH)) {
      const existing = JSON.parse(fs.readFileSync(SETTINGS_PATH, "utf-8")) as PersistedSettings;
      existingKeys = existing.keys;
    }
  } catch { /* ignore */ }

  const persisted: PersistedSettings = {
    defaultProvider: merged.defaultProvider,
    fallbackProvider: merged.fallbackProvider,
    activePreset: merged.activePreset,
    defaultTemperature: merged.defaultTemperature,
    defaultMaxTokens: merged.defaultMaxTokens,
    timeoutMs: merged.timeoutMs,
    streamingEnabled: merged.streamingEnabled,
    providers: merged.providers,
    ...(existingKeys ? { keys: existingKeys } : {}),
  };

  fs.writeFileSync(SETTINGS_PATH, JSON.stringify(persisted, null, 2), "utf-8");
  return merged;
}

// ─── API Key Management (Server-Side Only) ──────────

const keyStore: Map<ProviderId, string> = new Map();
let keysLoaded = false;

function loadKeys(): void {
  if (keysLoaded) return;

  // Load from env vars first
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

  // Load from settings file keys field
  try {
    if (fs.existsSync(SETTINGS_PATH)) {
      const raw = JSON.parse(fs.readFileSync(SETTINGS_PATH, "utf-8")) as PersistedSettings;
      if (raw.keys) {
        for (const [provider, key] of Object.entries(raw.keys)) {
          if (key && !keyStore.has(provider as ProviderId)) {
            keyStore.set(provider as ProviderId, key);
          }
        }
      }
    }
  } catch {
    // ignore
  }

  keysLoaded = true;
}

export function getProviderKey(provider: ProviderId): string | undefined {
  loadKeys();
  return keyStore.get(provider);
}

export function setProviderKey(provider: ProviderId, key: string): void {
  loadKeys();
  keyStore.set(provider, key);

  // Persist to settings file under keys field
  try {
    let persisted: PersistedSettings;
    if (fs.existsSync(SETTINGS_PATH)) {
      persisted = JSON.parse(fs.readFileSync(SETTINGS_PATH, "utf-8"));
    } else {
      persisted = {
        defaultProvider: DEFAULT_SETTINGS.defaultProvider,
        fallbackProvider: DEFAULT_SETTINGS.fallbackProvider,
        activePreset: DEFAULT_SETTINGS.activePreset,
        defaultTemperature: DEFAULT_SETTINGS.defaultTemperature,
        defaultMaxTokens: DEFAULT_SETTINGS.defaultMaxTokens,
        timeoutMs: DEFAULT_SETTINGS.timeoutMs,
        streamingEnabled: DEFAULT_SETTINGS.streamingEnabled,
        providers: DEFAULT_SETTINGS.providers,
      };
    }
    persisted.keys = persisted.keys ?? {};
    persisted.keys[provider] = key;
    fs.writeFileSync(SETTINGS_PATH, JSON.stringify(persisted, null, 2), "utf-8");
  } catch {
    // Key is in memory at minimum
  }
}

export function clearProviderKey(provider: ProviderId): void {
  loadKeys();
  keyStore.delete(provider);

  try {
    if (fs.existsSync(SETTINGS_PATH)) {
      const persisted = JSON.parse(fs.readFileSync(SETTINGS_PATH, "utf-8")) as PersistedSettings;
      if (persisted.keys) {
        delete persisted.keys[provider];
        fs.writeFileSync(SETTINGS_PATH, JSON.stringify(persisted, null, 2), "utf-8");
      }
    }
  } catch {
    // ignore
  }
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
