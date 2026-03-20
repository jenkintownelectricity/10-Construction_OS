import OpenAI from "openai";
import type { AIRequest, ModelInfo } from "../provider-types";
import { normalizeResponse } from "../normalize-response";
import { normalizeError } from "../provider-errors";

export const OPENAI_MODELS: ModelInfo[] = [
  { id: "gpt-4o", name: "GPT-4o", capabilities: ["detail_explainer", "premium_reasoning", "assembly_summarizer", "manufacturer_note_drafter"], contextWindow: 128000, supportsStreaming: true },
  { id: "gpt-4o-mini", name: "GPT-4o Mini", capabilities: ["fast_classification", "observation_classifier", "field_note_cleaner", "artifact_summary"], contextWindow: 128000, supportsStreaming: true },
  { id: "gpt-4-turbo", name: "GPT-4 Turbo", capabilities: ["detail_explainer", "related_detail_suggester", "assembly_summarizer"], contextWindow: 128000, supportsStreaming: true },
  { id: "o1", name: "o1", capabilities: ["premium_reasoning"], contextWindow: 200000, supportsStreaming: false },
];

export function createOpenAIClient(apiKey: string, baseUrl?: string): OpenAI {
  return new OpenAI({ apiKey, baseURL: baseUrl });
}

export async function executeOpenAI(apiKey: string, request: AIRequest, baseUrl?: string) {
  const startTime = Date.now();
  try {
    const client = createOpenAIClient(apiKey, baseUrl);
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
    return normalizeResponse("openai", request.model, {
      text: choice?.message?.content ?? "",
      promptTokens: response.usage?.prompt_tokens,
      completionTokens: response.usage?.completion_tokens,
      totalTokens: response.usage?.total_tokens,
      finishReason: choice?.finish_reason ?? undefined,
      metadata: { id: response.id },
    }, startTime);
  } catch (err) {
    throw normalizeError("openai", err);
  }
}

export async function testOpenAI(apiKey: string, baseUrl?: string): Promise<{ ok: boolean; latencyMs: number; error?: string }> {
  const start = Date.now();
  try {
    const client = createOpenAIClient(apiKey, baseUrl);
    await client.models.list();
    return { ok: true, latencyMs: Date.now() - start };
  } catch (err) {
    return { ok: false, latencyMs: Date.now() - start, error: err instanceof Error ? err.message : String(err) };
  }
}
