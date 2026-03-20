import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["openai", "@anthropic-ai/sdk", "@google/generative-ai", "groq-sdk"],
};

export default nextConfig;
