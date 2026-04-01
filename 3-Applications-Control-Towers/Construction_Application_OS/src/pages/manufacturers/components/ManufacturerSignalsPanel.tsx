/**
 * Manufacturer Hub — Signals Panel
 * Presentational UI interaction state signals only.
 * These are NOT real bus emissions or historical telemetry.
 * No fabricated event history, timestamps, or prior transitions.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { UISignal } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface ManufacturerSignalsPanelProps {
  signals: UISignal[];
  surface: Record<string, string>;
}

export function ManufacturerSignalsPanel({ signals, surface }: ManufacturerSignalsPanelProps) {
  return (
    <div style={{
      padding: '16px',
      borderTop: `1px solid ${surface.border}`,
    }}>
      <div style={{
        fontSize: '10px',
        fontWeight: Number(t.font.weightSemibold),
        color: surface.fgMuted,
        textTransform: 'uppercase',
        letterSpacing: '0.08em',
        marginBottom: '10px',
      }}>
        Signals
      </div>

      <div style={{
        fontSize: '9px',
        color: surface.fgMuted,
        marginBottom: '8px',
        fontStyle: 'italic',
      }}>
        Presentational UI state only — not bus emissions
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {signals.map(signal => (
          <div
            key={signal.type}
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              padding: '6px 10px',
              borderRadius: t.radius.sm,
              background: signal.active ? `${surface.accent}12` : 'transparent',
            }}
          >
            <span style={{
              width: 5,
              height: 5,
              borderRadius: '50%',
              background: signal.active ? surface.accent : surface.fgMuted,
              flexShrink: 0,
            }} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{
                fontSize: '10px',
                fontWeight: Number(t.font.weightSemibold),
                color: signal.active ? surface.fg : surface.fgMuted,
                fontFamily: t.font.familyMono,
              }}>
                {signal.type}
              </div>
              <div style={{
                fontSize: '10px',
                color: surface.fgSecondary,
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis',
              }}>
                {signal.label}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
