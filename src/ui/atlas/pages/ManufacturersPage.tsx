/**
 * Construction Atlas — Manufacturers Page
 *
 * Manufacturer cards with detail/product counts + detail library table.
 */

import { DEFAULT_BRANDING } from '../../../lib/branding/branding-types';

const c = DEFAULT_BRANDING.colors;

const cardStyle: React.CSSProperties = {
  background: '#ffffff',
  border: `1px solid ${c.border}`,
  borderRadius: '8px',
  padding: '16px',
};

const MANUFACTURERS = [
  { name: 'Sika Corporation', category: 'Waterproofing & Sealants', status: 'Active', details: 34, products: 18 },
  { name: 'Carlisle SynTec', category: 'Roofing Membranes', status: 'Active', details: 28, products: 12 },
  { name: 'Tremco', category: 'Sealants & Coatings', status: 'Active', details: 22, products: 15 },
  { name: 'YKK AP', category: 'Curtain Wall Systems', status: 'Active', details: 19, products: 8 },
  { name: 'Henry Company', category: 'Building Envelope', status: 'Active', details: 16, products: 11 },
  { name: 'W.R. Grace', category: 'Waterproofing', status: 'Inactive', details: 14, products: 9 },
  { name: 'Georgia-Pacific', category: 'Sheathing & Barriers', status: 'Active', details: 12, products: 7 },
  { name: 'Firestone Building Products', category: 'Roofing Systems', status: 'Active', details: 21, products: 10 },
];

const DETAIL_LIBRARY = [
  { manufacturer: 'Sika Corporation', detail: 'SikaProof A+ Below-Grade Waterproofing', system: 'Below Grade', type: 'Installation Guide' },
  { manufacturer: 'Sika Corporation', detail: 'Sikaflex-15 LM Joint Sealant', system: 'Sealants', type: 'Technical Data' },
  { manufacturer: 'Carlisle SynTec', detail: 'Sure-Weld TPO Membrane', system: 'Roofing', type: 'Installation Guide' },
  { manufacturer: 'Carlisle SynTec', detail: 'Carlisle FleeceBACK Securement', system: 'Roofing', type: 'Detail Drawing' },
  { manufacturer: 'YKK AP', detail: 'YCW 750 OG Curtain Wall', system: 'Fenestration', type: 'Shop Drawing Reference' },
  { manufacturer: 'Tremco', detail: 'Spectrem 1 Silicone Sealant', system: 'Sealants', type: 'Technical Data' },
];

const SYSTEM_COLORS: Record<string, { bg: string; fg: string }> = {
  'Below Grade': { bg: '#fef3c7', fg: '#92400e' },
  Sealants: { bg: '#e0e7ff', fg: '#3730a3' },
  Roofing: { bg: '#dcfce7', fg: '#166534' },
  Fenestration: { bg: '#dbeafe', fg: '#1e40af' },
};

export function ManufacturersPage() {
  return (
    <div>
      <h1 style={{ fontSize: '24px', fontWeight: 700, color: c.text, margin: 0 }}>Manufacturers</h1>
      <p style={{ color: c.textMuted, margin: '4px 0 24px', fontSize: '14px' }}>Manufacturer detail library and product references</p>

      {/* Manufacturer cards */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px', marginBottom: '32px' }}>
        {MANUFACTURERS.map((mfr) => (
          <div key={mfr.name} style={cardStyle}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
              <span style={{ fontWeight: 600, fontSize: '14px', color: c.text }}>{mfr.name}</span>
              <span style={{
                padding: '2px 8px', borderRadius: '10px', fontSize: '10px', fontWeight: 600,
                background: mfr.status === 'Active' ? '#dcfce7' : '#f1f5f9',
                color: mfr.status === 'Active' ? '#166534' : '#475569',
              }}>
                {mfr.status}
              </span>
            </div>
            <div style={{ fontSize: '12px', color: c.textMuted, marginBottom: '8px' }}>{mfr.category}</div>
            <div style={{ fontSize: '12px', color: c.textMuted }}>
              {mfr.details} details \u00B7 {mfr.products} products
            </div>
          </div>
        ))}
      </div>

      {/* Detail Library table */}
      <div style={{ ...cardStyle, padding: '20px' }}>
        <h2 style={{ fontSize: '18px', fontWeight: 600, color: c.text, margin: '0 0 16px' }}>Detail Library</h2>
        <div style={{ display: 'flex', padding: '8px 0', borderBottom: `1px solid ${c.border}`, fontWeight: 600, fontSize: '12px', color: c.textMuted }}>
          <div style={{ flex: 2 }}>Manufacturer</div>
          <div style={{ flex: 4 }}>Detail</div>
          <div style={{ flex: 1.5 }}>System</div>
          <div style={{ flex: 2 }}>Type</div>
        </div>
        {DETAIL_LIBRARY.map((item, i) => {
          const sc = SYSTEM_COLORS[item.system];
          return (
            <div key={i} style={{ display: 'flex', alignItems: 'center', padding: '10px 0', borderBottom: `1px solid ${c.border}`, fontSize: '13px' }}>
              <div style={{ flex: 2, fontWeight: 500, color: c.text }}>{item.manufacturer}</div>
              <div style={{ flex: 4, color: c.text }}>{item.detail}</div>
              <div style={{ flex: 1.5 }}>
                {sc ? (
                  <span style={{ padding: '2px 8px', borderRadius: '10px', fontSize: '11px', fontWeight: 600, background: sc.bg, color: sc.fg }}>
                    {item.system}
                  </span>
                ) : item.system}
              </div>
              <div style={{ flex: 2, color: c.textMuted }}>{item.type}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
