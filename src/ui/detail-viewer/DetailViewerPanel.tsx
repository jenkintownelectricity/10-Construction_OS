/**
 * Detail Viewer Panel — Real artifact viewing surface
 *
 * Displays generated detail artifacts with:
 *   1. SVG preview derived from the same artifact lineage as DXF
 *   2. Artifact metadata (status, type, filename, seam)
 *   3. DXF download affordance
 *   4. Generation diagnostics
 *   5. Fail-closed display for unsupported categories
 *
 * Flow: assembly draft → generate detail → artifact metadata → viewer
 *
 * Governance: VKGL04R — Ring 1 Outcome 1: "Detail Viewer UI surface"
 */

import { useCallback, useState } from 'react';
import { tokens } from '../theme/tokens';
import { getSampleFireproofingDraft } from '../assembly-builder/fireproofingSourceAdapter';
import { generateDetailPreview } from './detailGenerationAdapter';
import { validateSourceContext } from './validateSourceContext';
import { mapContextToRoofingDraft } from './contextToRoofingDraft';
import { eventBus } from '../events/EventBus';
import { generationStore, type LatestResult } from '../stores/generationStore';
import { activeArtifactDisplay } from '../viewer/ActiveArtifactDisplay';
import type { DetailPreviewResult, ViewerTab, DetailCategory } from './types';

// ─── Styles ──────────────────────────────────────────────────────────

const sectionStyle: React.CSSProperties = {
  marginBottom: tokens.space.lg,
  padding: tokens.space.md,
  background: tokens.color.bgBase,
  borderRadius: tokens.radius.md,
  border: `1px solid ${tokens.color.border}`,
};

const metaRowStyle: React.CSSProperties = {
  display: 'flex',
  justifyContent: 'space-between',
  padding: `${tokens.space.xs} 0`,
  borderBottom: `1px solid ${tokens.color.borderSubtle}`,
  fontSize: tokens.font.sizeSm,
};

const metaLabelStyle: React.CSSProperties = {
  color: tokens.color.fgMuted,
  fontWeight: tokens.font.weightMedium,
  textTransform: 'uppercase' as const,
  fontSize: tokens.font.sizeXs,
  letterSpacing: '0.04em',
};

const metaValueStyle: React.CSSProperties = {
  color: tokens.color.fgPrimary,
  fontFamily: tokens.font.familyMono,
  fontSize: tokens.font.sizeXs,
};

const btnPrimary: React.CSSProperties = {
  padding: `${tokens.space.sm} ${tokens.space.lg}`,
  background: tokens.color.accentPrimary,
  color: '#fff',
  border: 'none',
  borderRadius: tokens.radius.sm,
  cursor: 'pointer',
  fontSize: tokens.font.sizeSm,
  fontFamily: tokens.font.family,
  fontWeight: tokens.font.weightMedium,
};

const btnSecondary: React.CSSProperties = {
  ...btnPrimary,
  background: tokens.color.bgElevated,
  color: tokens.color.fgSecondary,
  border: `1px solid ${tokens.color.border}`,
};

// ─── Status Badge ────────────────────────────────────────────────────

function StatusBadge({ status }: { status: string }) {
  const colorMap: Record<string, string> = {
    success: '#22c55e',
    pending: tokens.color.fgMuted,
    generating: tokens.color.accentPrimary,
    validation_failed: tokens.color.error,
    generation_error: tokens.color.error,
    unsupported: '#f59e0b',
  };
  const color = colorMap[status] ?? tokens.color.fgMuted;

  return (
    <span style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: tokens.space.xs,
      padding: `2px ${tokens.space.sm}`,
      borderRadius: tokens.radius.sm,
      background: `${color}15`,
      color,
      fontSize: tokens.font.sizeXs,
      fontWeight: tokens.font.weightSemibold,
      textTransform: 'uppercase',
    }}>
      <span style={{
        width: '6px',
        height: '6px',
        borderRadius: '50%',
        background: color,
      }} />
      {status.replace(/_/g, ' ')}
    </span>
  );
}

// ─── Download helper ─────────────────────────────────────────────────

function downloadDxf(content: string, filename: string) {
  const blob = new Blob([content], { type: 'application/dxf' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

// ─── Component ───────────────────────────────────────────────────────

export function DetailViewerPanel() {
  const [activeTab, setActiveTab] = useState<ViewerTab>('preview');
  const [previewResult, setPreviewResult] = useState<DetailPreviewResult | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<DetailCategory>('roofing');
  const [isGenerating, setIsGenerating] = useState(false);

  // ─── Generate roofing detail from sourceContext ──────────────────

  const handleGenerateRoofing = useCallback(() => {
    setIsGenerating(true);
    setSelectedCategory('roofing');

    // Step 1: Begin request (idle → validating)
    generationStore.beginRequest();

    // Step 2: Validate source context
    const sourceContext = generationStore.getState().sourceContext;
    const validation = validateSourceContext(sourceContext);
    if (!validation.valid) {
      generationStore.completeError(validation.errorCode!, validation.errorMessage!);
      setIsGenerating(false);
      setPreviewResult(null);
      setActiveTab('diagnostics');
      return;
    }

    // Step 3: Map context to draft (validating → mapping)
    generationStore.advanceToMapping();
    const mapping = mapContextToRoofingDraft(sourceContext!);
    if (!mapping.success) {
      generationStore.completeError(mapping.errorCode!, mapping.errorMessage!);
      setIsGenerating(false);
      setPreviewResult(null);
      setActiveTab('diagnostics');
      return;
    }

    // Step 4: Generate detail (mapping → generating)
    generationStore.advanceToGenerating();
    const result = generateDetailPreview(mapping.draft!, 'roofing');
    setPreviewResult(result);
    setIsGenerating(false);

    if (result.success) {
      setActiveTab('preview');
      // Step 5: Store result (generating → success)
      const latestResult: LatestResult = {
        sourceSubmittalId: sourceContext!.submittalId,
        detailId: result.detail_id,
        artifactType: result.artifact_type,
        filename: result.artifact_filename,
        success: true,
        generationStatus: result.generation_status,
        artifactIds: [result.svg_artifact_id, result.dxf_artifact_id].filter(Boolean),
      };
      generationStore.completeSuccess(latestResult);

      // Step 5b: Publish SVG to active artifact display for Viewer rendering
      activeArtifactDisplay.setPayload({
        svgContent: result.svg_content,
        detailId: result.detail_id,
        sourceSubmittalId: sourceContext!.submittalId,
        artifactType: result.artifact_type,
        filename: result.artifact_filename,
      });
    } else {
      setActiveTab('diagnostics');
      generationStore.completeError('GENERATION_FAILED', result.diagnostics.join('; '));
      // Clear active artifact on failure
      activeArtifactDisplay.clear();
    }

    // Step 6: Emit generation.completed for Atlas auto-navigate
    eventBus.emit('generation.completed', {
      objectId: result.detail_id,
      status: result.success ? 'success' : 'generation_error',
      dxfFilename: result.dxf_available ? result.artifact_filename : null,
      generatorSeam: result.generator_seam,
      diagnostics: [...result.diagnostics],
      timestamp: Date.now(),
    });
  }, []);

  // ─── Generate fireproofing (FAIL_CLOSED) ──────────────────────────

  const handleGenerateFireproofing = useCallback(() => {
    setIsGenerating(true);
    setSelectedCategory('fireproofing');
    generationStore.beginRequest();
    generationStore.advanceToMapping();
    generationStore.advanceToGenerating();

    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');
    setPreviewResult(result);
    setIsGenerating(false);
    setActiveTab(result.success ? 'preview' : 'diagnostics');

    // Always fail-closed for fireproofing
    generationStore.completeError(
      'UNSUPPORTED_CATEGORY',
      result.diagnostics.join('; '),
    );
    // Clear active artifact on fail-closed
    activeArtifactDisplay.clear();

    eventBus.emit('generation.completed', {
      objectId: result.detail_id,
      status: 'generation_error',
      dxfFilename: null,
      generatorSeam: result.generator_seam,
      diagnostics: [...result.diagnostics],
      timestamp: Date.now(),
    });
  }, []);

  const handleClear = useCallback(() => {
    setPreviewResult(null);
    setActiveTab('preview');
    activeArtifactDisplay.clear();
  }, []);

  const handleDownloadDxf = useCallback(() => {
    if (previewResult?.dxf_available && previewResult.dxf_content) {
      downloadDxf(previewResult.dxf_content, previewResult.artifact_filename || 'detail.dxf');
    }
  }, [previewResult]);

  // ─── Tab bar ───────────────────────────────────────────────────────

  const tabs: { key: ViewerTab; label: string }[] = [
    { key: 'preview', label: 'Preview' },
    { key: 'artifacts', label: 'Artifacts' },
    { key: 'diagnostics', label: 'Diagnostics' },
  ];

  const diagnosticCount = previewResult?.diagnostics.length ?? 0;
  const errorCount = previewResult?.errors.length ?? 0;

  return (
    <div style={{
      height: '100%',
      display: 'flex',
      flexDirection: 'column',
      background: tokens.color.bgSurface,
      color: tokens.color.fgPrimary,
      fontFamily: tokens.font.family,
    }}>
      {/* Header */}
      <div style={{
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: tokens.color.bgElevated,
        borderBottom: `1px solid ${tokens.color.border}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        minHeight: '40px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <span style={{
            fontSize: tokens.font.sizeMd,
            fontWeight: tokens.font.weightSemibold,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
          }}>
            DETAIL VIEWER
          </span>
          {previewResult && (
            <StatusBadge status={previewResult.generation_status} />
          )}
          {!previewResult && (
            <span style={{
              fontSize: tokens.font.sizeXs,
              color: tokens.color.fgMuted,
              fontStyle: 'italic',
            }}>
              No artifact loaded
            </span>
          )}
        </div>
        <div style={{ display: 'flex', gap: tokens.space.sm }}>
          <button onClick={handleGenerateRoofing} style={btnPrimary} disabled={isGenerating}>
            Generate Roofing Detail
          </button>
          <button onClick={handleGenerateFireproofing} style={btnSecondary} disabled={isGenerating}>
            Generate Fireproofing Detail
          </button>
          {previewResult && (
            <button onClick={handleClear} style={{
              ...btnSecondary,
              color: tokens.color.error,
              borderColor: tokens.color.error,
            }}>
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Tab Bar */}
      <div style={{ display: 'flex', gap: '1px', background: tokens.color.border }}>
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
              transition: `all ${tokens.transition.fast}`,
            }}
          >
            {tab.label}
            {tab.key === 'diagnostics' && (errorCount > 0 || diagnosticCount > 0) && (
              <span style={{
                marginLeft: tokens.space.xs,
                background: errorCount > 0 ? tokens.color.error : tokens.color.accentPrimary,
                color: '#fff',
                padding: '1px 6px',
                borderRadius: '8px',
                fontSize: '0.7rem',
                fontWeight: tokens.font.weightBold,
              }}>
                {errorCount > 0 ? errorCount : diagnosticCount}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflow: 'auto', padding: tokens.space.md }}>

        {/* ─── No Result ─── */}
        {!previewResult && (
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            height: '100%',
            color: tokens.color.fgMuted,
            gap: tokens.space.md,
          }}>
            <span style={{ fontSize: tokens.font.sizeLg }}>
              No detail artifact loaded
            </span>
            <span style={{ fontSize: tokens.font.sizeSm }}>
              Use "Generate Roofing Detail" to produce an artifact from the selected Shop Drawings context.
            </span>
            <span style={{ fontSize: tokens.font.sizeXs, fontStyle: 'italic' }}>
              Flow: Shop Drawings selection → validate → map to draft → generate detail → view here
            </span>
          </div>
        )}

        {/* ─── PREVIEW TAB ─── */}
        {previewResult && activeTab === 'preview' && (
          <div>
            {previewResult.success && previewResult.svg_content ? (
              <div>
                {/* Preview label */}
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                  marginBottom: tokens.space.md,
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
                    <span style={{
                      fontSize: tokens.font.sizeSm,
                      fontWeight: tokens.font.weightSemibold,
                      color: tokens.color.fgPrimary,
                    }}>
                      Runtime-Derived SVG Preview
                    </span>
                    <span style={{
                      fontSize: tokens.font.sizeXs,
                      color: tokens.color.derived ?? tokens.color.fgMuted,
                      padding: '2px 8px',
                      borderRadius: tokens.radius.sm,
                      background: `${tokens.color.derived ?? tokens.color.fgMuted}15`,
                    }}>
                      derived
                    </span>
                  </div>
                  {previewResult.dxf_available && (
                    <button onClick={handleDownloadDxf} style={btnPrimary}>
                      Download DXF
                    </button>
                  )}
                </div>

                {/* SVG Preview */}
                <div style={{
                  ...sectionStyle,
                  padding: tokens.space.lg,
                  overflow: 'auto',
                  maxHeight: '500px',
                  background: '#ffffff',
                  display: 'flex',
                  justifyContent: 'center',
                }}>
                  <div
                    dangerouslySetInnerHTML={{ __html: previewResult.svg_content }}
                    style={{ maxWidth: '100%' }}
                  />
                </div>

                {/* Quick metadata */}
                <div style={sectionStyle}>
                  <div style={metaRowStyle}>
                    <span style={metaLabelStyle}>Detail ID</span>
                    <span style={metaValueStyle}>{previewResult.detail_id}</span>
                  </div>
                  <div style={metaRowStyle}>
                    <span style={metaLabelStyle}>Artifact Type</span>
                    <span style={metaValueStyle}>{previewResult.artifact_type}</span>
                  </div>
                  <div style={metaRowStyle}>
                    <span style={metaLabelStyle}>DXF Filename</span>
                    <span style={metaValueStyle}>{previewResult.artifact_filename}</span>
                  </div>
                  <div style={metaRowStyle}>
                    <span style={metaLabelStyle}>Generator Seam</span>
                    <span style={metaValueStyle}>{previewResult.generator_seam}</span>
                  </div>
                </div>
              </div>
            ) : (
              /* Fail-closed view */
              <div style={{
                ...sectionStyle,
                borderColor: tokens.color.error,
                background: `${tokens.color.error}08`,
              }}>
                <div style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: tokens.space.sm,
                  marginBottom: tokens.space.md,
                }}>
                  <StatusBadge status={previewResult.generation_status} />
                  <span style={{
                    fontSize: tokens.font.sizeSm,
                    color: tokens.color.fgPrimary,
                  }}>
                    Detail generation was not completed
                  </span>
                </div>
                {previewResult.diagnostics.map((diag, i) => (
                  <div key={i} style={{
                    padding: `${tokens.space.sm} ${tokens.space.md}`,
                    background: tokens.color.bgBase,
                    borderRadius: tokens.radius.sm,
                    marginBottom: tokens.space.xs,
                    fontSize: tokens.font.sizeXs,
                    fontFamily: tokens.font.familyMono,
                    color: tokens.color.error,
                  }}>
                    {diag}
                  </div>
                ))}
                {previewResult.errors.map((err, i) => (
                  <div key={`err-${i}`} style={{
                    padding: `${tokens.space.sm} ${tokens.space.md}`,
                    background: tokens.color.bgBase,
                    borderRadius: tokens.radius.sm,
                    marginBottom: tokens.space.xs,
                    fontSize: tokens.font.sizeXs,
                    fontFamily: tokens.font.familyMono,
                    color: tokens.color.fgMuted,
                  }}>
                    [{err.code}] {err.message}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* ─── ARTIFACTS TAB ─── */}
        {previewResult && activeTab === 'artifacts' && (
          <div>
            <div style={sectionStyle}>
              <div style={{
                fontSize: tokens.font.sizeSm,
                fontWeight: tokens.font.weightSemibold,
                marginBottom: tokens.space.md,
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
              }}>
                Artifact Metadata
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Generation Status</span>
                <StatusBadge status={previewResult.generation_status} />
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Category</span>
                <span style={metaValueStyle}>{previewResult.category}</span>
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Detail ID</span>
                <span style={metaValueStyle}>{previewResult.detail_id || '—'}</span>
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Artifact Type</span>
                <span style={metaValueStyle}>{previewResult.artifact_type || '—'}</span>
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Artifact Filename / Path</span>
                <span style={metaValueStyle}>{previewResult.artifact_filename || '—'}</span>
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Generator Seam</span>
                <span style={metaValueStyle}>{previewResult.generator_seam}</span>
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Seam ID</span>
                <span style={metaValueStyle}>{previewResult.seam_id}</span>
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Manifest ID</span>
                <span style={metaValueStyle}>{previewResult.manifest_id || '—'}</span>
              </div>
              <div style={metaRowStyle}>
                <span style={metaLabelStyle}>Instruction Set ID</span>
                <span style={metaValueStyle}>{previewResult.instruction_set_id || '—'}</span>
              </div>
            </div>

            {/* SVG artifact */}
            {previewResult.svg_artifact_id && (
              <div style={sectionStyle}>
                <div style={{
                  fontSize: tokens.font.sizeSm,
                  fontWeight: tokens.font.weightSemibold,
                  marginBottom: tokens.space.sm,
                }}>
                  SVG Artifact
                </div>
                <div style={metaRowStyle}>
                  <span style={metaLabelStyle}>Artifact ID</span>
                  <span style={metaValueStyle}>{previewResult.svg_artifact_id}</span>
                </div>
                <div style={metaRowStyle}>
                  <span style={metaLabelStyle}>Content Hash</span>
                  <span style={metaValueStyle}>{previewResult.svg_content_hash}</span>
                </div>
              </div>
            )}

            {/* DXF artifact */}
            {previewResult.dxf_artifact_id && (
              <div style={sectionStyle}>
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginBottom: tokens.space.sm,
                }}>
                  <span style={{
                    fontSize: tokens.font.sizeSm,
                    fontWeight: tokens.font.weightSemibold,
                  }}>
                    DXF Artifact
                  </span>
                  {previewResult.dxf_available && (
                    <button onClick={handleDownloadDxf} style={btnSecondary}>
                      Download DXF
                    </button>
                  )}
                </div>
                <div style={metaRowStyle}>
                  <span style={metaLabelStyle}>Artifact ID</span>
                  <span style={metaValueStyle}>{previewResult.dxf_artifact_id}</span>
                </div>
                <div style={metaRowStyle}>
                  <span style={metaLabelStyle}>Content Hash</span>
                  <span style={metaValueStyle}>{previewResult.dxf_content_hash}</span>
                </div>
                <div style={metaRowStyle}>
                  <span style={metaLabelStyle}>Available</span>
                  <span style={metaValueStyle}>{previewResult.dxf_available ? 'Yes' : 'No'}</span>
                </div>
              </div>
            )}

            {/* Lineage */}
            {previewResult.lineage && Object.keys(previewResult.lineage).length > 0 && (
              <div style={sectionStyle}>
                <div style={{
                  fontSize: tokens.font.sizeSm,
                  fontWeight: tokens.font.weightSemibold,
                  marginBottom: tokens.space.sm,
                }}>
                  Artifact Lineage
                </div>
                <pre style={{
                  fontSize: tokens.font.sizeXs,
                  fontFamily: tokens.font.familyMono,
                  color: tokens.color.fgSecondary,
                  background: tokens.color.bgBase,
                  padding: tokens.space.md,
                  borderRadius: tokens.radius.sm,
                  overflow: 'auto',
                  maxHeight: '200px',
                  margin: 0,
                }}>
                  {JSON.stringify(previewResult.lineage, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}

        {/* ─── DIAGNOSTICS TAB ─── */}
        {previewResult && activeTab === 'diagnostics' && (
          <div>
            {/* Diagnostics */}
            <div style={sectionStyle}>
              <div style={{
                fontSize: tokens.font.sizeSm,
                fontWeight: tokens.font.weightSemibold,
                marginBottom: tokens.space.md,
                textTransform: 'uppercase',
                letterSpacing: '0.04em',
              }}>
                Generation Diagnostics
              </div>
              {previewResult.diagnostics.length === 0 && previewResult.errors.length === 0 && (
                <div style={{
                  color: tokens.color.fgMuted,
                  fontSize: tokens.font.sizeSm,
                  fontStyle: 'italic',
                }}>
                  No diagnostics
                </div>
              )}
              {previewResult.diagnostics.map((diag, i) => (
                <div key={i} style={{
                  padding: `${tokens.space.sm} ${tokens.space.md}`,
                  background: diag.includes('FAIL_CLOSED')
                    ? `${tokens.color.error}10`
                    : tokens.color.bgBase,
                  borderRadius: tokens.radius.sm,
                  marginBottom: tokens.space.xs,
                  fontSize: tokens.font.sizeXs,
                  fontFamily: tokens.font.familyMono,
                  color: diag.includes('FAIL_CLOSED')
                    ? tokens.color.error
                    : tokens.color.fgSecondary,
                  borderLeft: diag.includes('FAIL_CLOSED')
                    ? `3px solid ${tokens.color.error}`
                    : `3px solid ${tokens.color.accentPrimary}`,
                }}>
                  {diag}
                </div>
              ))}
            </div>

            {/* Errors */}
            {previewResult.errors.length > 0 && (
              <div style={{
                ...sectionStyle,
                borderColor: tokens.color.error,
              }}>
                <div style={{
                  fontSize: tokens.font.sizeSm,
                  fontWeight: tokens.font.weightSemibold,
                  marginBottom: tokens.space.md,
                  color: tokens.color.error,
                  textTransform: 'uppercase',
                  letterSpacing: '0.04em',
                }}>
                  Errors
                </div>
                {previewResult.errors.map((err, i) => (
                  <div key={i} style={{
                    padding: `${tokens.space.sm} ${tokens.space.md}`,
                    background: `${tokens.color.error}08`,
                    borderRadius: tokens.radius.sm,
                    marginBottom: tokens.space.xs,
                    borderLeft: `3px solid ${tokens.color.error}`,
                  }}>
                    <div style={{
                      fontSize: tokens.font.sizeXs,
                      fontWeight: tokens.font.weightSemibold,
                      color: tokens.color.error,
                      fontFamily: tokens.font.familyMono,
                    }}>
                      {err.code}
                    </div>
                    <div style={{
                      fontSize: tokens.font.sizeXs,
                      color: tokens.color.fgSecondary,
                      marginTop: '2px',
                    }}>
                      {err.message}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
