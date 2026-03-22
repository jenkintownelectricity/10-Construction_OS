/**
 * Construction OS — Deck Picker
 *
 * UI component for selecting, creating, renaming, and deleting Command Decks.
 * Renders in the workspace status bar as a dropdown deck selector.
 *
 * Deck activation:
 *   - Clears GravityStack
 *   - Applies full cockpit state atomically
 *   - Reports any FAIL_CLOSED fields
 *   - NEVER executes runtime or assistant actions
 */

import { useCallback, useEffect, useRef, useState } from 'react';
import { tokens } from '../theme/tokens';
import { deckStore } from './DeckStore';
import { activateDeck } from './DeckActivation';
import { activeObjectStore } from '../stores/activeObjectStore';
import { useActiveObject } from '../stores/useSyncExternalStore';
import type { DeckState, DeckActivationResult } from '../contracts/deck-types';
import type { PanelId } from '../contracts/events';

interface DeckPickerProps {
  /** Callback to apply layout changes in the workspace shell */
  applyLayout: (visiblePanels: readonly PanelId[], promotedPanel: PanelId) => void;
}

export function DeckPicker({ applyLayout }: DeckPickerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [activeDeckId, setActiveDeckId] = useState<string | null>(null);
  const [decks, setDecks] = useState<readonly DeckState[]>(deckStore.getAll());
  const [activationResult, setActivationResult] = useState<DeckActivationResult | null>(null);
  const [showSaveDialog, setShowSaveDialog] = useState(false);
  const [showRenameDialog, setShowRenameDialog] = useState<string | null>(null);
  const [dialogInput, setDialogInput] = useState('');
  const dropdownRef = useRef<HTMLDivElement>(null);
  const { activeObject, workspaceMode } = useActiveObject();

  // Subscribe to deck store changes
  useEffect(() => {
    const unsub = deckStore.subscribe(() => {
      setDecks(deckStore.getAll());
    });
    return unsub;
  }, []);

  // Close dropdown on outside click
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    }
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);

  // Clear activation result after 5s
  useEffect(() => {
    if (activationResult) {
      const timer = setTimeout(() => setActivationResult(null), 5000);
      return () => clearTimeout(timer);
    }
  }, [activationResult]);

  const handleActivateDeck = useCallback((deck: DeckState) => {
    const result = activateDeck(deck, applyLayout);
    setActiveDeckId(deck.deck_id);
    setActivationResult(result);
    setIsOpen(false);
  }, [applyLayout]);

  const handleSaveDeck = useCallback(() => {
    if (!dialogInput.trim()) return;

    const state = activeObjectStore.getState();
    deckStore.saveDeck({
      deck_name: dialogInput.trim(),
      gravity_context: {
        activeObject: state.activeObject,
        basis: state.basis,
        sourcePanel: state.sourcePanel,
        compareObject: state.compareObject,
        workspaceMode: state.workspaceMode,
      },
      panel_modes: [],
      layout_state: {
        visiblePanels: ['explorer', 'work', 'reference', 'spatial', 'system', 'awareness', 'proposals', 'diagnostics', 'assistant'],
        arrangement: 'custom',
      },
      promoted_panel: 'work',
      filters: [],
    });

    setDialogInput('');
    setShowSaveDialog(false);
  }, [dialogInput]);

  const handleRenameDeck = useCallback(() => {
    if (!showRenameDialog || !dialogInput.trim()) return;
    deckStore.renameDeck(showRenameDialog, dialogInput.trim());
    setDialogInput('');
    setShowRenameDialog(null);
  }, [showRenameDialog, dialogInput]);

  const handleDeleteDeck = useCallback((deckId: string) => {
    deckStore.deleteDeck(deckId);
    if (activeDeckId === deckId) {
      setActiveDeckId(null);
    }
  }, [activeDeckId]);

  const activeDeck = activeDeckId ? deckStore.getDeck(activeDeckId) : null;
  const systemDecks = decks.filter((d) => d.is_system_deck);
  const userDecks = decks.filter((d) => !d.is_system_deck);

  return (
    <div ref={dropdownRef} style={{ position: 'relative', display: 'inline-block' }}>
      {/* Deck Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '4px',
          padding: `2px ${tokens.space.sm}`,
          background: activeDeckId ? tokens.color.accentMuted : tokens.color.bgElevated,
          color: activeDeckId ? tokens.color.accentPrimary : tokens.color.fgSecondary,
          border: `1px solid ${activeDeckId ? tokens.color.accentPrimary : tokens.color.border}`,
          borderRadius: tokens.radius.sm,
          cursor: 'pointer',
          fontSize: tokens.font.sizeXs,
          fontFamily: tokens.font.family,
          fontWeight: tokens.font.weightMedium,
        }}
      >
        <span style={{ fontFamily: tokens.font.familyMono, letterSpacing: '0.05em' }}>
          DECK
        </span>
        <span style={{ color: activeDeck ? tokens.color.fgPrimary : tokens.color.fgMuted, maxWidth: '120px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
          {activeDeck ? activeDeck.deck_name : 'None'}
        </span>
        <span style={{ fontSize: tokens.font.sizeXs, opacity: 0.5 }}>{isOpen ? '\u25B2' : '\u25BC'}</span>
      </button>

      {/* Activation Result Notification */}
      {activationResult && activationResult.unavailable.length > 0 && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: 0,
          marginTop: '4px',
          padding: tokens.space.sm,
          background: tokens.color.bgElevated,
          border: `1px solid ${tokens.color.warning}`,
          borderRadius: tokens.radius.sm,
          fontSize: tokens.font.sizeXs,
          color: tokens.color.warning,
          minWidth: '250px',
          zIndex: 1001,
          boxShadow: tokens.shadow.elevated,
        }}>
          <div style={{ fontWeight: tokens.font.weightSemibold, marginBottom: '4px' }}>
            FAIL_CLOSED: Some deck fields unavailable
          </div>
          {activationResult.unavailable.map((u, i) => (
            <div key={i} style={{ marginTop: '2px', color: u.severity === 'error' ? tokens.color.error : tokens.color.warning }}>
              {u.field}: {u.reason}
            </div>
          ))}
        </div>
      )}

      {/* Dropdown */}
      {isOpen && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: 0,
          marginTop: '4px',
          minWidth: '280px',
          maxHeight: '400px',
          overflow: 'auto',
          background: tokens.color.bgElevated,
          border: `1px solid ${tokens.color.border}`,
          borderRadius: tokens.radius.md,
          boxShadow: tokens.shadow.elevated,
          zIndex: 1000,
        }}>
          {/* System Decks */}
          <div style={{ padding: `${tokens.space.xs} ${tokens.space.sm}`, borderBottom: `1px solid ${tokens.color.border}` }}>
            <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.xs }}>
              SYSTEM DECKS
            </div>
            {systemDecks.map((deck) => (
              <DeckItem
                key={deck.deck_id}
                deck={deck}
                isActive={activeDeckId === deck.deck_id}
                onActivate={() => handleActivateDeck(deck)}
                onRename={undefined}
                onDelete={undefined}
              />
            ))}
          </div>

          {/* User Decks */}
          <div style={{ padding: `${tokens.space.xs} ${tokens.space.sm}`, borderBottom: `1px solid ${tokens.color.border}` }}>
            <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.xs }}>
              USER DECKS
            </div>
            {userDecks.length === 0 ? (
              <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, padding: tokens.space.xs }}>
                No user decks saved yet.
              </div>
            ) : (
              userDecks.map((deck) => (
                <DeckItem
                  key={deck.deck_id}
                  deck={deck}
                  isActive={activeDeckId === deck.deck_id}
                  onActivate={() => handleActivateDeck(deck)}
                  onRename={() => { setShowRenameDialog(deck.deck_id); setDialogInput(deck.deck_name); }}
                  onDelete={() => handleDeleteDeck(deck.deck_id)}
                />
              ))
            )}
          </div>

          {/* Save New Deck */}
          <div style={{ padding: tokens.space.sm }}>
            {showSaveDialog ? (
              <div style={{ display: 'flex', gap: tokens.space.xs }}>
                <input
                  type="text"
                  value={dialogInput}
                  onChange={(e) => setDialogInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleSaveDeck(); if (e.key === 'Escape') { setShowSaveDialog(false); setDialogInput(''); } }}
                  placeholder="Deck name..."
                  autoFocus
                  style={{
                    flex: 1,
                    padding: `${tokens.space.xs} ${tokens.space.sm}`,
                    background: tokens.color.bgBase,
                    color: tokens.color.fgPrimary,
                    border: `1px solid ${tokens.color.border}`,
                    borderRadius: tokens.radius.sm,
                    fontSize: tokens.font.sizeXs,
                    fontFamily: tokens.font.family,
                    outline: 'none',
                  }}
                />
                <button
                  onClick={handleSaveDeck}
                  disabled={!dialogInput.trim()}
                  style={{
                    padding: `${tokens.space.xs} ${tokens.space.sm}`,
                    background: tokens.color.success,
                    color: tokens.color.fgInverse,
                    border: 'none',
                    borderRadius: tokens.radius.sm,
                    cursor: dialogInput.trim() ? 'pointer' : 'not-allowed',
                    fontSize: tokens.font.sizeXs,
                    fontWeight: tokens.font.weightSemibold,
                    opacity: dialogInput.trim() ? 1 : 0.5,
                  }}
                >
                  SAVE
                </button>
              </div>
            ) : (
              <button
                onClick={() => { setShowSaveDialog(true); setDialogInput(''); }}
                style={{
                  width: '100%',
                  padding: `${tokens.space.xs} ${tokens.space.sm}`,
                  background: tokens.color.bgBase,
                  color: tokens.color.fgSecondary,
                  border: `1px dashed ${tokens.color.border}`,
                  borderRadius: tokens.radius.sm,
                  cursor: 'pointer',
                  fontSize: tokens.font.sizeXs,
                  fontFamily: tokens.font.family,
                }}
              >
                + Save Current State as Deck
              </button>
            )}
          </div>
        </div>
      )}

      {/* Rename Dialog (overlays dropdown) */}
      {showRenameDialog && (
        <div style={{
          position: 'absolute',
          top: '100%',
          right: 0,
          marginTop: '4px',
          padding: tokens.space.sm,
          background: tokens.color.bgElevated,
          border: `1px solid ${tokens.color.border}`,
          borderRadius: tokens.radius.md,
          boxShadow: tokens.shadow.elevated,
          zIndex: 1002,
          minWidth: '250px',
        }}>
          <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, fontWeight: tokens.font.weightSemibold, marginBottom: tokens.space.xs }}>
            RENAME DECK
          </div>
          <div style={{ display: 'flex', gap: tokens.space.xs }}>
            <input
              type="text"
              value={dialogInput}
              onChange={(e) => setDialogInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleRenameDeck(); if (e.key === 'Escape') { setShowRenameDialog(null); setDialogInput(''); } }}
              autoFocus
              style={{
                flex: 1,
                padding: `${tokens.space.xs} ${tokens.space.sm}`,
                background: tokens.color.bgBase,
                color: tokens.color.fgPrimary,
                border: `1px solid ${tokens.color.border}`,
                borderRadius: tokens.radius.sm,
                fontSize: tokens.font.sizeXs,
                fontFamily: tokens.font.family,
                outline: 'none',
              }}
            />
            <button
              onClick={handleRenameDeck}
              disabled={!dialogInput.trim()}
              style={{
                padding: `${tokens.space.xs} ${tokens.space.sm}`,
                background: tokens.color.accentPrimary,
                color: tokens.color.fgPrimary,
                border: 'none',
                borderRadius: tokens.radius.sm,
                cursor: dialogInput.trim() ? 'pointer' : 'not-allowed',
                fontSize: tokens.font.sizeXs,
                fontWeight: tokens.font.weightSemibold,
                opacity: dialogInput.trim() ? 1 : 0.5,
              }}
            >
              RENAME
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// ─── Deck Item Row ─────────────────────────────────────────────────────────

function DeckItem({
  deck,
  isActive,
  onActivate,
  onRename,
  onDelete,
}: {
  deck: DeckState;
  isActive: boolean;
  onActivate: () => void;
  onRename?: () => void;
  onDelete?: () => void;
}) {
  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: tokens.space.sm,
        padding: `${tokens.space.xs} ${tokens.space.sm}`,
        marginBottom: '2px',
        background: isActive ? tokens.color.accentMuted : 'transparent',
        borderRadius: tokens.radius.sm,
        cursor: 'pointer',
        fontSize: tokens.font.sizeXs,
      }}
    >
      {/* Activate button (deck name) */}
      <button
        onClick={onActivate}
        style={{
          flex: 1,
          textAlign: 'left',
          background: 'none',
          border: 'none',
          cursor: 'pointer',
          color: isActive ? tokens.color.accentPrimary : tokens.color.fgPrimary,
          fontWeight: isActive ? tokens.font.weightSemibold : tokens.font.weightNormal,
          fontSize: tokens.font.sizeXs,
          fontFamily: tokens.font.family,
          padding: 0,
        }}
      >
        {deck.deck_name}
      </button>

      {/* Arrangement badge */}
      <span style={{
        fontSize: tokens.font.sizeXs,
        color: tokens.color.fgMuted,
        background: tokens.color.bgBase,
        padding: '0 4px',
        borderRadius: tokens.radius.sm,
      }}>
        {deck.layout_state.arrangement}
      </span>

      {/* Actions (user decks only) */}
      {onRename && (
        <button
          onClick={(e) => { e.stopPropagation(); onRename(); }}
          title="Rename"
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            color: tokens.color.fgMuted,
            fontSize: tokens.font.sizeXs,
            padding: '0 2px',
          }}
        >
          REN
        </button>
      )}
      {onDelete && (
        <button
          onClick={(e) => { e.stopPropagation(); onDelete(); }}
          title="Delete"
          style={{
            background: 'none',
            border: 'none',
            cursor: 'pointer',
            color: tokens.color.error,
            fontSize: tokens.font.sizeXs,
            padding: '0 2px',
          }}
        >
          DEL
        </button>
      )}
    </div>
  );
}
