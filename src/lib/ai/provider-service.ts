import type { AIRequest, AIResponse, AISettings, ProviderId } from "./provider-types";
import { executeOpenAI, testOpenAI } from "./providers/openai";
import { executeAnthropic, testAnthropic } from "./providers/anthropic";
import { executeGemini, testGemini } from "./providers/gemini";
import { executeGroq, testGroq } from "./providers/groq";
import { recordSuccess, recordFailure, markMisconfigured } from "./provider-health";
import { resolveProvider } from "./provider-routing";
import { logAudit, logRoutingDecision } from "./provider-audit";
import { normalizeError, ProviderError } from "./provider-errors";
import { loadSettings, getProviderKey } from "./settings-store";

const CONCURRENCY_LIMIT = 5;
let activeCalls = 0;

export async function executeAIRequest(request: AIRequest): Promise<AIResponse> {
  const settings = loadSettings();

  // Resolve the actual provider to use
  const enabledProviders = new Set<ProviderId>(
    (Object.entries(settings.providers) as [ProviderId, { enabled: boolean }][])
      .filter(([, v]) => v.enabled)
      .map(([k]) => k)
  );

  const decision = resolveProvider(
    request.capability,
    settings.activePreset,
    request.provider,
    enabledProviders,
    settings.routing
  );
  logRoutingDecision(decision, request.capability, settings.activePreset);

  const provider = decision.provider;
  const apiKey = getProviderKey(provider);
  if (!apiKey) {
    markMisconfigured(provider, "API key not configured");
    throw new ProviderError({
      provider,
      errorType: "config_error",
      message: `API key not configured for ${provider}`,
      retryable: false,
    });
  }

  // Concurrency guard
  if (activeCalls >= CONCURRENCY_LIMIT) {
    throw new ProviderError({
      provider,
      errorType: "unavailable_error",
      message: "Concurrency limit reached",
      retryable: true,
    });
  }

  activeCalls++;
  const resolvedRequest = { ...request, provider, model: request.model || settings.providers[provider].defaultModel };

  // Timeout wrapper
  const timeoutMs = request.timeoutMs ?? settings.timeoutMs;

  try {
    const result = await Promise.race([
      executeForProvider(provider, apiKey, resolvedRequest, settings),
      new Promise<never>((_, reject) =>
        setTimeout(() => reject(new Error("Request timed out")), timeoutMs)
      ),
    ]);

    recordSuccess(provider, result.latencyMs);
    logAudit({ action: "response", provider, detail: `${result.model} — ${result.latencyMs}ms` });
    return result;
  } catch (err) {
    const normalized = err instanceof ProviderError ? err : normalizeError(provider, err);
    recordFailure(provider, normalized.message);
    logAudit({ action: "error", provider, detail: normalized.message, metadata: { errorType: normalized.errorType } });
    throw normalized;
  } finally {
    activeCalls--;
  }
}

async function executeForProvider(
  provider: ProviderId,
  apiKey: string,
  request: AIRequest,
  settings: AISettings
): Promise<AIResponse> {
  const baseUrl = settings.providers[provider]?.baseUrl;

  switch (provider) {
    case "openai":
      return executeOpenAI(apiKey, request, baseUrl);
    case "anthropic":
      return executeAnthropic(apiKey, request);
    case "gemini":
      return executeGemini(apiKey, request);
    case "groq":
      return executeGroq(apiKey, request);
    default:
      throw new ProviderError({
        provider,
        errorType: "config_error",
        message: `Unknown provider: ${provider}`,
        retryable: false,
      });
  }
}

export async function testProvider(provider: ProviderId): Promise<{ ok: boolean; latencyMs: number; error?: string }> {
  const apiKey = getProviderKey(provider);
  if (!apiKey) {
    return { ok: false, latencyMs: 0, error: "API key not configured" };
  }

  const settings = loadSettings();
  const baseUrl = settings.providers[provider]?.baseUrl;

  switch (provider) {
    case "openai":
      return testOpenAI(apiKey, baseUrl);
    case "anthropic":
      return testAnthropic(apiKey);
    case "gemini":
      return testGemini(apiKey);
    case "groq":
      return testGroq(apiKey);
    default:
      return { ok: false, latencyMs: 0, error: `Unknown provider: ${provider}` };
  }
}
