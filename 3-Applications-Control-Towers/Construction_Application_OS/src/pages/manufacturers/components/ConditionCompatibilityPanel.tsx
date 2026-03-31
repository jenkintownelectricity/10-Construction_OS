/**
 * Manufacturer Hub — Condition Compatibility Panel (SYSTEM mode)
 * Shows grounded conditions only as tags/cards.
 * No invented conditions beyond what is grounded in current records.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { ConditionSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface ConditionCompatibilityPanelProps {
  conditions: ConditionSummary[];
  surface: Record<string, string>;
}

const CONDITION_TYPE_COLORS: Record<string, string> = {
  'application-condition': '#3b82f6',
  'detail-condition': '#a855f7',
};

export function ConditionCompatibilityPanel({ conditions, surface }: ConditionCompatibilityPanelProps) {
  if (conditions.length === 0) return null;

  const grouped = conditions.reduce<Record<string, ConditionSummary[]>>((acc, cond) => {
    const key = cond.conditionType;
    if (!acc[key]) acc[key] = [];
    acc[key].push(cond);
    return acc;
  }, {});

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
        Condition Compatibility
      </div>

      {Object.entries(grouped).map(([type, conds]) => {
        const color = CONDITION_TYPE_COLORS[type] || surface.accent;

        return (
          <div key={type} style={{ marginBottom: '12px' }}>
            <div style={{
              fontSize: '10px',
              color: surface.fgMuted,
              marginBottom: '8px',
              textTransform: 'uppercase',
              letterSpacing: '0.06em',
            }}>
              {type.replace(/-/g, ' ')}
            </div>
            <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
              {conds.map(cond => (
                <div key={cond.id} style={{
                  padding: '8px 14px',
                  background: surface.bgElevated,
                  borderRadius: t.radius.md,
                  borderLeft: `3px solid ${color}`,
                  fontSize: t.font.sizeXs,
                  fontWeight: Number(t.font.weightMedium),
                  color: surface.fg,
                }}>
                  {cond.name}
                </div>
              ))}
            </div>
          </div>
        );
      })}

      <div style={{
        marginTop: '8px',
        fontSize: '10px',
        color: surface.fgMuted,
        fontStyle: 'italic',
      }}>
        Grounded conditions only — no invented compatibility claims
      </div>
    </div>
  );
}
