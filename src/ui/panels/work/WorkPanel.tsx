/**
 * Construction OS — Work Panel
 *
 * Primary live work surface — detail, drawing, artifact workspace shell.
 * Center-of-gravity layout. Bounded local commands.
 * Emits: object.selected, validation.requested, artifact.requested, compare.requested, generation.requested, generation.completed
 * Subscribes to: truth-echo.propagated, object.selected, validation.updated, workspace.mode.changed
 * State owned: activeTab, draftState, localCommands, generationResult
 *
 * Division 07 Contextual Overlay: Split-view comparison mode.
 * Visual hierarchy: Work panel is visually dominant via emphasis styling.
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { eventBus } from '../../events/EventBus';
import { adapters } from '../../adapters';
import { dxfGenerationAdapter } from '../../adapters/dxfGenerationAdapter';
import { useActiveObject } from '../../stores/useSyncExternalStore';
import { activeObjectStore } from '../../stores/activeObjectStore';
import { tokens } from '../../theme/tokens';
import { useValidationWorker } from '../../workers/useValidationWorker';
import { ContextualOverlay } from '../../components/ContextualOverlay';
import type { ValidationResult } from '../../contracts/adapters';
import type { GenerationResult } from '../../contracts/assemblyDraft';
import { validateAssemblyDraft } from '../../contracts/assemblyDraft';
import type { CanonicalAssemblyDraft, AssemblyCategory } from '../../contracts/assemblyDraft';

type WorkTab = 'detail' | 'drawing' | 'validation' | 'artifact' | 'spatial';

/**
 * Extract a CanonicalAssemblyDraft from an ActiveObjectIdentity if it
 * carries assembly metadata with layers. Returns null if the active
 * object is not a valid assembly draft.
 */
function extractAssemblyDraft(
  obj: { id: string; name: string; type: string; metadata?: Record<string, unknown> },
): CanonicalAssemblyDraft | null {
  if (obj.type !== 'assembly' || !obj.metadata) return null;
  const meta = obj.metadata;
  if (!meta.category || !meta.layers || typeof meta.layers !== 'object') return null;

  return {
    id: obj.id,
    name: obj.name,
    type: 'assembly',
    category: meta.category as AssemblyCategory,
    layers: meta.layers as CanonicalAssemblyDraft['layers'],
    project: meta.project as CanonicalAssemblyDraft['project'],
  };
}

export function WorkPanel() {
  const { activeObject, workspaceMode, compareObject, overlayActive } = useActiveObject();
  const [activeTab, setActiveTab] = useState<WorkTab>('detail');
  const [validationResult, setValidationResult] = useState<ValidationResult | null>(null);
  const { validate: workerValidate, result: workerResult, isRunning: workerRunning } = useValidationWorker();

  // ── Generation state ─────────────────────────────────────────────────
  const [generationResult, setGenerationResult] = useState<GenerationResult | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  // Fetch validation status when active object changes
  useEffect(() => {
    if (!activeObject) return;
    adapters.validation.getValidationStatus(activeObject.id).then((result) => {
      if (result.data) setValidationResult(result.data);
    });
    // Reset generation result on object change
    setGenerationResult(null);
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

  // ── Generate Detail handler ──────────────────────────────────────────
  const handleGenerateDetail = useCallback(async () => {
    if (!activeObject) return;

    const draft = extractAssemblyDraft(activeObject);
    if (!draft) return;

    // Pre-flight validation (fail-closed)
    const preValidation = validateAssemblyDraft(draft);
    if (!preValidation.valid) {
      const failResult: GenerationResult = {
        status: 'validation_failed',
        draftId: draft.id,
        generatorSeam: null,
        dxfFilename: null,
        dxfPath: null,
        diagnostics: preValidation.errors,
        timestamp: Date.now(),
      };
      setGenerationResult(failResult);
      setActiveTab('artifact');
      eventBus.emit('generation.completed', {
        objectId: draft.id,
        status: 'validation_failed',
        dxfFilename: null,
        generatorSeam: null,
        diagnostics: preValidation.errors.map((e) => e.message),
        timestamp: Date.now(),
      });
      return;
    }

    setIsGenerating(true);
    setGenerationResult(null);

    eventBus.emit('generation.requested', {
      objectId: draft.id,
      category: draft.category,
      source: 'work',
    });

    const result = await dxfGenerationAdapter.generateDetail(draft);

    setGenerationResult(result);
    setIsGenerating(false);
    setActiveTab('artifact');

    eventBus.emit('generation.completed', {
      objectId: draft.id,
      status: result.status === 'success' ? 'success' : result.status === 'validation_failed' ? 'validation_failed' : 'generation_error',
      dxfFilename: result.dxfFilename,
      generatorSeam: result.generatorSeam,
      diagnostics: result.diagnostics.map((d) => d.message),
      timestamp: Date.now(),
    });
  }, [activeObject]);

  // ── Derived state ────────────────────────────────────────────────────
  const assemblyDraft = activeObject ? extractAssemblyDraft(activeObject) : null;
  const isAssembly = activeObject?.type === 'assembly' && !!assemblyDraft;

  const tabs: { key: WorkTab; label: string }[] = [
    { key: 'detail', label: 'Detail' },
    { key: 'drawing', label: 'Drawing' },
    { key: 'validation', label: 'Validation' },
    { key: 'artifact', label: 'Artifacts' },
    { key: 'spatial', label: 'Spatial' },
  ];

  const validationBadge = validationResult?.issues?.length ?? 0;

  return (
    <PanelShell panelId="work" title="Work" basis={isAssembly ? 'draft' : 'mock'} badgeCount={validationBadge > 0 ? validationBadge : undefined}>
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
                      {assemblyDraft && (
                        <span style={{ color: tokens.color.fgMuted }}>Category: <span style={{ color: tokens.color.accentPrimary }}>{assemblyDraft.category}</span></span>
                      )}
                    </div>
                  </div>

                  {/* Assembly Layer Summary */}
                  {assemblyDraft && (
                    <div style={{
                      padding: tokens.space.md,
                      background: tokens.color.bgBase,
                      borderRadius: tokens.radius.sm,
                      border: `1px solid ${tokens.color.border}`,
                      marginBottom: tokens.space.md,
                      fontSize: tokens.font.sizeSm,
                    }}>
                      <div style={{ fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.sm }}>Assembly Layers</div>
                      {assemblyDraft.layers.membrane_1 && (
                        <div style={{ marginBottom: '2px' }}><span style={{ color: tokens.color.fgMuted }}>Membrane:</span> {assemblyDraft.layers.membrane_1}</div>
                      )}
                      {assemblyDraft.layers.coverboard_1 && (
                        <div style={{ marginBottom: '2px' }}><span style={{ color: tokens.color.fgMuted }}>Coverboard:</span> {assemblyDraft.layers.coverboard_1}</div>
                      )}
                      {assemblyDraft.layers.insulation_layer_1 && (
                        <div style={{ marginBottom: '2px' }}><span style={{ color: tokens.color.fgMuted }}>Insulation 1:</span> {assemblyDraft.layers.insulation_layer_1}</div>
                      )}
                      {assemblyDraft.layers.insulation_layer_2 && (
                        <div style={{ marginBottom: '2px' }}><span style={{ color: tokens.color.fgMuted }}>Insulation 2:</span> {assemblyDraft.layers.insulation_layer_2}</div>
                      )}
                      {assemblyDraft.layers.vapor_barrier && (
                        <div style={{ marginBottom: '2px' }}><span style={{ color: tokens.color.fgMuted }}>Vapor Barrier:</span> {assemblyDraft.layers.vapor_barrier}</div>
                      )}
                      <div><span style={{ color: tokens.color.fgMuted }}>Deck:</span> {assemblyDraft.layers.deck_slope}</div>
                      {assemblyDraft.layers.manufacturer && (
                        <div style={{ marginTop: tokens.space.sm, color: tokens.color.fgMuted }}>
                          Manufacturer: <span style={{ color: tokens.color.fgSecondary }}>{assemblyDraft.layers.manufacturer}</span>
                          {assemblyDraft.layers.system && <> / {assemblyDraft.layers.system}</>}
                        </div>
                      )}
                    </div>
                  )}

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

                    {/* Generate Detail — only for assembly objects with layer data */}
                    {isAssembly && (
                      <button
                        onClick={handleGenerateDetail}
                        disabled={isGenerating}
                        style={{
                          padding: `${tokens.space.sm} ${tokens.space.md}`,
                          background: tokens.color.success,
                          color: '#fff',
                          border: 'none',
                          borderRadius: tokens.radius.sm,
                          cursor: isGenerating ? 'wait' : 'pointer',
                          fontSize: tokens.font.sizeSm,
                          fontFamily: tokens.font.family,
                          fontWeight: tokens.font.weightSemibold,
                          opacity: isGenerating ? 0.6 : 1,
                        }}
                      >
                        {isGenerating ? 'Generating...' : 'Generate Detail'}
                      </button>
                    )}

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
                <div>
                  <h3 style={{ fontSize: tokens.font.sizeMd, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.md }}>
                    DXF Generation
                  </h3>

                  {isGenerating && (
                    <div style={{
                      padding: tokens.space.md,
                      background: tokens.color.accentPrimary + '15',
                      border: `1px solid ${tokens.color.accentPrimary}`,
                      borderRadius: tokens.radius.sm,
                      fontSize: tokens.font.sizeSm,
                      color: tokens.color.accentPrimary,
                    }}>
                      Generating DXF detail via AssemblyDXFGenerator...
                    </div>
                  )}

                  {!isGenerating && !generationResult && (
                    <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
                      {isAssembly ? (
                        <div style={{ padding: tokens.space.lg, textAlign: 'center', border: `1px dashed ${tokens.color.border}`, borderRadius: tokens.radius.md }}>
                          Select "Generate Detail" on the Detail tab to create a real DXF from this assembly draft.
                        </div>
                      ) : (
                        <div style={{ padding: tokens.space.lg, textAlign: 'center', border: `1px dashed ${tokens.color.border}`, borderRadius: tokens.radius.md }}>
                          Generation is available for assembly objects with layer data.
                        </div>
                      )}
                    </div>
                  )}

                  {generationResult && (
                    <div>
                      {/* Status badge */}
                      <div style={{
                        display: 'inline-block',
                        padding: `${tokens.space.sm} ${tokens.space.sm}`,
                        borderRadius: tokens.radius.sm,
                        background: generationResult.status === 'success'
                          ? tokens.color.success + '20'
                          : tokens.color.error + '20',
                        color: generationResult.status === 'success'
                          ? tokens.color.success
                          : tokens.color.error,
                        fontSize: tokens.font.sizeSm,
                        fontWeight: tokens.font.weightSemibold,
                        marginBottom: tokens.space.md,
                      }}>
                        {generationResult.status.toUpperCase().replace(/_/g, ' ')}
                      </div>

                      {/* Success — download affordance */}
                      {generationResult.status === 'success' && generationResult.dxfFilename && (
                        <div style={{
                          padding: tokens.space.md,
                          background: tokens.color.success + '10',
                          border: `1px solid ${tokens.color.success}40`,
                          borderRadius: tokens.radius.sm,
                          marginBottom: tokens.space.md,
                        }}>
                          <div style={{ fontSize: tokens.font.sizeSm, marginBottom: tokens.space.sm }}>
                            <span style={{ fontWeight: tokens.font.weightSemibold }}>DXF Output:</span>{' '}
                            <code style={{ fontFamily: tokens.font.familyMono }}>{generationResult.dxfFilename}</code>
                          </div>
                          <div style={{ fontSize: tokens.font.sizeSm, marginBottom: tokens.space.sm, color: tokens.color.fgMuted }}>
                            <span style={{ fontWeight: tokens.font.weightMedium }}>Generator Seam:</span>{' '}
                            <code style={{ fontFamily: tokens.font.familyMono }}>{generationResult.generatorSeam}</code>
                          </div>
                          <div style={{ fontSize: tokens.font.sizeSm, color: tokens.color.fgMuted }}>
                            <span style={{ fontWeight: tokens.font.weightMedium }}>Path:</span>{' '}
                            <code style={{ fontFamily: tokens.font.familyMono }}>{generationResult.dxfPath}</code>
                          </div>
                          <a
                            href={dxfGenerationAdapter.getDownloadUrl(generationResult.dxfFilename)}
                            download
                            style={{
                              display: 'inline-block',
                              marginTop: tokens.space.md,
                              padding: `${tokens.space.sm} ${tokens.space.md}`,
                              background: tokens.color.success,
                              color: '#fff',
                              borderRadius: tokens.radius.sm,
                              fontSize: tokens.font.sizeSm,
                              fontFamily: tokens.font.family,
                              fontWeight: tokens.font.weightSemibold,
                              textDecoration: 'none',
                              cursor: 'pointer',
                            }}
                          >
                            Download DXF
                          </a>
                        </div>
                      )}

                      {/* Diagnostics */}
                      {generationResult.diagnostics.length > 0 && (
                        <div>
                          <div style={{ fontWeight: tokens.font.weightSemibold, fontSize: tokens.font.sizeSm, marginBottom: tokens.space.sm }}>
                            Diagnostics ({generationResult.diagnostics.length})
                          </div>
                          {generationResult.diagnostics.map((diag, idx) => (
                            <div key={idx} style={{
                              padding: tokens.space.sm,
                              marginBottom: tokens.space.sm,
                              background: tokens.color.bgBase,
                              borderRadius: tokens.radius.sm,
                              borderLeft: `3px solid ${tokens.color.error}`,
                              fontSize: tokens.font.sizeSm,
                              lineHeight: tokens.font.lineNormal,
                            }}>
                              <span style={{
                                fontWeight: tokens.font.weightMedium,
                                fontFamily: tokens.font.familyMono,
                                color: tokens.color.error,
                                marginRight: tokens.space.sm,
                              }}>
                                {diag.code}
                              </span>
                              {diag.message}
                              {diag.field && (
                                <span style={{ color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono, marginLeft: tokens.space.sm }}>
                                  [{diag.field}]
                                </span>
                              )}
                            </div>
                          ))}
                        </div>
                      )}

                      <div style={{ marginTop: tokens.space.md, fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                        Draft ID: {generationResult.draftId} | Generated: {new Date(generationResult.timestamp).toLocaleTimeString()}
                      </div>
                    </div>
                  )}
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
