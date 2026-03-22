/**
 * Construction Atlas — Dashboard Page
 *
 * Stat cards, recent projects, quick links, recent observations.
 * Presentation shell. Data is presentational placeholder.
 */

import { DEFAULT_BRANDING } from '../../../lib/branding/branding-types';
import type { AtlasRoute } from '../types';

const c = DEFAULT_BRANDING.colors;

const cardStyle: React.CSSProperties = {
  background: '#ffffff',
  border: `1px solid ${c.border}`,
  borderRadius: '8px',
  padding: '20px',
};

const statStyle: React.CSSProperties = {
  ...cardStyle,
  textAlign: 'center',
  flex: 1,
};

interface DashboardPageProps {
  onNavigate: (route: AtlasRoute) => void;
}

const STATUS_COLORS: Record<string, { bg: string; fg: string }> = {
  Active: { bg: '#dcfce7', fg: '#166534' },
  'In Review': { bg: '#fef9c3', fg: '#854d0e' },
  Planning: { bg: '#f1f5f9', fg: '#475569' },
};

const SEVERITY_COLORS: Record<string, { bg: string; fg: string }> = {
  High: { bg: '#fecaca', fg: '#991b1b' },
  Medium: { bg: '#fef9c3', fg: '#854d0e' },
  Low: { bg: '#dbeafe', fg: '#1e40af' },
};

export function DashboardPage({ onNavigate }: DashboardPageProps) {
  return (
    <div>
      <h1 style={{ fontSize: '24px', fontWeight: 700, color: c.text, margin: 0 }}>Dashboard</h1>
      <p style={{ color: c.textMuted, margin: '4px 0 24px', fontSize: '14px' }}>Construction intelligence overview</p>

      {/* Stat cards */}
      <div style={{ display: 'flex', gap: '16px', marginBottom: '24px' }}>
        {[
          { value: '12', label: 'Active Projects' },
          { value: '87', label: 'Open Conditions' },
          { value: '234', label: 'Observations (7d)' },
          { value: '156', label: 'Detail Families' },
        ].map((stat) => (
          <div key={stat.label} style={statStyle}>
            <div style={{ fontSize: '32px', fontWeight: 700, color: c.text }}>{stat.value}</div>
            <div style={{ fontSize: '13px', color: c.textMuted, marginTop: '4px' }}>{stat.label}</div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', gap: '24px' }}>
        {/* Recent Projects */}
        <div style={{ ...cardStyle, flex: 2 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h2 style={{ fontSize: '18px', fontWeight: 600, color: c.text, margin: 0 }}>Recent Projects</h2>
            <button
              onClick={() => onNavigate('projects')}
              style={{ background: 'none', border: 'none', color: c.secondary, fontSize: '13px', fontWeight: 600, cursor: 'pointer' }}
            >
              View All
            </button>
          </div>
          {[
            { name: 'Heritage Plaza Renovation', info: '24 conditions \u00B7 156 observations', status: 'Active' },
            { name: 'Waterfront Tower Phase 2', info: '18 conditions \u00B7 89 observations', status: 'Active' },
            { name: 'Metro Station Canopy', info: '12 conditions \u00B7 47 observations', status: 'In Review' },
            { name: 'Industrial Park Building C', info: '8 conditions \u00B7 23 observations', status: 'Planning' },
          ].map((project) => {
            const sc = STATUS_COLORS[project.status] ?? STATUS_COLORS.Planning;
            return (
              <div key={project.name} style={{
                display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                padding: '12px 0', borderBottom: `1px solid ${c.border}`,
              }}>
                <div>
                  <div style={{ fontWeight: 500, color: c.text, fontSize: '14px' }}>{project.name}</div>
                  <div style={{ fontSize: '12px', color: c.textMuted, marginTop: '2px' }}>{project.info}</div>
                </div>
                <span style={{
                  padding: '3px 10px', borderRadius: '12px', fontSize: '11px', fontWeight: 600,
                  background: sc.bg, color: sc.fg,
                }}>
                  {project.status}
                </span>
              </div>
            );
          })}
        </div>

        {/* Quick Links */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 600, color: c.text, margin: '0 0 4px' }}>Quick Links</h2>
          {[
            { route: 'atlas' as AtlasRoute, label: 'Atlas', desc: 'Detail canvas and reference graph' },
            { route: 'projects' as AtlasRoute, label: 'Projects', desc: 'Active project tracking' },
            { route: 'observations' as AtlasRoute, label: 'Observations', desc: 'Field observation feed' },
            { route: 'ai-settings' as AtlasRoute, label: 'AI Settings', desc: 'Configure AI providers' },
          ].map((link) => (
            <button
              key={link.route}
              onClick={() => onNavigate(link.route)}
              style={{
                ...cardStyle, padding: '16px', cursor: 'pointer', textAlign: 'left',
                transition: 'box-shadow 0.15s',
              }}
              onMouseEnter={(e) => { e.currentTarget.style.boxShadow = '0 2px 8px rgba(0,0,0,0.08)'; }}
              onMouseLeave={(e) => { e.currentTarget.style.boxShadow = 'none'; }}
            >
              <div style={{ fontWeight: 600, color: c.text, fontSize: '14px' }}>{link.label}</div>
              <div style={{ fontSize: '12px', color: c.textMuted, marginTop: '2px' }}>{link.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Recent Observations */}
      <div style={{ ...cardStyle, marginTop: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h2 style={{ fontSize: '18px', fontWeight: 600, color: c.text, margin: 0 }}>Recent Observations</h2>
          <button
            onClick={() => onNavigate('observations')}
            style={{ background: 'none', border: 'none', color: c.secondary, fontSize: '13px', fontWeight: 600, cursor: 'pointer' }}
          >
            View All
          </button>
        </div>
        <div style={{ display: 'flex', borderBottom: `1px solid ${c.border}`, padding: '8px 0', fontWeight: 600, fontSize: '12px', color: c.textMuted }}>
          <div style={{ flex: 3 }}>Detail</div>
          <div style={{ flex: 1 }}>Severity</div>
          <div style={{ flex: 2 }}>Project</div>
          <div style={{ flex: 1 }}>Time</div>
        </div>
        {[
          { detail: 'Flashing at parapet intersection', severity: 'High', project: 'Heritage Plaza', time: '2 hours ago' },
          { detail: 'Sealant joint at curtain wall', severity: 'Medium', project: 'Waterfront Tower', time: '4 hours ago' },
          { detail: 'Roof membrane termination', severity: 'Low', project: 'Metro Station', time: '6 hours ago' },
          { detail: 'Window head flashing continuity', severity: 'High', project: 'Heritage Plaza', time: '8 hours ago' },
        ].map((obs) => {
          const sc = SEVERITY_COLORS[obs.severity] ?? SEVERITY_COLORS.Low;
          return (
            <div key={obs.detail} style={{ display: 'flex', alignItems: 'center', padding: '10px 0', borderBottom: `1px solid ${c.border}`, fontSize: '13px' }}>
              <div style={{ flex: 3, color: c.text }}>{obs.detail}</div>
              <div style={{ flex: 1 }}>
                <span style={{ padding: '2px 8px', borderRadius: '10px', fontSize: '11px', fontWeight: 600, background: sc.bg, color: sc.fg }}>
                  {obs.severity}
                </span>
              </div>
              <div style={{ flex: 2, color: c.textMuted }}>{obs.project}</div>
              <div style={{ flex: 1, color: c.textMuted }}>{obs.time}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
