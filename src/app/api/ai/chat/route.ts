import { NextRequest, NextResponse } from "next/server";
import { executeAIRequest } from "@/lib/ai/provider-service";
import { ProviderError } from "@/lib/ai/provider-errors";
import type { AIRequest, ProviderId, CapabilityClass } from "@/lib/ai/provider-types";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    if (!body.messages || !Array.isArray(body.messages) || body.messages.length === 0) {
      return NextResponse.json({ error: "messages array is required" }, { status: 400 });
    }

    const aiRequest: AIRequest = {
      provider: body.provider as ProviderId,
      model: body.model ?? "",
      capability: body.capability as CapabilityClass | undefined,
      system: body.system,
      messages: body.messages,
      temperature: body.temperature,
      maxTokens: body.maxTokens,
      timeoutMs: body.timeoutMs,
    };

    const response = await executeAIRequest(aiRequest);

    return NextResponse.json(response);
  } catch (err) {
    if (err instanceof ProviderError) {
      return NextResponse.json(
        { error: err.toJSON() },
        { status: err.statusCode ?? 500 }
      );
    }
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Internal error" },
      { status: 500 }
    );
  }
}
