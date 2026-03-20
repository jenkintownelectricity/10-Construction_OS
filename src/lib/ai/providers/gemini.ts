import { GoogleGenerativeAI } from "@google/generative-ai";
import type { AIRequest, ModelInfo } from "../provider-types";
import { normalizeResponse } from "../normalize-response";
import { normalizeError } from "../provider-errors";

export const GEMINI_MODELS: ModelInfo[] = [
  { id: "gemini-2.0-flash", name: "Gemini 2.0 Flash", capabilities: ["fast_classification", "observation_classifier", "field_note_cleaner"], contextWindow: 1048576, supportsStreaming: true },
  { id: "gemini-2.5-pro", name: "Gemini 2.5 Pro", capabilities: ["premium_reasoning", "detail_explainer", "assembly_summarizer", "manufacturer_note_drafter"], contextWindow: 1048576, supportsStreaming: true },
  { id: "gemini-2.5-flash", name: "Gemini 2.5 Flash", capabilities: ["fast_classification", "artifact_summary", "related_detail_suggester"], contextWindow: 1048576, supportsStreaming: true },
];

export async function executeGemini(apiKey: string, request: AIRequest) {
  const startTime = Date.now();
  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: request.model,
      generationConfig: {
        temperature: request.temperature ?? 0.7,
        maxOutputTokens: request.maxTokens ?? 2048,
      },
      ...(request.system ? { systemInstruction: request.system } : {}),
    });

    const contents = request.messages.map((m) => ({
      role: m.role === "assistant" ? "model" : "user",
      parts: [{ text: m.content }],
    }));

    const result = await model.generateContent({ contents });
    const response = result.response;
    const text = response.text();
    const usage = response.usageMetadata;

    return normalizeResponse("gemini", request.model, {
      text,
      promptTokens: usage?.promptTokenCount,
      completionTokens: usage?.candidatesTokenCount,
      totalTokens: usage?.totalTokenCount,
      finishReason: response.candidates?.[0]?.finishReason ?? undefined,
    }, startTime);
  } catch (err) {
    throw normalizeError("gemini", err);
  }
}

export async function testGemini(apiKey: string): Promise<{ ok: boolean; latencyMs: number; error?: string }> {
  const start = Date.now();
  try {
    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({ model: "gemini-2.0-flash" });
    await model.generateContent("ping");
    return { ok: true, latencyMs: Date.now() - start };
  } catch (err) {
    return { ok: false, latencyMs: Date.now() - start, error: err instanceof Error ? err.message : String(err) };
  }
}
