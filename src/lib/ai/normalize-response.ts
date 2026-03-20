import type { AIResponse, FinishReason, ProviderId } from "./provider-types";

interface RawProviderResponse {
  text: string;
  promptTokens?: number;
  completionTokens?: number;
  totalTokens?: number;
  finishReason?: string;
  metadata?: Record<string, unknown>;
}

export function normalizeResponse(
  provider: ProviderId,
  model: string,
  raw: RawProviderResponse,
  startTime: number
): AIResponse {
  const latencyMs = Date.now() - startTime;
  const promptTokens = raw.promptTokens ?? 0;
  const completionTokens = raw.completionTokens ?? 0;

  return {
    provider,
    model,
    text: raw.text,
    usage: {
      promptTokens,
      completionTokens,
      totalTokens: raw.totalTokens ?? promptTokens + completionTokens,
    },
    latencyMs,
    finishReason: mapFinishReason(raw.finishReason),
    metadata: raw.metadata ?? {},
  };
}

function mapFinishReason(reason?: string): FinishReason {
  if (!reason) return "unknown";
  const r = reason.toLowerCase();
  if (r === "stop" || r === "end_turn") return "stop";
  if (r === "length" || r === "max_tokens") return "length";
  if (r === "content_filter" || r === "safety") return "content_filter";
  return "unknown";
}
