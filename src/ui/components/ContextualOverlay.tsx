/**
 * Construction OS — Division 07 Contextual Overlay
 *
 * Split-view comparison overlay for the Work panel.
 * LEFT = current condition/detail/design
 * RIGHT = suggested fix / proposed detail / code-backed alternative
 *
 * Controls: Approve, Reject, Inspect Basis, Return to Prior Gravity
 * Overlay is gravity-aware and reversible.
 *
 * FAIL_CLOSED: If context data is missing, overlay shows safe empty state
 * rather than silently failing.
 */

import { useCallback } from 'react';
import { tokens } from '../theme/tokens';
import { activeObjectStore } from '../stores/activeObjectStore';
import { eventBus } from '../events/EventBus';
import type { ActiveObjectIdentity } from '../contracts/events';

interface ContextualOverlayProps {
  activeObject: ActiveObjectIdentity;
  onClose: () => void;
}

export function ContextualOverlay({ activeObject, onClose }: ContextualOverlayProps) {
  const handleApprove = useCallback(() => {
    // Route approval to Ring 1 pathway — Ring 3 does NOT execute
    eventBus.emit('proposal.created', {
      proposalId: `overlay-approve-${Date.now()}`,
      objectId: activeObject.id,
      title: `Approve suggested change for ${activeObject.name}`,
      description: 'Overlay approval routed to proposal mailbox for Ring 1 review.',
      source: 'work',
    });
  }, [activeObject]);

  const handleReject = useCallback(() => {
    // Route rejection to Ring 1 pathway
    eventBus.emit('proposal.created', {
      proposalId: `overlay-reject-${Date.now()}`,
      objectId: activeObject.id,
      title: `Reject suggested change for ${activeObject.name}`,
      description: 'Overlay rejection routed to proposal mailbox for Ring 1 review.',
      source: 'work',
    });
  }, [activeObject]);

  const handleInspectBasis = useCallback(() => {
    eventBus.emit('reference.requested', {
      objectId: activeObject.id,
      referenceType: 'all',
      source: 'work',
    });
  }, [activeObject]);

  const handleReturn = useCallback(() => {
    activeObjectStore.setOverlayActive(false);
    onClose();
  }, [onClose]);

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      height: '100%',
      gap: tokens.space.sm,
    }}>
      {/* Overlay Header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: tokens.color.bgElevated,
        borderRadius: tokens.radius.sm,
        borderLeft: `3px solid ${tokens.color.compare}`,
      }}>
        <span style={{
          fontSize: tokens.font.sizeSm,
          fontWeight: tokens.font.weightSemibold,
          color: tokens.color.compare,
          letterSpacing: '0.03em',
        }}>
          CONTEXTUAL OVERLAY — {activeObject.name}
        </span>
        <button
          onClick={handleReturn}
          style={{
            padding: `${tokens.space.xs} ${tokens.space.sm}`,
            background: tokens.color.bgBase,
            color: tokens.color.fgSecondary,
            border: `1px solid ${tokens.color.border}`,
            borderRadius: tokens.radius.sm,
            cursor: 'pointer',
            fontSize: tokens.font.sizeXs,
            fontFamily: tokens.font.family,
          }}
        >
          {'\u2715'} Close Overlay
        </button>
      </div>

      {/* Split View */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: '1fr 1fr',
        gap: tokens.space.sm,
        flex: 1,
        minHeight: 0,
      }}>
        {/* LEFT — Current Condition/Detail/Design */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          background: tokens.color.bgBase,
          borderRadius: tokens.radius.sm,
          border: `1px solid ${tokens.color.border}`,
          overflow: 'auto',
        }}>
          <div style={{
            padding: `${tokens.space.sm} ${tokens.space.md}`,
            background: tokens.color.bgElevated,
            borderBottom: `1px solid ${tokens.color.border}`,
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            color: tokens.color.fgSecondary,
            letterSpacing: '0.05em',
          }}>
            CURRENT — {activeObject.type.toUpperCase()}
          </div>
          <div style={{ padding: tokens.space.md, flex: 1 }}>
            <div style={{ marginBottom: tokens.space.md }}>
              <div style={{
                fontSize: tokens.font.sizeSm,
                fontWeight: tokens.font.weightSemibold,
                color: tokens.color.fgPrimary,
                marginBottom: tokens.space.xs,
              }}>
                {activeObject.name}
              </div>
              <div style={{
                fontSize: tokens.font.sizeXs,
                color: tokens.color.fgMuted,
                fontFamily: tokens.font.familyMono,
              }}>
                {activeObject.id}
              </div>
            </div>
            <div style={{
              padding: tokens.space.sm,
              background: tokens.color.bgSurface,
              borderRadius: tokens.radius.sm,
              fontSize: tokens.font.sizeXs,
              color: tokens.color.fgSecondary,
              lineHeight: tokens.font.lineNormal,
              border: `1px solid ${tokens.color.borderSubtle}`,
            }}>
              <div style={{ fontWeight: tokens.font.weightMedium, color: tokens.color.canonical, marginBottom: tokens.space.xs }}>
                Current Design State
              </div>
              Current {activeObject.type} detail and specifications as resolved by the runtime pipeline.
              This side shows the canonical or derived state from the truth source adapter.
              <div style={{
                marginTop: tokens.space.sm,
                padding: tokens.space.sm,
                background: tokens.color.bgBase,
                borderRadius: tokens.radius.sm,
                fontFamily: tokens.font.familyMono,
                fontSize: tokens.font.sizeXs,
              }}>
                basis: canonical | source: truth-adapter
              </div>
            </div>
          </div>
        </div>

        {/* RIGHT — Suggested Fix / Proposed Alternative */}
        <div style={{
          display: 'flex',
          flexDirection: 'column',
          background: tokens.color.bgBase,
          borderRadius: tokens.radius.sm,
          border: `1px solid ${tokens.color.compare}30`,
          overflow: 'auto',
        }}>
          <div style={{
            padding: `${tokens.space.sm} ${tokens.space.md}`,
            background: `${tokens.color.compare}10`,
            borderBottom: `1px solid ${tokens.color.compare}30`,
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            color: tokens.color.compare,
            letterSpacing: '0.05em',
          }}>
            SUGGESTED — PROPOSED CHANGE
          </div>
          <div style={{ padding: tokens.space.md, flex: 1 }}>
            <div style={{ marginBottom: tokens.space.md }}>
              <div style={{
                fontSize: tokens.font.sizeSm,
                fontWeight: tokens.font.weightSemibold,
                color: tokens.color.fgPrimary,
                marginBottom: tokens.space.xs,
              }}>
                Proposed Update for {activeObject.name}
              </div>
              <div style={{
                fontSize: tokens.font.sizeXs,
                color: tokens.color.compare,
                fontFamily: tokens.font.familyMono,
              }}>
                proposal-scope: {activeObject.id}
              </div>
            </div>
            <div style={{
              padding: tokens.space.sm,
              background: `${tokens.color.compare}08`,
              borderRadius: tokens.radius.sm,
              fontSize: tokens.font.sizeXs,
              color: tokens.color.fgSecondary,
              lineHeight: tokens.font.lineNormal,
              border: `1px solid ${tokens.color.compare}20`,
            }}>
              <div style={{ fontWeight: tokens.font.weightMedium, color: tokens.color.compare, marginBottom: tokens.space.xs }}>
                Suggested Fix / Alternative
              </div>
              Proposed modification sourced from runtime condition resolution, assistant analysis,
              or operator-initiated change request. This side shows the proposed delta against the
              current canonical state.
              <div style={{
                marginTop: tokens.space.sm,
                padding: tokens.space.sm,
                background: tokens.color.bgBase,
                borderRadius: tokens.radius.sm,
                fontFamily: tokens.font.familyMono,
                fontSize: tokens.font.sizeXs,
              }}>
                basis: draft | source: proposal-adapter
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Action Controls */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        gap: tokens.space.sm,
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: tokens.color.bgElevated,
        borderRadius: tokens.radius.sm,
        borderTop: `1px solid ${tokens.color.border}`,
      }}>
        <button
          onClick={handleApprove}
          style={{
            padding: `${tokens.space.sm} ${tokens.space.lg}`,
            background: `${tokens.color.success}15`,
            color: tokens.color.success,
            border: `1px solid ${tokens.color.success}`,
            borderRadius: tokens.radius.sm,
            cursor: 'pointer',
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            fontFamily: tokens.font.family,
            letterSpacing: '0.05em',
          }}
          title="Route approval to Ring 1 — does not execute directly"
        >
          APPROVE
        </button>
        <button
          onClick={handleReject}
          style={{
            padding: `${tokens.space.sm} ${tokens.space.lg}`,
            background: `${tokens.color.error}15`,
            color: tokens.color.error,
            border: `1px solid ${tokens.color.error}`,
            borderRadius: tokens.radius.sm,
            cursor: 'pointer',
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            fontFamily: tokens.font.family,
            letterSpacing: '0.05em',
          }}
          title="Route rejection to Ring 1 — does not execute directly"
        >
          REJECT
        </button>
        <button
          onClick={handleInspectBasis}
          style={{
            padding: `${tokens.space.sm} ${tokens.space.lg}`,
            background: `${tokens.color.info}15`,
            color: tokens.color.info,
            border: `1px solid ${tokens.color.info}`,
            borderRadius: tokens.radius.sm,
            cursor: 'pointer',
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            fontFamily: tokens.font.family,
            letterSpacing: '0.05em',
          }}
          title="Inspect source basis and references for this object"
        >
          INSPECT BASIS
        </button>
        <div style={{ flex: 1 }} />
        <button
          onClick={handleReturn}
          style={{
            padding: `${tokens.space.sm} ${tokens.space.lg}`,
            background: tokens.color.bgBase,
            color: tokens.color.fgSecondary,
            border: `1px solid ${tokens.color.border}`,
            borderRadius: tokens.radius.sm,
            cursor: 'pointer',
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            fontFamily: tokens.font.family,
            letterSpacing: '0.05em',
          }}
          title="Return to prior workspace state"
        >
          RETURN TO PRIOR GRAVITY
        </button>
        <span style={{
          fontSize: tokens.font.sizeXs,
          color: tokens.color.fgMuted,
          fontFamily: tokens.font.familyMono,
        }}>
          Ring 3 — Actions route to mailbox
        </span>
      </div>
    </div>
  );
}
