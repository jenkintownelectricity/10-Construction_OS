/**
 * Construction OS — Atlas Page (Control Tower Surface)
 * Wave C1 — Placeholder panels only. No live spatial rendering.
 * No runtime/atlas repo coupling.
 */

import { tokens } from '../../ui/theme/tokens';

const t = tokens;

function PlaceholderPanel({ title, description }: { title: string; description: string }) {
  return (
    <div
      style={{
        background: t.color.bgSurface,
        border: `1px solid ${t.color.border}`,
        borderRadius: t.radius.md,
        padding: '32px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '200px',
      }}
    >
      <div style={{ fontSize: '24px', marginBottom: '12px', color: t.color.fgMuted }}>\u25C7</div>
      <h3 style={{ fontSize: t.font.sizeMd, fontWeight: Number(t.font.weightSemibold), margin: '0 0 8px 0', color: t.color.fgPrimary }}>
        {title}
      </h3>
      <p style={{ fontSize: t.font.sizeXs, color: t.color.fgMuted, textAlign: 'center', maxWidth: '300px' }}>
        {description}
      </p>
      <div
        style={{
          marginTop: '16px',
          padding: '4px 12px',
          background: t.color.bgElevated,
          borderRadius: t.radius.sm,
          fontSize: '11px',
          color: t.color.fgMuted,
          border: `1px solid ${t.color.borderSubtle}`,
        }}
      >
        Wave C1 — Placeholder
      </div>
    </div>
  );
}

export function AtlasPage() {
  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Atlas</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Spatial intelligence surface — building context and detail resolution
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        <PlaceholderPanel
          title="Atlas Map"
          description="Spatial building map with zone selection, layer overlays, and condition mapping."
        />
        <PlaceholderPanel
          title="Assembly Context"
          description="Contextual assembly viewer showing active assemblies for the selected spatial zone."
        />
        <PlaceholderPanel
          title="Detail Resolver"
          description="Automatic detail resolution engine for edge conditions, penetrations, and transitions."
        />
        <PlaceholderPanel
          title="Condition Graph"
          description="Condition relationship graph showing dependencies between spatial conditions and assemblies."
        />
      </div>
    </div>
  );
}
