/**
 * Shop Drawings Shell — Page Thumbnail Rail
 *
 * Ported from OMNI-VIEW legacy layout. Vertical thumbnail sidebar with:
 * - Collapsible via visibility toggle
 * - Canvas-style page preview placeholders
 * - Active page indicator with accent border
 * - Page numbering
 *
 * Presentation shell only. No PDF rendering logic.
 */

import { tokens } from '../theme/tokens';
import type { PageThumbnail } from './types';

// ─── Styles ────────────────────────────────────────────────────────────

const railStyle: React.CSSProperties = {
  width: '110px',
  background: tokens.color.bgDeep,
  borderRight: `1px solid ${tokens.color.border}`,
  display: 'flex',
  flexDirection: 'column',
  flexShrink: 0,
};

const railHiddenStyle: React.CSSProperties = {
  ...railStyle,
  display: 'none',
};

const headerStyle: React.CSSProperties = {
  height: '32px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '0 10px',
  background: tokens.color.bgElevated,
  borderBottom: `1px solid ${tokens.color.border}`,
  flexShrink: 0,
};

const headerLabelStyle: React.CSSProperties = {
  fontSize: '9px',
  fontWeight: 700,
  letterSpacing: '1.5px',
  color: tokens.color.fgMuted,
  textTransform: 'uppercase',
};

const listStyle: React.CSSProperties = {
  flex: 1,
  overflowY: 'auto',
  padding: '6px',
  display: 'flex',
  flexDirection: 'column',
  gap: '6px',
};

// ─── Component ────────────────────────────────────────────────────────

interface ThumbnailRailProps {
  visible: boolean;
  pages: PageThumbnail[];
  activePageNumber: number;
  onPageSelect?: (pageNumber: number) => void;
}

export function ThumbnailRail({ visible, pages, activePageNumber, onPageSelect }: ThumbnailRailProps) {
  if (!visible) return <div style={railHiddenStyle} />;

  return (
    <div style={railStyle}>
      <div style={headerStyle}>
        <span style={headerLabelStyle}>PAGES</span>
      </div>
      <div style={listStyle}>
        {pages.map((page) => {
          const isActive = page.pageNumber === activePageNumber;
          return (
            <button
              key={page.pageNumber}
              onClick={() => onPageSelect?.(page.pageNumber)}
              style={{
                cursor: 'pointer',
                border: `2px solid ${isActive ? tokens.color.accentPrimary : tokens.color.border}`,
                borderRadius: '3px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                padding: '3px',
                background: isActive ? `${tokens.color.accentPrimary}12` : 'transparent',
                transition: 'border-color 0.12s',
                color: 'inherit',
              }}
              onMouseEnter={(e) => {
                if (!isActive) e.currentTarget.style.borderColor = tokens.color.fgMuted;
              }}
              onMouseLeave={(e) => {
                if (!isActive) e.currentTarget.style.borderColor = tokens.color.border;
              }}
            >
              {/* Thumbnail placeholder — aspect ratio mimics a document page */}
              <div style={{
                width: '100%',
                aspectRatio: '8.5 / 11',
                background: '#ffffff',
                borderRadius: '1px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '18px',
                color: '#c0c0c0',
                fontWeight: 700,
              }}>
                {page.pageNumber}
              </div>
              <span style={{
                fontSize: '8px',
                color: isActive ? tokens.color.accentPrimary : tokens.color.fgMuted,
                marginTop: '2px',
                fontWeight: 700,
              }}>
                {page.label}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}
