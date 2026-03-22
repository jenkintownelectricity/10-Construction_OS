/**
 * Construction OS — Runtime Diagnostics Panel
 *
 * Displays runtime pipeline state and events:
 *   - ConditionDetected
 *   - DetailResolved
 *   - ArtifactRendered
 *   - ValidationFailed
 *   - RuntimeError
 *   - Artifact lifecycle: pending / delivered / quarantined
 *
 * FAIL_CLOSED events are prominently visible with error styling.
 * Pipeline stages are displayed as an ordered status strip.
 *
 * Data source: RuntimeDiagnosticsAdapter (bounded UI facade)
 * FAIL_CLOSED: Missing or invalid data displays explicit error state.
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { tokens } from '../../theme/tokens';
import { mockRuntimeDiagnosticsAdapter } from '../../adapters/runtimeDiagnosticsAdapter';
import type {
  RuntimeDiagnosticsState,
  RuntimeDiagnosticEvent,
  RuntimeEventType,
  PipelineStageStatus,
} from '../../contracts/cockpit-types';

type DiagnosticsTab = 'pipeline' | 'events' | 'artifacts';

export function RuntimeDiagnosticsPanel() {
  const [state, setState] = useState<RuntimeDiagnosticsState | null>(null);
  const [activeTab, setActiveTab] = useState<DiagnosticsTab>('pipeline');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadState = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const diagnostics = await mockRuntimeDiagnosticsAdapter.getDiagnosticsState();
      setState(diagnostics);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'FAIL_CLOSED: Unable to load runtime diagnostics');
      setState(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadState();
  }, [loadState]);

  const failEvents = state?.events.filter(
    (e) => e.event_type === 'ValidationFailed' || e.event_type === 'RuntimeError'
  ) ?? [];

  const tabs: { key: DiagnosticsTab; label: string; count?: number }[] = [
    { key: 'pipeline', label: 'Pipeline' },
    { key: 'events', label: 'Events', count: state?.events.length ?? 0 },
    { key: 'artifacts', label: 'Artifacts', count: state?.artifact_states.length ?? 0 },
  ];

  return (
    <PanelShell panelId="diagnostics" title="Runtime Diagnostics" isMock={mockRuntimeDiagnosticsAdapter.isMock}>
      {/* Connection Status */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `${tokens.space.sm} ${tokens.space.sm}`,
        marginBottom: tokens.space.sm,
        background: tokens.color.bgBase,
        borderRadius: tokens.radius.sm,
        fontSize: tokens.font.sizeXs,
        fontFamily: tokens.font.familyMono,
        lineHeight: tokens.font.lineNormal,
      }}>
        <span style={{ color: tokens.color.fgMuted }}>
          RUNTIME SIGNAL STREAM
        </span>
        <span style={{
          color: state?.status === 'connected' ? tokens.color.success
            : state?.status === 'error' ? tokens.color.error
            : tokens.color.warning,
          fontWeight: tokens.font.weightSemibold,
        }}>
          {loading ? 'LOADING...' : (state?.status ?? 'UNKNOWN').toUpperCase()}
        </span>
      </div>

      {/* FAIL_CLOSED Banner — prominent when failures exist */}
      {failEvents.length > 0 && (
        <div style={{
          padding: tokens.space.sm,
          marginBottom: tokens.space.sm,
          background: 'rgba(239,68,68,0.12)',
          border: `1px solid ${tokens.color.error}`,
          borderRadius: tokens.radius.sm,
          fontSize: tokens.font.sizeXs,
          color: tokens.color.error,
          fontWeight: tokens.font.weightSemibold,
          textAlign: 'center',
        }}>
          FAIL_CLOSED: {failEvents.length} failure event{failEvents.length !== 1 ? 's' : ''} detected in pipeline
        </div>
      )}

      {/* Error State */}
      {error && (
        <div style={{
          padding: tokens.space.sm,
          marginBottom: tokens.space.sm,
          background: 'rgba(239,68,68,0.1)',
          borderLeft: `3px solid ${tokens.color.error}`,
          borderRadius: tokens.radius.sm,
          fontSize: tokens.font.sizeXs,
          color: tokens.color.error,
        }}>
          {error}
        </div>
      )}

      {/* Loading */}
      {loading && (
        <div style={{ padding: tokens.space.lg, textAlign: 'center', color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
          Loading runtime diagnostics...
        </div>
      )}

      {!loading && state && (
        <>
          {/* Tab Bar */}
          <div style={{
            display: 'flex',
            gap: '1px',
            marginBottom: tokens.space.md,
            background: tokens.color.border,
            borderRadius: tokens.radius.sm,
            overflow: 'hidden',
          }}>
            {tabs.map((tab) => (
              <button
                key={tab.key}
                onClick={() => setActiveTab(tab.key)}
                style={{
                  flex: 1,
                  padding: `${tokens.space.sm} ${tokens.space.sm}`,
                  background: activeTab === tab.key ? tokens.color.bgActive : tokens.color.bgElevated,
                  color: activeTab === tab.key ? tokens.color.fgPrimary : tokens.color.fgSecondary,
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: tokens.font.sizeXs,
                  fontFamily: tokens.font.family,
                  fontWeight: activeTab === tab.key ? tokens.font.weightSemibold : tokens.font.weightNormal,
                  lineHeight: tokens.font.lineTight,
                }}
              >
                {tab.label}
                {tab.count !== undefined && tab.count > 0 && (
                  <span style={{ marginLeft: '4px', opacity: 0.7 }}>({tab.count})</span>
                )}
              </button>
            ))}
          </div>

          {/* Pipeline View */}
          {activeTab === 'pipeline' && (
            <div>
              {state.pipeline_stages.map((stage, i) => (
                <PipelineStageRow key={i} stage={stage} />
              ))}
            </div>
          )}

          {/* Events View */}
          {activeTab === 'events' && (
            <div>
              {state.events.length === 0 ? (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
                  No runtime events received.
                </div>
              ) : (
                state.events.map((evt) => (
                  <EventRow key={evt.event_id} event={evt} />
                ))
              )}
            </div>
          )}

          {/* Artifacts View */}
          {activeTab === 'artifacts' && (
            <div>
              {state.artifact_states.length === 0 ? (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
                  No artifact state data.
                </div>
              ) : (
                state.artifact_states.map((artifact, i) => {
                  const lifecycleColor = artifact.lifecycle === 'delivered' ? tokens.color.success
                    : artifact.lifecycle === 'quarantined' ? tokens.color.error
                    : tokens.color.warning;

                  return (
                    <div key={i} style={{
                      padding: tokens.space.sm,
                      marginBottom: tokens.space.sm,
                      background: tokens.color.bgBase,
                      borderRadius: tokens.radius.sm,
                      borderLeft: `3px solid ${lifecycleColor}`,
                      fontSize: tokens.font.sizeXs,
                      lineHeight: tokens.font.lineNormal,
                    }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <span style={{ fontWeight: tokens.font.weightMedium, color: tokens.color.fgPrimary, fontFamily: tokens.font.familyMono }}>
                          {artifact.artifact_id}
                        </span>
                        <span style={{
                          color: lifecycleColor,
                          fontWeight: tokens.font.weightSemibold,
                          textTransform: 'uppercase',
                        }}>
                          {artifact.lifecycle}
                        </span>
                      </div>
                      <div style={{ marginTop: '4px', color: tokens.color.fgSecondary }}>
                        {artifact.artifact_type} | {artifact.renderer_name} | {artifact.pipeline_stage}
                      </div>
                      {artifact.quarantine_reason && (
                        <div style={{ marginTop: '4px', color: tokens.color.error }}>
                          {artifact.quarantine_reason}
                        </div>
                      )}
                    </div>
                  );
                })
              )}
            </div>
          )}
        </>
      )}
    </PanelShell>
  );
}

// ─── Pipeline Stage Row ────────────────────────────────────────────────────

function PipelineStageRow({ stage }: { stage: PipelineStageStatus }) {
  const statusColor: Record<string, string> = {
    idle: tokens.color.fgMuted,
    active: tokens.color.info,
    completed: tokens.color.success,
    failed: tokens.color.error,
    error: tokens.color.error,
  };

  const statusIcon: Record<string, string> = {
    idle: '\u2500',      // ─
    active: '\u25B6',    // ▶
    completed: '\u2713', // ✓
    failed: '\u2717',    // ✗
    error: '\u2717',     // ✗
  };

  const isFail = stage.status === 'failed' || stage.status === 'error';

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: tokens.space.sm,
      padding: `${tokens.space.sm} ${tokens.space.sm}`,
      marginBottom: '1px',
      background: isFail ? 'rgba(239,68,68,0.08)' : tokens.color.bgBase,
      borderRadius: tokens.radius.sm,
      fontSize: tokens.font.sizeXs,
      lineHeight: tokens.font.lineNormal,
    }}>
      <span style={{
        width: '16px',
        textAlign: 'center',
        color: statusColor[stage.status] ?? tokens.color.fgMuted,
        fontWeight: tokens.font.weightBold,
      }}>
        {statusIcon[stage.status] ?? '?'}
      </span>
      <span style={{
        flex: 1,
        color: isFail ? tokens.color.error : tokens.color.fgPrimary,
        fontFamily: tokens.font.familyMono,
        fontWeight: isFail ? tokens.font.weightSemibold : tokens.font.weightNormal,
      }}>
        {stage.stage}
      </span>
      <span style={{
        color: statusColor[stage.status] ?? tokens.color.fgMuted,
        fontWeight: tokens.font.weightMedium,
        textTransform: 'uppercase',
      }}>
        {stage.status}
      </span>
      {stage.last_event_type && (
        <span style={{
          color: tokens.color.fgMuted,
          fontSize: tokens.font.sizeXs,
        }}>
          {stage.last_event_type}
        </span>
      )}
    </div>
  );
}

// ─── Event Row ─────────────────────────────────────────────────────────────

const EVENT_TYPE_COLORS: Record<RuntimeEventType, string> = {
  ConditionDetected: tokens.color.info,
  DetailResolved: tokens.color.success,
  ArtifactRendered: tokens.color.canonical,
  ValidationFailed: tokens.color.error,
  RuntimeError: tokens.color.error,
};

function EventRow({ event }: { event: RuntimeDiagnosticEvent }) {
  const color = EVENT_TYPE_COLORS[event.event_type] ?? tokens.color.fgMuted;
  const isFail = event.event_type === 'ValidationFailed' || event.event_type === 'RuntimeError';

  // Extract display message from payload
  let message = '';
  const p = event.payload;
  switch (p.type) {
    case 'ConditionDetected':
      message = `${p.condition_signature_id} (${p.node_type})`;
      break;
    case 'DetailResolved':
      message = `${p.condition_signature_id} → ${p.resolved_detail_id}`;
      break;
    case 'ArtifactRendered':
      message = `${p.artifact_id} (${p.artifact_type})`;
      break;
    case 'ValidationFailed':
      message = `${p.error_code}: ${p.failure_reason}`;
      break;
    case 'RuntimeError':
      message = `${p.exception_type}: ${p.failure_reason}`;
      break;
  }

  return (
    <div style={{
      padding: tokens.space.sm,
      marginBottom: tokens.space.sm,
      background: isFail ? 'rgba(239,68,68,0.08)' : tokens.color.bgBase,
      borderRadius: tokens.radius.sm,
      borderLeft: `3px solid ${color}`,
      fontSize: tokens.font.sizeXs,
      lineHeight: tokens.font.lineNormal,
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <span style={{
          color,
          fontWeight: tokens.font.weightSemibold,
          fontFamily: tokens.font.familyMono,
        }}>
          {event.event_type}
        </span>
        <span style={{
          color: event.severity === 'critical' ? tokens.color.error
            : event.severity === 'error' ? tokens.color.error
            : tokens.color.fgMuted,
          fontWeight: event.severity === 'critical' || event.severity === 'error' ? tokens.font.weightBold : tokens.font.weightNormal,
          textTransform: 'uppercase',
        }}>
          {event.severity}
        </span>
      </div>
      <div style={{ marginTop: '4px', color: isFail ? tokens.color.error : tokens.color.fgPrimary }}>
        {message}
      </div>
      <div style={{ marginTop: '2px', color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
        Stage: {event.pipeline_stage} | {new Date(event.timestamp).toLocaleTimeString()}
      </div>
    </div>
  );
}
