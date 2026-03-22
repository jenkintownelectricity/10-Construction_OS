/**
 * SVG Detail View — Bounded SVG presentation component
 *
 * Renders a single SVG detail string in a responsive viewer container.
 * Display pattern informed by CADless_drawings:
 *   - renderers/utils.js: createSVG viewBox-based responsive scaling
 *   - public/index.html: modal viewer with white SVG canvas on dark chrome
 *   - renderers/templates/detail_sheet.html: bordered detail container with label
 *
 * Does NOT own truth. Does NOT generate. Display-only.
 *
 * Governance: VKGL04R — Viewer-facing SVG presentation only
 */

import { tokens } from '../theme/tokens';

// ─── Props ───────────────────────────────────────────────────────────

interface SvgDetailViewProps {
  /** Raw SVG markup string */
  svgContent: string;
  /** Detail ID label */
  detailId: string;
  /** Artifact type label */
  artifactType: string;
  /** Filename label */
  filename: string;
}

// ─── Component ───────────────────────────────────────────────────────

export function SvgDetailView({
  svgContent,
  detailId,
  artifactType,
  filename,
}: SvgDetailViewProps) {
  return (
    <div
      data-testid="svg-detail-view"
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        background: tokens.color.bgSurface,
        fontFamily: tokens.font.family,
      }}
    >
      {/* Detail header bar — informed by CADless_drawings detail_sheet.html title bar */}
      <div
        style={{
          flexShrink: 0,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '8px 16px',
          background: tokens.color.bgElevated,
          borderBottom: `1px solid ${tokens.color.border}`,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          <span
            style={{
              fontSize: '13px',
              fontWeight: 600,
              color: tokens.color.fgPrimary,
              textTransform: 'uppercase',
              letterSpacing: '0.04em',
            }}
          >
            {detailId}
          </span>
          <span
            style={{
              fontSize: '11px',
              color: tokens.color.fgMuted,
              fontFamily: tokens.font.familyMono,
            }}
          >
            {artifactType}
          </span>
        </div>
        <span
          style={{
            fontSize: '11px',
            color: tokens.color.fgMuted,
            fontFamily: tokens.font.familyMono,
          }}
        >
          {filename}
        </span>
      </div>

      {/* SVG canvas — informed by CADless_drawings modal viewer + detail_sheet container */}
      <div
        style={{
          flex: 1,
          overflow: 'auto',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: '24px',
          background: tokens.color.bgBase,
        }}
      >
        {/*
         * White canvas for SVG detail rendering.
         * Pattern from CADless_drawings:
         *   - public/index.html uses white background modal for SVG preview
         *   - renderers/templates/detail_sheet.html uses white sheet with border
         *   - All SVGs use viewBox for responsive scaling (renderers/utils.js createSVG)
         */}
        <div
          data-testid="svg-detail-canvas"
          style={{
            background: '#ffffff',
            borderRadius: '4px',
            border: `1px solid ${tokens.color.border}`,
            padding: '16px',
            maxWidth: '100%',
            maxHeight: '100%',
            overflow: 'auto',
            boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
          }}
          dangerouslySetInnerHTML={{ __html: svgContent }}
        />
      </div>
    </div>
  );
}
