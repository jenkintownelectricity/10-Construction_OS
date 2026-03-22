/**
 * Construction OS — Assistant Console
 *
 * Renders assistant bounded output responses and provides query input.
 *
 * RING AUTHORITY:
 * - Assistant responses CANNOT invoke runtime directly from Ring 3.
 * - Assistant-generated proposals are routed into the Proposal Mailbox
 *   via event bus emission, NOT executed directly.
 * - The query input submits to the assistant adapter, which processes
 *   against the current awareness snapshot. No execution authority.
 *
 * Output types: verified_truth, uncertainty, insufficiency, next_valid_action
 * Each response includes confidence_basis and snapshot_id for provenance.
 *
 * FAIL_CLOSED: If response data is invalid, error state is displayed.
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { tokens } from '../../theme/tokens';
import { eventBus } from '../../events/EventBus';
import { mockAssistantAdapter } from '../../adapters/assistantAdapter';
import type { AssistantResponse, AssistantOutputType } from '../../contracts/cockpit-types';

export function AssistantConsole() {
  const [responses, setResponses] = useState<AssistantResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [query, setQuery] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const loadResponses = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const state = await mockAssistantAdapter.getConsoleState();
      setResponses([...state.responses]);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'FAIL_CLOSED: Unable to load assistant responses');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadResponses();
  }, [loadResponses]);

  const handleSubmitQuery = useCallback(async () => {
    if (!query.trim() || submitting) return;
    setSubmitting(true);
    setError(null);
    try {
      const response = await mockAssistantAdapter.submitQuery(query.trim());
      setResponses((prev) => [response, ...prev]);

      // If the response contains a proposal, route it into the Proposal Mailbox
      // via the event bus. Ring 3 does NOT execute the proposal.
      if (response.has_proposal && response.proposal) {
        eventBus.emit('proposal.created', {
          proposalId: response.proposal.proposal_id,
          objectId: '',
          title: response.proposal.proposal_type,
          description: response.proposal.reasoning_summary,
          source: 'assistant',
        });
      }

      setQuery('');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'FAIL_CLOSED: Query submission failed');
    } finally {
      setSubmitting(false);
    }
  }, [query, submitting]);

  const handleKeyDown = useCallback((e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmitQuery();
    }
  }, [handleSubmitQuery]);

  return (
    <PanelShell panelId="assistant" title="Assistant Console" isMock={mockAssistantAdapter.isMock}>
      {/* Authority Notice */}
      <div style={{
        padding: `${tokens.space.sm} ${tokens.space.sm}`,
        marginBottom: tokens.space.sm,
        background: tokens.color.bgBase,
        borderRadius: tokens.radius.sm,
        fontSize: tokens.font.sizeXs,
        color: tokens.color.fgMuted,
        fontFamily: tokens.font.familyMono,
        textAlign: 'center',
        lineHeight: tokens.font.lineNormal,
      }}>
        RING 3 — READ-ONLY | NO EXECUTION AUTHORITY | PROPOSALS ROUTE TO MAILBOX
      </div>

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

      {/* Query Input */}
      <div style={{
        display: 'flex',
        gap: tokens.space.sm,
        marginBottom: tokens.space.md,
      }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about current awareness state..."
          disabled={submitting}
          style={{
            flex: 1,
            padding: `${tokens.space.sm} ${tokens.space.md}`,
            background: tokens.color.bgBase,
            color: tokens.color.fgPrimary,
            border: `1px solid ${tokens.color.border}`,
            borderRadius: tokens.radius.sm,
            fontSize: tokens.font.sizeSm,
            fontFamily: tokens.font.family,
            outline: 'none',
          }}
        />
        <button
          onClick={handleSubmitQuery}
          disabled={submitting || !query.trim()}
          style={{
            padding: `${tokens.space.sm} ${tokens.space.lg}`,
            background: submitting ? tokens.color.bgElevated : tokens.color.accentPrimary,
            color: submitting ? tokens.color.fgMuted : tokens.color.fgPrimary,
            border: 'none',
            borderRadius: tokens.radius.sm,
            cursor: submitting || !query.trim() ? 'not-allowed' : 'pointer',
            fontSize: tokens.font.sizeXs,
            fontWeight: tokens.font.weightSemibold,
            fontFamily: tokens.font.family,
            opacity: submitting || !query.trim() ? 0.5 : 1,
          }}
        >
          {submitting ? 'THINKING...' : 'ASK'}
        </button>
      </div>

      {/* Loading */}
      {loading && (
        <div style={{ padding: tokens.space.lg, textAlign: 'center', color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>
          Loading assistant responses...
        </div>
      )}

      {/* Responses */}
      {!loading && responses.length === 0 && (
        <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.sm }}>
          No assistant responses yet.
        </div>
      )}

      {!loading && responses.map((response) => (
        <ResponseCard key={response.response_id} response={response} />
      ))}
    </PanelShell>
  );
}

// ─── Response Card ─────────────────────────────────────────────────────────

const OUTPUT_TYPE_CONFIG: Record<AssistantOutputType, { label: string; color: string }> = {
  verified_truth: { label: 'VERIFIED TRUTH', color: tokens.color.success },
  uncertainty: { label: 'UNCERTAINTY', color: tokens.color.warning },
  insufficiency: { label: 'INSUFFICIENT DATA', color: tokens.color.error },
  next_valid_action: { label: 'NEXT VALID ACTION', color: tokens.color.info },
};

function ResponseCard({ response }: { response: AssistantResponse }) {
  const config = OUTPUT_TYPE_CONFIG[response.output_type] ?? { label: response.output_type, color: tokens.color.fgMuted };

  return (
    <div style={{
      padding: tokens.space.md,
      marginBottom: tokens.space.sm,
      background: tokens.color.bgBase,
      borderRadius: tokens.radius.sm,
      borderLeft: `3px solid ${config.color}`,
      fontSize: tokens.font.sizeXs,
      lineHeight: tokens.font.lineNormal,
    }}>
      {/* Header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: tokens.space.sm }}>
        <span style={{
          color: config.color,
          fontWeight: tokens.font.weightSemibold,
          textTransform: 'uppercase',
          letterSpacing: '0.05em',
        }}>
          {config.label}
        </span>
        {response.has_proposal && (
          <span style={{
            color: tokens.color.compare,
            background: `${tokens.color.compare}15`,
            padding: '1px 6px',
            borderRadius: tokens.radius.sm,
            fontWeight: tokens.font.weightMedium,
          }}>
            HAS PROPOSAL
          </span>
        )}
      </div>

      {/* Content */}
      <div style={{
        color: tokens.color.fgPrimary,
        lineHeight: '1.5',
        marginBottom: tokens.space.sm,
      }}>
        {response.content}
      </div>

      {/* Confidence Basis */}
      <div style={{
        padding: tokens.space.sm,
        background: tokens.color.bgSurface,
        borderRadius: tokens.radius.sm,
        marginBottom: tokens.space.sm,
      }}>
        <div style={{ color: tokens.color.fgMuted, fontWeight: tokens.font.weightMedium, marginBottom: '2px' }}>
          CONFIDENCE BASIS
        </div>
        <div style={{ color: tokens.color.fgSecondary, lineHeight: '1.4' }}>
          {response.confidence_basis}
        </div>
      </div>

      {/* Proposal Indicator */}
      {response.has_proposal && response.proposal && (
        <div style={{
          padding: tokens.space.sm,
          background: `${tokens.color.compare}08`,
          border: `1px solid ${tokens.color.compare}30`,
          borderRadius: tokens.radius.sm,
          marginBottom: tokens.space.sm,
        }}>
          <div style={{ color: tokens.color.compare, fontWeight: tokens.font.weightMedium, marginBottom: '2px' }}>
            PROPOSAL ROUTED TO MAILBOX
          </div>
          <div style={{ color: tokens.color.fgSecondary }}>
            {response.proposal.reasoning_summary}
          </div>
        </div>
      )}

      {/* Footer */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        color: tokens.color.fgMuted,
        fontFamily: tokens.font.familyMono,
      }}>
        <span>Snapshot: {response.snapshot_id}</span>
        <span>{new Date(response.timestamp).toLocaleTimeString()}</span>
      </div>
    </div>
  );
}
