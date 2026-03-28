/**
 * Construction OS — Receipts Page
 * Wave C1 — Deterministic receipt entries from frozen mock data.
 */

import { useState } from 'react';
import { tokens } from '../../ui/theme/tokens';
import { MOCK_RECEIPTS, type ReceiptCategory } from '../../mock/primitives/mockReceipts';

const t = tokens;

const categoryColors: Record<ReceiptCategory, string> = {
  EXECUTION: t.color.accentPrimary,
  SIGNAL: t.color.compare,
  REGISTRY: t.color.warning,
  RUNTIME: t.color.success,
};

const statusColors: Record<string, string> = {
  SUCCESS: t.color.success,
  FAILED: t.color.error,
  PENDING: t.color.warning,
};

const ALL_CATEGORIES: (ReceiptCategory | 'ALL')[] = ['ALL', 'EXECUTION', 'SIGNAL', 'REGISTRY', 'RUNTIME'];

export function ReceiptsPage() {
  const [filter, setFilter] = useState<ReceiptCategory | 'ALL'>('ALL');

  const filtered = filter === 'ALL' ? MOCK_RECEIPTS : MOCK_RECEIPTS.filter((r) => r.category === filter);

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Receipts</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Immutable operation receipts — execution, signal, registry, and runtime
        </p>
      </div>

      {/* Category filter */}
      <div
        style={{
          display: 'flex',
          gap: '6px',
          marginBottom: '16px',
        }}
      >
        {ALL_CATEGORIES.map((cat) => {
          const isActive = filter === cat;
          const color = cat === 'ALL' ? t.color.fgPrimary : categoryColors[cat as ReceiptCategory];
          return (
            <button
              key={cat}
              onClick={() => setFilter(cat)}
              style={{
                padding: '5px 14px',
                borderRadius: '12px',
                border: `1px solid ${isActive ? color : t.color.border}`,
                background: isActive ? color + '22' : 'transparent',
                color: isActive ? color : t.color.fgSecondary,
                cursor: 'pointer',
                fontSize: '11px',
                fontWeight: isActive ? Number(t.font.weightSemibold) : Number(t.font.weightMedium),
                fontFamily: t.font.family,
              }}
            >
              {cat}
            </button>
          );
        })}
      </div>

      {/* Receipt table */}
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
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>ID</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Category</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Operation</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Status</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Detail</th>
              <th style={{ textAlign: 'left', padding: '8px 14px', color: t.color.fgSecondary, fontWeight: Number(t.font.weightMedium) }}>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((receipt) => (
              <tr key={receipt.id} style={{ borderBottom: `1px solid ${t.color.borderSubtle}` }}>
                <td style={{ padding: '8px 14px', color: t.color.fgMuted, fontFamily: t.font.familyMono }}>{receipt.id}</td>
                <td style={{ padding: '8px 14px' }}>
                  <span
                    style={{
                      fontSize: '10px',
                      padding: '2px 7px',
                      borderRadius: '8px',
                      background: categoryColors[receipt.category] + '22',
                      color: categoryColors[receipt.category],
                      fontWeight: Number(t.font.weightSemibold),
                    }}
                  >
                    {receipt.category}
                  </span>
                </td>
                <td style={{ padding: '8px 14px', color: t.color.fgPrimary, fontWeight: Number(t.font.weightMedium) }}>{receipt.operation}</td>
                <td style={{ padding: '8px 14px' }}>
                  <span style={{ color: statusColors[receipt.status], fontWeight: Number(t.font.weightMedium) }}>
                    {receipt.status}
                  </span>
                </td>
                <td style={{ padding: '8px 14px', color: t.color.fgSecondary, maxWidth: '300px' }}>{receipt.detail}</td>
                <td style={{ padding: '8px 14px', color: t.color.fgMuted, fontSize: '11px', whiteSpace: 'nowrap' }}>
                  {receipt.timestamp.replace('T', ' ').split('.')[0]}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
