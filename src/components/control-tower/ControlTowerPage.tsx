/**
 * Construction OS — Control Tower Page
 * Primary control tower view consuming the shared design-token system.
 *
 * Token source: src/ui/theme/tokens.ts
 * Spacing: tokens.spacing (governed named steps)
 * Typography: tokens.font (line heights via lineNormal / lineTight)
 */

import { tokens } from '../../ui/theme/tokens';

const t = tokens;

export function ControlTowerPage() {
  return (
    <div
      style={{
        padding: t.spacing.lg,
        fontFamily: t.font.family,
        color: t.color.fgPrimary,
        lineHeight: t.font.lineNormal,
      }}
    >
      {/* Page header */}
      <header
        style={{
          marginBottom: t.spacing.xl,
        }}
      >
        <h1
          style={{
            fontSize: t.font.sizeXl,
            fontWeight: Number(t.font.weightBold),
            lineHeight: t.font.lineTight,
            margin: 0,
          }}
        >
          Control Tower
        </h1>
        <p
          style={{
            fontSize: t.font.sizeSm,
            color: t.color.fgSecondary,
            marginTop: t.spacing.xs,
          }}
        >
          System overview and operational command surface
        </p>
      </header>

      {/* Status strip */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: t.spacing.md,
          padding: `${t.spacing.sm} ${t.spacing.lg}`,
          background: t.color.bgSurface,
          borderRadius: t.radius.md,
          border: `1px solid ${t.color.border}`,
          marginBottom: t.spacing.xl,
          fontSize: t.font.sizeXs,
        }}
      >
        <span style={{ color: t.color.fgMuted }}>STATUS</span>
        <span style={{ display: 'flex', alignItems: 'center', gap: t.spacing.xs }}>
          <span
            style={{
              width: 8,
              height: 8,
              borderRadius: '50%',
              background: t.color.success,
              display: 'inline-block',
            }}
          />
          <span style={{ color: t.color.success, fontWeight: Number(t.font.weightSemibold) }}>
            NOMINAL
          </span>
        </span>
      </div>

      {/* Panel grid */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
          gap: t.spacing.lg,
        }}
      >
        {(['Runtime', 'Registry', 'Governance', 'Kernel'] as const).map((label) => (
          <div
            key={label}
            style={{
              background: t.color.bgSurface,
              border: `1px solid ${t.color.border}`,
              borderRadius: t.radius.md,
              padding: t.spacing.lg,
            }}
          >
            <h2
              style={{
                fontSize: t.font.sizeMd,
                fontWeight: Number(t.font.weightSemibold),
                lineHeight: t.font.lineTight,
                margin: 0,
                marginBottom: t.spacing.sm,
              }}
            >
              {label}
            </h2>
            <p
              style={{
                fontSize: t.font.sizeSm,
                color: t.color.fgSecondary,
                lineHeight: t.font.lineNormal,
                margin: 0,
              }}
            >
              Subsystem telemetry panel
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
