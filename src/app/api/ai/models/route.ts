import { NextRequest, NextResponse } from "next/server";
import { getModelsForProvider, getAllProviders } from "@/lib/ai/provider-registry";
import type { ProviderId } from "@/lib/ai/provider-types";

export async function GET(request: NextRequest) {
  const providerId = request.nextUrl.searchParams.get("provider") as ProviderId | null;

  if (providerId) {
    try {
      const models = getModelsForProvider(providerId);
      return NextResponse.json({ provider: providerId, models });
    } catch {
      return NextResponse.json({ error: "Unknown provider" }, { status: 400 });
    }
  }

  const all = getAllProviders().map((p) => ({
    provider: p.id,
    models: p.models,
  }));

  return NextResponse.json({ providers: all });
}
