/**
 * Manufacturer Hub — Sidebar
 * Left rail showing manufacturer list with seed status indicators.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { ManufacturerSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface ManufacturerSidebarProps {
  manufacturers: ManufacturerSummary[];
  selectedId: string;
  onSelect: (id: string) => void;
  surface: Record<string, string>;
}

const SEED_STATUS_COLORS: Record<string, string> = {
  seeded: '#22c55e',
  scaffold: '#eab308',
  'not-seeded': '#555d73',
};

const SEED_STATUS_LABELS: Record<string, string> = {
  seeded: 'Seeded',
  scaffold: 'Scaffold',
  'not-seeded': 'Not Seeded',
};

export function ManufacturerSidebar({ manufacturers, selectedId, onSelect, surface }: ManufacturerSidebarProps) {
  return (
    <div style={{
      width: 220,
      minWidth: 220,
      borderRight: `1px solid ${surface.border}`,
      overflow: 'auto',
      background: surface.bgPanel,
      display: 'flex',
      flexDirection: 'column',
    }}>
      <div style={{
        padding: '16px',
        borderBottom: `1px solid ${surface.border}`,
        fontSize: '10px',
        fontWeight: Number(t.font.weightSemibold),
        color: surface.fgMuted,
        textTransform: 'uppercase',
        letterSpacing: '0.08em',
      }}>
        Manufacturers
      </div>
      {manufacturers.map(mfg => {
        const isSelected = mfg.id === selectedId;
        return (
          <button
            key={mfg.id}
            onClick={() => onSelect(mfg.id)}
            style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '4px',
              width: '100%',
              padding: '12px 16px',
              border: 'none',
              borderLeft: isSelected ? `3px solid ${surface.accent}` : '3px solid transparent',
              cursor: 'pointer',
              textAlign: 'left',
              fontFamily: t.font.family,
              background: isSelected ? surface.bgHover : 'transparent',
              transition: `background ${t.transition.fast}`,
            }}
          >
            <span style={{
              fontSize: t.font.sizeSm,
              fontWeight: Number(isSelected ? t.font.weightSemibold : t.font.weightMedium),
              color: isSelected ? surface.fg : surface.fgSecondary,
            }}>
              {mfg.name}
            </span>
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '6px',
              fontSize: '10px',
              color: surface.fgMuted,
            }}>
              <span style={{
                width: 6,
                height: 6,
                borderRadius: '50%',
                background: SEED_STATUS_COLORS[mfg.seedStatus],
                display: 'inline-block',
                flexShrink: 0,
              }} />
              {SEED_STATUS_LABELS[mfg.seedStatus]}
            </span>
          </button>
        );
      })}
    </div>
  );
}
