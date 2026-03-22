/**
 * Construction OS — Gravity Glass Workspace Shell
 *
 * Gravity-reactive workstation with:
 * - Center workspace always dominant
 * - Reactive edge panels (left=docs, right=visual)
 * - Proximity field model for cursor intent
 * - Glass morph secondary panels
 * - Workspace bias controls (+/- and ←/→)
 * - Hover peek preview
 * - Gravity deck fan-out
 * - Bottom command dock (proximity-reactive)
 * - Command palette (CMD+K / CTRL+K)
 * - Authority HUD
 * - Dev tools isolation
 *
 * No freeform manual resizing. Deterministic bias steps.
 * FAIL_CLOSED: Invalid proximity state → idle layout.
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
import { AssemblyBuilderPanel } from '../assembly-builder/AssemblyBuilderPanel';
import { DetailViewerPanel } from '../detail-viewer/DetailViewerPanel';
import { DeckPicker } from '../decks/DeckPicker';
import { AuthorityHUD } from '../components/AuthorityHUD';
import { CommandPalette } from '../components/CommandPalette';
import { BottomDock } from '../layout/BottomDock';
import { DevToolsPanel } from '../devtools/DevToolsPanel';
import { WorkspaceBiasControls, getDefaultBias, type BiasState } from '../gravity/WorkspaceBias';
import { EdgePanel } from '../gravity/EdgePanel';
import { GravityDeckFan } from '../gravity/GravityDeckFan';
import { proximityField } from '../gravity/ProximityField';
import { PROXIMITY, type ProximityFieldSnapshot } from '../gravity/ProximityConstants';
import { initTruthEcho, destroyTruthEcho } from '../orchestration/TruthEcho';
import { detectDeviceClass } from '../orchestration/DeviceOrchestrator';
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
function AssemblyBuilderWrapper(_props: IDockviewPanelProps) { return <AssemblyBuilderPanel />; }
function DetailViewerWrapper(_props: IDockviewPanelProps) { return <DetailViewerPanel />; }

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
  'assembly-builder': AssemblyBuilderWrapper,
  'detail-viewer': DetailViewerWrapper,
};

// ─── Workspace Presets ──────────────────────────────────────────────────────

function applyWorkspaceLayout(api: DockviewReadyEvent['api'], deviceClass: DeviceClass) {
  api.panels.forEach((p) => api.removePanel(p));

  if (deviceClass === 'phone') {
    api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
    activeObjectStore.setPinnedCompanion('explorer');
  } else if (deviceClass === 'tablet') {
    const workPanel = api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
    api.addPanel({ id: 'explorer', component: 'explorer', title: 'EXPLORER', position: { referencePanel: workPanel, direction: 'left' } });
  } else {
    // Laptop/Desktop/Ultrawide: workspace-dominant with Explorer | Work+AssemblyBuilder+DetailViewer | Reference
    const workPanel = api.addPanel({ id: 'work', component: 'work', title: 'WORK' });
    api.addPanel({ id: 'assembly-builder', component: 'assembly-builder', title: 'ASSEMBLY BUILDER', position: { referencePanel: workPanel, direction: 'within' } });
    api.addPanel({ id: 'detail-viewer', component: 'detail-viewer', title: 'DETAIL VIEWER', position: { referencePanel: workPanel, direction: 'within' } });
    api.addPanel({ id: 'explorer', component: 'explorer', title: 'EXPLORER', position: { referencePanel: workPanel, direction: 'left' } });
    api.addPanel({ id: 'reference', component: 'reference', title: 'REFERENCE', position: { referencePanel: workPanel, direction: 'right' } });
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
      display: 'flex', gap: '1px', background: tokens.color.border,
      borderRadius: tokens.radius.sm, overflow: 'hidden', padding: 0,
    }}>
      {panels.map((p) => (
        <button key={p.id} onClick={() => onSwitch(p.id)} style={{
          flex: 1, padding: `${tokens.space.sm} ${tokens.space.xs}`,
          background: currentPanel === p.id ? tokens.color.bgActive : tokens.color.bgElevated,
          color: currentPanel === p.id ? tokens.color.accentPrimary : tokens.color.fgMuted,
          border: 'none', cursor: 'pointer', fontSize: tokens.font.sizeXs,
          fontWeight: tokens.font.weightSemibold, fontFamily: tokens.font.family,
        }}>
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
  const [bias, setBias] = useState<BiasState>(getDefaultBias);
  const [proxSnapshot, setProxSnapshot] = useState<ProximityFieldSnapshot | null>(null);
  const { devToolsVisible } = useActiveObject();

  const showGravityLayout = deviceClass !== 'phone' && deviceClass !== 'tablet';

  // ─── Initialize systems ──────────────────────────────────────────────
  useEffect(() => {
    initTruthEcho();
    if (showGravityLayout) {
      proximityField.start();
    }
    return () => {
      destroyTruthEcho();
      proximityField.stop();
    };
  }, [showGravityLayout]);

  // ─── Proximity field subscription ────────────────────────────────────
  useEffect(() => {
    if (!showGravityLayout) return;
    const unsub = proximityField.subscribe((snapshot) => {
      setProxSnapshot(snapshot);
    });
    return unsub;
  }, [showGravityLayout]);

  // ─── Device class detection ──────────────────────────────────────────
  useEffect(() => {
    const handleResize = () => {
      const newClass = detectDeviceClass();
      if (newClass !== deviceClass) {
        setDeviceClass(newClass);
        activeObjectStore.setDeviceClass(newClass);
        setIsPhoneMode(newClass === 'phone');
        if (apiRef.current) {
          applyWorkspaceLayout(apiRef.current, newClass);
        }
      }
    };
    window.addEventListener('resize', handleResize);
    activeObjectStore.setDeviceClass(deviceClass);
    return () => window.removeEventListener('resize', handleResize);
  }, [deviceClass]);

  // ─── Command Palette keyboard shortcut ───────────────────────────────
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

  // ─── Sync bias to store ──────────────────────────────────────────────
  const handleBiasChange = useCallback((newBias: BiasState) => {
    setBias(newBias);
    activeObjectStore.setWorkspaceBias(newBias);
  }, []);

  const handleReady = useCallback((event: DockviewReadyEvent) => {
    apiRef.current = event.api;
    applyWorkspaceLayout(event.api, deviceClass);
  }, [deviceClass]);

  const handlePhoneSwitch = useCallback((panelId: PanelId) => {
    setPhonePanel(panelId);
    if (apiRef.current) {
      apiRef.current.panels.forEach((p) => apiRef.current!.removePanel(p));
      apiRef.current.addPanel({ id: panelId, component: panelId, title: panelId.toUpperCase() });
    }
  }, []);

  const applyDeckLayout = useCallback((visiblePanels: readonly PanelId[], promotedPanel: PanelId) => {
    if (!apiRef.current) return;
    const api = apiRef.current;
    api.panels.forEach((p) => api.removePanel(p));
    if (visiblePanels.length === 0) return;
    const promoted = api.addPanel({ id: promotedPanel, component: promotedPanel, title: promotedPanel.toUpperCase() });
    const remaining = visiblePanels.filter((p) => p !== promotedPanel);
    let lastRight = promoted;
    let lastBelow = promoted;
    for (let i = 0; i < remaining.length; i++) {
      const panelId = remaining[i];
      if (i % 3 === 0) {
        lastRight = api.addPanel({ id: panelId, component: panelId, title: panelId.toUpperCase(), position: { referencePanel: lastRight, direction: 'right' } });
      } else if (i % 3 === 1) {
        lastBelow = api.addPanel({ id: panelId, component: panelId, title: panelId.toUpperCase(), position: { referencePanel: promoted, direction: 'below' } });
      } else {
        api.addPanel({ id: panelId, component: panelId, title: panelId.toUpperCase(), position: { referencePanel: lastBelow, direction: 'right' } });
      }
    }
  }, []);

  const handleToggleDevTools = useCallback(() => {
    activeObjectStore.setDevToolsVisible(!devToolsVisible);
  }, [devToolsVisible]);

  // ─── Proximity-derived state (discrete states only) ───────────────────
  const idle = { edge: 'left' as const, proximity: 0, state: 'idle' as const, intentTimestamp: null, lockedAt: null, collapsedAt: null };
  const leftEdge = proxSnapshot?.left ?? idle;
  const rightEdge = proxSnapshot?.right ?? { ...idle, edge: 'right' as const };
  const bottomEdge = proxSnapshot?.bottom ?? { ...idle, edge: 'bottom' as const };
  const leftActive = leftEdge.state === 'preview' || leftEdge.state === 'locked';
  const rightActive = rightEdge.state === 'preview' || rightEdge.state === 'locked';
  const deckFanExpanded = leftEdge.state === 'preview' || leftEdge.state === 'locked';

  // Bottom dock proximity state
  const bottomProximity = bottomEdge.proximity;
  const bottomActive = bottomEdge.state === 'preview' || bottomEdge.state === 'locked';

  // ─── Workspace sizing from bias (drives real layout) ─────────────────
  // Discrete edge widths — no continuous pointer-driven resizing
  const leftEdgeWidth = leftActive
    ? (leftEdge.state === 'locked' ? PROXIMITY.edgeLockedWidth : PROXIMITY.edgePreviewWidth)
    : PROXIMITY.edgeIdleWidth;
  const rightEdgeWidth = rightActive
    ? (rightEdge.state === 'locked' ? PROXIMITY.edgeLockedWidth : PROXIMITY.edgePreviewWidth)
    : PROXIMITY.edgeIdleWidth;

  // Apply horizontal bias to edge widths when edges are not active
  const biasLeftExtra = !leftActive && bias.horizontalBias > 0 ? bias.horizontalBias * 2 : 0;
  const biasRightExtra = !rightActive && bias.horizontalBias < 0 ? Math.abs(bias.horizontalBias) * 2 : 0;

  const workspaceMarginLeft = leftEdgeWidth + biasLeftExtra;
  const workspaceMarginRight = rightEdgeWidth + biasRightExtra;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: tokens.color.bgDeep, minHeight: 0, position: 'relative', overflow: 'hidden' }}>
      {/* ─── Status Bar with Authority HUD + Bias Controls ─── */}
      <div style={{
        display: 'flex', alignItems: 'center', justifyContent: 'space-between',
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: tokens.color.bgBase, borderBottom: `1px solid ${tokens.color.border}`,
        minHeight: '40px', flexShrink: 0, zIndex: 200,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.md }}>
          <span style={{
            fontSize: tokens.font.sizeMd, fontWeight: tokens.font.weightBold,
            color: tokens.color.fgPrimary, letterSpacing: '0.08em', lineHeight: tokens.font.lineTight,
          }}>
            CONSTRUCTION OS
          </span>
          <span style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
            WORKSTATION
          </span>
          <AuthorityHUD />
          {/* Workspace Bias Controls */}
          {showGravityLayout && (
            <WorkspaceBiasControls bias={bias} onBiasChange={handleBiasChange} />
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <DeckPicker applyLayout={applyDeckLayout} />
          <button
            onClick={() => setCommandPaletteOpen(true)}
            style={{
              padding: `${tokens.space.xs} ${tokens.space.sm}`, background: tokens.color.bgElevated,
              color: tokens.color.fgMuted, border: `1px solid ${tokens.color.border}`,
              borderRadius: tokens.radius.sm, cursor: 'pointer', fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.familyMono, display: 'flex', alignItems: 'center', gap: tokens.space.xs,
            }}
            title="Command Palette (Ctrl+K / Cmd+K)"
          >
            {'\u2318'}K
          </button>
          <button
            onClick={handleToggleDevTools}
            style={{
              padding: `${tokens.space.xs} ${tokens.space.sm}`,
              background: devToolsVisible ? `${tokens.color.mock}15` : tokens.color.bgElevated,
              color: devToolsVisible ? tokens.color.mock : tokens.color.fgMuted,
              border: `1px solid ${devToolsVisible ? tokens.color.mock + '40' : tokens.color.border}`,
              borderRadius: tokens.radius.sm, cursor: 'pointer', fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.familyMono,
            }}
            title="Toggle Dev Tools"
          >
            DEV
          </button>
          <span style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
            {deviceClass.toUpperCase()}
          </span>
        </div>
      </div>

      {/* ─── Main Workspace Area ─── */}
      <div style={{
        flex: 1, position: 'relative', overflow: 'hidden', minHeight: 0,
      }}>
        {/* Gravity Deck Fan-Out (left edge inner) */}
        {showGravityLayout && (
          <GravityDeckFan
            expanded={deckFanExpanded}
            proximity={leftEdge.proximity}
          />
        )}

        {/* Left Edge Panel — Documents/Specs/References */}
        {showGravityLayout && (
          <EdgePanel
            edge="left"
            edgeState={leftEdge.state}
            proximity={leftEdge.proximity}
            title="Documents / References"
          >
            <ReferencePanel />
          </EdgePanel>
        )}

        {/* Right Edge Panel — Drawings/Spatial/Visual */}
        {showGravityLayout && (
          <EdgePanel
            edge="right"
            edgeState={rightEdge.state}
            proximity={rightEdge.proximity}
            title="Drawings / Spatial"
          >
            <SpatialPanel />
          </EdgePanel>
        )}

        {/* Center Workspace — always dominant */}
        <div style={{
          position: 'absolute',
          top: 0,
          bottom: 0,
          left: showGravityLayout ? `${Math.max(PROXIMITY.edgeIdleWidth, workspaceMarginLeft)}px` : 0,
          right: showGravityLayout ? `${Math.max(PROXIMITY.edgeIdleWidth, workspaceMarginRight)}px` : 0,
          transition: `left ${PROXIMITY.expandDuration}ms ${PROXIMITY.easing}, right ${PROXIMITY.expandDuration}ms ${PROXIMITY.easing}`,
          overflow: 'hidden',
          zIndex: 50,
        }}>
          <DockviewReact
            className="dockview-theme-dark"
            onReady={handleReady}
            components={PANEL_COMPONENTS}
          />
        </div>
      </div>

      {/* ─── Bottom Command Dock ─── */}
      <BottomDock bottomProximity={bottomProximity} bottomActive={bottomActive} />

      {/* Phone Companion Switcher */}
      {isPhoneMode && (
        <CompanionSwitcher onSwitch={handlePhoneSwitch} currentPanel={phonePanel} />
      )}

      {/* Command Palette Overlay */}
      {commandPaletteOpen && (
        <CommandPalette onClose={() => setCommandPaletteOpen(false)} />
      )}

      {/* Dev Tools Panel */}
      <DevToolsPanel />
    </div>
  );
}
