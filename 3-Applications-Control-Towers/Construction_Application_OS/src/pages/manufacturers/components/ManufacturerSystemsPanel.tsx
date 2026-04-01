/**
 * Manufacturer Hub — Systems Panel (WORK mode)
 * Office-style system list with certification badge summary.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { SystemSummary, CertificationSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface ManufacturerSystemsPanelProps {
  systems: SystemSummary[];
  certifications: CertificationSummary[];
  selectedSystemId: string | null;
  onSelectSystem: (id: string) => void;
  surface: Record<string, string>;
}

const STATUS_COLORS: Record<string, string> = {
  certified: '#22c55e',
  unverified: '#8b93a8',
  partial: '#eab308',
  blocked: '#ef4444',
};

export function ManufacturerSystemsPanel({
  systems, certifications, selectedSystemId, onSelectSystem, surface,
}: ManufacturerSystemsPanelProps) {
  if (systems.length === 0) return null;

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
        Systems
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {systems.map(system => {
          const isSelected = system.id === selectedSystemId;
          const sysCerts = certifications.filter(c => c.systemId === system.id);

          return (
            <button
              key={system.id}
              onClick={() => onSelectSystem(system.id)}
              style={{
                display: 'flex',
                flexDirection: 'column',
                gap: '8px',
                width: '100%',
                padding: '14px 16px',
                background: isSelected ? surface.bgHover : surface.bgElevated,
                borderRadius: t.radius.md,
                border: isSelected ? `1px solid ${surface.accent}` : `1px solid ${surface.border}`,
                cursor: 'pointer',
                textAlign: 'left',
                fontFamily: t.font.family,
                transition: `all ${t.transition.fast}`,
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{
                  fontSize: t.font.sizeSm,
                  fontWeight: Number(t.font.weightSemibold),
                  color: surface.fg,
                }}>
                  {system.name}
                </div>
                <span style={{
                  padding: '2px 8px',
                  borderRadius: t.radius.sm,
                  fontSize: '10px',
                  color: surface.fgSecondary,
                  background: surface.border,
                  fontFamily: t.font.familyMono,
                }}>
                  {system.systemType}
                </span>
              </div>
              <div style={{
                fontSize: t.font.sizeXs,
                color: surface.fgSecondary,
              }}>
                {system.description}
              </div>
              {sysCerts.length > 0 && (
                <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
                  {sysCerts.map(cert => (
                    <span
                      key={cert.id}
                      style={{
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        padding: '2px 8px',
                        borderRadius: t.radius.sm,
                        fontSize: '10px',
                        color: STATUS_COLORS[cert.status],
                        background: `${STATUS_COLORS[cert.status]}18`,
                      }}
                    >
                      <span style={{
                        width: 5, height: 5, borderRadius: '50%',
                        background: STATUS_COLORS[cert.status],
                      }} />
                      {cert.name}
                    </span>
                  ))}
                </div>
              )}
            </button>
          );
        })}
      </div>
    </div>
  );
}
