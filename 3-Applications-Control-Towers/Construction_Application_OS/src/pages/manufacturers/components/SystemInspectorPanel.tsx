/**
 * Manufacturer Hub — System Inspector Panel (SYSTEM mode)
 * Dark control-tower visualization of selected system details.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { SystemSummary, ManufacturerSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface SystemInspectorPanelProps {
  system: SystemSummary;
  manufacturer: ManufacturerSummary;
  surface: Record<string, string>;
}

export function SystemInspectorPanel({ system, manufacturer, surface }: SystemInspectorPanelProps) {
  const fields = [
    { label: 'System Name', value: system.name },
    { label: 'Manufacturer', value: manufacturer.name },
    { label: 'System Type', value: system.systemType },
    { label: 'Products', value: `${system.productIds.length} components` },
    { label: 'Certifications', value: `${system.certificationIds.length} tracked` },
    { label: 'Conditions', value: `${system.conditionIds.length} grounded` },
    { label: 'Seeded Truth Status', value: manufacturer.seedStatus === 'seeded' ? 'Fully Seeded' : 'Scaffold Only' },
  ];

  return (
    <div style={{
      padding: '20px',
      background: surface.bgPanel,
      border: `1px solid ${surface.border}`,
      borderRadius: t.radius.lg,
    }}>
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '16px',
      }}>
        <div style={{
          fontSize: '10px',
          fontWeight: Number(t.font.weightSemibold),
          color: surface.fgMuted,
          textTransform: 'uppercase',
          letterSpacing: '0.08em',
        }}>
          System Inspector
        </div>
        <span style={{
          padding: '2px 8px',
          borderRadius: t.radius.sm,
          fontSize: '10px',
          color: surface.accent,
          background: surface.accentMuted,
          fontFamily: t.font.familyMono,
        }}>
          INSPECT
        </span>
      </div>

      <div style={{
        fontSize: t.font.sizeMd,
        fontWeight: Number(t.font.weightBold),
        color: surface.fg,
        marginBottom: '16px',
      }}>
        {system.name}
      </div>

      <div style={{
        fontSize: t.font.sizeXs,
        color: surface.fgSecondary,
        marginBottom: '16px',
        lineHeight: t.font.lineNormal,
      }}>
        {system.description}
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {fields.map(field => (
          <div key={field.label} style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            padding: '8px 12px',
            background: surface.bgElevated,
            borderRadius: t.radius.sm,
          }}>
            <span style={{
              fontSize: t.font.sizeXs,
              color: surface.fgMuted,
              fontWeight: Number(t.font.weightMedium),
            }}>
              {field.label}
            </span>
            <span style={{
              fontSize: t.font.sizeXs,
              color: surface.fg,
              fontFamily: t.font.familyMono,
            }}>
              {field.value}
            </span>
          </div>
        ))}
      </div>

      <div style={{
        marginTop: '12px',
        fontSize: '10px',
        color: surface.fgMuted,
        fontStyle: 'italic',
      }}>
        Observer-derived system inspection — not engine-executed truth
      </div>
    </div>
  );
}
