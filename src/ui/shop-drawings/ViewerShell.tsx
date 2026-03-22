/**
 * Shop Drawings Shell — Viewer Shell (Center Viewport)
 *
 * Ported from OMNI-VIEW legacy layout. Center document viewport with:
 * - Primary viewport (vpa)
 * - Split divider (optional split view)
 * - Secondary viewport (vpb)
 * - Empty state placeholder
 * - Page column layout with white page wrappers
 *
 * Presentation shell only. No PDF.js or Fabric.js rendering logic.
 * Viewer surface is ready for future PDF/DXF rendering integration.
 */

import { tokens } from '../theme/tokens';
import type { ShopDrawingFile, PageThumbnail } from './types';

// ─── Styles ────────────────────────────────────────────────────────────

const viewportContainerStyle: React.CSSProperties = {
  flex: 1,
  display: 'flex',
  overflow: 'hidden',
  position: 'relative',
};

const viewportStyle: React.CSSProperties = {
  flex: 1,
  overflow: 'auto',
  background: '#1a1c22',
  position: 'relative',
};

const emptyStateStyle: React.CSSProperties = {
  flex: 1,
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  gap: '8px',
};

const pageColumnStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: '20px 0',
  gap: '16px',
  minHeight: '100%',
};

// ─── Component ────────────────────────────────────────────────────────

interface ViewerShellProps {
  activeFile: ShopDrawingFile | null;
  activePage: number;
  pages: PageThumbnail[];
  onPageClick?: (pageNumber: number) => void;
}

export function ViewerShell({ activeFile, activePage, pages }: ViewerShellProps) {
  return (
    <div style={viewportContainerStyle}>
      <div style={viewportStyle}>
        {!activeFile ? (
          /* Empty state — matching OMNI-VIEW visual */
          <div style={emptyStateStyle}>
            <div style={{
              fontSize: '56px',
              color: tokens.color.accentPrimary,
              opacity: 0.12,
              fontWeight: 900,
            }}>
              {'\u25C6'}
            </div>
            <div style={{
              fontSize: '26px',
              fontWeight: 900,
              color: '#222838',
              letterSpacing: '6px',
            }}>
              CONSTRUCTION OS
            </div>
            <div style={{
              fontSize: '10px',
              color: tokens.color.fgMuted,
              letterSpacing: '3px',
              textTransform: 'uppercase',
            }}>
              Shop Drawings Workspace
            </div>
          </div>
        ) : (
          /* Document viewport — page column layout */
          <div style={pageColumnStyle}>
            {pages.map((page) => {
              const isCurrent = page.pageNumber === activePage;
              return (
                <div
                  key={page.pageNumber}
                  style={{
                    position: 'relative',
                    background: '#ffffff',
                    flexShrink: 0,
                    boxShadow: isCurrent
                      ? `0 0 0 2px ${tokens.color.accentPrimary}, 0 4px 28px rgba(0,0,0,0.45)`
                      : '0 4px 28px rgba(0,0,0,0.45)',
                    borderRadius: '1px',
                    /* Standard letter size aspect ratio scaled to viewport */
                    width: '680px',
                    height: '880px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                  }}
                >
                  {/* Page content placeholder — ready for canvas/PDF rendering */}
                  <div style={{
                    color: '#c0c0c0',
                    fontSize: '14px',
                    textAlign: 'center',
                    fontFamily: tokens.font.familyMono,
                  }}>
                    <div style={{ fontSize: '32px', marginBottom: '8px', color: '#e0e0e0' }}>
                      {activeFile.name}
                    </div>
                    <div>Page {page.pageNumber} of {pages.length}</div>
                    <div style={{ marginTop: '12px', fontSize: '11px', color: '#d0d0d0' }}>
                      Viewer surface ready for rendering integration
                    </div>
                  </div>

                  {/* Page label */}
                  <div style={{
                    position: 'absolute',
                    bottom: '-18px',
                    left: '50%',
                    transform: 'translateX(-50%)',
                    fontSize: '9px',
                    color: tokens.color.fgMuted,
                    whiteSpace: 'nowrap',
                  }}>
                    {page.label}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
