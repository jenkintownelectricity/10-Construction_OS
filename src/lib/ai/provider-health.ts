import type { HealthStatus, ProviderId, ProviderHealth } from "./provider-types";

const CIRCUIT_BREAKER_THRESHOLD = 5;
const DEGRADED_LATENCY_MS = 5000;

const healthState: Map<ProviderId, ProviderHealth> = new Map();

export function getHealth(provider: ProviderId): ProviderHealth {
  return healthState.get(provider) ?? {
    provider,
    status: "misconfigured",
    lastCheck: new Date().toISOString(),
    consecutiveFailures: 0,
    circuitOpen: false,
    reason: "No health check performed",
  };
}

export function getAllHealth(): Record<ProviderId, ProviderHealth> {
  const providers: ProviderId[] = ["openai", "anthropic", "gemini", "groq"];
  const result = {} as Record<ProviderId, ProviderHealth>;
  for (const p of providers) {
    result[p] = getHealth(p);
  }
  return result;
}

export function recordSuccess(provider: ProviderId, latencyMs: number): void {
  const status: HealthStatus = latencyMs > DEGRADED_LATENCY_MS ? "degraded" : "healthy";
  healthState.set(provider, {
    provider,
    status,
    lastCheck: new Date().toISOString(),
    latencyMs,
    consecutiveFailures: 0,
    circuitOpen: false,
    reason: status === "degraded" ? `High latency: ${latencyMs}ms` : undefined,
  });
}

export function recordFailure(provider: ProviderId, reason: string): void {
  const current = getHealth(provider);
  const failures = current.consecutiveFailures + 1;
  const circuitOpen = failures >= CIRCUIT_BREAKER_THRESHOLD;

  healthState.set(provider, {
    provider,
    status: circuitOpen ? "unavailable" : "degraded",
    lastCheck: new Date().toISOString(),
    consecutiveFailures: failures,
    circuitOpen,
    reason,
  });
}

export function markMisconfigured(provider: ProviderId, reason: string): void {
  healthState.set(provider, {
    provider,
    status: "misconfigured",
    lastCheck: new Date().toISOString(),
    consecutiveFailures: 0,
    circuitOpen: false,
    reason,
  });
}

export function isAvailable(provider: ProviderId): boolean {
  const health = getHealth(provider);
  return health.status !== "unavailable" && !health.circuitOpen;
}
