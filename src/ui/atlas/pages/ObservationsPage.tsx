/**
 * Construction Atlas — Observations Page
 *
 * Field observation feed and severity tracking.
 */

import { DEFAULT_BRANDING } from '../../../lib/branding/branding-types';

const c = DEFAULT_BRANDING.colors;

const cardStyle: React.CSSProperties = {
  background: '#ffffff',
  border: `1px solid ${c.border}`,
  borderRadius: '8px',
  padding: '20px',
  marginBottom: '12px',
};

const STATUS_COLORS: Record<string, { bg: string; fg: string }> = {
  Open: { bg: '#dcfce7', fg: '#166534' },
  'In Review': { bg: '#fef9c3', fg: '#854d0e' },
  Resolved: { bg: '#e0e7ff', fg: '#3730a3' },
};

const SEVERITY_COLORS: Record<string, { bg: string; fg: string }> = {
  High: { bg: '#fecaca', fg: '#991b1b' },
  Medium: { bg: '#fef9c3', fg: '#854d0e' },
  Low: { bg: '#dbeafe', fg: '#1e40af' },
};

const OBSERVATIONS = [
  { id: 'OBS-0147', title: 'Flashing at parapet intersection', project: 'Heritage Plaza Renovation', author: 'Sarah Chen', date: '2026-03-20', status: 'Open', severity: 'High', desc: 'Membrane lap is only 2 inches at intersection. Code requires 4 inches minimum. Ponding water observed at low point.' },
  { id: 'OBS-0146', title: 'Sealant joint at curtain wall', project: 'Waterfront Tower Phase 2', author: 'Michael Torres', date: '2026-03-20', status: 'Open', severity: 'Medium', desc: 'Joint width exceeds manufacturer maximum. Sealant shows early signs of adhesion loss at south elevation.' },
  { id: 'OBS-0145', title: 'Roof membrane termination', project: 'Metro Station Canopy', author: 'Rachel Kim', date: '2026-03-19', status: 'Resolved', severity: 'Low', desc: 'Termination bar secured correctly. Minor aesthetic issue with exposed fastener heads.' },
  { id: 'OBS-0144', title: 'Window head flashing continuity', project: 'Heritage Plaza Renovation', author: 'Sarah Chen', date: '2026-03-19', status: 'Open', severity: 'High', desc: 'Head flashing discontinuous at mullion. No end dam installed at left jamb transition.' },
  { id: 'OBS-0143', title: 'Below-grade waterproofing overlap', project: 'Airport Terminal B Extension', author: 'James Park', date: '2026-03-18', status: 'In Review', severity: 'Medium', desc: 'Overlap meets minimum requirement but alignment is inconsistent. Protection board not yet installed.' },
  { id: 'OBS-0142', title: 'Expansion joint cover alignment', project: 'Civic Center Library Wing', author: 'Lisa Wang', date: '2026-03-18', status: 'Resolved', severity: 'Low', desc: 'Cover plate re-aligned after initial installation. Now meets tolerance requirements.' },
];

export function ObservationsPage() {
  const highCount = OBSERVATIONS.filter((o) => o.severity === 'High').length;
  const medCount = OBSERVATIONS.filter((o) => o.severity === 'Medium').length;
  const lowCount = OBSERVATIONS.filter((o) => o.severity === 'Low').length;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <h1 style={{ fontSize: '24px', fontWeight: 700, color: c.text, margin: 0 }}>Observations</h1>
          <p style={{ color: c.textMuted, margin: '4px 0 24px', fontSize: '14px' }}>Field observation feed and severity tracking</p>
        </div>
        <div style={{ display: 'flex', gap: '16px', textAlign: 'center' }}>
          <div><div style={{ fontSize: '24px', fontWeight: 700, color: '#991b1b' }}>{highCount}</div><div style={{ fontSize: '11px', color: c.textMuted }}>High</div></div>
          <div><div style={{ fontSize: '24px', fontWeight: 700, color: '#854d0e' }}>{medCount}</div><div style={{ fontSize: '11px', color: c.textMuted }}>Medium</div></div>
          <div><div style={{ fontSize: '24px', fontWeight: 700, color: '#1e40af' }}>{lowCount}</div><div style={{ fontSize: '11px', color: c.textMuted }}>Low</div></div>
        </div>
      </div>

      {OBSERVATIONS.map((obs) => {
        const sc = STATUS_COLORS[obs.status] ?? STATUS_COLORS.Open;
        const sev = SEVERITY_COLORS[obs.severity] ?? SEVERITY_COLORS.Low;
        return (
          <div key={obs.id} style={cardStyle}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '12px', color: c.textMuted, fontFamily: 'monospace' }}>{obs.id}</span>
                <span style={{ fontWeight: 600, fontSize: '15px', color: c.text }}>{obs.title}</span>
              </div>
              <div style={{ display: 'flex', gap: '6px' }}>
                <span style={{ padding: '2px 10px', borderRadius: '10px', fontSize: '11px', fontWeight: 600, background: sc.bg, color: sc.fg }}>{obs.status}</span>
                <span style={{ padding: '2px 10px', borderRadius: '10px', fontSize: '11px', fontWeight: 600, background: sev.bg, color: sev.fg }}>{obs.severity}</span>
              </div>
            </div>
            <div style={{ fontSize: '12px', color: c.textMuted, marginBottom: '8px' }}>
              {obs.project} \u00B7 {obs.author} \u00B7 {obs.date}
            </div>
            <div style={{ fontSize: '13px', color: c.text, lineHeight: '1.5' }}>{obs.desc}</div>
          </div>
        );
      })}
    </div>
  );
}
