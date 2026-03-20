"use client";

import { useState, useEffect, useCallback } from "react";
import { ProviderCard } from "@/components/ai/ProviderCard";
import { GlobalAISettings } from "@/components/ai/GlobalAISettings";
import type { ProviderConfig } from "@/lib/ai/provider-types";

const PROVIDER_REGISTRY_CLIENT = [
  {
    id: "openai" as const,
    name: "OpenAI",
    description: "GPT-4o, GPT-4 Turbo, and o1 reasoning models",
    defaultModel: "gpt-4o-mini",
    supportsBaseUrl: true,
    icon: "OpenAI",
    models: [
      { id: "gpt-4o", name: "GPT-4o", capabilities: [], contextWindow: 128000, supportsStreaming: true },
      { id: "gpt-4o-mini", name: "GPT-4o Mini", capabilities: [], contextWindow: 128000, supportsStreaming: true },
      { id: "gpt-4-turbo", name: "GPT-4 Turbo", capabilities: [], contextWindow: 128000, supportsStreaming: true },
      { id: "o1", name: "o1", capabilities: [], contextWindow: 200000, supportsStreaming: false },
    ],
  },
  {
    id: "anthropic" as const,
    name: "Anthropic",
    description: "Claude Opus, Sonnet, and Haiku models",
    defaultModel: "claude-sonnet-4-6",
    supportsBaseUrl: false,
    icon: "Anthropic",
    models: [
      { id: "claude-opus-4-6", name: "Claude Opus 4.6", capabilities: [], contextWindow: 200000, supportsStreaming: true },
      { id: "claude-sonnet-4-6", name: "Claude Sonnet 4.6", capabilities: [], contextWindow: 200000, supportsStreaming: true },
      { id: "claude-haiku-4-5-20251001", name: "Claude Haiku 4.5", capabilities: [], contextWindow: 200000, supportsStreaming: true },
    ],
  },
  {
    id: "gemini" as const,
    name: "Google Gemini",
    description: "Gemini 2.5 Pro, Flash, and multimodal models",
    defaultModel: "gemini-2.5-flash",
    supportsBaseUrl: false,
    icon: "Gemini",
    models: [
      { id: "gemini-2.0-flash", name: "Gemini 2.0 Flash", capabilities: [], contextWindow: 1048576, supportsStreaming: true },
      { id: "gemini-2.5-pro", name: "Gemini 2.5 Pro", capabilities: [], contextWindow: 1048576, supportsStreaming: true },
      { id: "gemini-2.5-flash", name: "Gemini 2.5 Flash", capabilities: [], contextWindow: 1048576, supportsStreaming: true },
    ],
  },
  {
    id: "groq" as const,
    name: "Groq",
    description: "Ultra-fast inference with Llama and Mixtral models",
    defaultModel: "llama-3.3-70b-versatile",
    supportsBaseUrl: false,
    icon: "Groq",
    models: [
      { id: "llama-3.3-70b-versatile", name: "Llama 3.3 70B", capabilities: [], contextWindow: 131072, supportsStreaming: true },
      { id: "llama-3.1-8b-instant", name: "Llama 3.1 8B", capabilities: [], contextWindow: 131072, supportsStreaming: true },
      { id: "mixtral-8x7b-32768", name: "Mixtral 8x7B", capabilities: [], contextWindow: 32768, supportsStreaming: true },
    ],
  },
];

export default function AISettingsPage() {
  const [providers, setProviders] = useState<ProviderConfig[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchProviders = useCallback(async () => {
    try {
      const res = await fetch("/api/ai/providers");
      const data = await res.json();
      if (data.providers) setProviders(data.providers);
    } catch {
      // silent
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    fetchProviders();
  }, [fetchProviders]);

  return (
    <div className="max-w-5xl mx-auto py-8 px-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>
          AI Control Plane
        </h1>
        <p className="text-sm text-brand-text-muted mt-1">
          Configure AI providers, models, and routing policies for Construction Atlas intelligence surfaces.
        </p>
      </div>

      {/* Global Settings */}
      <div className="mb-8">
        <GlobalAISettings onUpdate={fetchProviders} />
      </div>

      {/* Provider Cards */}
      <div className="mb-4">
        <h2 className="text-lg font-semibold">Providers</h2>
        <p className="text-xs text-brand-text-muted">
          Configure each AI provider independently. Keys are stored server-side only.
        </p>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="card animate-pulse h-72" />
          ))}
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {PROVIDER_REGISTRY_CLIENT.map((reg) => {
            const providerData = providers.find((p) => p.id === reg.id) ?? {
              id: reg.id,
              name: reg.name,
              enabled: false,
              apiKeySet: false,
              apiKeyMasked: "",
              defaultModel: reg.defaultModel,
              models: reg.models,
              healthStatus: "misconfigured" as const,
            };
            return (
              <ProviderCard
                key={reg.id}
                provider={providerData}
                registry={reg}
                onUpdate={fetchProviders}
              />
            );
          })}
        </div>
      )}

      {/* Routing Policy Info */}
      <div className="mt-8 card">
        <h2 className="text-lg font-semibold mb-3">Capability Routing Map</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                <th className="text-left py-2 pr-4 font-medium">Capability</th>
                <th className="text-left py-2 pr-4 font-medium">Preferred</th>
                <th className="text-left py-2 pr-4 font-medium">Fallbacks</th>
                <th className="text-left py-2 font-medium">Preset</th>
              </tr>
            </thead>
            <tbody className="text-brand-text-muted">
              {[
                { cap: "Detail Explainer", pref: "Anthropic", fb: "OpenAI, Gemini", preset: "balanced" },
                { cap: "Observation Classifier", pref: "Groq", fb: "OpenAI, Gemini", preset: "fast" },
                { cap: "Related Detail Suggester", pref: "OpenAI", fb: "Anthropic, Gemini", preset: "balanced" },
                { cap: "Manufacturer Note Drafter", pref: "Anthropic", fb: "OpenAI, Gemini", preset: "balanced" },
                { cap: "Assembly Summarizer", pref: "OpenAI", fb: "Anthropic, Gemini", preset: "balanced" },
                { cap: "Field Note Cleaner", pref: "Groq", fb: "OpenAI, Gemini", preset: "fast" },
                { cap: "Artifact Summary", pref: "OpenAI", fb: "Anthropic, Groq", preset: "low_cost" },
                { cap: "Premium Reasoning", pref: "Anthropic", fb: "OpenAI, Gemini", preset: "premium" },
                { cap: "Fast Classification", pref: "Groq", fb: "Gemini, OpenAI", preset: "fast" },
              ].map((row) => (
                <tr key={row.cap} className="border-b" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                  <td className="py-2 pr-4 font-medium text-brand-text">{row.cap}</td>
                  <td className="py-2 pr-4">{row.pref}</td>
                  <td className="py-2 pr-4">{row.fb}</td>
                  <td className="py-2">
                    <span className="badge badge-unknown">{row.preset}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
