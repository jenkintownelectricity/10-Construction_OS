/**
 * Construction OS — Registry Ledger Page
 * Wave C1 — Deterministic registry entries from frozen mock data.
 */

import { tokens } from '../../ui/theme/tokens';
import { MOCK_REGISTRY_ENTRIES, MOCK_REGISTRY_HEALTH } from '../../mock/primitives/mockRegistry';

const t = tokens;

const actionColors: Record<string, string> = {
  REGISTERED: t.color.success,
  DRAFT_CREATED: t.color.warning,
  DEPRECATED: t.color.fgMuted,
  VERSION_SEALED: t.color.accentPrimary,
};

const healthColors: Record<string, string> = {
  HEALTHY: t.color.success,
  DEGRADED: t.color.warning,
  OFFLINE: t.color.error,
};

export function RegistryPage() {
  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Registry</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Immutable ledger — primitive registrations and state transitions
        </p>
      </div>

      {/* Health Panel */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(6, 1fr)',
          gap: '12px',
          marginBottom: '24px',
        }}
      >
        {[
          { label: 'Total Entries', value: MOCK_REGISTRY_HEALTH.totalEntries },
          { label: 'Canonical', value: MOCK_REGISTRY_HEALTH.canonical, color: t.color.success },
          { label: 'Draft', value: MOCK_REGISTRY_HEALTH.draft, color: t.color.warning },
          { label: 'Deprecated', value: MOCK_REGISTRY_HEALTH.deprecated, color: t.color.fgMuted },
          { label: 'Last Sync', value: MOCK_REGISTRY_HEALTH.lastSyncTimestamp.split('T')[0] },
          { label: 'Integrity', value: MOCK_REGISTRY_HEALTH.integrityStatus, color: healthColors[MOCK_REGISTRY_HEALTH.integrityStatus] },
        ].map((item) => (
          <div
            key={item.label}
            style={{
              background: t.color.bgSurface,
              border: `1px solid ${t.color.border}`,
              borderRadius: t.radius.md,
              padding: '14px',
            }}
          >
            <div style={{ fontSize: '11px', color: t.color.fgMuted, marginBottom: '4px' }}>{item.label}</div>
            <div style={{ fontSize: t.font.sizeMd, fontWeight: Number(t.font.weightBold), color: item.color || t.color.fgPrimary }}>
              {item.value}
            </div>
          </div>
        ))}
      </div>

      {/* Ledger Table */}
      <div
        style={{
          background: t.color.bgSurface,
          border: `1px solid ${t.color.border}`,
          borderRadius: t.radius.md,
          overflow: 'hidden',
          marginBottom: '16px',
        }}
      >
        <div style={{ padding: '14px 16px', borderBottom: `1px solid ${t.color.border}` }}>
          <h2 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: 0 }}>Registry Ledger</h2>
        </div>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: t.font.sizeXs }}>
          <thead>
            <tr style={{ background: t.color.bgElevated, borderBottom: `1px solid ${t.color.border}` }}>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>ID</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Primitive</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Type</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Action</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Actor</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Version</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {MOCK_REGISTRY_ENTRIES.map((entry) => (
              <tr key={entry.id} style={{ borderBottom: `1px solid ${t.color.borderSubtle}` }}>
                <td style={{ padding: '8px 14px', color: t.color.fgMuted, fontFamily: t.font.familyMono }}>{entry.id}</td>
                <td style={{ padding: '8px 14px', color: t.color.fgPrimary, fontFamily: t.font.familyMono }}>{entry.primitiveId}</td>
                <td style={{ padding: '8px 14px', color: t.color.fgSecondary }}>{entry.primitiveType}</td>
                <td style={{ padding: '8px 14px' }}>
                  <span style={{ color: actionColors[entry.action] || t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>
                    {entry.action}
                  </span>
                </td>
                <td style={{ padding: '8px 14px', color: t.color.fgSecondary }}>{entry.actor}</td>
                <td style={{ padding: '8px 14px', color: t.color.fgSecondary, fontFamily: t.font.familyMono }}>{entry.version}</td>
                <td style={{ padding: '8px 14px', color: t.color.fgMuted, fontSize: '11px' }}>{entry.timestamp.replace('T', ' ').split('.')[0]}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
