/**
 * Manufacturer Hub — Product Stack Panel (SYSTEM mode)
 * Dark control-tower visualization of ordered product layer stack.
 *
 * Barrett HyppoCoat Trafficable example stack:
 * HyppoCoat PC (primer) -> HyppoCoat BC (base) -> HyppoCoat 100 (membrane) -> HyppoCoat TC (top)
 */

import { tokens } from '../../../ui/theme/tokens';
import type { ProductSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface ProductStackPanelProps {
  products: ProductSummary[];
  surface: Record<string, string>;
}

const ROLE_COLORS: Record<string, string> = {
  'primer-coat': '#a855f7',
  'base-coat': '#3b82f6',
  'base-membrane': '#22c55e',
  'top-coat': '#eab308',
  'grout-coat': '#f97316',
  'flashing-membrane': '#ef4444',
};

export function ProductStackPanel({ products, surface }: ProductStackPanelProps) {
  if (products.length === 0) return null;

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
          Product Stack
        </div>
        <span style={{
          fontSize: '10px',
          color: surface.fgMuted,
        }}>
          {products.length} layers
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
        {products.map((product, index) => {
          const roleColor = ROLE_COLORS[product.role] || surface.accent;
          const isFirst = index === 0;
          const isLast = index === products.length - 1;

          return (
            <div key={product.id} style={{ display: 'flex', alignItems: 'stretch', gap: '12px' }}>
              {/* Stack connector line */}
              <div style={{
                width: '24px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                position: 'relative',
              }}>
                {!isFirst && (
                  <div style={{
                    position: 'absolute',
                    top: 0,
                    width: '2px',
                    height: '50%',
                    background: surface.border,
                  }} />
                )}
                <div style={{
                  width: '10px',
                  height: '10px',
                  borderRadius: '50%',
                  background: roleColor,
                  border: `2px solid ${surface.bgPanel}`,
                  flexShrink: 0,
                  alignSelf: 'center',
                  zIndex: 1,
                  marginTop: 'auto',
                  marginBottom: 'auto',
                }} />
                {!isLast && (
                  <div style={{
                    position: 'absolute',
                    bottom: 0,
                    width: '2px',
                    height: '50%',
                    background: surface.border,
                  }} />
                )}
              </div>

              {/* Layer card */}
              <div style={{
                flex: 1,
                padding: '10px 14px',
                background: surface.bgElevated,
                borderRadius: t.radius.md,
                borderLeft: `3px solid ${roleColor}`,
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}>
                <div>
                  <div style={{
                    fontSize: t.font.sizeSm,
                    fontWeight: Number(t.font.weightSemibold),
                    color: surface.fg,
                  }}>
                    {product.name}
                  </div>
                  <div style={{
                    fontSize: t.font.sizeXs,
                    color: surface.fgSecondary,
                    marginTop: '2px',
                  }}>
                    {product.description}
                  </div>
                </div>
                <span style={{
                  padding: '2px 8px',
                  borderRadius: t.radius.sm,
                  fontSize: '10px',
                  color: roleColor,
                  background: `${roleColor}18`,
                  fontFamily: t.font.familyMono,
                  flexShrink: 0,
                  marginLeft: '8px',
                }}>
                  {product.role}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {/* Stack flow arrow */}
      <div style={{
        marginTop: '12px',
        padding: '8px 12px',
        background: surface.bgElevated,
        borderRadius: t.radius.sm,
        textAlign: 'center',
        fontSize: t.font.sizeXs,
        color: surface.fgMuted,
        fontFamily: t.font.familyMono,
      }}>
        {products.map(p => p.name.replace(/^Barrett\s+/i, '')).join(' \u2192 ')}
      </div>
    </div>
  );
}
