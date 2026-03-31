/**
 * Manufacturer Hub — Header
 * Shows selected manufacturer name, mode indicator, and seed status.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { ManufacturerSummary, ManufacturerHubMode } from '../../../lib/manufacturers/manufacturerHubTypes';
import { MODE_LABELS } from '../../../lib/manufacturers/manufacturerHubMode';

const t = tokens;

interface ManufacturerHeaderProps {
  manufacturer: ManufacturerSummary;
  mode: ManufacturerHubMode;
  surface: Record<string, string>;
}

export function ManufacturerHeader({ manufacturer, mode, surface }: ManufacturerHeaderProps) {
  const seedColor = manufacturer.seedStatus === 'seeded' ? '#22c55e'
    : manufacturer.seedStatus === 'scaffold' ? '#eab308' : '#555d73';

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      padding: '12px 16px',
      background: surface.bgPanel,
      border: `1px solid ${surface.border}`,
      borderRadius: t.radius.lg,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <div style={{
          width: 36,
          height: 36,
          borderRadius: t.radius.md,
          background: surface.accent,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontSize: '16px',
          fontWeight: 800,
          color: '#ffffff',
        }}>
          {manufacturer.name.charAt(0)}
        </div>
        <div>
          <div style={{
            fontSize: t.font.sizeMd,
            fontWeight: Number(t.font.weightBold),
            color: surface.fg,
          }}>
            {manufacturer.name}
          </div>
          <div style={{
            fontSize: t.font.sizeXs,
            color: surface.fgSecondary,
            marginTop: '2px',
          }}>
            {manufacturer.description}
          </div>
        </div>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span style={{
          display: 'inline-flex',
          alignItems: 'center',
          gap: '6px',
          padding: '4px 10px',
          borderRadius: t.radius.sm,
          fontSize: '10px',
          fontWeight: Number(t.font.weightSemibold),
          color: seedColor,
          background: `${seedColor}18`,
          letterSpacing: '0.04em',
          textTransform: 'uppercase',
        }}>
          <span style={{
            width: 6, height: 6, borderRadius: '50%', background: seedColor,
          }} />
          {manufacturer.seedStatus}
        </span>
        <span style={{
          padding: '4px 10px',
          borderRadius: t.radius.sm,
          fontSize: '10px',
          fontWeight: Number(t.font.weightSemibold),
          color: surface.fgMuted,
          background: surface.border,
          letterSpacing: '0.06em',
        }}>
          {MODE_LABELS[mode]} MODE
        </span>
      </div>
    </div>
  );
}
