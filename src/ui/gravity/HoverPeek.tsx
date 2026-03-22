/**
 * Construction OS — Hover Peek Mode
 *
 * Hovering a detail, drawing, or document produces a temporary 50/50 preview:
 *   WORKSPACE | PREVIEW
 *
 * Actions:
 *   hover → preview
 *   click → lock
 *   mouse away → collapse
 *
 * Preview never destroys current workspace state.
 */

import { type ReactNode, useCallback, useEffect, useRef, useState } from 'react';
import { tokens } from '../theme/tokens';
import { PROXIMITY } from './ProximityConstants';
import { glassMorphStyle } from './GlassMorph';

interface HoverPeekProps {
  /** Content to peek at */
  peekContent: ReactNode;
  /** Whether peek is visible */
  visible: boolean;
  /** Whether peek is locked open */
  locked: boolean;
  /** Called when peek should close */
  onClose: () => void;
  /** Called when peek is clicked (lock) */
  onLock: () => void;
}

export function HoverPeekPanel({ peekContent, visible, locked, onClose, onLock }: HoverPeekProps) {
  const easing = PROXIMITY.easing;

  if (!visible) return null;

  return (
    <div
      onClick={locked ? undefined : onLock}
      style={{
        ...glassMorphStyle,
        position: 'absolute',
        right: 0,
        top: 0,
        bottom: 0,
        width: `${PROXIMITY.peekShare}%`,
        zIndex: 150,
        display: 'flex',
        flexDirection: 'column',
        transition: `width ${PROXIMITY.expandDuration}ms ${easing}, opacity ${PROXIMITY.expandDuration}ms ${easing}`,
        overflow: 'hidden',
        cursor: locked ? 'default' : 'pointer',
      }}
    >
      {/* Peek header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        borderBottom: '1px solid rgba(255,255,255,0.04)',
        minHeight: '32px',
        flexShrink: 0,
      }}>
        <span style={{
          fontSize: tokens.font.sizeXs,
          color: tokens.color.fgMuted,
          fontFamily: tokens.font.familyMono,
          letterSpacing: '0.05em',
        }}>
          {locked ? 'PREVIEW — LOCKED' : 'PREVIEW — click to lock'}
        </span>
        <button
          onClick={(e) => { e.stopPropagation(); onClose(); }}
          style={{
            padding: `${tokens.space.xs} ${tokens.space.sm}`,
            background: 'rgba(255,255,255,0.06)',
            color: tokens.color.fgMuted,
            border: 'none',
            borderRadius: tokens.radius.sm,
            cursor: 'pointer',
            fontSize: tokens.font.sizeXs,
          }}
        >
          {'\u2715'}
        </button>
      </div>

      {/* Peek content */}
      <div style={{ flex: 1, overflow: 'auto', padding: tokens.space.sm }}>
        {peekContent}
      </div>
    </div>
  );
}

/**
 * Hook: manages hover peek state for a peekable item.
 * Returns handlers and visibility state.
 */
export function useHoverPeek() {
  const [visible, setVisible] = useState(false);
  const [locked, setLocked] = useState(false);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  const handleMouseEnter = useCallback(() => {
    if (locked) return;
    timerRef.current = setTimeout(() => {
      setVisible(true);
    }, PROXIMITY.peekDelay);
  }, [locked]);

  const handleMouseLeave = useCallback(() => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
    if (!locked) {
      setVisible(false);
    }
  }, [locked]);

  const handleLock = useCallback(() => {
    setLocked(true);
    setVisible(true);
  }, []);

  const handleClose = useCallback(() => {
    setLocked(false);
    setVisible(false);
  }, []);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  return {
    visible,
    locked,
    handleMouseEnter,
    handleMouseLeave,
    handleLock,
    handleClose,
  };
}
