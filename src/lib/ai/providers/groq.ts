import Groq from "groq-sdk";
import type { AIRequest, ModelInfo } from "../provider-types";
import { normalizeResponse } from "../normalize-response";
import { normalizeError } from "../provider-errors";

export const GROQ_MODELS: ModelInfo[] = [
  { id: "llama-3.3-70b-versatile", name: "Llama 3.3 70B", capabilities: ["fast_classification", "observation_classifier", "field_note_cleaner", "artifact_summary"], contextWindow: 131072, supportsStreaming: true },
  { id: "llama-3.1-8b-instant", name: "Llama 3.1 8B", capabilities: ["fast_classification", "field_note_cleaner"], contextWindow: 131072, supportsStreaming: true },
  { id: "mixtral-8x7b-32768", name: "Mixtral 8x7B", capabilities: ["fast_classification", "observation_classifier", "related_detail_suggester"], contextWindow: 32768, supportsStreaming: true },
];

export function createGroqClient(apiKey: string): Groq {
  return new Groq({ apiKey });
}

export async function executeGroq(apiKey: string, request: AIRequest) {
  const startTime = Date.now();
  try {
    const client = createGroqClient(apiKey);
    const response = await client.chat.completions.create({
      model: request.model,
      messages: [
        ...(request.system ? [{ role: "system" as const, content: request.system }] : []),
        ...request.messages.map((m) => ({ role: m.role, content: m.content })),
      ],
      temperature: request.temperature ?? 0.7,
      max_tokens: request.maxTokens ?? 2048,
    });

    const choice = response.choices[0];
    return normalizeResponse("groq", request.model, {
      text: choice?.message?.content ?? "",
      promptTokens: response.usage?.prompt_tokens,
      completionTokens: response.usage?.completion_tokens,
      totalTokens: response.usage?.total_tokens,
      finishReason: choice?.finish_reason ?? undefined,
      metadata: { id: response.id },
    }, startTime);
  } catch (err) {
    throw normalizeError("groq", err);
  }
}

export async function testGroq(apiKey: string): Promise<{ ok: boolean; latencyMs: number; error?: string }> {
  const start = Date.now();
  try {
    const client = createGroqClient(apiKey);
    await client.chat.completions.create({
      model: "llama-3.1-8b-instant",
      max_tokens: 16,
      messages: [{ role: "user", content: "ping" }],
    });
    return { ok: true, latencyMs: Date.now() - start };
  } catch (err) {
    return { ok: false, latencyMs: Date.now() - start, error: err instanceof Error ? err.message : String(err) };
  }
}
