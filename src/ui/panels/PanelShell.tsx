/**
 * Construction OS — Panel Shell
 * Common wrapper for all panel systems. Provides Truth Echo visual feedback,
 * source basis indicator, context collapse behavior, and consistent panel chrome.
 *
 * Typography: panel titles use sizeMd, body content uses sizeSm,
 * meta/status uses sizeXs. All >= 0.85rem.
 *
 * MOCK / dev controls have been moved to the isolated DevTools panel.
 * Panel headers no longer show MOCK badges directly.
 *
 * Context Collapse: When gravity object is active, irrelevant panels
 * dim to summary state. Relevant panels auto-focus their best mode.
 * All collapsed views remain recoverable and non-destructive.
 */

import { type ReactNode, useEffect, useState } from 'react';
import { tokens } from '../theme/tokens';
import type { PanelId, SourceBasis } from '../contracts/events';
import { useActiveObject } from '../stores/useSyncExternalStore';

interface PanelShellProps {
  panelId: PanelId;
  title: string;
  children: ReactNode;
  basis?: SourceBasis;
  isMock?: boolean;
  /** Badge count for waiting content (validation, artifacts, proposals, diagnostics) */
  badgeCount?: number;
}

/** Panels that are always relevant regardless of active object */
const ALWAYS_RELEVANT: PanelId[] = ['work', 'system'];

/** Panels that are relevant when a specific object type is active */
const RELEVANCE_MAP: Record<string, PanelId[]> = {
  element: ['explorer', 'work', 'reference', 'spatial', 'diagnostics', 'awareness'],
  assembly: ['explorer', 'work', 'reference', 'spatial', 'diagnostics', 'awareness'],
  zone: ['explorer', 'spatial', 'work', 'awareness'],
  document: ['explorer', 'work', 'reference'],
  specification: ['explorer', 'work', 'reference'],
  project: ['explorer', 'work', 'system', 'awareness'],
};

export function PanelShell({ panelId, title, children, basis = 'mock', isMock = true, badgeCount }: PanelShellProps) {
  const { activeObject, sourcePanel, lastEchoTimestamp, echoFailure, workspaceMode } = useActiveObject();
  const [echoFlash, setEchoFlash] = useState(false);

  // Truth Echo visual sync — flash when this panel receives echo from another panel
  useEffect(() => {
    if (sourcePanel && sourcePanel !== panelId && lastEchoTimestamp > 0) {
      setEchoFlash(true);
      const timer = setTimeout(() => setEchoFlash(false), 600);
      return () => clearTimeout(timer);
    }
  }, [lastEchoTimestamp, sourcePanel, panelId]);

  const isEchoSource = sourcePanel === panelId;

  // Context Collapse: determine if this panel is relevant to the current gravity object
  const isContextCollapsed = (() => {
    if (workspaceMode !== 'focus') return false;
    if (!activeObject) return false;
    if (ALWAYS_RELEVANT.includes(panelId)) return false;
    const relevant = RELEVANCE_MAP[activeObject.type] ?? [];
    return !relevant.includes(panelId);
  })();

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        background: tokens.color.bgSurface,
        borderRadius: tokens.radius.sm,
        overflow: 'hidden',
        opacity: isContextCollapsed ? 0.4 : 1,
        transition: `opacity ${tokens.transition.normal}`,
        position: 'relative',
      }}
      className={echoFlash ? 'truth-echo-active' : ''}
    >
      {/* Panel Header — refined visual hierarchy */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: `${tokens.space.sm} ${tokens.space.md}`,
          background: tokens.color.bgElevated,
          borderBottom: `1px solid ${tokens.color.border}`,
          minHeight: '40px',
          gap: tokens.space.sm,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <span
            style={{
              fontSize: tokens.font.sizeMd,
              fontWeight: tokens.font.weightSemibold,
              color: tokens.color.fgPrimary,
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              lineHeight: tokens.font.lineTight,
            }}
          >
            {title}
          </span>
          {/* Panel sublabel — visually distinct from title */}
          {isContextCollapsed && (
            <span style={{
              fontSize: tokens.font.sizeXs,
              color: tokens.color.fgMuted,
              fontStyle: 'italic',
            }}>
              collapsed
            </span>
          )}
          {isEchoSource && (
            <span
              style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                background: tokens.color.echoActive,
                boxShadow: `0 0 6px ${tokens.color.echoActive}`,
              }}
            />
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.xs }}>
          {/* Badge dot for waiting content */}
          {badgeCount != null && badgeCount > 0 && (
            <span style={{
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              minWidth: '18px',
              height: '18px',
              padding: '0 4px',
              borderRadius: '9px',
              background: tokens.color.accentPrimary,
              color: '#fff',
              fontSize: '0.7rem',
              fontWeight: tokens.font.weightBold,
              lineHeight: '1',
            }}>
              {badgeCount > 99 ? '99+' : badgeCount}
            </span>
          )}
          <span
            style={{
              fontSize: tokens.font.sizeXs,
              color: tokens.color[basis] ?? tokens.color.fgMuted,
              padding: '2px 8px',
              borderRadius: tokens.radius.sm,
              background: `${tokens.color[basis] ?? tokens.color.fgMuted}15`,
              lineHeight: tokens.font.lineNormal,
            }}
          >
            {basis}
          </span>
        </div>
      </div>

      {/* Active Object Bar — shows what this panel is oriented around */}
      {activeObject && !isContextCollapsed && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: tokens.space.sm,
            padding: `${tokens.space.xs} ${tokens.space.md}`,
            background: tokens.color.echoTrace,
            borderBottom: `1px solid ${tokens.color.borderSubtle}`,
            fontSize: tokens.font.sizeXs,
            lineHeight: tokens.font.lineNormal,
            color: tokens.color.fgSecondary,
          }}
        >
          <span style={{ color: tokens.color.echoActive, fontWeight: tokens.font.weightMedium }}>
            ACTIVE
          </span>
          <span style={{ color: tokens.color.fgPrimary }}>
            {activeObject.name}
          </span>
          <span style={{ color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
            {activeObject.id}
          </span>
          <span style={{ color: tokens.color.fgMuted }}>
            {activeObject.type}
          </span>
        </div>
      )}

      {/* Context Collapse Summary — shows when panel is collapsed */}
      {isContextCollapsed && activeObject && (
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          padding: tokens.space.lg,
          color: tokens.color.fgMuted,
          fontSize: tokens.font.sizeXs,
          fontStyle: 'italic',
          textAlign: 'center',
          flex: 1,
        }}>
          Panel dimmed — not relevant to {activeObject.type}: {activeObject.name}
        </div>
      )}

      {/* Echo Failure Warning */}
      {echoFailure && !isContextCollapsed && (
        <div
          style={{
            padding: `${tokens.space.sm} ${tokens.space.md}`,
            background: 'rgba(239,68,68,0.1)',
            borderBottom: `1px solid ${tokens.color.error}`,
            fontSize: tokens.font.sizeXs,
            lineHeight: tokens.font.lineNormal,
            color: tokens.color.error,
          }}
        >
          Truth Echo Failed: {echoFailure}
        </div>
      )}

      {/* Panel Content */}
      {!isContextCollapsed && (
        <div style={{ flex: 1, overflow: 'auto', padding: tokens.space.md, lineHeight: tokens.font.lineNormal }}>
          {children}
        </div>
      )}
    </div>
  );
}
