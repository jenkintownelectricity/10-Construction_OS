import { NextResponse } from "next/server";
import { getAllProviders } from "@/lib/ai/provider-registry";
import { loadSettings, hasKey, getMaskedKey } from "@/lib/ai/settings-store";
import { getHealth } from "@/lib/ai/provider-health";
import type { ProviderId, ProviderConfig } from "@/lib/ai/provider-types";

export async function GET() {
  const settings = loadSettings();
  const registry = getAllProviders();

  const providers: ProviderConfig[] = registry.map((entry) => {
    const id = entry.id as ProviderId;
    const provSettings = settings.providers[id];
    const health = getHealth(id);

    return {
      id,
      name: entry.name,
      enabled: provSettings?.enabled ?? false,
      apiKeySet: hasKey(id),
      apiKeyMasked: getMaskedKey(id),
      defaultModel: provSettings?.defaultModel ?? entry.defaultModel,
      baseUrl: provSettings?.baseUrl,
      models: entry.models,
      healthStatus: health.status,
      lastHealthCheck: health.lastCheck,
      lastLatencyMs: health.latencyMs,
    };
  });

  return NextResponse.json({ providers });
}
