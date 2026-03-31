/**
 * Manufacturer Hub — Certification Panel (SYSTEM mode)
 * Dark control-tower display of certification status badges.
 * Observer-derived status only — no engine-executed truth.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { CertificationSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface CertificationPanelProps {
  certifications: CertificationSummary[];
  surface: Record<string, string>;
}

const STATUS_VISUAL: Record<string, { color: string; label: string }> = {
  certified: { color: '#22c55e', label: 'CERTIFIED' },
  unverified: { color: '#8b93a8', label: 'UNVERIFIED' },
  partial: { color: '#eab308', label: 'PARTIAL' },
  blocked: { color: '#ef4444', label: 'BLOCKED' },
};

export function CertificationPanel({ certifications, surface }: CertificationPanelProps) {
  if (certifications.length === 0) return null;

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
        Certifications
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
        {certifications.map(cert => {
          const visual = STATUS_VISUAL[cert.status] || STATUS_VISUAL.unverified;

          return (
            <div key={cert.id} style={{
              padding: '14px 16px',
              background: surface.bgElevated,
              borderRadius: t.radius.md,
              borderLeft: `3px solid ${visual.color}`,
            }}>
              <div style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                marginBottom: '8px',
              }}>
                <span style={{
                  fontSize: t.font.sizeSm,
                  fontWeight: Number(t.font.weightSemibold),
                  color: surface.fg,
                }}>
                  {cert.name}
                </span>
                <span style={{
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '4px',
                  padding: '2px 8px',
                  borderRadius: t.radius.sm,
                  fontSize: '10px',
                  fontWeight: Number(t.font.weightSemibold),
                  color: visual.color,
                  background: `${visual.color}18`,
                  letterSpacing: '0.06em',
                }}>
                  <span style={{
                    width: 6, height: 6, borderRadius: '50%', background: visual.color,
                  }} />
                  {visual.label}
                </span>
              </div>
              <div style={{
                fontSize: t.font.sizeXs,
                color: surface.fgSecondary,
                lineHeight: t.font.lineNormal,
              }}>
                {cert.requirementSummary}
              </div>
            </div>
          );
        })}
      </div>

      <div style={{
        marginTop: '12px',
        fontSize: '10px',
        color: surface.fgMuted,
        fontStyle: 'italic',
      }}>
        Observer-derived certification status — not engine-executed
      </div>
    </div>
  );
}
