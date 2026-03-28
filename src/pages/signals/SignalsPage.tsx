/**
 * Construction OS — Signals Page
 * Wave C1 — Deterministic signal feed. No live pulse behavior.
 */

import { tokens } from '../../ui/theme/tokens';
import { MOCK_SIGNALS, type SignalType } from '../../mock/primitives/mockSignals';

const t = tokens;

const signalTypeColors: Record<SignalType, string> = {
  ASSEMBLY_CREATED: t.color.accentPrimary,
  DETAIL_RESOLVED: t.color.success,
  MATERIAL_LINKED: '#06b6d4',
  PATTERN_MATCHED: t.color.compare,
  CONDITION_DETECTED: t.color.warning,
  ARTIFACT_RENDERED: t.color.info,
};

const severityColors: Record<string, string> = {
  INFO: t.color.info,
  WARNING: t.color.warning,
  CRITICAL: t.color.error,
};

export function SignalsPage() {
  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Signals</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Signal feed — deterministic event stream snapshot
        </p>
      </div>

      {/* Signal type legend */}
      <div
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '8px',
          marginBottom: '20px',
        }}
      >
        {Object.entries(signalTypeColors).map(([type, color]) => (
          <span
            key={type}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '5px',
              padding: '3px 10px',
              background: color + '18',
              borderRadius: '10px',
              fontSize: '11px',
              color,
            }}
          >
            <span style={{ width: 5, height: 5, borderRadius: '50%', background: color }} />
            {type}
          </span>
        ))}
      </div>

      {/* Signal feed */}
      <div
        style={{
          background: t.color.bgSurface,
          border: `1px solid ${t.color.border}`,
          borderRadius: t.radius.md,
          overflow: 'hidden',
        }}
      >
        {MOCK_SIGNALS.map((signal, idx) => (
          <div
            key={signal.id}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '14px',
              padding: '14px 16px',
              borderBottom: idx < MOCK_SIGNALS.length - 1 ? `1px solid ${t.color.borderSubtle}` : 'none',
            }}
          >
            {/* Severity dot */}
            <span
              style={{
                width: 8,
                height: 8,
                borderRadius: '50%',
                background: severityColors[signal.severity],
                flexShrink: 0,
                marginTop: '5px',
              }}
            />

            {/* Content */}
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <span
                  style={{
                    fontSize: '11px',
                    padding: '1px 7px',
                    borderRadius: '8px',
                    background: signalTypeColors[signal.type] + '22',
                    color: signalTypeColors[signal.type],
                    fontWeight: Number(t.font.weightSemibold),
                  }}
                >
                  {signal.type}
                </span>
                <span style={{ fontSize: '11px', color: t.color.fgMuted }}>{signal.severity}</span>
              </div>
              <div style={{ fontSize: t.font.sizeXs, color: t.color.fgPrimary, marginBottom: '4px' }}>
                {signal.payload}
              </div>
              <div style={{ fontSize: '11px', color: t.color.fgMuted }}>
                {signal.source} \u2192 {signal.target}
              </div>
            </div>

            {/* Timestamp */}
            <span style={{ fontSize: '11px', color: t.color.fgMuted, flexShrink: 0 }}>
              {signal.timestamp.split('T')[1].split('.')[0]}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
}
