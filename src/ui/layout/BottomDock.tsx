/**
 * Construction OS — Bottom Dock
 *
 * Replaces crowded simultaneous lower panels with a docked bottom drawer.
 * Tabs: Awareness | Diagnostics | Proposals | Spatial | Assistant | System
 *
 * - One open at a time by default
 * - Preserves panel state when switching tabs
 * - Supports expand / collapse / pin
 * - Non-destructive: collapsed panels remain recoverable
 */

import { useCallback, useState } from 'react';
import { tokens } from '../theme/tokens';
import { AwarenessPanel } from '../panels/awareness/AwarenessPanel';
import { RuntimeDiagnosticsPanel } from '../panels/diagnostics/RuntimeDiagnosticsPanel';
import { ProposalMailbox } from '../panels/proposals/ProposalMailbox';
import { SpatialPanel } from '../panels/spatial/SpatialPanel';
import { AssistantConsole } from '../panels/assistant/AssistantConsole';
import { SystemPanel } from '../panels/system/SystemPanel';

export type DockTab = 'awareness' | 'diagnostics' | 'proposals' | 'spatial' | 'assistant' | 'system';

interface DockTabConfig {
  id: DockTab;
  label: string;
  badge?: number;
}

const DOCK_TABS: DockTabConfig[] = [
  { id: 'awareness', label: 'Awareness' },
  { id: 'diagnostics', label: 'Diagnostics' },
  { id: 'proposals', label: 'Proposals' },
  { id: 'spatial', label: 'Spatial' },
  { id: 'assistant', label: 'Assistant' },
  { id: 'system', label: 'System' },
];

export function BottomDock() {
  const [activeTab, setActiveTab] = useState<DockTab>('awareness');
  const [expanded, setExpanded] = useState(false);
  const [collapsed, setCollapsed] = useState(false);
  const [pinned, setPinned] = useState(false);

  const handleToggleExpand = useCallback(() => {
    if (collapsed) {
      setCollapsed(false);
    } else {
      setExpanded((prev) => !prev);
    }
  }, [collapsed]);

  const handleToggleCollapse = useCallback(() => {
    setCollapsed((prev) => !prev);
    if (!collapsed) setExpanded(false);
  }, [collapsed]);

  const handleTogglePin = useCallback(() => {
    setPinned((prev) => !prev);
  }, []);

  const handleTabClick = useCallback((tab: DockTab) => {
    if (collapsed) setCollapsed(false);
    setActiveTab(tab);
  }, [collapsed]);

  const dockHeight = collapsed ? '36px' : expanded ? '55vh' : '280px';

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: dockHeight,
      minHeight: collapsed ? '36px' : '120px',
      maxHeight: expanded ? '55vh' : '380px',
      background: tokens.color.bgSurface,
      borderTop: `1px solid ${tokens.color.border}`,
      transition: `height ${tokens.transition.normal}`,
      overflow: 'hidden',
      flexShrink: 0,
    }}>
      {/* Dock Tab Bar */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        minHeight: '36px',
        background: tokens.color.bgElevated,
        borderBottom: collapsed ? 'none' : `1px solid ${tokens.color.border}`,
        flexShrink: 0,
      }}>
        {/* Tab Buttons */}
        <div style={{
          display: 'flex',
          flex: 1,
          gap: '1px',
          overflow: 'hidden',
        }}>
          {DOCK_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => handleTabClick(tab.id)}
              style={{
                flex: 1,
                padding: `${tokens.space.sm} ${tokens.space.sm}`,
                background: activeTab === tab.id && !collapsed
                  ? tokens.color.bgActive
                  : 'transparent',
                color: activeTab === tab.id && !collapsed
                  ? tokens.color.fgPrimary
                  : tokens.color.fgMuted,
                border: 'none',
                borderBottom: activeTab === tab.id && !collapsed
                  ? `2px solid ${tokens.color.accentPrimary}`
                  : '2px solid transparent',
                cursor: 'pointer',
                fontSize: tokens.font.sizeXs,
                fontWeight: activeTab === tab.id ? tokens.font.weightSemibold : tokens.font.weightNormal,
                fontFamily: tokens.font.family,
                lineHeight: tokens.font.lineTight,
                transition: `all ${tokens.transition.fast}`,
                whiteSpace: 'nowrap',
              }}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Dock Controls */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: '2px',
          padding: `0 ${tokens.space.sm}`,
          flexShrink: 0,
        }}>
          <DockControlButton
            label={pinned ? '\u25C9' : '\u25CB'}
            title={pinned ? 'Unpin dock' : 'Pin dock'}
            active={pinned}
            onClick={handleTogglePin}
          />
          <DockControlButton
            label={expanded ? '\u25BC' : '\u25B2'}
            title={expanded ? 'Shrink dock' : 'Expand dock'}
            active={expanded}
            onClick={handleToggleExpand}
          />
          <DockControlButton
            label={collapsed ? '\u25B2' : '\u25BC'}
            title={collapsed ? 'Show dock' : 'Collapse dock'}
            active={false}
            onClick={handleToggleCollapse}
          />
        </div>
      </div>

      {/* Dock Content — all panels rendered but only active one visible */}
      {!collapsed && (
        <div style={{ flex: 1, overflow: 'hidden', position: 'relative', minHeight: 0 }}>
          <DockPanelContainer visible={activeTab === 'awareness'}>
            <AwarenessPanel />
          </DockPanelContainer>
          <DockPanelContainer visible={activeTab === 'diagnostics'}>
            <RuntimeDiagnosticsPanel />
          </DockPanelContainer>
          <DockPanelContainer visible={activeTab === 'proposals'}>
            <ProposalMailbox />
          </DockPanelContainer>
          <DockPanelContainer visible={activeTab === 'spatial'}>
            <SpatialPanel />
          </DockPanelContainer>
          <DockPanelContainer visible={activeTab === 'assistant'}>
            <AssistantConsole />
          </DockPanelContainer>
          <DockPanelContainer visible={activeTab === 'system'}>
            <SystemPanel />
          </DockPanelContainer>
        </div>
      )}
    </div>
  );
}

// ─── Dock Panel Container ──────────────────────────────────────────────────
// Preserves panel state by keeping all panels mounted but hiding inactive ones.

function DockPanelContainer({ visible, children }: { visible: boolean; children: React.ReactNode }) {
  return (
    <div style={{
      position: 'absolute',
      inset: 0,
      display: visible ? 'flex' : 'none',
      flexDirection: 'column',
      overflow: 'hidden',
    }}>
      {children}
    </div>
  );
}

// ─── Dock Control Button ───────────────────────────────────────────────────

function DockControlButton({
  label,
  title,
  active,
  onClick,
}: {
  label: string;
  title: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      title={title}
      style={{
        width: '24px',
        height: '24px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: active ? tokens.color.bgActive : 'transparent',
        color: active ? tokens.color.fgPrimary : tokens.color.fgMuted,
        border: 'none',
        borderRadius: tokens.radius.sm,
        cursor: 'pointer',
        fontSize: tokens.font.sizeXs,
        padding: 0,
      }}
    >
      {label}
    </button>
  );
}
