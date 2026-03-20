"use client";

import { useState } from "react";
import type { ProviderConfig, HealthStatus } from "@/lib/ai/provider-types";
import type { ProviderRegistryEntry } from "@/lib/ai/provider-registry";

interface ProviderCardProps {
  provider: ProviderConfig;
  registry: ProviderRegistryEntry;
  onUpdate: () => void;
}

function HealthBadge({ status }: { status: HealthStatus }) {
  const cls = `badge badge-${status}`;
  const labels: Record<HealthStatus, string> = {
    healthy: "Healthy",
    degraded: "Degraded",
    unavailable: "Unavailable",
    misconfigured: "Not Configured",
  };
  return <span className={cls}>{labels[status]}</span>;
}

export function ProviderCard({ provider, registry, onUpdate }: ProviderCardProps) {
  const [keyInput, setKeyInput] = useState("");
  const [showKeyInput, setShowKeyInput] = useState(false);
  const [baseUrlInput, setBaseUrlInput] = useState(provider.baseUrl ?? "");
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<{ ok: boolean; latencyMs: number; error?: string } | null>(null);
  const [saving, setSaving] = useState(false);
  const [selectedModel, setSelectedModel] = useState(provider.defaultModel);

  async function handleToggle() {
    setSaving(true);
    await fetch("/api/ai/settings", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ providers: { [provider.id]: { enabled: !provider.enabled } } }),
    });
    setSaving(false);
    onUpdate();
  }

  async function handleSaveKey() {
    if (!keyInput.trim()) return;
    setSaving(true);
    await fetch("/api/ai/settings", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ setKey: { provider: provider.id, key: keyInput.trim() } }),
    });
    setKeyInput("");
    setShowKeyInput(false);
    setSaving(false);
    onUpdate();
  }

  async function handleClearKey() {
    setSaving(true);
    await fetch("/api/ai/settings", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ clearKey: { provider: provider.id } }),
    });
    setSaving(false);
    onUpdate();
  }

  async function handleSaveModel() {
    setSaving(true);
    await fetch("/api/ai/settings", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        providers: {
          [provider.id]: {
            defaultModel: selectedModel,
            ...(registry.supportsBaseUrl ? { baseUrl: baseUrlInput || undefined } : {}),
          },
        },
      }),
    });
    setSaving(false);
    onUpdate();
  }

  async function handleTest() {
    setTesting(true);
    setTestResult(null);
    try {
      const res = await fetch("/api/ai/test", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ provider: provider.id }),
      });
      const data = await res.json();
      setTestResult(data);
    } catch {
      setTestResult({ ok: false, latencyMs: 0, error: "Network error" });
    }
    setTesting(false);
    onUpdate();
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <div
            className="w-10 h-10 rounded-lg flex items-center justify-center text-white font-bold text-sm"
            style={{ backgroundColor: "var(--wl-primary, #1e3a5f)" }}
          >
            {registry.icon.slice(0, 2)}
          </div>
          <div>
            <h3 className="font-semibold text-base">{registry.name}</h3>
            <p className="text-xs text-brand-text-muted">{registry.description}</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <HealthBadge status={provider.healthStatus} />
          <button
            onClick={handleToggle}
            disabled={saving}
            className={`relative w-11 h-6 rounded-full transition-colors ${
              provider.enabled ? "bg-brand-success" : "bg-gray-300"
            }`}
            aria-label={`Toggle ${registry.name}`}
          >
            <span
              className={`absolute top-0.5 left-0.5 w-5 h-5 bg-white rounded-full shadow transition-transform ${
                provider.enabled ? "translate-x-5" : ""
              }`}
            />
          </button>
        </div>
      </div>

      {/* API Key Section */}
      <div className="border-t pt-3 mt-3" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium">API Key</span>
          <div className="flex gap-2">
            {provider.apiKeySet && (
              <>
                <span className="text-xs text-brand-text-muted font-mono">{provider.apiKeyMasked}</span>
                <button onClick={() => setShowKeyInput(true)} className="text-xs text-brand-secondary hover:underline">
                  Replace
                </button>
                <button onClick={handleClearKey} className="text-xs text-brand-danger hover:underline">
                  Clear
                </button>
              </>
            )}
            {!provider.apiKeySet && !showKeyInput && (
              <button onClick={() => setShowKeyInput(true)} className="btn-secondary text-xs">
                Set Key
              </button>
            )}
          </div>
        </div>
        {showKeyInput && (
          <div className="flex gap-2 mt-2">
            <input
              type="password"
              value={keyInput}
              onChange={(e) => setKeyInput(e.target.value)}
              placeholder={`Enter ${registry.name} API key`}
              className="input-field flex-1"
              autoComplete="off"
            />
            <button onClick={handleSaveKey} disabled={saving || !keyInput.trim()} className="btn-primary">
              Save
            </button>
            <button onClick={() => { setShowKeyInput(false); setKeyInput(""); }} className="btn-secondary">
              Cancel
            </button>
          </div>
        )}
      </div>

      {/* Model Selection */}
      <div className="border-t pt-3 mt-3" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
        <label className="text-sm font-medium block mb-1">Default Model</label>
        <div className="flex gap-2">
          <select
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value)}
            className="input-field flex-1"
          >
            {registry.models.map((m) => (
              <option key={m.id} value={m.id}>{m.name} ({m.contextWindow.toLocaleString()} ctx)</option>
            ))}
          </select>
          <button onClick={handleSaveModel} disabled={saving} className="btn-secondary">
            Save
          </button>
        </div>
      </div>

      {/* Base URL (if supported) */}
      {registry.supportsBaseUrl && (
        <div className="border-t pt-3 mt-3" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
          <label className="text-sm font-medium block mb-1">Base URL (optional)</label>
          <div className="flex gap-2">
            <input
              type="url"
              value={baseUrlInput}
              onChange={(e) => setBaseUrlInput(e.target.value)}
              placeholder="https://api.openai.com/v1"
              className="input-field flex-1"
            />
            <button onClick={handleSaveModel} disabled={saving} className="btn-secondary">
              Save
            </button>
          </div>
        </div>
      )}

      {/* Test & Latency */}
      <div className="border-t pt-3 mt-3 flex items-center justify-between" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
        <button onClick={handleTest} disabled={testing || !provider.apiKeySet} className="btn-primary">
          {testing ? "Testing..." : "Test Connection"}
        </button>
        {testResult && (
          <span className={`text-sm font-medium ${testResult.ok ? "text-brand-success" : "text-brand-danger"}`}>
            {testResult.ok ? `Connected (${testResult.latencyMs}ms)` : testResult.error}
          </span>
        )}
        {provider.lastLatencyMs && !testResult && (
          <span className="text-xs text-brand-text-muted">Last: {provider.lastLatencyMs}ms</span>
        )}
      </div>
    </div>
  );
}
