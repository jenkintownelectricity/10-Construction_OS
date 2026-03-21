/**
 * Construction OS — Panel Shell
 * Common wrapper for all panel systems. Provides Truth Echo visual feedback,
 * source basis indicator, and consistent panel chrome.
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
}

export function PanelShell({ panelId, title, children, basis = 'mock', isMock = true }: PanelShellProps) {
  const { activeObject, sourcePanel, lastEchoTimestamp, echoFailure } = useActiveObject();
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

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column',
        height: '100%',
        background: tokens.color.bgSurface,
        borderRadius: tokens.radius.sm,
        overflow: 'hidden',
      }}
      className={echoFlash ? 'truth-echo-active' : ''}
    >
      {/* Panel Header */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: `${tokens.space.xs} ${tokens.space.md}`,
          background: tokens.color.bgElevated,
          borderBottom: `1px solid ${tokens.color.border}`,
          minHeight: '32px',
          gap: tokens.space.sm,
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <span
            style={{
              fontSize: tokens.font.sizeSm,
              fontWeight: tokens.font.weightSemibold,
              color: tokens.color.fgPrimary,
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
            }}
          >
            {title}
          </span>
          {isEchoSource && (
            <span
              style={{
                width: '6px',
                height: '6px',
                borderRadius: '50%',
                background: tokens.color.echoActive,
                boxShadow: `0 0 6px ${tokens.color.echoActive}`,
              }}
            />
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.xs }}>
          {isMock && (
            <span
              style={{
                fontSize: tokens.font.sizeXs,
                color: tokens.color.mock,
                background: 'rgba(249,115,22,0.1)',
                padding: '1px 6px',
                borderRadius: tokens.radius.sm,
                fontWeight: tokens.font.weightMedium,
              }}
            >
              MOCK
            </span>
          )}
          <span
            style={{
              fontSize: tokens.font.sizeXs,
              color: tokens.color[basis] ?? tokens.color.fgMuted,
              padding: '1px 6px',
              borderRadius: tokens.radius.sm,
              background: `${tokens.color[basis] ?? tokens.color.fgMuted}15`,
            }}
          >
            {basis}
          </span>
        </div>
      </div>

      {/* Active Object Bar — shows what this panel is oriented around */}
      {activeObject && (
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: tokens.space.sm,
            padding: `${tokens.space.xs} ${tokens.space.md}`,
            background: tokens.color.echoTrace,
            borderBottom: `1px solid ${tokens.color.borderSubtle}`,
            fontSize: tokens.font.sizeXs,
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

      {/* Echo Failure Warning */}
      {echoFailure && (
        <div
          style={{
            padding: `${tokens.space.xs} ${tokens.space.md}`,
            background: 'rgba(239,68,68,0.1)',
            borderBottom: `1px solid ${tokens.color.error}`,
            fontSize: tokens.font.sizeXs,
            color: tokens.color.error,
          }}
        >
          Truth Echo Failed: {echoFailure}
        </div>
      )}

      {/* Panel Content */}
      <div style={{ flex: 1, overflow: 'auto', padding: tokens.space.md }}>
        {children}
      </div>
    </div>
  );
}
