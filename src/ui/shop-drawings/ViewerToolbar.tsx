/**
 * Shop Drawings Shell — Viewer Toolbar
 *
 * Ported from OMNI-VIEW legacy layout. Top toolbar with:
 * - File/refresh buttons
 * - Undo/redo
 * - Thumbnail toggle
 * - Zoom controls (out, label, in, fit)
 * - Drawing tool palette
 * - Edit tool palette
 * - Save/load buttons
 *
 * Presentation shell only. Tool state is local UI state.
 * No deprecated logic reintroduced.
 */

import { useCallback, useState } from 'react';
import { tokens } from '../theme/tokens';
import type { ViewerTool, ToolGroup } from './types';

// ─── Tool definitions ──────────────────────────────────────────────────

const DRAW_TOOLS: ToolGroup = {
  label: 'DRAW',
  tools: [
    { id: 'cursor', title: 'Cursor (V)', icon: '\u2197' },
    { id: 'pen', title: 'Pen (P)', icon: '\u270E' },
    { id: 'highlighter', title: 'Highlighter (H)', icon: '\u{1F58D}' },
    { id: 'text', title: 'Text (T)', icon: 'T' },
    { id: 'arrow', title: 'Arrow (A)', icon: '\u2192' },
    { id: 'rect', title: 'Rectangle (R)', icon: '\u25A1' },
    { id: 'polyline', title: 'Polyline (N)', icon: '\u2F00' },
    { id: 'cloud', title: 'Cloud (C)', icon: '\u2601' },
    { id: 'callout', title: 'Callout (Q)', icon: '\u{1F4AC}' },
    { id: 'dimension', title: 'Dimension (L)', icon: '\u21A4' },
    { id: 'count', title: 'Count (G)', icon: '#' },
    { id: 'stamp', title: 'Stamp (I)', icon: '\u{1F4F7}' },
    { id: 'eraser', title: 'Eraser (E)', icon: '\u2716' },
  ],
};

const EDIT_TOOLS: ToolGroup = {
  label: 'EDIT',
  tools: [
    { id: 'snapshot', title: 'Snapshot', icon: '\u{1F4F8}' },
    { id: 'redact', title: 'Redaction', icon: '\u25A0' },
    { id: 'fill', title: 'Dynamic Fill', icon: '\u{1F3A8}' },
    { id: 'format-painter', title: 'Format Painter', icon: '\u{1F58C}' },
  ],
};

// ─── Styles ────────────────────────────────────────────────────────────

const toolbarStyle: React.CSSProperties = {
  height: '40px',
  display: 'flex',
  alignItems: 'center',
  gap: '2px',
  padding: '0 8px',
  background: tokens.color.bgElevated,
  borderBottom: `1px solid ${tokens.color.border}`,
  flexShrink: 0,
  overflowX: 'auto',
};

const btnBase: React.CSSProperties = {
  width: '34px',
  height: '30px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  background: 'transparent',
  border: '1px solid transparent',
  borderRadius: '5px',
  color: tokens.color.fgSecondary,
  cursor: 'pointer',
  fontSize: '16px',
  transition: 'all 0.12s',
  flexShrink: 0,
};

const btnActive: React.CSSProperties = {
  ...btnBase,
  background: `${tokens.color.accentPrimary}12`,
  color: tokens.color.accentPrimary,
  borderColor: `${tokens.color.accentPrimary}4D`,
};

const sepStyle: React.CSSProperties = {
  width: '1px',
  height: '22px',
  background: tokens.color.border,
  margin: '0 4px',
  flexShrink: 0,
};

const labelStyle: React.CSSProperties = {
  fontSize: '10px',
  color: tokens.color.fgMuted,
  padding: '0 6px',
  letterSpacing: '0.5px',
  whiteSpace: 'nowrap',
  flexShrink: 0,
};

// ─── Component ────────────────────────────────────────────────────────

interface ViewerToolbarProps {
  zoom: number;
  onZoomIn?: () => void;
  onZoomOut?: () => void;
  onZoomFit?: () => void;
  onZoomReset?: () => void;
  onToggleThumbnails?: () => void;
  activeTool: ViewerTool;
  onToolSelect?: (tool: ViewerTool) => void;
}

export function ViewerToolbar({
  zoom,
  onZoomIn,
  onZoomOut,
  onZoomFit,
  onZoomReset,
  onToggleThumbnails,
  activeTool,
  onToolSelect,
}: ViewerToolbarProps) {
  const renderToolBtn = (tool: { id: ViewerTool; title: string; icon: string }) => {
    const isActive = activeTool === tool.id;
    return (
      <button
        key={tool.id}
        title={tool.title}
        onClick={() => onToolSelect?.(tool.id)}
        style={isActive ? btnActive : btnBase}
        onMouseEnter={(e) => {
          if (!isActive) {
            e.currentTarget.style.background = tokens.color.bgHover;
            e.currentTarget.style.color = tokens.color.fgPrimary;
            e.currentTarget.style.borderColor = tokens.color.border;
          }
        }}
        onMouseLeave={(e) => {
          if (!isActive) {
            e.currentTarget.style.background = 'transparent';
            e.currentTarget.style.color = tokens.color.fgSecondary;
            e.currentTarget.style.borderColor = 'transparent';
          }
        }}
      >
        {tool.icon}
      </button>
    );
  };

  return (
    <div style={toolbarStyle}>
      {/* File operations */}
      <button style={btnBase} title="Open Workspace (Ctrl+O)"
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u{1F4C2}'}
      </button>
      <button style={btnBase} title="Refresh (F5)"
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u21BB'}
      </button>

      <div style={sepStyle} />

      {/* Undo / Redo */}
      <button style={btnBase} title="Undo (Ctrl+Z)"
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u21A9'}
      </button>
      <button style={btnBase} title="Redo (Ctrl+Y)"
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u21AA'}
      </button>

      <div style={sepStyle} />

      {/* Thumbnail toggle */}
      <button
        style={btnBase}
        title="Thumbnails"
        onClick={onToggleThumbnails}
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u2630'}
      </button>

      <div style={sepStyle} />

      {/* Zoom controls */}
      <button style={btnBase} title="Zoom Out" onClick={onZoomOut}
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        -
      </button>
      <span
        style={{
          fontSize: '11px',
          color: tokens.color.fgSecondary,
          fontWeight: 700,
          minWidth: '44px',
          textAlign: 'center',
          padding: '0 4px',
          cursor: 'pointer',
          flexShrink: 0,
        }}
        onClick={onZoomReset}
        title="Click for 100%"
      >
        {Math.round(zoom)}%
      </span>
      <button style={btnBase} title="Zoom In" onClick={onZoomIn}
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        +
      </button>
      <button style={btnBase} title="Fit Width" onClick={onZoomFit}
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u2922'}
      </button>

      <div style={sepStyle} />

      {/* Draw tools */}
      <span style={labelStyle}>{DRAW_TOOLS.label}:</span>
      {DRAW_TOOLS.tools.map(renderToolBtn)}

      <div style={sepStyle} />

      {/* Edit tools */}
      <span style={labelStyle}>{EDIT_TOOLS.label}:</span>
      {EDIT_TOOLS.tools.map(renderToolBtn)}

      <div style={sepStyle} />

      {/* Save / Load */}
      <button style={btnBase} title="Save Markups (JSON)"
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u{1F4BE}'}
      </button>
      <button style={btnBase} title="Load Markups"
        onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
        onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
      >
        {'\u{1F4C2}'}
      </button>
    </div>
  );
}
