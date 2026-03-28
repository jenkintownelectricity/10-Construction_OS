/**
 * Construction OS — Branding Page
 * Wave C1 — White-label controls with local UI state.
 * No forced theme-system refactor.
 */

import { useState } from 'react';
import { tokens } from '../../ui/theme/tokens';

const t = tokens;

interface BrandingState {
  brandName: string;
  primaryColor: string;
  accentColor: string;
  dashboardTitle: string;
  fontFamily: string;
}

const INITIAL_BRANDING: BrandingState = {
  brandName: 'Construction OS',
  primaryColor: '#3b82f6',
  accentColor: '#f59e0b',
  dashboardTitle: 'Construction Control Tower',
  fontFamily: 'Inter',
};

function BrandingField({
  label,
  value,
  onChange,
  type = 'text',
}: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  type?: 'text' | 'color';
}) {
  return (
    <div style={{ marginBottom: '16px' }}>
      <label
        style={{
          display: 'block',
          fontSize: t.font.sizeXs,
          color: t.color.fgSecondary,
          marginBottom: '6px',
          fontWeight: Number(t.font.weightMedium),
        }}
      >
        {label}
      </label>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
        {type === 'color' && (
          <input
            type="color"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            style={{
              width: 32,
              height: 32,
              border: `1px solid ${t.color.border}`,
              borderRadius: t.radius.sm,
              cursor: 'pointer',
              padding: 0,
              background: 'transparent',
            }}
          />
        )}
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          style={{
            flex: 1,
            padding: '8px 12px',
            background: t.color.bgElevated,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            color: t.color.fgPrimary,
            fontSize: t.font.sizeXs,
            fontFamily: t.font.family,
            outline: 'none',
          }}
        />
      </div>
    </div>
  );
}

export function BrandingPage() {
  const [branding, setBranding] = useState<BrandingState>(INITIAL_BRANDING);

  const update = (key: keyof BrandingState) => (value: string) => {
    setBranding((prev) => ({ ...prev, [key]: value }));
  };

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Branding</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          White-label configuration — local state in Wave C1
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        {/* Controls */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '24px',
          }}
        >
          <h2 style={{ fontSize: t.font.sizeMd, fontWeight: Number(t.font.weightSemibold), margin: '0 0 20px 0' }}>Brand Controls</h2>
          <BrandingField label="Brand Name" value={branding.brandName} onChange={update('brandName')} />
          <BrandingField label="Primary Color" value={branding.primaryColor} onChange={update('primaryColor')} type="color" />
          <BrandingField label="Accent Color" value={branding.accentColor} onChange={update('accentColor')} type="color" />
          <BrandingField label="Dashboard Title" value={branding.dashboardTitle} onChange={update('dashboardTitle')} />
          <BrandingField label="Font Family" value={branding.fontFamily} onChange={update('fontFamily')} />
        </div>

        {/* Preview */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '24px',
          }}
        >
          <h2 style={{ fontSize: t.font.sizeMd, fontWeight: Number(t.font.weightSemibold), margin: '0 0 20px 0' }}>Preview</h2>
          <div
            style={{
              background: t.color.bgElevated,
              borderRadius: t.radius.md,
              padding: '20px',
              border: `1px solid ${t.color.border}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '16px' }}>
              <div
                style={{
                  width: 28,
                  height: 28,
                  borderRadius: t.radius.sm,
                  background: branding.primaryColor,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '13px',
                  fontWeight: 800,
                  color: '#ffffff',
                }}
              >
                {branding.brandName.charAt(0).toUpperCase()}
              </div>
              <span
                style={{
                  fontSize: t.font.sizeSm,
                  fontWeight: Number(t.font.weightBold),
                  color: t.color.fgPrimary,
                  fontFamily: branding.fontFamily + ', sans-serif',
                }}
              >
                {branding.brandName}
              </span>
            </div>
            <div
              style={{
                fontSize: t.font.sizeLg,
                fontWeight: Number(t.font.weightBold),
                color: t.color.fgPrimary,
                marginBottom: '8px',
                fontFamily: branding.fontFamily + ', sans-serif',
              }}
            >
              {branding.dashboardTitle}
            </div>
            <div style={{ display: 'flex', gap: '8px', marginTop: '12px' }}>
              <div style={{ width: 60, height: 24, borderRadius: t.radius.sm, background: branding.primaryColor }} />
              <div style={{ width: 60, height: 24, borderRadius: t.radius.sm, background: branding.accentColor }} />
            </div>
          </div>
          <p style={{ fontSize: '11px', color: t.color.fgMuted, marginTop: '12px' }}>
            Wave C1 — Branding changes are local UI state only. Persistence not connected.
          </p>
        </div>
      </div>
    </div>
  );
}
