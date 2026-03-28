/**
 * Construction OS — Control Tower Dashboard
 * Wave C1 — Deterministic metrics from frozen mock data.
 */

import { tokens } from '../../ui/theme/tokens';
import { DASHBOARD_METRICS, GOVERNED_OPERATIONS, PRIMITIVE_SUMMARY } from '../../mock/primitives/mockDashboard';

const t = tokens;

const statusColors: Record<string, string> = {
  NOMINAL: t.color.success,
  WARNING: t.color.warning,
  CRITICAL: t.color.error,
  OFFLINE: t.color.fgMuted,
};

const opStatusColors: Record<string, string> = {
  SUCCESS: t.color.success,
  FAILED: t.color.error,
  PENDING: t.color.warning,
};

export function ConstructionDashboard() {
  return (
    <div>
      {/* Header */}
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0, color: t.color.fgPrimary }}>
          Construction Control Tower
        </h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Wave C1 — System overview and operational status
        </p>
      </div>

      {/* Status Strip */}
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
        <span style={{ color: t.color.fgMuted }}>STATUS</span>
        <span style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: t.color.success, display: 'inline-block' }} />
          <span style={{ color: t.color.success, fontWeight: Number(t.font.weightSemibold) }}>ALL SYSTEMS NOMINAL</span>
        </span>
        <span style={{ color: t.color.fgMuted, marginLeft: 'auto' }}>Wave C1 — Surface Only</span>
      </div>

      {/* Metrics Grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(4, 1fr)',
          gap: '12px',
          marginBottom: '24px',
        }}
      >
        {DASHBOARD_METRICS.map((metric) => (
          <div
            key={metric.label}
            style={{
              background: t.color.bgSurface,
              border: `1px solid ${t.color.border}`,
              borderRadius: t.radius.md,
              padding: '16px',
            }}
          >
            <div style={{ fontSize: t.font.sizeXs, color: t.color.fgSecondary, marginBottom: '6px' }}>
              {metric.label}
            </div>
            <div style={{ fontSize: t.font.sizeLg, fontWeight: Number(t.font.weightBold), color: t.color.fgPrimary }}>
              {metric.value}
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginTop: '4px' }}>
              <span
                style={{
                  width: 6,
                  height: 6,
                  borderRadius: '50%',
                  background: statusColors[metric.status] || t.color.fgMuted,
                  display: 'inline-block',
                }}
              />
              <span style={{ fontSize: '11px', color: statusColors[metric.status] || t.color.fgMuted }}>
                {metric.status}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Two-column layout */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
        {/* Governed Operations */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '20px',
          }}
        >
          <h2 style={{ fontSize: t.font.sizeMd, fontWeight: Number(t.font.weightSemibold), margin: '0 0 16px 0', color: t.color.fgPrimary }}>
            Recent Governed Operations
          </h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
            {GOVERNED_OPERATIONS.map((op) => (
              <div
                key={op.id}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  padding: '8px 10px',
                  background: t.color.bgElevated,
                  borderRadius: t.radius.sm,
                  fontSize: t.font.sizeXs,
                }}
              >
                <span
                  style={{
                    width: 6,
                    height: 6,
                    borderRadius: '50%',
                    background: opStatusColors[op.status],
                    flexShrink: 0,
                  }}
                />
                <span style={{ flex: 1, color: t.color.fgPrimary }}>{op.operation}</span>
                <span style={{ color: t.color.fgMuted, fontSize: '11px', flexShrink: 0 }}>
                  {op.timestamp.split('T')[0]}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Primitive Summary */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '20px',
          }}
        >
          <h2 style={{ fontSize: t.font.sizeMd, fontWeight: Number(t.font.weightSemibold), margin: '0 0 16px 0', color: t.color.fgPrimary }}>
            Construction Primitive Summary
          </h2>
          <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: t.font.sizeXs }}>
            <thead>
              <tr style={{ borderBottom: `1px solid ${t.color.border}` }}>
                <th style={{ textAlign: 'left', padding: '6px 8px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Type</th>
                <th style={{ textAlign: 'right', padding: '6px 8px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Total</th>
                <th style={{ textAlign: 'right', padding: '6px 8px', color: t.color.success, fontWeight: Number(t.font.weightMedium) }}>Canonical</th>
                <th style={{ textAlign: 'right', padding: '6px 8px', color: t.color.warning, fontWeight: Number(t.font.weightMedium) }}>Draft</th>
                <th style={{ textAlign: 'right', padding: '6px 8px', color: t.color.fgMuted, fontWeight: Number(t.font.weightMedium) }}>Deprecated</th>
              </tr>
            </thead>
            <tbody>
              {PRIMITIVE_SUMMARY.map((row) => (
                <tr key={row.type} style={{ borderBottom: `1px solid ${t.color.borderSubtle}` }}>
                  <td style={{ padding: '8px', color: t.color.fgPrimary, fontWeight: Number(t.font.weightMedium) }}>{row.type}</td>
                  <td style={{ padding: '8px', textAlign: 'right', color: t.color.fgPrimary }}>{row.total}</td>
                  <td style={{ padding: '8px', textAlign: 'right', color: t.color.success }}>{row.canonical}</td>
                  <td style={{ padding: '8px', textAlign: 'right', color: t.color.warning }}>{row.draft}</td>
                  <td style={{ padding: '8px', textAlign: 'right', color: t.color.fgMuted }}>{row.deprecated}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
