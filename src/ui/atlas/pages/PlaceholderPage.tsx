/**
 * Construction Atlas — Placeholder Page
 *
 * Used for pages that are structurally present in navigation
 * but not yet fully built: Projects, Details, Artifacts.
 */

import { DEFAULT_BRANDING } from '../../../lib/branding/branding-types';

const c = DEFAULT_BRANDING.colors;

interface PlaceholderPageProps {
  title: string;
  description: string;
}

export function PlaceholderPage({ title, description }: PlaceholderPageProps) {
  return (
    <div>
      <h1 style={{ fontSize: '24px', fontWeight: 700, color: c.text, margin: 0 }}>{title}</h1>
      <p style={{ color: c.textMuted, margin: '4px 0 24px', fontSize: '14px' }}>{description}</p>
      <div style={{
        background: '#ffffff',
        border: `1px solid ${c.border}`,
        borderRadius: '8px',
        padding: '48px',
        textAlign: 'center',
      }}>
        <div style={{ fontSize: '32px', marginBottom: '12px', opacity: 0.2 }}>{'\u25C6'}</div>
        <div style={{ fontSize: '16px', fontWeight: 600, color: c.text, marginBottom: '8px' }}>{title}</div>
        <div style={{ fontSize: '13px', color: c.textMuted }}>
          Page shell ready. Content surface available for data integration.
        </div>
      </div>
    </div>
  );
}
