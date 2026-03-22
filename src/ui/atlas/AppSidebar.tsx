/**
 * Construction Atlas — App Sidebar
 *
 * Primary left navigation sidebar with dark navy theme.
 * Grouped nav sections: PRODUCT, TOOLS, CONFIG.
 * Collapsible. Active item highlighted.
 *
 * Colors from DEFAULT_BRANDING: primary=#1e3a5f
 */

import { useState } from 'react';
import { DEFAULT_BRANDING } from '../../lib/branding/branding-types';
import { NAV_GROUPS, type AtlasRoute } from './types';

const c = DEFAULT_BRANDING.colors;

// ─── Styles ────────────────────────────────────────────────────────────

const sidebarStyle: React.CSSProperties = {
  width: '160px',
  minWidth: '160px',
  background: c.primary,
  display: 'flex',
  flexDirection: 'column',
  flexShrink: 0,
  color: '#ffffff',
  fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
  fontSize: '13px',
  userSelect: 'none',
  overflow: 'hidden',
  transition: 'width 200ms ease, min-width 200ms ease',
};

const sidebarCollapsedStyle: React.CSSProperties = {
  ...sidebarStyle,
  width: '0px',
  minWidth: '0px',
};

const logoStyle: React.CSSProperties = {
  padding: '16px 16px 20px',
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  flexShrink: 0,
};

const logoIconStyle: React.CSSProperties = {
  width: '28px',
  height: '28px',
  borderRadius: '6px',
  background: c.secondary,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  fontSize: '14px',
  fontWeight: 800,
  color: '#ffffff',
  flexShrink: 0,
};

const logoTextStyle: React.CSSProperties = {
  fontSize: '14px',
  fontWeight: 700,
  letterSpacing: '0.02em',
  whiteSpace: 'nowrap',
};

const groupLabelStyle: React.CSSProperties = {
  fontSize: '10px',
  fontWeight: 600,
  letterSpacing: '1.2px',
  color: 'rgba(255,255,255,0.4)',
  padding: '16px 16px 6px',
  textTransform: 'uppercase',
};

const navItemStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '10px',
  padding: '8px 16px',
  cursor: 'pointer',
  borderRadius: '6px',
  margin: '1px 8px',
  transition: 'background 0.12s',
  border: 'none',
  width: 'calc(100% - 16px)',
  textAlign: 'left',
  fontSize: '13px',
  fontWeight: 500,
  color: 'rgba(255,255,255,0.7)',
  background: 'transparent',
};

const navItemActiveStyle: React.CSSProperties = {
  ...navItemStyle,
  background: c.secondary,
  color: '#ffffff',
  fontWeight: 600,
};

const collapseStyle: React.CSSProperties = {
  padding: '12px 16px',
  display: 'flex',
  alignItems: 'center',
  gap: '8px',
  cursor: 'pointer',
  color: 'rgba(255,255,255,0.4)',
  fontSize: '12px',
  border: 'none',
  background: 'transparent',
  width: '100%',
  textAlign: 'left',
};

const footerStyle: React.CSSProperties = {
  padding: '8px 16px 12px',
  fontSize: '10px',
  color: 'rgba(255,255,255,0.25)',
};

// ─── Component ────────────────────────────────────────────────────────

interface AppSidebarProps {
  activeRoute: AtlasRoute;
  onNavigate: (route: AtlasRoute) => void;
}

export function AppSidebar({ activeRoute, onNavigate }: AppSidebarProps) {
  const [collapsed, setCollapsed] = useState(false);

  if (collapsed) {
    return (
      <div style={sidebarCollapsedStyle}>
        <button
          onClick={() => setCollapsed(false)}
          style={{
            ...collapseStyle,
            padding: '16px 8px',
            justifyContent: 'center',
          }}
          title="Expand sidebar"
        >
          {'\u203A'}
        </button>
      </div>
    );
  }

  return (
    <div style={sidebarStyle}>
      {/* Logo */}
      <div style={logoStyle}>
        <div style={logoIconStyle}>C</div>
        <span style={logoTextStyle}>Construction Atlas</span>
      </div>

      {/* Nav groups */}
      <div style={{ flex: 1, overflowY: 'auto' }}>
        {NAV_GROUPS.map((group) => (
          <div key={group.label}>
            <div style={groupLabelStyle}>{group.label}</div>
            {group.items.map((item) => {
              const isActive = activeRoute === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  style={isActive ? navItemActiveStyle : navItemStyle}
                  onMouseEnter={(e) => {
                    if (!isActive) e.currentTarget.style.background = 'rgba(255,255,255,0.08)';
                  }}
                  onMouseLeave={(e) => {
                    if (!isActive) e.currentTarget.style.background = 'transparent';
                  }}
                >
                  <span style={{ fontSize: '15px', width: '18px', textAlign: 'center', flexShrink: 0 }}>
                    {item.icon}
                  </span>
                  <span>{item.label}</span>
                </button>
              );
            })}
          </div>
        ))}
      </div>

      {/* Collapse */}
      <button onClick={() => setCollapsed(true)} style={collapseStyle}>
        <span>{'\u2039'}</span>
        <span>Collapse</span>
      </button>

      {/* Footer */}
      <div style={footerStyle}>Atlas Systems</div>
    </div>
  );
}
