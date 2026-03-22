/**
 * Construction Atlas — Viewer Page
 *
 * Wraps ShopDrawingsShell with an artifact result banner and
 * active SVG detail display. Reads latestResult metadata (thin
 * projection) from generationStore and SVG display payload from
 * activeArtifactDisplay module.
 *
 * When a successful generation payload is present, the SVG detail
 * is shown via SvgDetailView. Otherwise falls back to
 * ShopDrawingsShell (OMNI-VIEW viewer).
 *
 * Resets viewerAutoOpenPending on mount.
 *
 * Governance: VKGL04R — No second renderer path.
 * Display pattern informed by CADless_drawings modal viewer.
 */

import { useCallback, useEffect, useState } from 'react';
import { tokens } from '../../theme/tokens';
import { ShopDrawingsShell } from '../../shop-drawings/ShopDrawingsShell';
import {
  generationStore,
  type GenerationSourceContext,
  type LatestResult,
} from '../../stores/generationStore';
import { useActiveArtifact } from '../../viewer/ActiveArtifactDisplay';
import { SvgDetailView } from '../../viewer/SvgDetailView';
import type { AtlasRoute } from '../types';

interface ViewerPageProps {
  onNavigate: (route: AtlasRoute) => void;
}

export function ViewerPage({ onNavigate }: ViewerPageProps) {
  const [latestResult, setLatestResult] = useState<LatestResult | null>(null);
  const [sourceContext, setSourceContext] = useState<GenerationSourceContext | null>(null);
  const [bannerExpanded, setBannerExpanded] = useState(true);

  const activeArtifact = useActiveArtifact();

  // Subscribe to generationStore + reset viewerAutoOpenPending on mount
  useEffect(() => {
    generationStore.resetViewerAutoOpen();

    const sync = () => {
      const state = generationStore.getState();
      setLatestResult(state.latestResult);
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

  const hasSuccessResult = latestResult?.success === true;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', overflow: 'hidden' }}>
      {/* Artifact Result Banner (metadata only — no artifact content) */}
      {latestResult && bannerExpanded && (
        <div style={{
          flexShrink: 0,
          background: hasSuccessResult ? tokens.color.bgElevated : `${tokens.color.error}10`,
          borderBottom: `1px solid ${hasSuccessResult ? tokens.color.borderActive : tokens.color.error}`,
          padding: '12px 16px',
          fontFamily: tokens.font.family,
          color: tokens.color.fgPrimary,
        }}>
          {/* Banner header row */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
              <span style={{
                display: 'inline-flex', alignItems: 'center', gap: '4px',
                padding: '2px 10px', borderRadius: '10px', fontSize: '11px', fontWeight: 700,
                background: hasSuccessResult ? `${tokens.color.success}20` : `${tokens.color.error}20`,
                color: hasSuccessResult ? tokens.color.success : tokens.color.error,
              }}>
                <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: 'currentColor' }} />
                {latestResult.generationStatus.replace(/_/g, ' ').toUpperCase()}
              </span>

              <span style={{ fontSize: '13px', fontWeight: 600 }}>
                {hasSuccessResult ? 'Generation Complete' : 'Generation Failed'}
              </span>

              {sourceContext && (
                <span style={{ fontSize: '11px', color: tokens.color.fgMuted }}>
                  from {sourceContext.submittalId} — {sourceContext.title}
                </span>
              )}
            </div>

            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
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
            <div style={{ display: 'flex', gap: '24px', fontSize: '11px', color: tokens.color.fgSecondary, fontFamily: tokens.font.familyMono, marginTop: '8px' }}>
              <span>Source: {latestResult.sourceSubmittalId}</span>
              <span>Detail: {latestResult.detailId}</span>
              <span>Type: {latestResult.artifactType}</span>
              <span>File: {latestResult.filename}</span>
              {latestResult.artifactIds && latestResult.artifactIds.length > 0 && (
                <span>Artifacts: {latestResult.artifactIds.join(', ')}</span>
              )}
            </div>
          )}
        </div>
      )}

      {/* Main content area — SVG detail display or OMNI-VIEW fallback */}
      <div style={{ flex: 1, overflow: 'hidden' }}>
        {activeArtifact ? (
          <SvgDetailView
            svgContent={activeArtifact.svgContent}
            detailId={activeArtifact.detailId}
            artifactType={activeArtifact.artifactType}
            filename={activeArtifact.filename}
          />
        ) : (
          <ShopDrawingsShell onSwitchToWorkstation={() => onNavigate('tools')} />
        )}
      </div>
    </div>
  );
}
