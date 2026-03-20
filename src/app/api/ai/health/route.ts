import { NextResponse } from "next/server";
import { getAllHealth } from "@/lib/ai/provider-health";

export async function GET() {
  const health = getAllHealth();
  return NextResponse.json({ health });
}
