/**
 * Manufacturer Hub — Overview Panel (WORK mode)
 * Office-style overview card with manufacturer summary stats.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { ManufacturerSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface ManufacturerOverviewPanelProps {
  manufacturer: ManufacturerSummary;
  surface: Record<string, string>;
}

export function ManufacturerOverviewPanel({ manufacturer, surface }: ManufacturerOverviewPanelProps) {
  const stats = [
    { label: 'Products', value: manufacturer.productsCount },
    { label: 'Systems', value: manufacturer.systemsCount },
    { label: 'Certifications', value: manufacturer.certificationsCount },
  ];

  return (
    <div style={{
      padding: '20px',
      background: surface.bgPanel,
      border: `1px solid ${surface.border}`,
      borderRadius: t.radius.lg,
    }}>
      <div style={{
        fontSize: '10px',
        fontWeight: Number(t.font.weightSemibold),
        color: surface.fgMuted,
        textTransform: 'uppercase',
        letterSpacing: '0.08em',
        marginBottom: '16px',
      }}>
        Overview
      </div>

      {manufacturer.seedStatus === 'scaffold' ? (
        <div style={{
          padding: '24px',
          textAlign: 'center',
          color: surface.fgMuted,
          fontSize: t.font.sizeSm,
          border: `1px dashed ${surface.border}`,
          borderRadius: t.radius.md,
        }}>
          <div style={{ fontSize: t.font.sizeMd, marginBottom: '8px', color: '#eab308' }}>
            Scaffold Entry
          </div>
          <div>This manufacturer is not yet seeded in the registry.</div>
          <div style={{ marginTop: '4px', fontSize: t.font.sizeXs }}>
            No products, systems, or certifications are available for display.
          </div>
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '16px',
        }}>
          {stats.map(stat => (
            <div key={stat.label} style={{
              padding: '16px',
              background: surface.bgElevated,
              borderRadius: t.radius.md,
              textAlign: 'center',
            }}>
              <div style={{
                fontSize: t.font.sizeXl,
                fontWeight: Number(t.font.weightBold),
                color: surface.accent,
              }}>
                {stat.value}
              </div>
              <div style={{
                fontSize: t.font.sizeXs,
                color: surface.fgSecondary,
                marginTop: '4px',
              }}>
                {stat.label}
              </div>
            </div>
          ))}
        </div>
      )}

      <div style={{
        marginTop: '12px',
        fontSize: '10px',
        color: surface.fgMuted,
        fontStyle: 'italic',
      }}>
        Observer-derived projection — not canonical truth
      </div>
    </div>
  );
}
