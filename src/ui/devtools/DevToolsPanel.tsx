/**
 * Construction OS — Dev Tools Panel
 *
 * Isolated development/debug-only area for MOCK controls
 * and dev diagnostics. Visible only when devToolsVisible is true
 * in the activeObjectStore (development mode or explicit debug toggle).
 *
 * Consolidates all dev-only controls that were previously
 * scattered across panel headers.
 */

import { useCallback, useState } from 'react';
import { tokens } from '../theme/tokens';
import { activeObjectStore, type AuthorityLevel } from '../stores/activeObjectStore';
import { useActiveObject } from '../stores/useSyncExternalStore';
import { eventBus } from '../events/EventBus';

export function DevToolsPanel() {
  const { authorityLevel, workspaceMode, activeObject, devToolsVisible } = useActiveObject();
  const [eventLogOpen, setEventLogOpen] = useState(false);

  const handleSetAuthority = useCallback((level: AuthorityLevel) => {
    activeObjectStore.setAuthorityLevel(level);
  }, []);

  const handleSetMode = useCallback((mode: 'default' | 'compare' | 'focus' | 'review') => {
    activeObjectStore.setWorkspaceMode(mode);
  }, []);

  const handleToggleOverlay = useCallback(() => {
    activeObjectStore.setOverlayActive(true);
  }, []);

  const handleEmitTestEvent = useCallback(() => {
    if (activeObject) {
      eventBus.emit('validation.requested', {
        objectId: activeObject.id,
        validationType: 'full',
        source: 'system',
      });
    }
  }, [activeObject]);

  if (!devToolsVisible) return null;

  const eventLog = eventBus.getLog().slice(-20).reverse();

  return (
    <div style={{
      position: 'fixed',
      right: tokens.space.md,
      top: '52px',
      width: '320px',
      maxHeight: '80vh',
      background: tokens.color.bgSurface,
      border: `1px solid ${tokens.color.mock}40`,
      borderRadius: tokens.radius.md,
      boxShadow: tokens.shadow.elevated,
      zIndex: 9000,
      overflow: 'auto',
      fontSize: tokens.font.sizeXs,
    }}>
      {/* Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: `${tokens.color.mock}15`,
        borderBottom: `1px solid ${tokens.color.mock}40`,
      }}>
        <span style={{
          color: tokens.color.mock,
          fontWeight: tokens.font.weightSemibold,
          letterSpacing: '0.05em',
          fontFamily: tokens.font.familyMono,
        }}>
          DEV TOOLS
        </span>
        <button
          onClick={() => activeObjectStore.setDevToolsVisible(false)}
          style={{
            background: 'none',
            border: 'none',
            color: tokens.color.fgMuted,
            cursor: 'pointer',
            fontSize: tokens.font.sizeSm,
            padding: tokens.space.xs,
          }}
        >
          {'\u2715'}
        </button>
      </div>

      <div style={{ padding: tokens.space.md }}>
        {/* Mock Adapter Status */}
        <DevSection title="MOCK ADAPTERS">
          <div style={{
            padding: tokens.space.sm,
            background: `${tokens.color.mock}10`,
            borderRadius: tokens.radius.sm,
            color: tokens.color.mock,
            fontFamily: tokens.font.familyMono,
          }}>
            All adapters: MOCK
          </div>
        </DevSection>

        {/* Authority Level Switcher */}
        <DevSection title="AUTHORITY LEVEL (display only)">
          <div style={{ display: 'flex', gap: tokens.space.xs }}>
            {(['L3', 'L2', 'L1'] as AuthorityLevel[]).map((level) => (
              <button
                key={level}
                onClick={() => handleSetAuthority(level)}
                style={{
                  flex: 1,
                  padding: tokens.space.sm,
                  background: authorityLevel === level ? tokens.color.bgActive : tokens.color.bgBase,
                  color: authorityLevel === level
                    ? (level === 'L3' ? tokens.color.authorityL3 : level === 'L2' ? tokens.color.authorityL2 : tokens.color.authorityL1)
                    : tokens.color.fgMuted,
                  border: `1px solid ${authorityLevel === level ? tokens.color.borderActive : tokens.color.border}`,
                  borderRadius: tokens.radius.sm,
                  cursor: 'pointer',
                  fontSize: tokens.font.sizeXs,
                  fontWeight: tokens.font.weightSemibold,
                  fontFamily: tokens.font.familyMono,
                }}
              >
                {level}
              </button>
            ))}
          </div>
        </DevSection>

        {/* Workspace Mode */}
        <DevSection title="WORKSPACE MODE">
          <div style={{ display: 'flex', gap: tokens.space.xs, flexWrap: 'wrap' }}>
            {(['default', 'compare', 'focus', 'review'] as const).map((mode) => (
              <button
                key={mode}
                onClick={() => handleSetMode(mode)}
                style={{
                  padding: `${tokens.space.xs} ${tokens.space.sm}`,
                  background: workspaceMode === mode ? tokens.color.bgActive : tokens.color.bgBase,
                  color: workspaceMode === mode ? tokens.color.fgPrimary : tokens.color.fgMuted,
                  border: `1px solid ${workspaceMode === mode ? tokens.color.borderActive : tokens.color.border}`,
                  borderRadius: tokens.radius.sm,
                  cursor: 'pointer',
                  fontSize: tokens.font.sizeXs,
                  fontFamily: tokens.font.family,
                }}
              >
                {mode}
              </button>
            ))}
          </div>
        </DevSection>

        {/* Quick Actions */}
        <DevSection title="QUICK ACTIONS">
          <div style={{ display: 'flex', flexDirection: 'column', gap: tokens.space.xs }}>
            <DevActionButton label="Open Overlay" onClick={handleToggleOverlay} />
            <DevActionButton label="Emit Test Validation" onClick={handleEmitTestEvent} />
            <DevActionButton
              label={eventLogOpen ? 'Hide Event Log' : 'Show Event Log'}
              onClick={() => setEventLogOpen(!eventLogOpen)}
            />
          </div>
        </DevSection>

        {/* Event Log */}
        {eventLogOpen && (
          <DevSection title="EVENT LOG (last 20)">
            <div style={{ maxHeight: '200px', overflow: 'auto' }}>
              {eventLog.length === 0 ? (
                <span style={{ color: tokens.color.fgMuted }}>No events</span>
              ) : (
                eventLog.map((entry, i) => (
                  <div key={i} style={{
                    padding: `${tokens.space.xs} ${tokens.space.sm}`,
                    marginBottom: '1px',
                    background: i % 2 === 0 ? tokens.color.bgBase : 'transparent',
                    fontFamily: tokens.font.familyMono,
                    lineHeight: tokens.font.lineNormal,
                  }}>
                    <span style={{ color: tokens.color.accentPrimary }}>{entry.event}</span>
                    <span style={{ color: tokens.color.fgMuted, marginLeft: tokens.space.sm }}>
                      {new Date(entry.timestamp).toLocaleTimeString()}
                    </span>
                  </div>
                ))
              )}
            </div>
          </DevSection>
        )}

        {/* Active Object */}
        <DevSection title="ACTIVE OBJECT">
          {activeObject ? (
            <div style={{
              padding: tokens.space.sm,
              background: tokens.color.bgBase,
              borderRadius: tokens.radius.sm,
              fontFamily: tokens.font.familyMono,
              lineHeight: tokens.font.lineNormal,
            }}>
              <div style={{ color: tokens.color.fgPrimary }}>{activeObject.name}</div>
              <div style={{ color: tokens.color.fgMuted }}>{activeObject.id} ({activeObject.type})</div>
            </div>
          ) : (
            <span style={{ color: tokens.color.fgMuted }}>None selected</span>
          )}
        </DevSection>
      </div>
    </div>
  );
}

// ─── Helpers ──────────────────────────────────────────────────────────────

function DevSection({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <div style={{ marginBottom: tokens.space.md }}>
      <div style={{
        fontSize: tokens.font.sizeXs,
        color: tokens.color.fgMuted,
        fontWeight: tokens.font.weightSemibold,
        letterSpacing: '0.05em',
        marginBottom: tokens.space.sm,
      }}>
        {title}
      </div>
      {children}
    </div>
  );
}

function DevActionButton({ label, onClick }: { label: string; onClick: () => void }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: tokens.color.bgBase,
        color: tokens.color.fgSecondary,
        border: `1px solid ${tokens.color.border}`,
        borderRadius: tokens.radius.sm,
        cursor: 'pointer',
        fontSize: tokens.font.sizeXs,
        fontFamily: tokens.font.family,
        textAlign: 'left',
      }}
    >
      {label}
    </button>
  );
}
