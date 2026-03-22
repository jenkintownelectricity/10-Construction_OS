/**
 * Construction OS — Reference Panel
 *
 * Specs, code, source docs, citations.
 * Compare-ready. Source basis visibility. "Why this is here" surfaces.
 * Emits: object.selected, compare.requested
 * Subscribes to: truth-echo.propagated, reference.requested, compare.requested
 * State owned: activeReferences, compareState, referenceFilter
 */

import { useEffect, useState, useCallback } from 'react';
import { PanelShell } from '../PanelShell';
import { eventBus } from '../../events/EventBus';
import { adapters } from '../../adapters';
import { useActiveObject } from '../../stores/useSyncExternalStore';
import { tokens } from '../../theme/tokens';
import type { ReferenceEntry } from '../../contracts/adapters';

type RefFilter = 'all' | 'spec' | 'code' | 'citation' | 'document';

export function ReferencePanel() {
  const { activeObject, workspaceMode } = useActiveObject();
  const [references, setReferences] = useState<readonly ReferenceEntry[]>([]);
  const [filter, setFilter] = useState<RefFilter>('all');
  const [compareRefs, setCompareRefs] = useState<{ a: readonly ReferenceEntry[]; b: readonly ReferenceEntry[] } | null>(null);

  // Fetch references when active object changes
  useEffect(() => {
    if (!activeObject) {
      setReferences([]);
      return;
    }
    const filterType = filter === 'all' ? undefined : filter;
    adapters.reference.getReferences(activeObject.id, filterType).then((result) => {
      setReferences(result.data);
    });
  }, [activeObject?.id, filter]);

  // Listen for compare requests
  useEffect(() => {
    const unsub = eventBus.on('compare.requested', (payload) => {
      if (payload.objectIdA && payload.objectIdB) {
        adapters.reference.getCompareReferences(payload.objectIdA, payload.objectIdB).then((result) => {
          setCompareRefs(result.data);
        });
      }
    });
    return unsub;
  }, []);

  const filters: { key: RefFilter; label: string }[] = [
    { key: 'all', label: 'All' },
    { key: 'spec', label: 'Specs' },
    { key: 'code', label: 'Code' },
    { key: 'citation', label: 'Citations' },
    { key: 'document', label: 'Docs' },
  ];

  const basisColor: Record<string, string> = {
    canonical: tokens.color.canonical,
    derived: tokens.color.derived,
    draft: tokens.color.draft,
    compare: tokens.color.compare,
    mock: tokens.color.mock,
  };

  return (
    <PanelShell panelId="reference" title="Reference" isMock={adapters.reference.isMock}>
      {/* Filter Bar */}
      <div style={{ display: 'flex', gap: tokens.space.sm, marginBottom: tokens.space.md, flexWrap: 'wrap' }}>
        {filters.map((f) => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            style={{
              padding: `${tokens.space.sm} ${tokens.space.sm}`,
              background: filter === f.key ? tokens.color.bgActive : tokens.color.bgElevated,
              color: filter === f.key ? tokens.color.fgPrimary : tokens.color.fgMuted,
              border: `1px solid ${filter === f.key ? tokens.color.borderActive : tokens.color.border}`,
              borderRadius: tokens.radius.sm,
              cursor: 'pointer',
              fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.family,
              lineHeight: tokens.font.lineTight,
            }}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* References */}
      {!activeObject ? (
        <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, paddingTop: tokens.space.lg }}>
          <div style={{ textAlign: 'center', marginBottom: tokens.space.lg }}>
            Select an object to view its references
          </div>
          <div style={{
            padding: tokens.space.md,
            background: tokens.color.bgBase,
            borderRadius: tokens.radius.sm,
            border: `1px solid ${tokens.color.borderSubtle}`,
          }}>
            <div style={{
              fontSize: tokens.font.sizeXs,
              fontWeight: tokens.font.weightSemibold,
              color: tokens.color.fgSecondary,
              marginBottom: tokens.space.sm,
              letterSpacing: '0.03em',
            }}>
              REFERENCE SOURCES
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: tokens.space.sm, fontSize: tokens.font.sizeXs, lineHeight: tokens.font.lineNormal }}>
              <ReferenceSourceHint icon={'\u25C7'} label="Specs" description="Industry standards, code references, and project specifications (AISC, ACI, ASTM)" color={tokens.color.canonical} />
              <ReferenceSourceHint icon={'\u25A1'} label="Code" description="Design code sections, compliance requirements, and regulatory references" color={tokens.color.accentPrimary} />
              <ReferenceSourceHint icon={'\u25A0'} label="Docs" description="Project drawings, assembly drawings, shop drawing references, and reports" color={tokens.color.derived} />
              <ReferenceSourceHint icon={'\u25B2'} label="Citations" description="Calculation reports, verification notes, and provenance documentation" color={tokens.color.warning} />
            </div>
          </div>
        </div>
      ) : references.length === 0 ? (
        <div style={{
          color: tokens.color.fgMuted,
          fontSize: tokens.font.sizeSm,
          padding: tokens.space.md,
          background: tokens.color.bgBase,
          borderRadius: tokens.radius.sm,
          border: `1px dashed ${tokens.color.border}`,
          lineHeight: tokens.font.lineNormal,
        }}>
          <div style={{ marginBottom: tokens.space.sm }}>No references found for {activeObject.name}.</div>
          <div style={{ fontSize: tokens.font.sizeXs }}>
            This object has no linked specs, code references, documents, or citations.
            References are populated by source adapters when real data is connected.
          </div>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: tokens.space.sm }}>
          {references.map((ref) => (
            <div
              key={ref.id}
              style={{
                padding: tokens.space.sm,
                background: tokens.color.bgBase,
                borderRadius: tokens.radius.sm,
                borderLeft: `3px solid ${basisColor[ref.sourceBasis] ?? tokens.color.fgMuted}`,
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: tokens.space.sm }}>
                <span style={{ fontSize: tokens.font.sizeSm, fontWeight: tokens.font.weightSemibold, color: tokens.color.fgPrimary }}>
                  {ref.title}
                </span>
                <span style={{
                  fontSize: tokens.font.sizeXs,
                  color: basisColor[ref.sourceBasis] ?? tokens.color.fgMuted,
                  background: `${basisColor[ref.sourceBasis] ?? tokens.color.fgMuted}15`,
                  padding: '1px 4px',
                  borderRadius: tokens.radius.sm,
                  flexShrink: 0,
                }}>
                  {ref.sourceBasis}
                </span>
              </div>
              <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgSecondary, marginBottom: tokens.space.sm, lineHeight: tokens.font.lineNormal }}>
                {ref.content}
              </div>
              <div style={{ display: 'flex', gap: tokens.space.sm, fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                <span>{ref.type}</span>
                {ref.sourceDocument && <span>Source: {ref.sourceDocument}</span>}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Compare View */}
      {compareRefs && workspaceMode === 'compare' && (
        <div style={{ marginTop: tokens.space.lg, borderTop: `1px solid ${tokens.color.border}`, paddingTop: tokens.space.md }}>
          <div style={{ fontSize: tokens.font.sizeSm, fontWeight: tokens.font.weightSemibold, color: tokens.color.compare, marginBottom: tokens.space.sm }}>
            Compare View
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: tokens.space.sm }}>
            <div>
              <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, marginBottom: tokens.space.sm }}>Object A</div>
              {compareRefs.a.map((r) => (
                <div key={r.id} style={{ fontSize: tokens.font.sizeXs, padding: tokens.space.sm, background: tokens.color.bgBase, borderRadius: tokens.radius.sm, marginBottom: '2px', lineHeight: tokens.font.lineNormal }}>
                  {r.title}
                </div>
              ))}
            </div>
            <div>
              <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, marginBottom: tokens.space.sm }}>Object B</div>
              {compareRefs.b.map((r) => (
                <div key={r.id} style={{ fontSize: tokens.font.sizeXs, padding: tokens.space.sm, background: tokens.color.bgBase, borderRadius: tokens.radius.sm, marginBottom: '2px', lineHeight: tokens.font.lineNormal }}>
                  {r.title}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </PanelShell>
  );
}

// ─── Reference Source Hint ─────────────────────────────────────────────────

function ReferenceSourceHint({ icon, label, description, color }: { icon: string; label: string; description: string; color: string }) {
  return (
    <div style={{ display: 'flex', alignItems: 'flex-start', gap: tokens.space.sm }}>
      <span style={{ color, fontSize: tokens.font.sizeXs, flexShrink: 0, marginTop: '2px' }}>{icon}</span>
      <div>
        <span style={{ fontWeight: tokens.font.weightSemibold, color: tokens.color.fgSecondary }}>{label}</span>
        <span style={{ color: tokens.color.fgMuted }}> — {description}</span>
      </div>
    </div>
  );
}
