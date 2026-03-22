/**
 * Construction OS — Workspace Shell
 *
 * Dockview-based multi-panel workspace with docking, resize, and movement.
 * Implements HERO_COCKPIT_DEFAULT preset and Command Deck activation.
 * No page-based navigation — panels are live systems.
 *
 * Cockpit Upgrade (VKGL04R):
 * - Authority HUD in top header (awareness only)
 * - Bottom Dock consolidation for lower panels
 * - Command Palette (CMD+K / CTRL+K)
 * - Dev Control Isolation (dev tools toggle)
 * - Visual hierarchy: Work panel visually dominant
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import {
  DockviewReact,
  type DockviewReadyEvent,
  type IDockviewPanelProps,
} from 'dockview-react';
import 'dockview-react/dist/styles/dockview.css';

import { ExplorerPanel } from '../panels/explorer/ExplorerPanel';
import { WorkPanel } from '../panels/work/WorkPanel';
import { ReferencePanel } from '../panels/reference/ReferencePanel';
import { SpatialPanel } from '../panels/spatial/SpatialPanel';
import { SystemPanel } from '../panels/system/SystemPanel';
import { AwarenessPanel } from '../panels/awareness/AwarenessPanel';
import { ProposalMailbox } from '../panels/proposals/ProposalMailbox';
import { RuntimeDiagnosticsPanel } from '../panels/diagnostics/RuntimeDiagnosticsPanel';
import { AssistantConsole } from '../panels/assistant/AssistantConsole';
import { DeckPicker } from '../decks/DeckPicker';
import { AuthorityHUD } from '../components/AuthorityHUD';
import { CommandPalette } from '../components/CommandPalette';
import { BottomDock } from '../layout/BottomDock';
import { DevToolsPanel } from '../devtools/DevToolsPanel';
import { initTruthEcho, destroyTruthEcho } from '../orchestration/TruthEcho';
import { detectDeviceClass, getDeviceLayout } from '../orchestration/DeviceOrchestrator';
import { activeObjectStore } from '../stores/activeObjectStore';
import { useActiveObject } from '../stores/useSyncExternalStore';
import { tokens } from '../theme/tokens';
import type { DeviceClass, PanelId } from '../contracts/events';

// ─── Panel Component Map ────────────────────────────────────────────────────

function ExplorerWrapper(_props: IDockviewPanelProps) { return <ExplorerPanel />; }
function WorkWrapper(_props: IDockviewPanelProps) { return <WorkPanel />; }
function ReferenceWrapper(_props: IDockviewPanelProps) { return <ReferencePanel />; }
function SpatialWrapper(_props: IDockviewPanelProps) { return <SpatialPanel />; }
function SystemWrapper(_props: IDockviewPanelProps) { return <SystemPanel />; }
function AwarenessWrapper(_props: IDockviewPanelProps) { return <AwarenessPanel />; }
function ProposalsWrapper(_props: IDockviewPanelProps) { return <ProposalMailbox />; }
function DiagnosticsWrapper(_props: IDockviewPanelProps) { return <RuntimeDiagnosticsPanel />; }
function AssistantWrapper(_props: IDockviewPanelProps) { return <AssistantConsole />; }

const PANEL_COMPONENTS: Record<string, React.FC<IDockviewPanelProps>> = {
  explorer: ExplorerWrapper,
  work: WorkWrapper,
  reference: ReferenceWrapper,
  spatial: SpatialWrapper,
  system: SystemWrapper,
  awareness: AwarenessWrapper,
  proposals: ProposalsWrapper,
  diagnostics: DiagnosticsWrapper,
  assistant: AssistantWrapper,
};

// ─── Top row panels (in Dockview) ────────────────────────────────────────
// Bottom panels are now in the BottomDock component.

const TOP_PANELS: PanelId[] = ['explorer', 'work', 'reference'];

// ─── Workspace Presets ──────────────────────────────────────────────────────

type PresetName = 'HERO_COCKPIT_DEFAULT';

function applyPreset(api: DockviewReadyEvent['api'], preset: PresetName, deviceClass: DeviceClass) {
  // Clear existing panels
  api.panels.forEach((p) => api.removePanel(p));

  if (preset === 'HERO_COCKPIT_DEFAULT') {
    if (deviceClass === 'phone') {
      // Phone: single primary + companion accessible
      api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
      activeObjectStore.setPinnedCompanion('explorer');
    } else if (deviceClass === 'tablet') {
      // Tablet: 2 panels
      const workPanel = api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
      api.addPanel({ id: 'explorer', component: 'explorer', title: 'EXPLORER', position: { referencePanel: workPanel, direction: 'left' } });
    } else {
      // Laptop / Desktop / Ultrawide: Top 3 panels in dockview + bottom dock
      const workPanel = api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
      api.addPanel({ id: 'explorer', component: 'explorer', title: 'EXPLORER', position: { referencePanel: workPanel, direction: 'left' } });
      api.addPanel({ id: 'reference', component: 'reference', title: 'REFERENCE', position: { referencePanel: workPanel, direction: 'right' } });
    }
  }
}

// ─── Phone Companion Switcher ───────────────────────────────────────────────

function CompanionSwitcher({ onSwitch, currentPanel }: { onSwitch: (panel: PanelId) => void; currentPanel: PanelId | null }) {
  const panels: { id: PanelId; label: string }[] = [
    { id: 'explorer', label: 'EXP' },
    { id: 'work', label: 'WRK' },
    { id: 'reference', label: 'REF' },
    { id: 'spatial', label: 'SPA' },
    { id: 'system', label: 'SYS' },
    { id: 'awareness', label: 'AWR' },
    { id: 'proposals', label: 'PRP' },
    { id: 'diagnostics', label: 'DGN' },
    { id: 'assistant', label: 'AST' },
  ];

  return (
    <div style={{
      display: 'flex',
      gap: '1px',
      background: tokens.color.border,
      borderRadius: tokens.radius.sm,
      overflow: 'hidden',
      padding: 0,
    }}>
      {panels.map((p) => (
        <button
          key={p.id}
          onClick={() => onSwitch(p.id)}
          style={{
            flex: 1,
            padding: `${tokens.space.sm} ${tokens.space.xs}`,
            background: currentPanel === p.id ? tokens.color.bgActive : tokens.color.bgElevated,
            color: currentPanel === p.id ? tokens.color.accentPrimary : tokens.color.fgMuted,
            border: 'none',
            cursor: 'pointer',
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            fontFamily: tokens.font.family,
          }}
        >
          {p.label}
        </button>
      ))}
    </div>
  );
}

// ─── Workspace Shell ────────────────────────────────────────────────────────

export function WorkspaceShell() {
  const [deviceClass, setDeviceClass] = useState<DeviceClass>(detectDeviceClass);
  const apiRef = useRef<DockviewReadyEvent['api'] | null>(null);
  const [isPhoneMode, setIsPhoneMode] = useState(deviceClass === 'phone');
  const [phonePanel, setPhonePanel] = useState<PanelId>('work');
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);
  const { devToolsVisible } = useActiveObject();

  const showBottomDock = deviceClass !== 'phone' && deviceClass !== 'tablet';

  // Initialize Truth Echo
  useEffect(() => {
    initTruthEcho();
    return () => destroyTruthEcho();
  }, []);

  // Device class detection
  useEffect(() => {
    const handleResize = () => {
      const newClass = detectDeviceClass();
      if (newClass !== deviceClass) {
        setDeviceClass(newClass);
        activeObjectStore.setDeviceClass(newClass);
        setIsPhoneMode(newClass === 'phone');
        if (apiRef.current) {
          applyPreset(apiRef.current, 'HERO_COCKPIT_DEFAULT', newClass);
        }
      }
    };
    window.addEventListener('resize', handleResize);
    activeObjectStore.setDeviceClass(deviceClass);
    return () => window.removeEventListener('resize', handleResize);
  }, [deviceClass]);

  // Command Palette keyboard shortcut (CMD+K / CTRL+K)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setCommandPaletteOpen((prev) => !prev);
      }
      if (e.key === 'Escape' && commandPaletteOpen) {
        setCommandPaletteOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [commandPaletteOpen]);

  const handleReady = useCallback((event: DockviewReadyEvent) => {
    apiRef.current = event.api;
    applyPreset(event.api, 'HERO_COCKPIT_DEFAULT', deviceClass);
  }, [deviceClass]);

  const handlePhoneSwitch = useCallback((panelId: PanelId) => {
    setPhonePanel(panelId);
    if (apiRef.current) {
      apiRef.current.panels.forEach((p) => apiRef.current!.removePanel(p));
      apiRef.current.addPanel({ id: panelId, component: panelId, title: panelId.toUpperCase() });
    }
  }, []);

  // ─── Deck Layout Application ──────────────────────────────────────────────

  const applyDeckLayout = useCallback((visiblePanels: readonly PanelId[], promotedPanel: PanelId) => {
    if (!apiRef.current) return;
    const api = apiRef.current;

    api.panels.forEach((p) => api.removePanel(p));

    if (visiblePanels.length === 0) return;

    const promoted = api.addPanel({
      id: promotedPanel,
      component: promotedPanel,
      title: promotedPanel.toUpperCase(),
    });

    const remaining = visiblePanels.filter((p) => p !== promotedPanel);
    let lastLeft = promoted;
    let lastRight = promoted;
    let lastBelow = promoted;

    for (let i = 0; i < remaining.length; i++) {
      const panelId = remaining[i];
      if (i % 3 === 0) {
        lastRight = api.addPanel({
          id: panelId,
          component: panelId,
          title: panelId.toUpperCase(),
          position: { referencePanel: lastRight, direction: 'right' },
        });
      } else if (i % 3 === 1) {
        lastLeft = api.addPanel({
          id: panelId,
          component: panelId,
          title: panelId.toUpperCase(),
          position: { referencePanel: promoted, direction: 'below' },
        });
        lastBelow = lastLeft;
      } else {
        api.addPanel({
          id: panelId,
          component: panelId,
          title: panelId.toUpperCase(),
          position: { referencePanel: lastBelow, direction: 'right' },
        });
      }
    }
  }, []);

  const handleToggleDevTools = useCallback(() => {
    activeObjectStore.setDevToolsVisible(!devToolsVisible);
  }, [devToolsVisible]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: tokens.color.bgDeep, minHeight: 0 }}>
      {/* Status Bar with Authority HUD */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: tokens.color.bgBase,
        borderBottom: `1px solid ${tokens.color.border}`,
        minHeight: '40px',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.md }}>
          <span style={{
            fontSize: tokens.font.sizeMd,
            fontWeight: tokens.font.weightBold,
            color: tokens.color.fgPrimary,
            letterSpacing: '0.08em',
            lineHeight: tokens.font.lineTight,
          }}>
            CONSTRUCTION OS
          </span>
          <span style={{
            fontSize: tokens.font.sizeXs,
            color: tokens.color.fgMuted,
            fontFamily: tokens.font.familyMono,
          }}>
            WORKSTATION
          </span>
          {/* Authority HUD — awareness only */}
          <AuthorityHUD />
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <DeckPicker applyLayout={applyDeckLayout} />
          {/* Command Palette trigger */}
          <button
            onClick={() => setCommandPaletteOpen(true)}
            style={{
              padding: `${tokens.space.xs} ${tokens.space.sm}`,
              background: tokens.color.bgElevated,
              color: tokens.color.fgMuted,
              border: `1px solid ${tokens.color.border}`,
              borderRadius: tokens.radius.sm,
              cursor: 'pointer',
              fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.familyMono,
              display: 'flex',
              alignItems: 'center',
              gap: tokens.space.xs,
            }}
            title="Command Palette (Ctrl+K / Cmd+K)"
          >
            {'\u2318'}K
          </button>
          {/* Dev Tools toggle — isolated from panel headers */}
          <button
            onClick={handleToggleDevTools}
            style={{
              padding: `${tokens.space.xs} ${tokens.space.sm}`,
              background: devToolsVisible ? `${tokens.color.mock}15` : tokens.color.bgElevated,
              color: devToolsVisible ? tokens.color.mock : tokens.color.fgMuted,
              border: `1px solid ${devToolsVisible ? tokens.color.mock + '40' : tokens.color.border}`,
              borderRadius: tokens.radius.sm,
              cursor: 'pointer',
              fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.familyMono,
            }}
            title="Toggle Dev Tools"
          >
            DEV
          </button>
          <span style={{
            fontSize: tokens.font.sizeXs,
            color: tokens.color.fgMuted,
            fontFamily: tokens.font.familyMono,
          }}>
            {deviceClass.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Main Workspace — Dockview (top panels: Explorer | Work | Reference) */}
      <div style={{ flex: 1, overflow: 'hidden', minHeight: 0 }}>
        <DockviewReact
          className="dockview-theme-dark"
          onReady={handleReady}
          components={PANEL_COMPONENTS}
        />
      </div>

      {/* Bottom Dock — consolidated lower panels */}
      {showBottomDock && <BottomDock />}

      {/* Phone Companion Switcher */}
      {isPhoneMode && (
        <CompanionSwitcher onSwitch={handlePhoneSwitch} currentPanel={phonePanel} />
      )}

      {/* Command Palette Overlay */}
      {commandPaletteOpen && (
        <CommandPalette onClose={() => setCommandPaletteOpen(false)} />
      )}

      {/* Dev Tools Panel — isolated from panel chrome */}
      <DevToolsPanel />
    </div>
  );
}
