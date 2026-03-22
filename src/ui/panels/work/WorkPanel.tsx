/**
 * Construction OS — Work Panel
 *
 * Primary live work surface — detail, drawing, artifact workspace shell.
 * Center-of-gravity layout. Bounded local commands.
 * Emits: object.selected, validation.requested, artifact.requested, compare.requested
 * Subscribes to: truth-echo.propagated, object.selected, validation.updated, workspace.mode.changed
 * State owned: activeTab, draftState, localCommands
 *
 * Division 07 Contextual Overlay: Split-view comparison mode.
 * Visual hierarchy: Work panel is visually dominant via emphasis styling.
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { eventBus } from '../../events/EventBus';
import { adapters } from '../../adapters';
import { useActiveObject } from '../../stores/useSyncExternalStore';
import { activeObjectStore } from '../../stores/activeObjectStore';
import { tokens } from '../../theme/tokens';
import { useValidationWorker } from '../../workers/useValidationWorker';
import { ContextualOverlay } from '../../components/ContextualOverlay';
import type { ValidationResult } from '../../contracts/adapters';

type WorkTab = 'detail' | 'drawing' | 'validation' | 'artifact' | 'spatial';

export function WorkPanel() {
  const { activeObject, workspaceMode, compareObject, overlayActive } = useActiveObject();
  const [activeTab, setActiveTab] = useState<WorkTab>('detail');
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const { validate: workerValidate, result: workerResult, isRunning: workerRunning } = useValidationWorker();

  // Fetch validation status when active object changes
  useEffect(() => {
    if (!activeObject) return;
    adapters.validation.getValidationStatus(activeObject.id).then((result) => {
      if (result.data) setValidationResult(result.data);
    });
  }, [activeObject?.id]);

  // Update from worker results
  useEffect(() => {
    if (workerResult && activeObject) {
      eventBus.emit('validation.updated', {
        objectId: workerResult.objectId,
        status: workerResult.status,
        issues: workerResult.issues.map((i) => ({
          ...i,
          severity: i.severity as 'error' | 'warning' | 'info',
        })),
        timestamp: Date.now(),
      });
    }
  }, [workerResult]);

  const handleRequestValidation = useCallback(() => {
    if (!activeObject) return;
    workerValidate(activeObject.id, 'full');
    eventBus.emit('validation.requested', {
      objectId: activeObject.id,
      validationType: 'full',
      source: 'work',
    });
  }, [activeObject, workerValidate]);

  const handleRequestCompare = useCallback(() => {
    if (!activeObject) return;
    eventBus.emit('compare.requested', {
      objectIdA: activeObject.id,
      objectIdB: compareObject?.id ?? '',
      compareType: 'version',
      source: 'work',
    });
  }, [activeObject, compareObject]);

  const handleOpenOverlay = useCallback(() => {
    activeObjectStore.setOverlayActive(true);
  }, []);

  const handleCloseOverlay = useCallback(() => {
    activeObjectStore.setOverlayActive(false);
  }, []);

  const tabs: { key: WorkTab; label: string }[] = [
    { key: 'detail', label: 'Detail' },
    { key: 'drawing', label: 'Drawing' },
    { key: 'validation', label: 'Validation' },
    { key: 'artifact', label: 'Artifacts' },
    { key: 'spatial', label: 'Spatial' },
  ];

  const validationBadge = validationResult?.issues?.length ?? 0;

  return (
    <PanelShell panelId="work" title="Work" basis="mock" badgeCount={validationBadge > 0 ? validationBadge : undefined}>
      {/* Contextual Overlay — Division 07 split-view */}
      {overlayActive && activeObject ? (
        <ContextualOverlay activeObject={activeObject} onClose={handleCloseOverlay} />
      ) : (
        <>
          {/* Tab Bar */}
          <div
            style={{
              display: 'flex',
              gap: '1px',
              marginBottom: tokens.space.md,
              background: tokens.color.border,
              borderRadius: tokens.radius.sm,
              overflow: 'hidden',
            }}
          >
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
                  fontSize: tokens.font.sizeSm,
                  fontWeight: activeTab === tab.key ? tokens.font.weightSemibold : tokens.font.weightNormal,
                  fontFamily: tokens.font.family,
                  lineHeight: tokens.font.lineTight,
                  transition: `all ${tokens.transition.fast}`,
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {/* Content */}
          {!activeObject ? (
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60%', color: tokens.color.fgMuted }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: tokens.font.sizeXl, marginBottom: tokens.space.sm }}>Select an object</div>
                <div style={{ fontSize: tokens.font.sizeSm }}>Use Explorer or Spatial to select an object</div>
              </div>
            </div>
          ) : (
            <div>
              {activeTab === 'detail' && (
                <div>
                  <div style={{ marginBottom: tokens.space.lg }}>
                    <h3 style={{ fontSize: tokens.font.sizeLg, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.sm }}>
                      {activeObject.name}
                    </h3>
                    <div style={{ display: 'flex', gap: tokens.space.md, fontSize: tokens.font.sizeSm }}>
                      <span style={{ color: tokens.color.fgMuted }}>ID: <code style={{ fontFamily: tokens.font.familyMono, color: tokens.color.fgSecondary }}>{activeObject.id}</code></span>
                      <span style={{ color: tokens.color.fgMuted }}>Type: <span style={{ color: tokens.color.accentPrimary }}>{activeObject.type}</span></span>
                    </div>
                  </div>

                  {/* Workspace mode indicator */}
                  {workspaceMode !== 'default' && (
                    <div style={{
                      padding: tokens.space.sm,
                      background: tokens.color.compare + '15',
                      border: `1px solid ${tokens.color.compare}`,
                      borderRadius: tokens.radius.sm,
                      fontSize: tokens.font.sizeSm,
                      color: tokens.color.compare,
                      marginBottom: tokens.space.md,
                    }}>
                      Mode: {workspaceMode.toUpperCase()}
                      {compareObject && ` — Comparing with ${compareObject.name}`}
                    </div>
                  )}

                  {/* Local Commands */}
                  <div style={{ display: 'flex', gap: tokens.space.sm, marginTop: tokens.space.lg, flexWrap: 'wrap' }}>
                    <button
                      onClick={handleRequestValidation}
                      disabled={workerRunning}
                      style={{
                        padding: `${tokens.space.sm} ${tokens.space.md}`,
                        background: tokens.color.accentPrimary,
                        color: '#fff',
                        border: 'none',
                        borderRadius: tokens.radius.sm,
                        cursor: workerRunning ? 'wait' : 'pointer',
                        fontSize: tokens.font.sizeSm,
                        fontFamily: tokens.font.family,
                        opacity: workerRunning ? 0.6 : 1,
                      }}
                    >
                      {workerRunning ? 'Validating...' : 'Validate (Worker)'}
                    </button>
                    <button
                      onClick={handleRequestCompare}
                      style={{
                        padding: `${tokens.space.sm} ${tokens.space.md}`,
                        background: tokens.color.bgElevated,
                        color: tokens.color.fgSecondary,
                        border: `1px solid ${tokens.color.border}`,
                        borderRadius: tokens.radius.sm,
                        cursor: 'pointer',
                        fontSize: tokens.font.sizeSm,
                        fontFamily: tokens.font.family,
                      }}
                    >
                      Compare
                    </button>
                    <button
                      onClick={handleOpenOverlay}
                      style={{
                        padding: `${tokens.space.sm} ${tokens.space.md}`,
                        background: `${tokens.color.compare}15`,
                        color: tokens.color.compare,
                        border: `1px solid ${tokens.color.compare}`,
                        borderRadius: tokens.radius.sm,
                        cursor: 'pointer',
                        fontSize: tokens.font.sizeSm,
                        fontFamily: tokens.font.family,
                      }}
                    >
                      Split View Overlay
                    </button>
                  </div>
                </div>
              )}

              {activeTab === 'validation' && (
                <div>
                  <h3 style={{ fontSize: tokens.font.sizeMd, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.md }}>
                    Validation Status
                  </h3>
                  {validationResult ? (
                    <div>
                      <div style={{
                        display: 'inline-block',
                        padding: `${tokens.space.sm} ${tokens.space.sm}`,
                        borderRadius: tokens.radius.sm,
                        background: validationResult.status === 'passed' ? tokens.color.success + '20' : tokens.color.error + '20',
                        color: validationResult.status === 'passed' ? tokens.color.success : tokens.color.error,
                        fontSize: tokens.font.sizeSm,
                        fontWeight: tokens.font.weightSemibold,
                        marginBottom: tokens.space.md,
                      }}>
                        {validationResult.status.toUpperCase()}
                      </div>
                      {validationResult.issues.length > 0 && (
                        <div style={{ marginTop: tokens.space.sm }}>
                          {validationResult.issues.map((issue) => (
                            <div key={issue.id} style={{
                              padding: tokens.space.sm,
                              marginBottom: tokens.space.sm,
                              background: tokens.color.bgBase,
                              borderRadius: tokens.radius.sm,
                              borderLeft: `3px solid ${issue.severity === 'error' ? tokens.color.error : issue.severity === 'warning' ? tokens.color.warning : tokens.color.info}`,
                              fontSize: tokens.font.sizeSm,
                              lineHeight: tokens.font.lineNormal,
                            }}>
                              <span style={{ fontWeight: tokens.font.weightMedium }}>{issue.severity.toUpperCase()}</span>: {issue.message}
                              {issue.rule && <span style={{ color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono, marginLeft: tokens.space.sm }}>{issue.rule}</span>}
                            </div>
                          ))}
                        </div>
                      )}
                      {workerResult && (
                        <div style={{ marginTop: tokens.space.md, fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                          Worker compute time: {workerResult.computeTimeMs.toFixed(1)}ms
                        </div>
                      )}
                    </div>
                  ) : (
                    <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
                      No validation results. Click "Validate" to run worker-backed validation.
                    </div>
                  )}
                </div>
              )}

              {activeTab === 'drawing' && (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
                  <div style={{ padding: tokens.space.lg, textAlign: 'center', border: `1px dashed ${tokens.color.border}`, borderRadius: tokens.radius.md }}>
                    Drawing workspace — adapter seam ready for real drawing/artifact integration.
                  </div>
                </div>
              )}

              {activeTab === 'artifact' && (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
                  <div style={{ padding: tokens.space.lg, textAlign: 'center', border: `1px dashed ${tokens.color.border}`, borderRadius: tokens.radius.md }}>
                    Artifact generation workspace — adapter seam ready.
                  </div>
                </div>
              )}

              {activeTab === 'spatial' && (
                <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
                  <div style={{ padding: tokens.space.lg, textAlign: 'center', border: `1px dashed ${tokens.color.border}`, borderRadius: tokens.radius.md }}>
                    Spatial view — zone and location context for the active object.
                    <div style={{ marginTop: tokens.space.sm, fontSize: tokens.font.sizeXs }}>
                      Use the right edge panel or spatial dock tab for full spatial navigation.
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </>
      )}
    </PanelShell>
  );
}
