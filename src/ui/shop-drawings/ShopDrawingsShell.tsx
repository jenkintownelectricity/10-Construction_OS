/**
 * Shop Drawings Shell — Main Layout Compositor
 *
 * Ported from OMNI-VIEW v3.0 legacy layout into Construction_Application_OS.
 * Composes the classic document workspace layout:
 *
 *   ┌─────────────────────────────────────────────────────────────────┐
 *   │  Title Bar: CONSTRUCTION OS — Shop Drawings                     │
 *   ├─────────────────────────────────────────────────────────────────┤
 *   │  Menu Bar: File | Edit | View | Document | Tools                │
 *   ├─────────────────────────────────────────────────────────────────┤
 *   │  Viewer Toolbar: [Open][Undo/Redo][Zoom][Draw Tools][Edit]      │
 *   ├──────────┬──────┬──────────────────────────────────┬────────────┤
 *   │ Explorer │ Page │              Viewer               │ Properties │
 *   │  (240px) │Thumbs│    (scrolling page view)          │  (280px)   │
 *   │          │(110px│                                    │            │
 *   │ filter   │      │   ┌────────────────────────┐      │ Props      │
 *   │ files    │ [1]  │   │  Page 1               │      │ Taxonomy   │
 *   │          │ [2]  │   └────────────────────────┘      │ Toolbox    │
 *   │          │ [3]  │   ┌────────────────────────┐      │            │
 *   │          │ ...  │   │  Page 2               │      │            │
 *   │          │      │   └────────────────────────┘      │            │
 *   ├──────────┴──────┴──────────────────────────────────┴────────────┤
 *   │  Status Bar                                                      │
 *   └─────────────────────────────────────────────────────────────────┘
 *
 * Preserves current runtime/generator/backend seams:
 * - Event bus (object.selected) for file selection
 * - Adapter contracts remain intact
 * - No deprecated mock logic reintroduced
 *
 * Governance: L0-CMD-CONOS-VKGL04R-PORT-LEGACY-UI-SHELL-001
 */

import { useCallback, useState } from 'react';
import { tokens } from '../theme/tokens';
import { LeftNavigation } from './LeftNavigation';
import { MenuBar } from './MenuBar';
import { ThumbnailRail } from './ThumbnailRail';
import { ViewerToolbar } from './ViewerToolbar';
import { ViewerShell } from './ViewerShell';
import { PropertiesPanel } from './PropertiesPanel';
import type { ShopDrawingFile, ViewerTool, PageThumbnail, DocumentProperties } from './types';

// ─── Helper: generate page thumbnails from page count ──────────────────

function generatePages(count: number): PageThumbnail[] {
  return Array.from({ length: count }, (_, i) => ({
    pageNumber: i + 1,
    label: `Page ${i + 1}`,
    isActive: false,
  }));
}

// ─── Component ────────────────────────────────────────────────────────

interface ShopDrawingsShellProps {
  onSwitchToWorkstation?: () => void;
}

export function ShopDrawingsShell({ onSwitchToWorkstation }: ShopDrawingsShellProps) {
  // ─── State ──────────────────────────────────────────────────────────
  const [activeFile, setActiveFile] = useState<ShopDrawingFile | null>(null);
  const [activePage, setActivePage] = useState(1);
  const [thumbnailsVisible, setThumbnailsVisible] = useState(true);
  const [zoom, setZoom] = useState(100);
  const [activeTool, setActiveTool] = useState<ViewerTool>('cursor');

  // Derived state
  const pages: PageThumbnail[] = activeFile?.pageCount
    ? generatePages(activeFile.pageCount)
    : [];

  const documentProps: DocumentProperties | null = activeFile
    ? {
        fileName: activeFile.name,
        pageCount: activeFile.pageCount ?? 0,
        fileSize: activeFile.size ?? '\u2014',
      }
    : null;

  // ─── Handlers ───────────────────────────────────────────────────────

  const handleFileSelect = useCallback((file: ShopDrawingFile) => {
    setActiveFile(file);
    setActivePage(1);
  }, []);

  const handlePageSelect = useCallback((pageNumber: number) => {
    setActivePage(pageNumber);
  }, []);

  const handleToggleThumbnails = useCallback(() => {
    setThumbnailsVisible((prev) => !prev);
  }, []);

  const handleZoomIn = useCallback(() => {
    setZoom((prev) => Math.min(prev + 25, 400));
  }, []);

  const handleZoomOut = useCallback(() => {
    setZoom((prev) => Math.max(prev - 25, 25));
  }, []);

  const handleZoomFit = useCallback(() => {
    setZoom(100);
  }, []);

  const handleZoomReset = useCallback(() => {
    setZoom(100);
  }, []);

  // ─── Render ─────────────────────────────────────────────────────────

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      background: tokens.color.bgDeep,
      fontFamily: tokens.font.familyMono,
      fontSize: '12px',
      color: tokens.color.fgPrimary,
      overflow: 'hidden',
    }}>
      {/* ─── Title Bar ─── */}
      <div style={{
        height: '38px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 12px',
        background: `linear-gradient(180deg, transparent, ${tokens.color.bgSurface})`,
        borderBottom: `1px solid ${tokens.color.border}`,
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <span style={{ color: tokens.color.accentPrimary, fontSize: '18px', fontWeight: 900 }}>{'\u25C6'}</span>
          <span style={{ color: '#e0e8f0', fontWeight: 800, fontSize: '14px', letterSpacing: '3px' }}>
            CONSTRUCTION OS
          </span>
          <span style={{
            color: '#f0a030',
            fontSize: '8px',
            fontWeight: 700,
            letterSpacing: '1.5px',
            background: 'rgba(240,160,48,0.1)',
            padding: '2px 6px',
            borderRadius: '3px',
          }}>
            SHOP DRAWINGS
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          {onSwitchToWorkstation && (
            <button
              onClick={onSwitchToWorkstation}
              style={{
                padding: `${tokens.space.xs} ${tokens.space.sm}`,
                background: tokens.color.bgElevated,
                color: tokens.color.fgMuted,
                border: `1px solid ${tokens.color.border}`,
                borderRadius: tokens.radius.sm,
                cursor: 'pointer',
                fontSize: tokens.font.sizeXs,
                fontFamily: tokens.font.familyMono,
              }}
            >
              WORKSTATION
            </button>
          )}
          <span style={{ color: tokens.color.fgMuted, fontSize: '10px' }}>Ready</span>
        </div>
      </div>

      {/* ─── Menu Bar — matches OMNI-VIEW .menubar ─── */}
      <MenuBar />

      {/* ─── Viewer Toolbar ─── */}
      <ViewerToolbar
        zoom={zoom}
        onZoomIn={handleZoomIn}
        onZoomOut={handleZoomOut}
        onZoomFit={handleZoomFit}
        onZoomReset={handleZoomReset}
        onToggleThumbnails={handleToggleThumbnails}
        activeTool={activeTool}
        onToolSelect={setActiveTool}
      />

      {/* ─── Main Layout ─── */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left Navigation */}
        <LeftNavigation
          onFileSelect={handleFileSelect}
          selectedFileId={activeFile?.id ?? null}
        />

        {/* Thumbnail Rail */}
        <ThumbnailRail
          visible={thumbnailsVisible && pages.length > 0}
          pages={pages}
          activePageNumber={activePage}
          onPageSelect={handlePageSelect}
        />

        {/* Center Viewer */}
        <ViewerShell
          activeFile={activeFile}
          activePage={activePage}
          pages={pages}
          onPageClick={handlePageSelect}
        />

        {/* Right Properties Panel */}
        <PropertiesPanel
          documentProps={documentProps}
          activeTool={activeTool}
          onToolSelect={setActiveTool}
        />
      </div>

      {/* ─── Status Bar ─── */}
      <div style={{
        height: '22px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: '0 12px',
        background: tokens.color.bgDeep,
        borderTop: `1px solid ${tokens.color.border}`,
        fontSize: '9px',
        color: tokens.color.fgMuted,
        flexShrink: 0,
      }}>
        <span>
          {activeFile ? `${activeFile.name} — Page ${activePage} of ${pages.length}` : 'Ready'}
        </span>
        <span>
          {activeFile ? `${zoom}% | ${activeFile.size ?? ''}` : ''}
        </span>
      </div>
    </div>
  );
}
