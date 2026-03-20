import { NextRequest, NextResponse } from "next/server";
import { testProvider } from "@/lib/ai/provider-service";
import { recordSuccess, recordFailure } from "@/lib/ai/provider-health";
import type { ProviderId } from "@/lib/ai/provider-types";

const VALID_PROVIDERS = new Set(["openai", "anthropic", "gemini", "groq"]);

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const provider = body.provider as ProviderId;

    if (!provider || !VALID_PROVIDERS.has(provider)) {
      return NextResponse.json({ error: "Invalid provider" }, { status: 400 });
    }

    const result = await testProvider(provider);

    if (result.ok) {
      recordSuccess(provider, result.latencyMs);
    } else {
      recordFailure(provider, result.error ?? "Test failed");
    }

    // Never echo secrets back
    return NextResponse.json({
      provider,
      ok: result.ok,
      latencyMs: result.latencyMs,
      error: result.error,
    });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Test failed" },
      { status: 500 }
    );
  }
}
