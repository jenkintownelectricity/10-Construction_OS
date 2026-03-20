import { NextRequest, NextResponse } from "next/server";
import {
  loadSettings,
  saveSettings,
  setProviderKey,
  clearProviderKey,
  hasKey,
  getMaskedKey,
} from "@/lib/ai/settings-store";
import type { ProviderId } from "@/lib/ai/provider-types";

const VALID_PROVIDERS = new Set(["openai", "anthropic", "gemini", "groq"]);

export const dynamic = "force-dynamic";

export async function GET() {
  const settings = loadSettings();

  // Build safe response — never include raw keys
  const providers: Record<string, unknown> = {};
  for (const [id, config] of Object.entries(settings.providers)) {
    providers[id] = {
      ...config,
      apiKeySet: hasKey(id as ProviderId),
      apiKeyMasked: getMaskedKey(id as ProviderId),
    };
  }

  return NextResponse.json({
    defaultProvider: settings.defaultProvider,
    fallbackProvider: settings.fallbackProvider,
    activePreset: settings.activePreset,
    defaultTemperature: settings.defaultTemperature,
    defaultMaxTokens: settings.defaultMaxTokens,
    timeoutMs: settings.timeoutMs,
    streamingEnabled: settings.streamingEnabled,
    providers,
    routing: settings.routing,
  });
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();

    // Handle key operations separately
    if (body.setKey) {
      const { provider, key } = body.setKey;
      if (!VALID_PROVIDERS.has(provider)) {
        return NextResponse.json({ error: "Invalid provider" }, { status: 400 });
      }
      if (!key || typeof key !== "string" || key.trim().length === 0) {
        return NextResponse.json({ error: "Invalid key" }, { status: 400 });
      }
      setProviderKey(provider as ProviderId, key.trim());
      return NextResponse.json({ ok: true, provider, masked: getMaskedKey(provider as ProviderId) });
    }

    if (body.clearKey) {
      const { provider } = body.clearKey;
      if (!VALID_PROVIDERS.has(provider)) {
        return NextResponse.json({ error: "Invalid provider" }, { status: 400 });
      }
      clearProviderKey(provider as ProviderId);
      return NextResponse.json({ ok: true, provider, cleared: true });
    }

    // Handle general settings update — build partial update object
    const updates: Record<string, unknown> = {};
    if (body.defaultProvider && VALID_PROVIDERS.has(body.defaultProvider)) updates.defaultProvider = body.defaultProvider;
    if (body.fallbackProvider && VALID_PROVIDERS.has(body.fallbackProvider)) updates.fallbackProvider = body.fallbackProvider;
    if (body.activePreset) updates.activePreset = body.activePreset;
    if (typeof body.defaultTemperature === "number") updates.defaultTemperature = Math.max(0, Math.min(2, body.defaultTemperature));
    if (typeof body.defaultMaxTokens === "number") updates.defaultMaxTokens = Math.max(1, Math.min(128000, body.defaultMaxTokens));
    if (typeof body.timeoutMs === "number") updates.timeoutMs = Math.max(5000, Math.min(120000, body.timeoutMs));
    if (typeof body.streamingEnabled === "boolean") updates.streamingEnabled = body.streamingEnabled;

    // Provider-specific settings: pass through partial fields directly
    if (body.providers && typeof body.providers === "object") {
      const providerUpdates: Record<string, Record<string, unknown>> = {};
      for (const [id, config] of Object.entries(body.providers)) {
        if (VALID_PROVIDERS.has(id) && typeof config === "object" && config) {
          const c = config as Record<string, unknown>;
          const partial: Record<string, unknown> = {};
          if (typeof c.enabled === "boolean") partial.enabled = c.enabled;
          if (typeof c.defaultModel === "string") partial.defaultModel = c.defaultModel;
          if (c.baseUrl !== undefined) partial.baseUrl = typeof c.baseUrl === "string" ? c.baseUrl : undefined;
          if (Object.keys(partial).length > 0) {
            providerUpdates[id] = partial;
          }
        }
      }
      if (Object.keys(providerUpdates).length > 0) {
        updates.providers = providerUpdates;
      }
    }

    const saved = saveSettings(updates);
    return NextResponse.json({ ok: true, settings: saved });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Failed to save settings" },
      { status: 500 }
    );
  }
}
