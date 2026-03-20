"use client";

import { useState } from "react";
import { useBranding } from "@/components/branding/BrandingProvider";

function ColorInput({ label, value, onChange }: { label: string; value: string; onChange: (v: string) => void }) {
  return (
    <div className="flex items-center gap-3">
      <input
        type="color"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-10 h-10 rounded border cursor-pointer"
        style={{ borderColor: "var(--wl-border)" }}
      />
      <div>
        <div className="text-sm font-medium">{label}</div>
        <div className="text-xs text-brand-text-muted font-mono">{value}</div>
      </div>
    </div>
  );
}

export default function BrandingPage() {
  const { branding, updateBranding } = useBranding();
  const [appName, setAppName] = useState(branding.appName);
  const [companyName, setCompanyName] = useState(branding.companyName);
  const [logoUrl, setLogoUrl] = useState(branding.logoUrl);
  const [colors, setColors] = useState(branding.colors);
  const [density, setDensity] = useState(branding.density);
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);

  async function handleSave() {
    setSaving(true);
    setSaved(false);
    await updateBranding({ appName, companyName, logoUrl, colors, density });
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  }

  function updateColor(key: keyof typeof colors, value: string) {
    setColors({ ...colors, [key]: value });
  }

  return (
    <div className="max-w-4xl mx-auto py-8 px-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>
          White-Label Branding
        </h1>
        <p className="text-sm text-brand-text-muted mt-1">
          Customize the platform identity, colors, and visual appearance. Changes apply globally including AI settings.
        </p>
      </div>

      {/* Identity */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Identity</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="text-sm font-medium block mb-1">Application Name</label>
            <input
              type="text"
              value={appName}
              onChange={(e) => setAppName(e.target.value)}
              className="input-field"
            />
          </div>
          <div>
            <label className="text-sm font-medium block mb-1">Company Name</label>
            <input
              type="text"
              value={companyName}
              onChange={(e) => setCompanyName(e.target.value)}
              className="input-field"
            />
          </div>
          <div className="md:col-span-2">
            <label className="text-sm font-medium block mb-1">Logo URL</label>
            <input
              type="url"
              value={logoUrl}
              onChange={(e) => setLogoUrl(e.target.value)}
              placeholder="https://example.com/logo.svg"
              className="input-field"
            />
          </div>
        </div>
      </div>

      {/* Colors */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Brand Colors</h2>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <ColorInput label="Primary" value={colors.primary} onChange={(v) => updateColor("primary", v)} />
          <ColorInput label="Secondary" value={colors.secondary} onChange={(v) => updateColor("secondary", v)} />
          <ColorInput label="Accent" value={colors.accent} onChange={(v) => updateColor("accent", v)} />
          <ColorInput label="Surface" value={colors.surface} onChange={(v) => updateColor("surface", v)} />
          <ColorInput label="Surface Alt" value={colors.surfaceAlt} onChange={(v) => updateColor("surfaceAlt", v)} />
          <ColorInput label="Border" value={colors.border} onChange={(v) => updateColor("border", v)} />
          <ColorInput label="Text" value={colors.text} onChange={(v) => updateColor("text", v)} />
          <ColorInput label="Text Muted" value={colors.textMuted} onChange={(v) => updateColor("textMuted", v)} />
        </div>
      </div>

      {/* Density */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Display Density</h2>
        <div className="flex gap-3">
          {(["compact", "comfortable", "spacious"] as const).map((d) => (
            <button
              key={d}
              onClick={() => setDensity(d)}
              className={`px-4 py-2 rounded-lg border text-sm capitalize transition-colors ${
                density === d
                  ? "border-brand-primary font-semibold"
                  : "border-brand-border hover:border-brand-secondary"
              }`}
              style={density === d ? { borderColor: "var(--wl-primary, #1e3a5f)" } : {}}
            >
              {d}
            </button>
          ))}
        </div>
      </div>

      {/* Preview */}
      <div className="card mb-6">
        <h2 className="text-lg font-semibold mb-4">Live Preview</h2>
        <div className="rounded-lg overflow-hidden border" style={{ borderColor: colors.border }}>
          <div className="px-4 py-2 flex items-center gap-3" style={{ backgroundColor: colors.primary }}>
            <span className="text-white font-semibold">{appName}</span>
            <span className="text-white/50 text-xs ml-auto">{companyName}</span>
          </div>
          <div className="p-4" style={{ backgroundColor: colors.surface }}>
            <div className="p-3 rounded-lg border" style={{ backgroundColor: "white", borderColor: colors.border }}>
              <span className="text-sm font-medium" style={{ color: colors.text }}>Sample card content</span>
              <p className="text-xs mt-1" style={{ color: colors.textMuted }}>This previews your branding configuration.</p>
              <button className="mt-2 px-3 py-1 rounded text-white text-xs font-medium" style={{ backgroundColor: colors.accent }}>
                Accent Action
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Save */}
      <div className="flex justify-end gap-3">
        {saved && <span className="text-sm text-brand-success self-center">Saved successfully</span>}
        <button onClick={handleSave} disabled={saving} className="btn-primary">
          {saving ? "Saving..." : "Save Branding"}
        </button>
      </div>
    </div>
  );
}
