"use client";

import { useState, useEffect } from "react";
import type { ProviderId, ProviderPreset } from "@/lib/ai/provider-types";

interface SettingsData {
  defaultProvider: ProviderId;
  fallbackProvider: ProviderId;
  activePreset: ProviderPreset;
  defaultTemperature: number;
  defaultMaxTokens: number;
  timeoutMs: number;
  streamingEnabled: boolean;
}

const PROVIDERS: { id: ProviderId; label: string }[] = [
  { id: "openai", label: "OpenAI" },
  { id: "anthropic", label: "Anthropic" },
  { id: "gemini", label: "Google Gemini" },
  { id: "groq", label: "Groq" },
];

const PRESETS: { id: ProviderPreset; label: string; desc: string }[] = [
  { id: "fast", label: "Fast", desc: "Fastest inference speed" },
  { id: "low_cost", label: "Low Cost", desc: "Lowest cost per token" },
  { id: "balanced", label: "Balanced", desc: "Balance of quality, speed, cost" },
  { id: "premium_reasoning", label: "Premium Reasoning", desc: "Highest quality analysis" },
  { id: "multimodal_ready", label: "Multimodal Ready", desc: "Multimodal input scaffold" },
];

export function GlobalAISettings({ onUpdate }: { onUpdate: () => void }) {
  const [settings, setSettings] = useState<SettingsData | null>(null);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetch("/api/ai/settings")
      .then((r) => r.json())
      .then((data) => {
        setSettings({
          defaultProvider: data.defaultProvider,
          fallbackProvider: data.fallbackProvider,
          activePreset: data.activePreset,
          defaultTemperature: data.defaultTemperature,
          defaultMaxTokens: data.defaultMaxTokens,
          timeoutMs: data.timeoutMs,
          streamingEnabled: data.streamingEnabled,
        });
      })
      .catch(() => {});
  }, []);

  async function handleSave() {
    if (!settings) return;
    setSaving(true);
    await fetch("/api/ai/settings", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(settings),
    });
    setSaving(false);
    onUpdate();
  }

  if (!settings) return <div className="card animate-pulse h-64" />;

  return (
    <div className="card">
      <h2 className="text-lg font-semibold mb-4">Global AI Configuration</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Default Provider */}
        <div>
          <label className="text-sm font-medium block mb-1">Default Provider</label>
          <select
            value={settings.defaultProvider}
            onChange={(e) => setSettings({ ...settings, defaultProvider: e.target.value as ProviderId })}
            className="input-field"
          >
            {PROVIDERS.map((p) => <option key={p.id} value={p.id}>{p.label}</option>)}
          </select>
        </div>

        {/* Fallback Provider */}
        <div>
          <label className="text-sm font-medium block mb-1">Fallback Provider</label>
          <select
            value={settings.fallbackProvider}
            onChange={(e) => setSettings({ ...settings, fallbackProvider: e.target.value as ProviderId })}
            className="input-field"
          >
            {PROVIDERS.map((p) => <option key={p.id} value={p.id}>{p.label}</option>)}
          </select>
        </div>

        {/* Temperature */}
        <div>
          <label className="text-sm font-medium block mb-1">
            Default Temperature: {settings.defaultTemperature.toFixed(1)}
          </label>
          <input
            type="range"
            min="0"
            max="2"
            step="0.1"
            value={settings.defaultTemperature}
            onChange={(e) => setSettings({ ...settings, defaultTemperature: parseFloat(e.target.value) })}
            className="w-full"
          />
        </div>

        {/* Max Tokens */}
        <div>
          <label className="text-sm font-medium block mb-1">Default Max Tokens</label>
          <input
            type="number"
            value={settings.defaultMaxTokens}
            onChange={(e) => setSettings({ ...settings, defaultMaxTokens: parseInt(e.target.value) || 2048 })}
            className="input-field"
            min={1}
            max={128000}
          />
        </div>

        {/* Timeout */}
        <div>
          <label className="text-sm font-medium block mb-1">Timeout (ms)</label>
          <input
            type="number"
            value={settings.timeoutMs}
            onChange={(e) => setSettings({ ...settings, timeoutMs: parseInt(e.target.value) || 30000 })}
            className="input-field"
            min={5000}
            max={120000}
            step={1000}
          />
        </div>

        {/* Streaming */}
        <div className="flex items-center gap-3">
          <label className="text-sm font-medium">Streaming (scaffold)</label>
          <button
            onClick={() => setSettings({ ...settings, streamingEnabled: !settings.streamingEnabled })}
            className={`relative w-11 h-6 rounded-full transition-colors ${
              settings.streamingEnabled ? "bg-brand-success" : "bg-gray-300"
            }`}
          >
            <span
              className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${
                settings.streamingEnabled ? "translate-x-5" : ""
              }`}
            />
          </button>
        </div>
      </div>

      {/* Preset Selector */}
      <div className="mt-6">
        <label className="text-sm font-medium block mb-2">Provider Preset</label>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-2">
          {PRESETS.map((preset) => (
            <button
              key={preset.id}
              onClick={() => setSettings({ ...settings, activePreset: preset.id })}
              className={`p-2 rounded-lg border text-xs text-center transition-colors ${
                settings.activePreset === preset.id
                  ? "border-brand-primary bg-brand-primary/5 font-semibold"
                  : "border-brand-border hover:border-brand-secondary"
              }`}
              style={
                settings.activePreset === preset.id
                  ? { borderColor: "var(--wl-primary, #1e3a5f)" }
                  : {}
              }
            >
              <div className="font-medium">{preset.label}</div>
              <div className="text-brand-text-muted mt-0.5">{preset.desc}</div>
            </button>
          ))}
        </div>
      </div>

      <div className="mt-6 flex justify-end">
        <button onClick={handleSave} disabled={saving} className="btn-primary">
          {saving ? "Saving..." : "Save Settings"}
        </button>
      </div>
    </div>
  );
}
