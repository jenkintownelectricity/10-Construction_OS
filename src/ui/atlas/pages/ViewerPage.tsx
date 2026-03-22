/**
 * Construction Atlas — Viewer Page
 *
 * Wraps ShopDrawingsShell with an artifact result banner.
 * When a generation result exists in generationStore, shows
 * the artifact metadata and SVG preview above the document viewer.
 *
 * This is NOT a second viewer pipeline — it reads from the same
 * generationStore that DetailViewerPanel writes to.
 *
 * Governance: VKGL04R — No second renderer path.
 */

import { useCallback, useEffect, useState } from 'react';
import { tokens } from '../../theme/tokens';
import { ShopDrawingsShell } from '../../shop-drawings/ShopDrawingsShell';
import { generationStore } from '../../stores/generationStore';
import type { DetailPreviewResult } from '../../detail-viewer/types';
import type { GenerationSourceContext } from '../../stores/generationStore';
import type { AtlasRoute } from '../types';

interface ViewerPageProps {
  onNavigate: (route: AtlasRoute) => void;
}

export function ViewerPage({ onNavigate }: ViewerPageProps) {
  const [result, setResult] = useState<DetailPreviewResult | null>(null);
  const [sourceContext, setSourceContext] = useState<GenerationSourceContext | null>(null);
  const [bannerExpanded, setBannerExpanded] = useState(true);

  // Subscribe to generationStore
  useEffect(() => {
    const sync = () => {
      const state = generationStore.getState();
      setResult(state.lastResult);
      setSourceContext(state.sourceContext);
    };
    sync();
    return generationStore.subscribe(sync);
  }, []);

  const handleDismissBanner = useCallback(() => {
    setBannerExpanded(false);
  }, []);

  const handleBackToShopDrawings = useCallback(() => {
    onNavigate('shop-drawings');
  }, [onNavigate]);

  const handleDownloadDxf = useCallback(() => {
    if (result?.dxf_available && result.dxf_content) {
      const blob = new Blob([result.dxf_content], { type: 'application/dxf' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = result.artifact_filename || 'detail.dxf';
      a.click();
      URL.revokeObjectURL(url);
    }
  }, [result]);

  const hasSuccessResult = result?.success === true;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      {/* Artifact Result Banner */}
      {result && bannerExpanded && (
        <div style={{
          flexShrink: 0,
          background: hasSuccessResult ? tokens.color.bgElevated : `${tokens.color.error}10`,
          borderBottom: `1px solid ${hasSuccessResult ? tokens.color.borderActive : tokens.color.error}`,
          padding: '12px 16px',
          fontFamily: tokens.font.family,
          color: tokens.color.fgPrimary,
        }}>
          {/* Banner header row */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: hasSuccessResult ? '8px' : '0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{
                display: 'inline-flex', alignItems: 'center', gap: '4px',
                padding: '2px 10px', borderRadius: '10px', fontSize: '11px', fontWeight: 700,
                background: hasSuccessResult ? `${tokens.color.success}20` : `${tokens.color.error}20`,
                color: hasSuccessResult ? tokens.color.success : tokens.color.error,
              }}>
                <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'currentColor' }} />
                {result.generation_status.replace(/_/g, ' ').toUpperCase()}
              </span>

              <span style={{ fontSize: '13px', fontWeight: 600 }}>
                {hasSuccessResult ? 'Generation Complete' : 'Generation Failed'}
              </span>

              {sourceContext && (
                <span style={{ fontSize: '11px', color: tokens.color.fgMuted }}>
                  from {sourceContext.submittalId} — {sourceContext.submittalTitle}
                </span>
              )}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              {hasSuccessResult && result.dxf_available && (
                <button onClick={handleDownloadDxf} style={{
                  padding: '4px 12px', borderRadius: '4px',
                  background: tokens.color.accentPrimary, color: '#fff',
                  border: 'none', fontSize: '11px', fontWeight: 600, cursor: 'pointer',
                }}>
                  Download DXF
                </button>
              )}
              <button onClick={handleBackToShopDrawings} style={{
                padding: '4px 12px', borderRadius: '4px',
                background: 'transparent', color: tokens.color.fgMuted,
                border: `1px solid ${tokens.color.border}`, fontSize: '11px', cursor: 'pointer',
              }}>
                Back to Shop Drawings
              </button>
              <button onClick={handleDismissBanner} style={{
                padding: '4px 8px', background: 'transparent',
                border: 'none', color: tokens.color.fgMuted, cursor: 'pointer', fontSize: '14px',
              }}>
                {'\u2715'}
              </button>
            </div>
          </div>

          {/* Artifact metadata row (success only) */}
          {hasSuccessResult && (
            <div style={{ display: 'flex', gap: '24px', fontSize: '11px', color: tokens.color.fgSecondary, fontFamily: tokens.font.familyMono }}>
              <span>Detail: {result.detail_id}</span>
              <span>Type: {result.artifact_type}</span>
              <span>File: {result.artifact_filename}</span>
              <span>Seam: {result.generator_seam}</span>
              <span>SVG: {result.svg_artifact_id}</span>
              {result.dxf_available && <span>DXF: {result.dxf_artifact_id}</span>}
            </div>
          )}

          {/* Diagnostics for failed generation */}
          {!hasSuccessResult && result.diagnostics.length > 0 && (
            <div style={{ marginTop: '8px' }}>
              {result.diagnostics.map((d, i) => (
                <div key={i} style={{
                  fontSize: '11px', fontFamily: tokens.font.familyMono,
                  color: tokens.color.error, padding: '2px 0',
                }}>
                  {d}
                </div>
              ))}
            </div>
          )}

          {/* SVG mini-preview for successful generation */}
          {hasSuccessResult && result.svg_content && (
            <div style={{
              marginTop: '8px', padding: '8px',
              background: '#fff', borderRadius: '4px',
              maxHeight: '200px', overflow: 'auto',
              display: 'flex', justifyContent: 'center',
            }}>
              <div
                dangerouslySetInnerHTML={{ __html: result.svg_content }}
                style={{ maxWidth: '100%', maxHeight: '180px' }}
              />
            </div>
          )}
        </div>
      )}

      {/* Shop Drawings Shell (OMNI-VIEW viewer) — full remaining space */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        <ShopDrawingsShell onSwitchToWorkstation={() => onNavigate('tools')} />
      </div>
    </div>
  );
}
