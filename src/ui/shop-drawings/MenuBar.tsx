/**
 * Shop Drawings Shell — Menu Bar
 *
 * Ported from OMNI-VIEW legacy layout (.menubar).
 * Horizontal menu strip with dropdown menus:
 * File | Edit | View | Document | Tools
 *
 * Presentation shell only. Menu items are display-ready
 * with shortcut labels but no wired behavior.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { tokens } from '../theme/tokens';
import type { MenuBarItem } from './types';

// ─── Menu definitions ──────────────────────────────────────────────────

const MENUS: MenuBarItem[] = [
  {
    label: 'File',
    items: [
      { label: 'Open Workspace', shortcut: 'Ctrl+O' },
      { label: 'Refresh', shortcut: 'F5' },
      { label: '', divider: true },
      { label: 'Save Markups', shortcut: 'Ctrl+S' },
      { label: 'Load Markups', shortcut: 'Ctrl+Shift+O' },
      { label: '', divider: true },
      { label: 'Export Page as PNG' },
      { label: 'Print', shortcut: 'Ctrl+P' },
    ],
  },
  {
    label: 'Edit',
    items: [
      { label: 'Undo', shortcut: 'Ctrl+Z' },
      { label: 'Redo', shortcut: 'Ctrl+Y' },
      { label: '', divider: true },
      { label: 'Copy', shortcut: 'Ctrl+C' },
      { label: 'Paste', shortcut: 'Ctrl+V' },
      { label: 'Delete', shortcut: 'Del' },
      { label: '', divider: true },
      { label: 'Select All', shortcut: 'Ctrl+A' },
    ],
  },
  {
    label: 'View',
    items: [
      { label: 'Thumbnails' },
      { label: 'Split View' },
      { label: '', divider: true },
      { label: 'Zoom In', shortcut: 'Ctrl+=' },
      { label: 'Zoom Out', shortcut: 'Ctrl+-' },
      { label: 'Fit Width' },
      { label: 'Actual Size', shortcut: 'Ctrl+0' },
      { label: '', divider: true },
      { label: 'Fullscreen', shortcut: 'F11' },
    ],
  },
  {
    label: 'Document',
    items: [
      { label: 'Rotate CW' },
      { label: 'Rotate CCW' },
      { label: '', divider: true },
      { label: 'Extract Page' },
      { label: 'Flatten Markups' },
      { label: '', divider: true },
      { label: 'OCR Page' },
      { label: 'Calibrate Scale' },
    ],
  },
  {
    label: 'Tools',
    items: [
      { label: 'Cursor', shortcut: 'V' },
      { label: 'Pen', shortcut: 'P' },
      { label: 'Text', shortcut: 'T' },
      { label: 'Arrow', shortcut: 'A' },
      { label: 'Rectangle', shortcut: 'R' },
      { label: '', divider: true },
      { label: 'Snapshot', shortcut: 'G' },
      { label: 'Format Painter', shortcut: 'Ctrl+Shift+C' },
    ],
  },
];

// ─── Component ────────────────────────────────────────────────────────

export function MenuBar() {
  const [openMenu, setOpenMenu] = useState<string | null>(null);
  const barRef = useRef<HTMLDivElement>(null);

  // Close on outside click
  useEffect(() => {
    if (!openMenu) return;
    const handleClick = (e: MouseEvent) => {
      if (barRef.current && !barRef.current.contains(e.target as Node)) {
        setOpenMenu(null);
      }
    };
    document.addEventListener('mousedown', handleClick);
    return () => document.removeEventListener('mousedown', handleClick);
  }, [openMenu]);

  const handleMenuClick = useCallback((label: string) => {
    setOpenMenu((prev) => (prev === label ? null : label));
  }, []);

  return (
    <div
      ref={barRef}
      style={{
        height: '28px',
        display: 'flex',
        alignItems: 'center',
        padding: '0 4px',
        background: tokens.color.bgSurface,
        borderBottom: `1px solid ${tokens.color.border}`,
        flexShrink: 0,
        gap: 0,
        position: 'relative',
      }}
    >
      {MENUS.map((menu) => {
        const isOpen = openMenu === menu.label;
        return (
          <div key={menu.label} style={{ position: 'relative' }}>
            <button
              onClick={() => handleMenuClick(menu.label)}
              onMouseEnter={() => {
                if (openMenu !== null) setOpenMenu(menu.label);
              }}
              style={{
                background: isOpen ? tokens.color.bgHover : 'transparent',
                border: 'none',
                color: isOpen ? tokens.color.fgPrimary : tokens.color.fgSecondary,
                padding: '4px 10px',
                fontSize: '11px',
                cursor: 'pointer',
                borderRadius: '3px',
              }}
            >
              {menu.label}
            </button>
            {isOpen && (
              <div style={{
                position: 'absolute',
                top: '100%',
                left: 0,
                minWidth: '240px',
                background: tokens.color.bgElevated,
                border: `1px solid ${tokens.color.border}`,
                borderRadius: '6px',
                boxShadow: '0 12px 40px rgba(0,0,0,0.7)',
                zIndex: 9000,
                padding: '4px 0',
              }}>
                {menu.items.map((item, idx) =>
                  item.divider ? (
                    <div key={idx} style={{ height: '1px', background: tokens.color.border, margin: '4px 10px' }} />
                  ) : (
                    <button
                      key={idx}
                      onClick={() => setOpenMenu(null)}
                      style={{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        width: '100%',
                        padding: '6px 14px',
                        background: 'transparent',
                        border: 'none',
                        color: tokens.color.fgPrimary,
                        fontSize: '11px',
                        cursor: 'pointer',
                        textAlign: 'left',
                      }}
                      onMouseEnter={(e) => { e.currentTarget.style.background = tokens.color.bgHover; }}
                      onMouseLeave={(e) => { e.currentTarget.style.background = 'transparent'; }}
                    >
                      <span>{item.label}</span>
                      {item.shortcut && (
                        <span style={{ color: tokens.color.fgMuted, fontSize: '9px', marginLeft: '16px' }}>
                          {item.shortcut}
                        </span>
                      )}
                    </button>
                  )
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}
