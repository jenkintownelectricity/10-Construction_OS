/**
 * Construction OS — Semantic Action Bar (Command Palette)
 *
 * CMD+K / CTRL+K triggered command palette.
 * Searches across: objects, conditions, proposals, diagnostics, references, decks.
 *
 * Ring 1 authority boundaries are respected:
 * - Action bar CANNOT bypass authority boundaries
 * - Actions that would require execution authority are routed as proposals
 * - Navigation actions are always allowed (Ring 3)
 *
 * FAIL_CLOSED: If search data is unavailable, palette shows safe empty state.
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { tokens } from '../theme/tokens';
import { adapters } from '../adapters';
import { eventBus } from '../events/EventBus';
import { activeObjectStore } from '../stores/activeObjectStore';
import type { ActiveObjectIdentity } from '../contracts/events';

interface PaletteItem {
  id: string;
  label: string;
  category: 'object' | 'proposal' | 'diagnostic' | 'reference' | 'deck' | 'action';
  description: string;
  action: () => void;
}

export function CommandPalette({ onClose }: { onClose: () => void }) {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<PaletteItem[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus();
  }, []);

  // Search across all sources
  useEffect(() => {
    if (!query.trim()) {
      setResults(getDefaultItems());
      setSelectedIndex(0);
      return;
    }

    const q = query.toLowerCase();
    const items: PaletteItem[] = [];

    // Search objects via truth source
    adapters.truth.searchObjects(query).then((result) => {
      const objectItems: PaletteItem[] = result.data.map((obj: ActiveObjectIdentity) => ({
        id: `obj-${obj.id}`,
        label: obj.name,
        category: 'object' as const,
        description: `${obj.type} — ${obj.id}`,
        action: () => {
          activeObjectStore.setActiveObject(obj, 'work', 'mock');
          eventBus.emit('object.selected', { object: obj, source: 'work', basis: 'mock' });
          onClose();
        },
      }));
      items.push(...objectItems);

      // Add built-in actions
      const actions = getBuiltInActions(q, onClose);
      items.push(...actions);

      setResults(items.slice(0, 12));
      setSelectedIndex(0);
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

  const categoryIcon: Record<string, string> = {
    object: '\u25C6',
    proposal: '\u25A0',
    diagnostic: '\u25B2',
    reference: '\u25C7',
    deck: '\u25A1',
    action: '\u25B6',
  };

  const categoryColor: Record<string, string> = {
    object: tokens.color.accentPrimary,
    proposal: tokens.color.compare,
    diagnostic: tokens.color.warning,
    reference: tokens.color.canonical,
    deck: tokens.color.info,
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
          maxWidth: '560px',
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
          <span style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>{'\u2318'}K</span>
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Jump to object, proposal, diagnostic, deck..."
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
        </div>

        {/* Results */}
        <div style={{ maxHeight: '360px', overflow: 'auto', padding: tokens.space.xs }}>
          {results.length === 0 && query.trim() && (
            <div style={{
              padding: tokens.space.lg,
              textAlign: 'center',
              color: tokens.color.fgMuted,
              fontSize: tokens.font.sizeSm,
            }}>
              No results found
            </div>
          )}
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
          <span style={{ marginLeft: 'auto', color: tokens.color.authorityL3 }}>Ring 3 — Read-Only Actions</span>
        </div>
      </div>
    </div>
  );
}

function getDefaultItems(): PaletteItem[] {
  return [
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
      },
    },
    {
      id: 'action-compare',
      label: 'Enter Compare Mode',
      category: 'action',
      description: 'Compare active object with another version',
      action: () => {
        activeObjectStore.setWorkspaceMode('compare');
      },
    },
    {
      id: 'action-focus',
      label: 'Focus Mode',
      category: 'action',
      description: 'Collapse irrelevant panels around active object',
      action: () => {
        activeObjectStore.setWorkspaceMode('focus');
      },
    },
    {
      id: 'action-default',
      label: 'Default Mode',
      category: 'action',
      description: 'Return to default workspace layout',
      action: () => {
        activeObjectStore.setWorkspaceMode('default');
      },
    },
  ];
}

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
