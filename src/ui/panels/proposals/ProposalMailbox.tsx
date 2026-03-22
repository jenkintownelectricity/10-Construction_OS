/**
 * Construction OS — Proposal Mailbox
 *
 * Displays proposals from the Cognitive Bus event stream with
 * approve / reject / elaborate workflow actions.
 *
 * RING AUTHORITY:
 * - Approve action routes ONLY to a Ring 1 pathway (event emission).
 *   Ring 3 (UI) does NOT execute the approval.
 * - Reject action routes ONLY to a Ring 1 pathway (event emission).
 *   Ring 3 (UI) does NOT execute the rejection.
 * - Elaborate action requests additional reasoning from the assistant.
 *   It does NOT execute any changes directly.
 *
 * Proposal items include: source, proposal_type, reasoning_summary,
 * timestamp, and status.
 *
 * Assistant-generated proposals arriving via event bus are rendered here.
 *
 * FAIL_CLOSED: If proposal data is invalid, an error state is displayed.
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { tokens } from '../../theme/tokens';
import { eventBus } from '../../events/EventBus';
import { mockProposalAdapter } from '../../adapters/proposalAdapter';
import type { ProposalItem, ProposalStatus } from '../../contracts/cockpit-types';

type MailboxFilter = 'all' | 'pending' | 'approved' | 'rejected';

export function ProposalMailbox() {
  const [proposals, setProposals] = useState<ProposalItem[]>([]);
  const [filter, setFilter] = useState<MailboxFilter>('all');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionInFlight, setActionInFlight] = useState<string | null>(null);

  const loadProposals = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const items = await mockProposalAdapter.getProposals();
      setProposals([...items]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'FAIL_CLOSED: Unable to load proposals');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadProposals();
  }, [loadProposals]);

  // Listen for assistant-generated proposals routed into mailbox
  useEffect(() => {
    const unsub = eventBus.on('proposal.created', (payload) => {
      const newProposal: ProposalItem = {
        proposal_id: payload.proposalId,
        source: payload.source,
        proposal_type: 'assistant_proposal',
        reasoning_summary: payload.description,
        timestamp: new Date().toISOString(),
        status: 'pending',
        payload: { title: payload.title, objectId: payload.objectId },
        origin: 'assistant',
      };
      setProposals((prev) => [newProposal, ...prev]);
    });
    return unsub;
  }, []);

  const handleAction = useCallback(async (proposalId: string, action: 'approve' | 'reject' | 'elaborate') => {
    setActionInFlight(proposalId);
    try {
      const result = await mockProposalAdapter.submitAction({
        proposal_id: proposalId,
        action,
        timestamp: Date.now(),
      });
      if (result.success) {
        setProposals((prev) =>
          prev.map((p) =>
            p.proposal_id === proposalId ? { ...p, status: result.new_status } : p
          )
        );
      } else {
        setError(result.error ?? 'FAIL_CLOSED: Action failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'FAIL_CLOSED: Action failed');
    } finally {
      setActionInFlight(null);
    }
  }, []);

  const filtered = proposals.filter((p) => filter === 'all' || p.status === filter);
  const pendingCount = proposals.filter((p) => p.status === 'pending').length;

  const filters: { key: MailboxFilter; label: string }[] = [
    { key: 'all', label: `All (${proposals.length})` },
    { key: 'pending', label: `Pending (${pendingCount})` },
    { key: 'approved', label: 'Approved' },
    { key: 'rejected', label: 'Rejected' },
  ];

  return (
    <PanelShell panelId="proposals" title="Proposal Mailbox" isMock={mockProposalAdapter.isMock}>
      {/* Error */}
      {error && (
        <div style={{
          padding: tokens.space.sm,
          marginBottom: tokens.space.sm,
          background: 'rgba(239,68,68,0.1)',
          borderLeft: `3px solid ${tokens.color.error}`,
          borderRadius: tokens.radius.sm,
          fontSize: tokens.font.sizeXs,
          color: tokens.color.error,
        }}>
          {error}
        </div>
      )}

      {/* Filter Bar */}
      <div style={{
        display: 'flex',
        gap: '1px',
        marginBottom: tokens.space.md,
        background: tokens.color.border,
        borderRadius: tokens.radius.sm,
        overflow: 'hidden',
      }}>
        {filters.map((f) => (
          <button
            key={f.key}
            onClick={() => setFilter(f.key)}
            style={{
              flex: 1,
              padding: `${tokens.space.sm} ${tokens.space.sm}`,
              background: filter === f.key ? tokens.color.bgActive : tokens.color.bgElevated,
              color: filter === f.key ? tokens.color.fgPrimary : tokens.color.fgSecondary,
              border: 'none',
              cursor: 'pointer',
              fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.family,
              fontWeight: filter === f.key ? tokens.font.weightSemibold : tokens.font.weightNormal,
              lineHeight: tokens.font.lineTight,
            }}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Loading */}
      {loading && (
        <div style={{ padding: tokens.space.lg, textAlign: 'center', color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
          Loading proposals...
        </div>
      )}

      {/* Proposal List */}
      {!loading && filtered.length === 0 && (
        <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
          No proposals match the current filter.
        </div>
      )}

      {!loading && filtered.map((proposal) => (
        <ProposalCard
          key={proposal.proposal_id}
          proposal={proposal}
          onAction={handleAction}
          isActionInFlight={actionInFlight === proposal.proposal_id}
        />
      ))}
    </PanelShell>
  );
}

// ─── Proposal Card ─────────────────────────────────────────────────────────

function ProposalCard({
  proposal,
  onAction,
  isActionInFlight,
}: {
  proposal: ProposalItem;
  onAction: (id: string, action: 'approve' | 'reject' | 'elaborate') => void;
  isActionInFlight: boolean;
}) {
  const statusColor: Record<ProposalStatus, string> = {
    pending: tokens.color.warning,
    approved: tokens.color.success,
    rejected: tokens.color.error,
    elaborating: tokens.color.info,
  };

  const originLabel: Record<string, string> = {
    runtime: 'RUNTIME',
    assistant: 'ASSISTANT',
    operator: 'OPERATOR',
    external: 'EXTERNAL',
  };

  return (
    <div style={{
      padding: tokens.space.md,
      marginBottom: tokens.space.sm,
      background: tokens.color.bgBase,
      borderRadius: tokens.radius.sm,
      borderLeft: `3px solid ${statusColor[proposal.status]}`,
      fontSize: tokens.font.sizeXs,
      lineHeight: tokens.font.lineNormal,
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: tokens.space.sm }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <span style={{
            color: statusColor[proposal.status],
            fontWeight: tokens.font.weightSemibold,
            textTransform: 'uppercase',
          }}>
            {proposal.status}
          </span>
          <span style={{
            color: tokens.color.fgMuted,
            background: tokens.color.bgElevated,
            padding: '1px 6px',
            borderRadius: tokens.radius.sm,
          }}>
            {originLabel[proposal.origin] ?? proposal.origin}
          </span>
        </div>
        <span style={{ color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono }}>
          {proposal.proposal_id}
        </span>
      </div>

      {/* Source & Type */}
      <div style={{ color: tokens.color.fgSecondary, marginBottom: tokens.space.sm }}>
        <span style={{ fontWeight: tokens.font.weightMedium }}>Source:</span> {proposal.source}
        <span style={{ marginLeft: tokens.space.md, fontWeight: tokens.font.weightMedium }}>Type:</span> {proposal.proposal_type}
      </div>

      {/* Reasoning Summary */}
      <div style={{
        color: tokens.color.fgPrimary,
        marginBottom: tokens.space.sm,
        lineHeight: '1.5',
        padding: tokens.space.sm,
        background: tokens.color.bgSurface,
        borderRadius: tokens.radius.sm,
      }}>
        {proposal.reasoning_summary}
      </div>

      {/* Timestamp */}
      <div style={{ color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono, marginBottom: tokens.space.sm }}>
        {new Date(proposal.timestamp).toLocaleString()}
      </div>

      {/* Action Buttons — only for pending proposals */}
      {proposal.status === 'pending' && (
        <div style={{ display: 'flex', gap: tokens.space.sm }}>
          <ActionButton
            label="APPROVE"
            color={tokens.color.success}
            onClick={() => onAction(proposal.proposal_id, 'approve')}
            disabled={isActionInFlight}
            title="Route approval to Ring 1 pathway"
          />
          <ActionButton
            label="REJECT"
            color={tokens.color.error}
            onClick={() => onAction(proposal.proposal_id, 'reject')}
            disabled={isActionInFlight}
            title="Route rejection to Ring 1 pathway"
          />
          <ActionButton
            label="ELABORATE"
            color={tokens.color.info}
            onClick={() => onAction(proposal.proposal_id, 'elaborate')}
            disabled={isActionInFlight}
            title="Request additional reasoning — does not execute changes"
          />
        </div>
      )}

      {/* Elaborating indicator */}
      {proposal.status === 'elaborating' && (
        <div style={{
          color: tokens.color.info,
          fontSize: tokens.font.sizeXs,
          fontStyle: 'italic',
        }}>
          Awaiting additional reasoning from assistant...
        </div>
      )}
    </div>
  );
}

// ─── Action Button ─────────────────────────────────────────────────────────

function ActionButton({
  label,
  color,
  onClick,
  disabled,
  title,
}: {
  label: string;
  color: string;
  onClick: () => void;
  disabled: boolean;
  title: string;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      title={title}
      style={{
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: `${color}15`,
        color: disabled ? tokens.color.fgMuted : color,
        border: `1px solid ${disabled ? tokens.color.border : color}`,
        borderRadius: tokens.radius.sm,
        cursor: disabled ? 'not-allowed' : 'pointer',
        fontSize: tokens.font.sizeXs,
        fontFamily: tokens.font.family,
        fontWeight: tokens.font.weightSemibold,
        letterSpacing: '0.05em',
        opacity: disabled ? 0.5 : 1,
      }}
    >
      {label}
    </button>
  );
}
