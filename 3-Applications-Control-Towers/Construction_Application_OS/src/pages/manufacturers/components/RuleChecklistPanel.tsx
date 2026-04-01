/**
 * Manufacturer Hub — Rule Checklist Panel (SYSTEM mode)
 * Shows known and deferred rules honestly.
 * Rules with materialized=false are clearly labeled as not yet materialized.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { RuleSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface RuleChecklistPanelProps {
  rules: RuleSummary[];
  surface: Record<string, string>;
}

export function RuleChecklistPanel({ rules, surface }: RuleChecklistPanelProps) {
  if (rules.length === 0) return null;

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
        Rule Checklist
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
        {rules.map(rule => (
          <div key={rule.id} style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '12px',
            padding: '10px 14px',
            background: surface.bgElevated,
            borderRadius: t.radius.md,
          }}>
            {/* Rule status indicator */}
            <div style={{
              width: '20px',
              height: '20px',
              borderRadius: t.radius.sm,
              border: `2px solid ${rule.materialized ? '#22c55e' : '#eab308'}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              marginTop: '2px',
              fontSize: '12px',
              color: rule.materialized ? '#22c55e' : '#eab308',
            }}>
              {rule.materialized ? '\u2713' : '\u25CB'}
            </div>

            <div style={{ flex: 1 }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}>
                <span style={{
                  fontSize: t.font.sizeSm,
                  fontWeight: Number(t.font.weightSemibold),
                  color: surface.fg,
                }}>
                  {rule.name}
                </span>
                {!rule.materialized && (
                  <span style={{
                    padding: '1px 6px',
                    borderRadius: t.radius.sm,
                    fontSize: '9px',
                    color: '#eab308',
                    background: 'rgba(234, 179, 8, 0.12)',
                    fontWeight: Number(t.font.weightSemibold),
                    letterSpacing: '0.04em',
                    textTransform: 'uppercase',
                  }}>
                    Not Materialized
                  </span>
                )}
              </div>
              <div style={{
                fontSize: t.font.sizeXs,
                color: surface.fgSecondary,
                marginTop: '4px',
                lineHeight: t.font.lineNormal,
              }}>
                {rule.description}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div style={{
        marginTop: '12px',
        fontSize: '10px',
        color: surface.fgMuted,
        fontStyle: 'italic',
      }}>
        Structured rule files not yet materialized — inferred from current records and projection logic
      </div>
    </div>
  );
}
