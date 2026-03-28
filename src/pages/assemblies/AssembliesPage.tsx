/**
 * Construction OS — Assemblies Vault Page
 * Wave C1 — Deterministic table from frozen mock data.
 */

import { tokens } from '../../ui/theme/tokens';
import { MOCK_ASSEMBLIES } from '../../mock/primitives/mockAssemblies';

const t = tokens;

const statusColors: Record<string, string> = {
  CANONICAL: t.color.success,
  DRAFT: t.color.warning,
  DEPRECATED: t.color.fgMuted,
};

export function AssembliesPage() {
  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Assemblies</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Construction assembly primitives — governed composition and layering
        </p>
      </div>
      <div
        style={{
          background: t.color.bgSurface,
          border: `1px solid ${t.color.border}`,
          borderRadius: t.radius.md,
          overflow: 'hidden',
        }}
      >
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: t.font.sizeXs }}>
          <thead>
            <tr style={{ background: t.color.bgElevated, borderBottom: `1px solid ${t.color.border}` }}>
              <th style={{ textAlign: 'left', padding: '10px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Name</th>
              <th style={{ textAlign: 'left', padding: '10px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Version</th>
              <th style={{ textAlign: 'left', padding: '10px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Status</th>
              <th style={{ textAlign: 'left', padding: '10px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Origin</th>
              <th style={{ textAlign: 'right', padding: '10px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Purity</th>
              <th style={{ textAlign: 'left', padding: '10px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Registry Source</th>
            </tr>
          </thead>
          <tbody>
            {MOCK_ASSEMBLIES.map((item) => (
              <tr key={item.id} style={{ borderBottom: `1px solid ${t.color.borderSubtle}` }}>
                <td style={{ padding: '10px 14px', color: t.color.fgPrimary, fontWeight: Number(t.font.weightMedium) }}>{item.name}</td>
                <td style={{ padding: '10px 14px', color: t.color.fgSecondary, fontFamily: t.font.familyMono }}>{item.version}</td>
                <td style={{ padding: '10px 14px' }}>
                  <span style={{
                    display: 'inline-flex', alignItems: 'center', gap: '5px',
                    padding: '2px 8px', borderRadius: '10px',
                    background: (statusColors[item.status] || t.color.fgMuted) + '18',
                    color: statusColors[item.status] || t.color.fgMuted,
                    fontSize: '11px', fontWeight: Number(t.font.weightSemibold),
                  }}>
                    <span style={{ width: 5, height: 5, borderRadius: '50%', background: 'currentColor' }} />
                    {item.status}
                  </span>
                </td>
                <td style={{ padding: '10px 14px', color: t.color.fgSecondary, fontSize: '11px' }}>{item.origin}</td>
                <td style={{ padding: '10px 14px', textAlign: 'right', color: item.purity >= 1.0 ? t.color.success : t.color.warning, fontFamily: t.font.familyMono }}>
                  {(item.purity * 100).toFixed(0)}%
                </td>
                <td style={{ padding: '10px 14px', color: t.color.fgMuted, fontSize: '11px' }}>{item.registrySource}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
