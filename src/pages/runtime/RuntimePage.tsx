/**
 * Construction OS — Runtime Monitor Page
 * Wave C1 — Deterministic module statuses from frozen mock data.
 */

import { tokens } from '../../ui/theme/tokens';
import { MOCK_RUNTIME_MODULES } from '../../mock/primitives/mockRuntime';

const t = tokens;

const statusColors: Record<string, string> = {
  ACTIVE: t.color.success,
  IDLE: t.color.warning,
  OFFLINE: t.color.fgMuted,
};

export function RuntimePage() {
  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Runtime Monitor</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Construction Runtime module status — deterministic snapshot
        </p>
      </div>

      {/* Status strip */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '16px',
          padding: '10px 16px',
          background: t.color.bgSurface,
          borderRadius: t.radius.md,
          border: `1px solid ${t.color.border}`,
          marginBottom: '24px',
          fontSize: t.font.sizeXs,
        }}
      >
        <span style={{ color: t.color.fgMuted }}>RUNTIME</span>
        {(['ACTIVE', 'IDLE', 'OFFLINE'] as const).map((status) => {
          const count = MOCK_RUNTIME_MODULES.filter((m) => m.status === status).length;
          return (
            <span key={status} style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <span style={{ width: 7, height: 7, borderRadius: '50%', background: statusColors[status], display: 'inline-block' }} />
              <span style={{ color: statusColors[status] }}>{count} {status}</span>
            </span>
          );
        })}
      </div>

      {/* Module cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '12px' }}>
        {MOCK_RUNTIME_MODULES.map((mod) => (
          <div
            key={mod.id}
            style={{
              background: t.color.bgSurface,
              border: `1px solid ${t.color.border}`,
              borderRadius: t.radius.md,
              padding: '20px',
              borderTop: `3px solid ${statusColors[mod.status]}`,
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
              <h3 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: 0 }}>{mod.name}</h3>
              <span
                style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  padding: '2px 8px',
                  borderRadius: '10px',
                  background: statusColors[mod.status] + '18',
                  color: statusColors[mod.status],
                  fontSize: '11px',
                  fontWeight: Number(t.font.weightSemibold),
                }}
              >
                <span style={{ width: 5, height: 5, borderRadius: '50%', background: 'currentColor' }} />
                {mod.status}
              </span>
            </div>
            <p style={{ fontSize: t.font.sizeXs, color: t.color.fgSecondary, margin: '0 0 12px 0', lineHeight: t.font.lineNormal }}>
              {mod.description}
            </p>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: t.color.fgMuted }}>
              <span>v{mod.version}</span>
              <span>Last: {mod.lastHeartbeat.split('T')[1].split('.')[0]}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
