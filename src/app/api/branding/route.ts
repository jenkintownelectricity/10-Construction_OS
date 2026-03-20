import { NextRequest, NextResponse } from "next/server";
import { loadBranding, saveBranding } from "@/lib/branding/branding-store";

export async function GET() {
  const branding = loadBranding();
  return NextResponse.json({ branding });
}

export async function PUT(request: NextRequest) {
  try {
    const body = await request.json();
    const updated = saveBranding(body);
    return NextResponse.json({ branding: updated });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Failed to save branding" },
      { status: 500 }
    );
  }
}
