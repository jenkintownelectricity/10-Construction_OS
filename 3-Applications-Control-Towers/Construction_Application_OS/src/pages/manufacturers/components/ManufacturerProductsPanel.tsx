/**
 * Manufacturer Hub — Products Panel (WORK mode)
 * Office-style product list with type and role information.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { ProductSummary } from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface ManufacturerProductsPanelProps {
  products: ProductSummary[];
  surface: Record<string, string>;
}

export function ManufacturerProductsPanel({ products, surface }: ManufacturerProductsPanelProps) {
  if (products.length === 0) return null;

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
        Products
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {products.map(product => (
          <div
            key={product.id}
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              padding: '12px 16px',
              background: surface.bgElevated,
              borderRadius: t.radius.md,
              border: `1px solid ${surface.border}`,
            }}
          >
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
            <div style={{ display: 'flex', gap: '8px', flexShrink: 0 }}>
              <span style={{
                padding: '2px 8px',
                borderRadius: t.radius.sm,
                fontSize: '10px',
                color: surface.fgSecondary,
                background: surface.border,
                fontFamily: t.font.familyMono,
              }}>
                {product.type}
              </span>
              <span style={{
                padding: '2px 8px',
                borderRadius: t.radius.sm,
                fontSize: '10px',
                color: surface.accent,
                background: surface.accentMuted,
                fontFamily: t.font.familyMono,
              }}>
                {product.role}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
