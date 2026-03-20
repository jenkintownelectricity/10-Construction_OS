import Anthropic from "@anthropic-ai/sdk";
import type { AIRequest, ModelInfo } from "../provider-types";
import { normalizeResponse } from "../normalize-response";
import { normalizeError } from "../provider-errors";

export const ANTHROPIC_MODELS: ModelInfo[] = [
  { id: "claude-opus-4-6", name: "Claude Opus 4.6", capabilities: ["premium_reasoning", "detail_explainer", "assembly_summarizer"], contextWindow: 200000, supportsStreaming: true },
  { id: "claude-sonnet-4-6", name: "Claude Sonnet 4.6", capabilities: ["detail_explainer", "manufacturer_note_drafter", "related_detail_suggester", "assembly_summarizer"], contextWindow: 200000, supportsStreaming: true },
  { id: "claude-haiku-4-5-20251001", name: "Claude Haiku 4.5", capabilities: ["fast_classification", "observation_classifier", "field_note_cleaner", "artifact_summary"], contextWindow: 200000, supportsStreaming: true },
];

export function createAnthropicClient(apiKey: string): Anthropic {
  return new Anthropic({ apiKey });
}

export async function executeAnthropic(apiKey: string, request: AIRequest) {
  const startTime = Date.now();
  try {
    const client = createAnthropicClient(apiKey);
    const response = await client.messages.create({
      model: request.model,
      max_tokens: request.maxTokens ?? 2048,
      ...(request.system ? { system: request.system } : {}),
      messages: request.messages.map((m) => ({
        role: m.role === "system" ? "user" : m.role,
        content: m.content,
      })),
      temperature: request.temperature ?? 0.7,
    });

    const textBlock = response.content.find((b) => b.type === "text");
    return normalizeResponse("anthropic", request.model, {
      text: textBlock && "text" in textBlock ? textBlock.text : "",
      promptTokens: response.usage.input_tokens,
      completionTokens: response.usage.output_tokens,
      finishReason: response.stop_reason ?? undefined,
      metadata: { id: response.id },
    }, startTime);
  } catch (err) {
    throw normalizeError("anthropic", err);
  }
}

export async function testAnthropic(apiKey: string): Promise<{ ok: boolean; latencyMs: number; error?: string }> {
  const start = Date.now();
  try {
    const client = createAnthropicClient(apiKey);
    await client.messages.create({
      model: "claude-haiku-4-5-20251001",
      max_tokens: 16,
      messages: [{ role: "user", content: "ping" }],
    });
    return { ok: true, latencyMs: Date.now() - start };
  } catch (err) {
    return { ok: false, latencyMs: Date.now() - start, error: err instanceof Error ? err.message : String(err) };
  }
}
