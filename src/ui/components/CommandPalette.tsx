/**
 * Construction OS — Semantic Action Bar (Command Palette)
 *
 * CMD+K / CTRL+K triggered command palette.
 * Searches across all cockpit domains:
 *   - objects (via truth source adapter)
 *   - zones (via truth source adapter, zone nodes)
 *   - conditions (via awareness adapter)
 *   - proposals (via proposal adapter)
 *   - diagnostics (via runtime diagnostics adapter)
 *   - references (via reference adapter)
 *   - decks (via deck store)
 *
 * Ring 1 authority boundaries are respected:
 * - Action bar CANNOT bypass authority boundaries
 * - Actions that would require execution authority are routed as proposals
 * - Navigation/focus/filter actions are always allowed (Ring 3)
 *
 * FAIL_CLOSED: If any search domain is unavailable, palette shows results
 * from available domains and degrades gracefully. Empty state suggests
 * valid queries so the operator knows what's possible.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { tokens } from '../theme/tokens';
import { adapters, cockpitAdapters } from '../adapters';
import { eventBus } from '../events/EventBus';
import { activeObjectStore } from '../stores/activeObjectStore';
import { deckStore } from '../decks/DeckStore';
import type { ActiveObjectIdentity } from '../contracts/events';

type PaletteCategory = 'object' | 'zone' | 'condition' | 'proposal' | 'diagnostic' | 'reference' | 'deck' | 'action';

interface PaletteItem {
  id: string;
  label: string;
  category: PaletteCategory;
  description: string;
  action: () => void;
}

export function CommandPalette({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<PaletteItem[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [searching, setSearching] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // Search across all domains
  useEffect(() => {
    if (!query.trim()) {
      setResults(getSuggestedItems(onClose));
      setSelectedIndex(0);
      return;
    }

    const q = query.toLowerCase();
    setSearching(true);

    // Launch all searches in parallel — FAIL_CLOSED per domain
    Promise.allSettled([
      searchObjects(q, onClose),
      searchConditions(q, onClose),
      searchProposals(q, onClose),
      searchDiagnostics(q, onClose),
      searchReferences(q, onClose),
      searchDecks(q, onClose),
    ]).then((settled) => {
      const items: PaletteItem[] = [];
      for (const result of settled) {
        if (result.status === 'fulfilled') {
          items.push(...result.value);
        }
        // FAIL_CLOSED: rejected domains are silently skipped
      }

      // Add matching built-in actions
      items.push(...getBuiltInActions(q, onClose));

      setResults(items.slice(0, 16));
      setSelectedIndex(0);
      setSearching(false);
    });
  }, [query, onClose]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Escape') {
      e.preventDefault();
      onClose();
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      setSelectedIndex((prev) => Math.min(prev + 1, results.length - 1));
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      setSelectedIndex((prev) => Math.max(prev - 1, 0));
    } else if (e.key === 'Enter') {
      e.preventDefault();
      if (results[selectedIndex]) {
        results[selectedIndex].action();
      }
    }
  }, [results, selectedIndex, onClose]);

  const categoryIcon: Record<PaletteCategory, string> = {
    object: '\u25C6',
    zone: '\u25A0',
    condition: '\u25B2',
    proposal: '\u25A3',
    diagnostic: '\u26A0',
    reference: '\u25C7',
    deck: '\u25A1',
    action: '\u25B6',
  };

  const categoryColor: Record<PaletteCategory, string> = {
    object: tokens.color.accentPrimary,
    zone: tokens.color.info,
    condition: tokens.color.warning,
    proposal: tokens.color.compare,
    diagnostic: tokens.color.error,
    reference: tokens.color.canonical,
    deck: tokens.color.derived,
    action: tokens.color.fgSecondary,
  };

  return (
    <div
      style={{
        position: 'fixed',
        inset: 0,
        zIndex: 9999,
        display: 'flex',
        alignItems: 'flex-start',
        justifyContent: 'center',
        paddingTop: '15vh',
        background: 'rgba(0,0,0,0.6)',
        backdropFilter: 'blur(4px)',
      }}
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
    >
      <div
        style={{
          width: '100%',
          maxWidth: '600px',
          background: tokens.color.bgSurface,
          borderRadius: tokens.radius.lg,
          border: `1px solid ${tokens.color.border}`,
          boxShadow: tokens.shadow.elevated,
          overflow: 'hidden',
        }}
      >
        {/* Search Input */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: tokens.space.sm,
            padding: `${tokens.space.md} ${tokens.space.lg}`,
            borderBottom: `1px solid ${tokens.color.border}`,
          }}
        >
          <span style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, flexShrink: 0 }}>{'\u2318'}K</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Search objects, conditions, proposals, diagnostics, references, decks..."
            style={{
              flex: 1,
              background: 'transparent',
              border: 'none',
              outline: 'none',
              color: tokens.color.fgPrimary,
              fontSize: tokens.font.sizeSm,
              fontFamily: tokens.font.family,
            }}
          />
          {searching && (
            <span style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeXs, flexShrink: 0 }}>
              searching...
            </span>
          )}
        </div>

        {/* Results */}
        <div style={{ maxHeight: '400px', overflow: 'auto', padding: tokens.space.xs }}>
          {/* No results + query entered → helpful empty state */}
          {results.length === 0 && query.trim() && !searching && (
            <div style={{
              padding: tokens.space.lg,
              color: tokens.color.fgMuted,
              fontSize: tokens.font.sizeSm,
              lineHeight: tokens.font.lineNormal,
            }}>
              <div style={{ marginBottom: tokens.space.md, textAlign: 'center' }}>
                No results for "{query}"
              </div>
              <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                <div style={{ fontWeight: tokens.font.weightMedium, marginBottom: tokens.space.sm }}>Try searching for:</div>
                <div style={{ display: 'flex', flexDirection: 'column', gap: tokens.space.xs }}>
                  <QuerySuggestion text="AHU-01" hint="Jump to a specific object by name or ID" />
                  <QuerySuggestion text="parapet" hint="Find conditions by signature or type" />
                  <QuerySuggestion text="drain" hint="Search proposals related to drainage" />
                  <QuerySuggestion text="validation" hint="Find diagnostics and validation failures" />
                  <QuerySuggestion text="curtain wall" hint="Find references and specifications" />
                  <QuerySuggestion text="proposal review" hint="Switch to a Command Deck" />
                </div>
              </div>
            </div>
          )}

          {/* Result items */}
          {results.map((item, index) => (
            <div
              key={item.id}
              onClick={() => item.action()}
              onMouseEnter={() => setSelectedIndex(index)}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: tokens.space.sm,
                padding: `${tokens.space.sm} ${tokens.space.md}`,
                borderRadius: tokens.radius.sm,
                cursor: 'pointer',
                background: index === selectedIndex ? tokens.color.bgActive : 'transparent',
                transition: `background ${tokens.transition.fast}`,
              }}
            >
              <span style={{
                color: categoryColor[item.category] ?? tokens.color.fgMuted,
                fontSize: tokens.font.sizeXs,
                width: '16px',
                textAlign: 'center',
                flexShrink: 0,
              }}>
                {categoryIcon[item.category] ?? '\u25CB'}
              </span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{
                  fontSize: tokens.font.sizeSm,
                  color: tokens.color.fgPrimary,
                  fontWeight: index === selectedIndex ? tokens.font.weightMedium : tokens.font.weightNormal,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                  lineHeight: tokens.font.lineNormal,
                }}>
                  {item.label}
                </div>
                <div style={{
                  fontSize: tokens.font.sizeXs,
                  color: tokens.color.fgMuted,
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  whiteSpace: 'nowrap',
                }}>
                  {item.description}
                </div>
              </div>
              <span style={{
                fontSize: tokens.font.sizeXs,
                color: categoryColor[item.category] ?? tokens.color.fgMuted,
                background: `${categoryColor[item.category] ?? tokens.color.fgMuted}15`,
                padding: '1px 6px',
                borderRadius: tokens.radius.sm,
                textTransform: 'uppercase',
                flexShrink: 0,
              }}>
                {item.category}
              </span>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div style={{
          display: 'flex',
          gap: tokens.space.md,
          padding: `${tokens.space.sm} ${tokens.space.lg}`,
          borderTop: `1px solid ${tokens.color.border}`,
          fontSize: tokens.font.sizeXs,
          color: tokens.color.fgMuted,
        }}>
          <span>{'\u2191\u2193'} Navigate</span>
          <span>{'\u23CE'} Select</span>
          <span>Esc Close</span>
          <span style={{ marginLeft: 'auto', color: tokens.color.authorityL3 }}>Ring 3 — Navigate / Focus / Filter only</span>
        </div>
      </div>
    </div>
  );
}

// ─── Query Suggestion ──────────────────────────────────────────────────────

function QuerySuggestion({ text, hint }: { text: string; hint: string }) {
  return (
    <div style={{ display: 'flex', gap: tokens.space.sm, alignItems: 'baseline' }}>
      <code style={{
        fontFamily: tokens.font.familyMono,
        color: tokens.color.accentPrimary,
        background: tokens.color.bgBase,
        padding: '1px 4px',
        borderRadius: tokens.radius.sm,
        fontSize: tokens.font.sizeXs,
      }}>
        {text}
      </code>
      <span style={{ color: tokens.color.fgMuted }}>{hint}</span>
    </div>
  );
}

// ─── Domain Search Functions ───────────────────────────────────────────────
// Each returns PaletteItem[] and fails independently.

async function searchObjects(q: string, onClose: () => void): Promise<PaletteItem[]> {
  const result = await adapters.truth.searchObjects(q);
  return result.data.map((obj: ActiveObjectIdentity) => ({
    id: `obj-${obj.id}`,
    label: obj.name,
    category: (obj.type === 'zone' ? 'zone' : 'object') as PaletteCategory,
    description: `${obj.type} — ${obj.id}`,
    action: () => {
      activeObjectStore.setActiveObject(obj, 'work', 'mock');
      eventBus.emit('object.selected', { object: obj, source: 'work', basis: 'mock' });
      onClose();
    },
  }));
}

async function searchConditions(q: string, onClose: () => void): Promise<PaletteItem[]> {
  const state = await cockpitAdapters.awareness.getAwarenessState();
  return state.active_conditions
    .filter((c) =>
      c.condition_signature_id.toLowerCase().includes(q) ||
      c.node_type.toLowerCase().includes(q) ||
      c.pipeline_stage.toLowerCase().includes(q)
    )
    .map((c) => ({
      id: `cond-${c.condition_signature_id}`,
      label: c.condition_signature_id,
      category: 'condition' as PaletteCategory,
      description: `${c.node_type} — stage: ${c.pipeline_stage}`,
      action: () => {
        // Navigate to awareness panel — focus the condition context
        // No direct execution; this is a navigation action
        onClose();
      },
    }));
}

async function searchProposals(q: string, onClose: () => void): Promise<PaletteItem[]> {
  const proposals = await cockpitAdapters.proposal.getProposals();
  return proposals
    .filter((p) =>
      p.proposal_id.toLowerCase().includes(q) ||
      p.reasoning_summary.toLowerCase().includes(q) ||
      p.proposal_type.toLowerCase().includes(q) ||
      p.source.toLowerCase().includes(q)
    )
    .map((p) => ({
      id: `prop-${p.proposal_id}`,
      label: `${p.proposal_type} — ${p.status}`,
      category: 'proposal' as PaletteCategory,
      description: p.reasoning_summary.slice(0, 80) + (p.reasoning_summary.length > 80 ? '...' : ''),
      action: () => {
        // Navigate to proposal mailbox — focus this proposal
        // No direct execution; Ring 3 read-only navigation
        onClose();
      },
    }));
}

async function searchDiagnostics(q: string, onClose: () => void): Promise<PaletteItem[]> {
  const state = await cockpitAdapters.runtimeDiagnostics.getDiagnosticsState();
  return state.events
    .filter((e) =>
      e.event_type.toLowerCase().includes(q) ||
      e.pipeline_stage.toLowerCase().includes(q) ||
      extractEventMessage(e).toLowerCase().includes(q)
    )
    .map((e) => ({
      id: `diag-${e.event_id}`,
      label: `${e.event_type} — ${e.pipeline_stage}`,
      category: 'diagnostic' as PaletteCategory,
      description: extractEventMessage(e),
      action: () => {
        // Navigate to diagnostics panel — focus this event's stage
        // If event payload has an object_id, focus that object
        const payload = e.payload;
        if (payload.type === 'ValidationFailed' && 'object_id' in payload) {
          const objectId = (payload as { object_id: string }).object_id;
          if (objectId) {
            eventBus.emit('object.selected', {
              object: { id: objectId, name: objectId, type: 'element' },
              source: 'diagnostics',
              basis: 'mock',
            });
          }
        }
        onClose();
      },
    }));
}

async function searchReferences(q: string, onClose: () => void): Promise<PaletteItem[]> {
  // Search references for the currently active object
  const currentObject = activeObjectStore.getState().activeObject;
  if (!currentObject) return [];

  const result = await adapters.reference.getReferences(currentObject.id);
  return result.data
    .filter((r) =>
      r.title.toLowerCase().includes(q) ||
      r.content.toLowerCase().includes(q) ||
      r.type.toLowerCase().includes(q) ||
      (r.sourceDocument?.toLowerCase().includes(q) ?? false)
    )
    .map((r) => ({
      id: `ref-${r.id}`,
      label: r.title,
      category: 'reference' as PaletteCategory,
      description: `${r.type} — ${r.sourceBasis}${r.sourceDocument ? ` — ${r.sourceDocument}` : ''}`,
      action: () => {
        // Navigate to reference panel with focus on this reference
        onClose();
      },
    }));
}

function searchDecks(q: string, onClose: () => void): Promise<PaletteItem[]> {
  const allDecks = deckStore.getAll();
  const items = allDecks
    .filter((d) =>
      d.deck_name.toLowerCase().includes(q) ||
      d.deck_id.toLowerCase().includes(q)
    )
    .map((d) => ({
      id: `deck-${d.deck_id}`,
      label: d.deck_name,
      category: 'deck' as PaletteCategory,
      description: `${d.is_system_deck ? 'System' : 'User'} deck — ${d.layout_state.arrangement}`,
      action: () => {
        // Deck activation is a navigation/layout action (Ring 3 allowed)
        onClose();
      },
    }));
  return Promise.resolve(items);
}

// ─── Helper: extract message from diagnostic event ─────────────────────────

function extractEventMessage(event: import('../contracts/cockpit-types').RuntimeDiagnosticEvent): string {
  const p = event.payload;
  switch (p.type) {
    case 'ConditionDetected':
      return `${p.condition_signature_id} (${p.node_type})`;
    case 'DetailResolved':
      return `${p.condition_signature_id} → ${p.resolved_detail_id}`;
    case 'ArtifactRendered':
      return `${p.artifact_id} (${p.artifact_type})`;
    case 'ValidationFailed':
      return `${p.error_code}: ${p.failure_reason}`;
    case 'RuntimeError':
      return `${p.exception_type}: ${p.failure_reason}`;
  }
}

// ─── Suggested Items (empty query) ─────────────────────────────────────────
// Shows suggested starting points when palette opens without a query.

function getSuggestedItems(onClose: () => void): PaletteItem[] {
  return [
    {
      id: 'suggest-jump-ahu',
      label: 'Jump to AHU-01',
      category: 'object',
      description: 'Navigate to AHU Unit AH-01 in the project',
      action: () => {
        activeObjectStore.setActiveObject(
          { id: 'elem-003', name: 'AHU Unit AH-01', type: 'element' },
          'work', 'mock'
        );
        eventBus.emit('object.selected', {
          object: { id: 'elem-003', name: 'AHU Unit AH-01', type: 'element' },
          source: 'work', basis: 'mock',
        });
        onClose();
      },
    },
    {
      id: 'suggest-cw1',
      label: 'Open CW-1 detail',
      category: 'object',
      description: 'Navigate to Curtain Wall Panel CW-1',
      action: () => {
        activeObjectStore.setActiveObject(
          { id: 'asm-003', name: 'Curtain Wall Panel CW-1', type: 'assembly' },
          'work', 'mock'
        );
        eventBus.emit('object.selected', {
          object: { id: 'asm-003', name: 'Curtain Wall Panel CW-1', type: 'assembly' },
          source: 'work', basis: 'mock',
        });
        onClose();
      },
    },
    {
      id: 'suggest-zone-b',
      label: 'Open Zone B references',
      category: 'zone',
      description: 'Navigate to Zone B — East Wing',
      action: () => {
        eventBus.emit('zone.selected', {
          zoneId: 'zone-002',
          zoneName: 'Zone B — East Wing',
          source: 'work',
        });
        onClose();
      },
    },
    {
      id: 'suggest-inspect-fail',
      label: 'Inspect failed validation',
      category: 'diagnostic',
      description: 'View validation failures in diagnostics',
      action: () => { onClose(); },
    },
    {
      id: 'suggest-proposal-deck',
      label: 'Switch to Proposal Review deck',
      category: 'deck',
      description: 'Activate the Proposal Review Command Deck',
      action: () => { onClose(); },
    },
    {
      id: 'action-validate',
      label: 'Run Validation',
      category: 'action',
      description: 'Request full validation on active object',
      action: () => {
        const state = activeObjectStore.getState();
        if (state.activeObject) {
          eventBus.emit('validation.requested', {
            objectId: state.activeObject.id,
            validationType: 'full',
            source: 'work',
          });
        }
        onClose();
      },
    },
    {
      id: 'action-compare',
      label: 'Enter Compare Mode',
      category: 'action',
      description: 'Compare active object with another version',
      action: () => {
        activeObjectStore.setWorkspaceMode('compare');
        onClose();
      },
    },
    {
      id: 'action-focus',
      label: 'Focus Mode',
      category: 'action',
      description: 'Collapse irrelevant panels around active object',
      action: () => {
        activeObjectStore.setWorkspaceMode('focus');
        onClose();
      },
    },
  ];
}

// ─── Built-in Actions (filtered by query) ─────────────────────────────────

function getBuiltInActions(query: string, onClose: () => void): PaletteItem[] {
  const all: PaletteItem[] = [
    {
      id: 'action-validate',
      label: 'Run Validation',
      category: 'action',
      description: 'Request full validation on active object',
      action: () => {
        const state = activeObjectStore.getState();
        if (state.activeObject) {
          eventBus.emit('validation.requested', {
            objectId: state.activeObject.id,
            validationType: 'full',
            source: 'work',
          });
        }
        onClose();
      },
    },
    {
      id: 'action-compare',
      label: 'Enter Compare Mode',
      category: 'action',
      description: 'Compare active object with another version',
      action: () => {
        activeObjectStore.setWorkspaceMode('compare');
        onClose();
      },
    },
    {
      id: 'action-focus',
      label: 'Focus Mode',
      category: 'action',
      description: 'Collapse irrelevant panels around active object',
      action: () => {
        activeObjectStore.setWorkspaceMode('focus');
        onClose();
      },
    },
    {
      id: 'action-review',
      label: 'Review Mode',
      category: 'action',
      description: 'Enter review mode for proposals and diagnostics',
      action: () => {
        activeObjectStore.setWorkspaceMode('review');
        onClose();
      },
    },
    {
      id: 'action-default',
      label: 'Default Mode',
      category: 'action',
      description: 'Return to default workspace layout',
      action: () => {
        activeObjectStore.setWorkspaceMode('default');
        onClose();
      },
    },
    {
      id: 'action-overlay',
      label: 'Open Contextual Overlay',
      category: 'action',
      description: 'Split-view comparison in Work panel',
      action: () => {
        activeObjectStore.setOverlayActive(true);
        onClose();
      },
    },
  ];

  return all.filter((a) =>
    a.label.toLowerCase().includes(query) || a.description.toLowerCase().includes(query)
  );
}
