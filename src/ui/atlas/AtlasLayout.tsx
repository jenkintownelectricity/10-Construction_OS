/**
 * Construction Atlas — Primary Layout
 *
 * Sidebar + routed content area. This is the primary application shell.
 * The Workstation cockpit and OMNI-VIEW viewer are embedded as "Tools"
 * and "Viewer" pages within this layout.
 */

import { useCallback, useState } from 'react';
import { DEFAULT_BRANDING } from '../../lib/branding/branding-types';
import { AppSidebar } from './AppSidebar';
import { DashboardPage } from './pages/DashboardPage';
import { AtlasPage } from './pages/AtlasPage';
import { ShopDrawingsPage } from './pages/ShopDrawingsPage';
import { ManufacturersPage } from './pages/ManufacturersPage';
import { ObservationsPage } from './pages/ObservationsPage';
import { PlaceholderPage } from './pages/PlaceholderPage';
import type { AtlasRoute } from './types';

const c = DEFAULT_BRANDING.colors;

// ─── Lazy imports for heavy shells ─────────────────────────────────────
// These are imported directly since they're already in the bundle.
// The WorkspaceShell and ShopDrawingsShell are embedded as pages.

import { WorkspaceShell } from '../workspace/WorkspaceShell';
import { ShopDrawingsShell } from '../shop-drawings/ShopDrawingsShell';

// ─── Component ────────────────────────────────────────────────────────

export function AtlasLayout() {
  const [activeRoute, setActiveRoute] = useState<AtlasRoute>('dashboard');

  const handleNavigate = useCallback((route: AtlasRoute) => {
    setActiveRoute(route);
  }, []);

  // Tools and Viewer pages render their own full shells (dark theme)
  // and fill the entire content area without the Atlas content wrapper
  const isFullShellPage = activeRoute === 'tools' || activeRoute === 'viewer';

  return (
    <div style={{
      display: 'flex',
      height: '100%',
      width: '100%',
      fontFamily: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
      overflow: 'hidden',
    }}>
      {/* Sidebar */}
      <AppSidebar activeRoute={activeRoute} onNavigate={handleNavigate} />

      {/* Content Area */}
      {isFullShellPage ? (
        <div style={{ flex: 1, overflow: 'hidden' }}>
          {activeRoute === 'tools' && <WorkspaceShell />}
          {activeRoute === 'viewer' && <ShopDrawingsShell />}
        </div>
      ) : (
        <div style={{
          flex: 1,
          overflow: 'auto',
          background: c.surface,
          padding: '32px 40px',
          color: c.text,
          fontSize: '14px',
        }}>
          {activeRoute === 'dashboard' && <DashboardPage onNavigate={handleNavigate} />}
          {activeRoute === 'atlas' && <AtlasPage />}
          {activeRoute === 'projects' && <PlaceholderPage title="Projects" description="Active project tracking and management" />}
          {activeRoute === 'details' && <PlaceholderPage title="Details" description="Construction detail families and variants" />}
          {activeRoute === 'shop-drawings' && <ShopDrawingsPage onNavigate={handleNavigate} />}
          {activeRoute === 'manufacturers' && <ManufacturersPage />}
          {activeRoute === 'observations' && <ObservationsPage />}
          {activeRoute === 'artifacts' && <PlaceholderPage title="Artifacts" description="Generated artifacts, DXF files, and detail outputs" />}
          {activeRoute === 'ai-settings' && <PlaceholderPage title="AI Settings" description="Configure AI providers and model preferences" />}
          {activeRoute === 'branding' && <PlaceholderPage title="Branding" description="White-label branding and theme configuration" />}
        </div>
      )}
    </div>
  );
}
