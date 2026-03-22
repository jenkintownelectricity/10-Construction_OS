/**
 * Construction Atlas — Primary Layout
 *
 * Sidebar + routed content area. This is the primary application shell.
 * The Workstation cockpit and OMNI-VIEW viewer are embedded as full
 * application surfaces launched from the sidebar.
 *
 * Loop: Shop Drawings → select context → Launch Workstation →
 *       Generate roofing detail → auto-open Viewer with result
 *
 * Governance: VKGL04R — Atlas remains primary shell.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { DEFAULT_BRANDING } from '../../lib/branding/branding-types';
import { eventBus } from '../events/EventBus';
import { AppSidebar } from './AppSidebar';
import { DashboardPage } from './pages/DashboardPage';
import { AtlasPage } from './pages/AtlasPage';
import { ShopDrawingsPage } from './pages/ShopDrawingsPage';
import { ManufacturersPage } from './pages/ManufacturersPage';
import { ObservationsPage } from './pages/ObservationsPage';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { ViewerPage } from './pages/ViewerPage';
import type { AtlasRoute } from './types';

const c = DEFAULT_BRANDING.colors;

// ─── Full application surfaces ────────────────────────────────────────

import { WorkspaceShell } from '../workspace/WorkspaceShell';

// ─── Component ────────────────────────────────────────────────────────

export function AtlasLayout() {
  const [activeRoute, setActiveRoute] = useState<AtlasRoute>('dashboard');
  const activeRouteRef = useRef(activeRoute);

  // Keep ref in sync for use in event handler closure
  useEffect(() => {
    activeRouteRef.current = activeRoute;
  }, [activeRoute]);

  const handleNavigate = useCallback((route: AtlasRoute) => {
    setActiveRoute(route);
  }, []);

  // ─── Listen for generation.completed → auto-open Viewer on success ──
  useEffect(() => {
    const unsub = eventBus.on('generation.completed', (payload) => {
      if (payload.status === 'success' && activeRouteRef.current === 'tools') {
        // Auto-navigate to viewer after successful generation
        setActiveRoute('viewer');
      }
    });
    return unsub;
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
          {activeRoute === 'tools' && (
            <WorkspaceShell
              onSwitchToShopDrawings={() => setActiveRoute('shop-drawings')}
            />
          )}
          {activeRoute === 'viewer' && (
            <ViewerPage onNavigate={handleNavigate} />
          )}
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
