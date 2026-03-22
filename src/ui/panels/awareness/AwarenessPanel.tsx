/**
 * Construction OS — Awareness Panel
 *
 * Displays Awareness Cache snapshot state:
 *   - Active conditions (ConditionDetected)
 *   - Pending / Delivered / Quarantined artifacts
 *   - Open proposals
 *   - FAIL_CLOSED log
 *
 * States: loading, current, stale, empty, error
 * Subscribes to: truth-echo.propagated
 * Data source: AwarenessAdapter (bounded UI facade)
 *
 * FAIL_CLOSED: Missing or invalid upstream data displays an explicit
 * error/placeholder state rather than fake completion.
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { tokens } from '../../theme/tokens';
import { mockAwarenessAdapter } from '../../adapters/awarenessAdapter';
import type { AwarenessState } from '../../contracts/cockpit-types';

type AwarenessTab = 'conditions' | 'artifacts' | 'proposals' | 'fail_closed';

export function AwarenessPanel() {
  const [state, setState] = useState<AwarenessState | null>(null);
  const [activeTab, setActiveTab] = useState<AwarenessTab>('conditions');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadState = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const awarenessState = await mockAwarenessAdapter.getAwarenessState();
      setState(awarenessState);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'FAIL_CLOSED: Unable to load awareness state');
      setState(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadState();
  }, [loadState]);

  const totalArtifacts = state
    ? state.pending_artifacts.length + state.delivered_artifacts.length + state.quarantined_artifacts.length
    : 0;

  const tabs: { key: AwarenessTab; label: string; count: number }[] = [
    { key: 'conditions', label: 'Conditions', count: state?.active_conditions.length ?? 0 },
    { key: 'artifacts', label: 'Artifacts', count: totalArtifacts },
    { key: 'proposals', label: 'Proposals', count: state?.open_proposals.length ?? 0 },
    { key: 'fail_closed', label: 'FAIL_CLOSED', count: state?.fail_closed_log.length ?? 0 },
  ];

  return (
    <PanelShell panelId="awareness" title="Awareness" isMock={mockAwarenessAdapter.isMock} badgeCount={state?.fail_closed_log.length ?? undefined}>
      {/* Snapshot Status Bar */}
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
          {state?.snapshot_id ? `SNAPSHOT ${state.snapshot_id}` : 'NO SNAPSHOT'}
        </span>
        <span style={{
          color: state?.status === 'current' ? tokens.color.success
            : state?.status === 'stale' ? tokens.color.warning
            : state?.status === 'error' ? tokens.color.error
            : tokens.color.fgMuted,
          fontWeight: tokens.font.weightSemibold,
        }}>
          {loading ? 'LOADING...' : (state?.status ?? 'UNKNOWN').toUpperCase()}
        </span>
      </div>

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

      {/* Stale Warning */}
      {state?.status === 'stale' && (
        <div style={{
          padding: tokens.space.sm,
          marginBottom: tokens.space.sm,
          background: 'rgba(234,179,8,0.1)',
          borderLeft: `3px solid ${tokens.color.warning}`,
          borderRadius: tokens.radius.sm,
          fontSize: tokens.font.sizeXs,
          color: tokens.color.warning,
        }}>
          STALE: Snapshot compiled at {state.compiled_at} — data may not reflect current system state
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div style={{
          padding: tokens.space.lg,
          textAlign: 'center',
          color: tokens.color.fgMuted,
          fontSize: tokens.font.sizeSm,
        }}>
          Loading awareness state...
        </div>
      )}

      {/* Tab Bar */}
      {!loading && state && (
        <>
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
                  color: activeTab === tab.key
                    ? (tab.key === 'fail_closed' && tab.count > 0 ? tokens.color.error : tokens.color.fgPrimary)
                    : (tab.key === 'fail_closed' && tab.count > 0 ? tokens.color.error : tokens.color.fgSecondary),
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: tokens.font.sizeXs,
                  fontFamily: tokens.font.family,
                  fontWeight: activeTab === tab.key ? tokens.font.weightSemibold : tokens.font.weightNormal,
                  lineHeight: tokens.font.lineTight,
                }}
              >
                {tab.label}
                {tab.count > 0 && (
                  <span style={{ marginLeft: '4px', opacity: 0.7 }}>({tab.count})</span>
                )}
              </button>
            ))}
          </div>

          {/* Active Conditions */}
          {activeTab === 'conditions' && (
            <div>
              {state.active_conditions.length === 0 ? (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
                  No active conditions detected.
                </div>
              ) : (
                state.active_conditions.map((c, i) => (
                  <div key={i} style={{
                    padding: tokens.space.sm,
                    marginBottom: tokens.space.sm,
                    background: tokens.color.bgBase,
                    borderRadius: tokens.radius.sm,
                    borderLeft: `3px solid ${tokens.color.info}`,
                    fontSize: tokens.font.sizeXs,
                    lineHeight: tokens.font.lineNormal,
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: tokens.font.weightSemibold, color: tokens.color.fgPrimary, fontFamily: tokens.font.familyMono }}>
                        {c.condition_signature_id}
                      </span>
                      <span style={{
                        color: tokens.color.fgMuted,
                        background: tokens.color.bgElevated,
                        padding: '1px 6px',
                        borderRadius: tokens.radius.sm,
                      }}>
                        {c.node_type}
                      </span>
                    </div>
                    <div style={{ marginTop: '4px', color: tokens.color.fgSecondary }}>
                      Stage: {c.pipeline_stage} | Project: {c.project_id || '—'}
                    </div>
                    <div style={{ marginTop: '2px', color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
                      {new Date(c.detected_at).toLocaleTimeString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Artifacts */}
          {activeTab === 'artifacts' && (
            <div>
              {totalArtifacts === 0 ? (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
                  No artifacts in current snapshot.
                </div>
              ) : (
                <>
                  {/* Pending */}
                  {state.pending_artifacts.length > 0 && (
                    <div style={{ marginBottom: tokens.space.md }}>
                      <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.warning, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.sm }}>
                        PENDING ({state.pending_artifacts.length})
                      </div>
                      {state.pending_artifacts.map((a, i) => (
                        <ArtifactRow key={i} artifact={a} />
                      ))}
                    </div>
                  )}

                  {/* Delivered */}
                  {state.delivered_artifacts.length > 0 && (
                    <div style={{ marginBottom: tokens.space.md }}>
                      <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.success, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.sm }}>
                        DELIVERED ({state.delivered_artifacts.length})
                      </div>
                      {state.delivered_artifacts.map((a, i) => (
                        <ArtifactRow key={i} artifact={a} />
                      ))}
                    </div>
                  )}

                  {/* Quarantined */}
                  {state.quarantined_artifacts.length > 0 && (
                    <div style={{ marginBottom: tokens.space.md }}>
                      <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.error, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.sm }}>
                        QUARANTINED ({state.quarantined_artifacts.length})
                      </div>
                      {state.quarantined_artifacts.map((a, i) => (
                        <ArtifactRow key={i} artifact={a} />
                      ))}
                    </div>
                  )}
                </>
              )}
            </div>
          )}

          {/* Open Proposals */}
          {activeTab === 'proposals' && (
            <div>
              {state.open_proposals.length === 0 ? (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
                  No open proposals in current snapshot.
                </div>
              ) : (
                state.open_proposals.map((p, i) => (
                  <div key={i} style={{
                    padding: tokens.space.sm,
                    marginBottom: tokens.space.sm,
                    background: tokens.color.bgBase,
                    borderRadius: tokens.radius.sm,
                    borderLeft: `3px solid ${tokens.color.compare}`,
                    fontSize: tokens.font.sizeXs,
                    lineHeight: tokens.font.lineNormal,
                  }}>
                    <div style={{ fontWeight: tokens.font.weightMedium, color: tokens.color.fgPrimary }}>
                      {p.event_id}
                    </div>
                    <div style={{ marginTop: '2px', color: tokens.color.fgSecondary }}>
                      Source: {p.source_component}
                    </div>
                    <div style={{ marginTop: '2px', color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
                      {new Date(p.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* FAIL_CLOSED Log */}
          {activeTab === 'fail_closed' && (
            <div>
              {state.fail_closed_log.length === 0 ? (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
                  No FAIL_CLOSED events in current snapshot.
                </div>
              ) : (
                state.fail_closed_log.map((entry, i) => (
                  <div key={i} style={{
                    padding: tokens.space.sm,
                    marginBottom: tokens.space.sm,
                    background: 'rgba(239,68,68,0.05)',
                    borderRadius: tokens.radius.sm,
                    borderLeft: `3px solid ${tokens.color.error}`,
                    fontSize: tokens.font.sizeXs,
                    lineHeight: tokens.font.lineNormal,
                  }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <span style={{ fontWeight: tokens.font.weightSemibold, color: tokens.color.error }}>
                        {entry.event_type}
                      </span>
                      <span style={{ color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
                        {entry.event_id}
                      </span>
                    </div>
                    <div style={{ marginTop: '4px', color: tokens.color.fgPrimary }}>
                      {entry.reason}
                    </div>
                    <div style={{ marginTop: '2px', color: tokens.color.fgMuted }}>
                      Source: {entry.source_component} | {new Date(entry.timestamp).toLocaleTimeString()}
                    </div>
                  </div>
                ))
              )}
            </div>
          )}
        </>
      )}

      {/* Empty State */}
      {!loading && !error && state?.status === 'empty' && (
        <div style={{
          padding: tokens.space.xl,
          textAlign: 'center',
          color: tokens.color.fgMuted,
          fontSize: tokens.font.sizeSm,
        }}>
          No awareness snapshot available. Waiting for Awareness Cache to compile a snapshot from Cognitive Bus events.
        </div>
      )}
    </PanelShell>
  );
}

// ─── Artifact Row Component ────────────────────────────────────────────────

function ArtifactRow({ artifact }: { artifact: import('../../contracts/cockpit-types').ArtifactState }) {
  const lifecycleColor = artifact.lifecycle === 'delivered' ? tokens.color.success
    : artifact.lifecycle === 'quarantined' ? tokens.color.error
    : tokens.color.warning;

  return (
    <div style={{
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
          fontSize: tokens.font.sizeXs,
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
      <div style={{ marginTop: '2px', color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
        {new Date(artifact.timestamp).toLocaleTimeString()}
      </div>
    </div>
  );
}
