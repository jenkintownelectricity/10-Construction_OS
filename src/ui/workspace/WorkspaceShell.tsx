/**
 * Construction OS — Workspace Shell
 *
 * Dockview-based multi-panel workspace with docking, resize, and movement.
 * Implements HERO_COCKPIT_DEFAULT preset and Command Deck activation.
 * No page-based navigation — panels are live systems.
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
import { initTruthEcho, destroyTruthEcho } from '../orchestration/TruthEcho';
import { detectDeviceClass, getDeviceLayout } from '../orchestration/DeviceOrchestrator';
import { activeObjectStore } from '../stores/activeObjectStore';
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

// ─── Workspace Presets ──────────────────────────────────────────────────────

type PresetName = 'HERO_COCKPIT_DEFAULT';

function applyPreset(api: DockviewReadyEvent['api'], preset: PresetName, deviceClass: DeviceClass) {
  const layout = getDeviceLayout(deviceClass);

  // Clear existing panels
  api.panels.forEach((p) => api.removePanel(p));

  if (preset === 'HERO_COCKPIT_DEFAULT') {
    if (deviceClass === 'phone') {
      // Phone: single primary + companion accessible
      api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
      // Companion panel available but not visible by default
      activeObjectStore.setPinnedCompanion('explorer');
    } else if (deviceClass === 'tablet') {
      // Tablet: 2 panels
      const workPanel = api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
      api.addPanel({ id: 'explorer', component: 'explorer', title: 'EXPLORER', position: { referencePanel: workPanel, direction: 'left' } });
    } else if (deviceClass === 'laptop') {
      // Laptop: 3 panels
      const workPanel = api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
      api.addPanel({ id: 'explorer', component: 'explorer', title: 'EXPLORER', position: { referencePanel: workPanel, direction: 'left' } });
      api.addPanel({ id: 'reference', component: 'reference', title: 'REFERENCE', position: { referencePanel: workPanel, direction: 'right' } });
    } else {
      // Desktop / Ultrawide: full cockpit with governance panels
      // Top row: Explorer | Work | Reference
      const workPanel = api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
      api.addPanel({ id: 'explorer', component: 'explorer', title: 'EXPLORER', position: { referencePanel: workPanel, direction: 'left' } });
      api.addPanel({ id: 'reference', component: 'reference', title: 'REFERENCE', position: { referencePanel: workPanel, direction: 'right' } });

      // Middle row: Awareness | Diagnostics | Proposals
      api.addPanel({ id: 'awareness', component: 'awareness', title: 'AWARENESS', position: { referencePanel: workPanel, direction: 'below' } });
      const awarenessPanel = api.panels.find((p) => p.id === 'awareness');
      if (awarenessPanel) {
        api.addPanel({ id: 'diagnostics', component: 'diagnostics', title: 'DIAGNOSTICS', position: { referencePanel: awarenessPanel, direction: 'right' } });
        const diagnosticsPanel = api.panels.find((p) => p.id === 'diagnostics');
        if (diagnosticsPanel) {
          api.addPanel({ id: 'proposals', component: 'proposals', title: 'PROPOSALS', position: { referencePanel: diagnosticsPanel, direction: 'right' } });
        }
      }

      // Bottom row: Spatial | System | Assistant
      if (awarenessPanel) {
        api.addPanel({ id: 'spatial', component: 'spatial', title: 'SPATIAL', position: { referencePanel: awarenessPanel, direction: 'below' } });
      }
      const spatialPanel = api.panels.find((p) => p.id === 'spatial');
      if (spatialPanel) {
        api.addPanel({ id: 'system', component: 'system', title: 'SYSTEM', position: { referencePanel: spatialPanel, direction: 'right' } });
        api.addPanel({ id: 'assistant', component: 'assistant', title: 'ASSISTANT', position: { referencePanel: spatialPanel, direction: 'right' } });
      }
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
        // Re-apply layout on device class change
        if (apiRef.current) {
          applyPreset(apiRef.current, 'HERO_COCKPIT_DEFAULT', newClass);
        }
      }
    };
    window.addEventListener('resize', handleResize);
    activeObjectStore.setDeviceClass(deviceClass);
    return () => window.removeEventListener('resize', handleResize);
  }, [deviceClass]);

  const handleReady = useCallback((event: DockviewReadyEvent) => {
    apiRef.current = event.api;
    applyPreset(event.api, 'HERO_COCKPIT_DEFAULT', deviceClass);
  }, [deviceClass]);

  const handlePhoneSwitch = useCallback((panelId: PanelId) => {
    setPhonePanel(panelId);
    if (apiRef.current) {
      // Remove all panels and add the selected one
      apiRef.current.panels.forEach((p) => apiRef.current!.removePanel(p));
      apiRef.current.addPanel({ id: panelId, component: panelId, title: panelId.toUpperCase() });
    }
  }, []);

  // ─── Deck Layout Application ──────────────────────────────────────────────
  // Called by DeckActivation to apply a deck's panel layout atomically.

  const applyDeckLayout = useCallback((visiblePanels: readonly PanelId[], promotedPanel: PanelId) => {
    if (!apiRef.current) return;
    const api = apiRef.current;

    // Clear all existing panels
    api.panels.forEach((p) => api.removePanel(p));

    if (visiblePanels.length === 0) return;

    // Add promoted panel first (it becomes the anchor)
    const promoted = api.addPanel({
      id: promotedPanel,
      component: promotedPanel,
      title: promotedPanel.toUpperCase(),
    });

    // Add remaining panels relative to promoted
    const remaining = visiblePanels.filter((p) => p !== promotedPanel);
    let lastLeft = promoted;
    let lastRight = promoted;
    let lastBelow = promoted;

    for (let i = 0; i < remaining.length; i++) {
      const panelId = remaining[i];
      // Alternate placement: right, left, below
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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: tokens.color.bgDeep, minHeight: 0 }}>
      {/* Status Bar */}
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
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <DeckPicker applyLayout={applyDeckLayout} />
          <span style={{
            fontSize: tokens.font.sizeXs,
            color: tokens.color.mock,
            background: 'rgba(249,115,22,0.1)',
            padding: '1px 8px',
            borderRadius: tokens.radius.sm,
          }}>
            MOCK ADAPTERS
          </span>
          <span style={{
            fontSize: tokens.font.sizeXs,
            color: tokens.color.fgMuted,
            fontFamily: tokens.font.familyMono,
          }}>
            {deviceClass.toUpperCase()}
          </span>
        </div>
      </div>

      {/* Workspace */}
      <div style={{ flex: 1, overflow: 'hidden', minHeight: 0 }}>
        <DockviewReact
          className="dockview-theme-dark"
          onReady={handleReady}
          components={PANEL_COMPONENTS}
        />
      </div>

      {/* Phone Companion Switcher */}
      {isPhoneMode && (
        <CompanionSwitcher onSwitch={handlePhoneSwitch} currentPanel={phonePanel} />
      )}
    </div>
  );
}
