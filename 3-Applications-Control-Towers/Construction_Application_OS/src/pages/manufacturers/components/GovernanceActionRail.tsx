/**
 * Manufacturer Hub — Governance & Action Rail
 * Right rail panel with clearly separated governance and action families.
 *
 * Governance family (gold/amber): certification state, projection state, truth debt
 * Action family (blue): inspect, navigate, mode-switch, future actions
 *
 * Colors do not invent truth — they are presentational separation only.
 */

import { tokens } from '../../../ui/theme/tokens';
import type {
  GovernanceStatus,
  ActionItem,
  ManufacturerHubMode,
} from '../../../lib/manufacturers/manufacturerHubTypes';

const t = tokens;

interface GovernanceActionRailProps {
  governance: GovernanceStatus;
  actions: ActionItem[];
  mode: ManufacturerHubMode;
  onModeChange: (mode: ManufacturerHubMode) => void;
  surface: Record<string, string>;
}

const CERT_STATE_COLORS: Record<string, string> = {
  certified: '#22c55e',
  unverified: '#8b93a8',
  partial: '#eab308',
  blocked: '#ef4444',
};

const PROJECTION_STATE_COLORS: Record<string, string> = {
  active: '#22c55e',
  stale: '#ef4444',
  scaffold: '#eab308',
};

export function GovernanceActionRail({
  governance, actions, mode, onModeChange, surface,
}: GovernanceActionRailProps) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', flex: 1 }}>
      {/* GOVERNANCE SECTION — gold/amber family */}
      <div style={{
        padding: '16px',
        borderBottom: `1px solid ${surface.border}`,
      }}>
        <div style={{
          fontSize: '10px',
          fontWeight: Number(t.font.weightSemibold),
          color: '#eab308',
          textTransform: 'uppercase',
          letterSpacing: '0.08em',
          marginBottom: '12px',
        }}>
          Governance
        </div>

        {/* Certification State */}
        <div style={{ marginBottom: '10px' }}>
          <div style={{
            fontSize: '10px',
            color: surface.fgMuted,
            marginBottom: '4px',
          }}>
            Certification State
          </div>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '4px 10px',
            borderRadius: t.radius.sm,
            fontSize: t.font.sizeXs,
            fontWeight: Number(t.font.weightSemibold),
            color: CERT_STATE_COLORS[governance.certificationState],
            background: `${CERT_STATE_COLORS[governance.certificationState]}18`,
          }}>
            <span style={{
              width: 6, height: 6, borderRadius: '50%',
              background: CERT_STATE_COLORS[governance.certificationState],
            }} />
            {governance.certificationState.toUpperCase()}
          </div>
        </div>

        {/* Projection State */}
        <div style={{ marginBottom: '10px' }}>
          <div style={{
            fontSize: '10px',
            color: surface.fgMuted,
            marginBottom: '4px',
          }}>
            Observer Projection State
          </div>
          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '6px',
            padding: '4px 10px',
            borderRadius: t.radius.sm,
            fontSize: t.font.sizeXs,
            fontWeight: Number(t.font.weightSemibold),
            color: PROJECTION_STATE_COLORS[governance.projectionState],
            background: `${PROJECTION_STATE_COLORS[governance.projectionState]}18`,
          }}>
            <span style={{
              width: 6, height: 6, borderRadius: '50%',
              background: PROJECTION_STATE_COLORS[governance.projectionState],
            }} />
            {governance.projectionState.toUpperCase()}
          </div>
        </div>

        {/* Seed Status */}
        <div style={{ marginBottom: '10px' }}>
          <div style={{
            fontSize: '10px',
            color: surface.fgMuted,
            marginBottom: '4px',
          }}>
            Seed Status
          </div>
          <div style={{
            fontSize: t.font.sizeXs,
            color: governance.seedStatus === 'seeded' ? '#22c55e' : '#eab308',
            fontWeight: Number(t.font.weightMedium),
          }}>
            {governance.seedStatus === 'seeded' ? 'Fully Seeded' : 'Scaffold Only'}
          </div>
        </div>

        {/* Truth Debt */}
        {governance.truthDebt.length > 0 && (
          <div>
            <div style={{
              fontSize: '10px',
              color: surface.fgMuted,
              marginBottom: '6px',
            }}>
              Truth Debt
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
              {governance.truthDebt.map((debt, i) => (
                <div key={i} style={{
                  padding: '6px 10px',
                  background: 'rgba(234, 179, 8, 0.08)',
                  borderRadius: t.radius.sm,
                  borderLeft: '2px solid #eab308',
                  fontSize: '11px',
                  color: surface.fgSecondary,
                  lineHeight: t.font.lineNormal,
                }}>
                  {debt}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* ACTIONS SECTION — blue family */}
      <div style={{
        padding: '16px',
      }}>
        <div style={{
          fontSize: '10px',
          fontWeight: Number(t.font.weightSemibold),
          color: '#3b82f6',
          textTransform: 'uppercase',
          letterSpacing: '0.08em',
          marginBottom: '12px',
        }}>
          Actions
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
          {actions.map(action => {
            const isModeSwitchRelevant =
              action.actionType === 'mode-switch' && action.targetMode !== mode;
            const showAction = action.actionType !== 'mode-switch' || isModeSwitchRelevant;

            if (!showAction) return null;

            return (
              <button
                key={action.id}
                onClick={() => {
                  if (action.actionType === 'mode-switch' && action.targetMode) {
                    onModeChange(action.targetMode);
                  }
                }}
                disabled={!action.enabled}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  width: '100%',
                  padding: '8px 12px',
                  border: 'none',
                  borderRadius: t.radius.md,
                  cursor: action.enabled ? 'pointer' : 'not-allowed',
                  textAlign: 'left',
                  fontFamily: t.font.family,
                  fontSize: t.font.sizeXs,
                  fontWeight: Number(t.font.weightMedium),
                  color: action.enabled ? surface.accent : surface.fgMuted,
                  background: action.enabled ? surface.accentMuted : surface.bgElevated,
                  opacity: action.enabled ? 1 : 0.6,
                  transition: `background ${t.transition.fast}`,
                }}
              >
                <span style={{
                  width: 6, height: 6, borderRadius: '50%',
                  background: action.enabled ? surface.accent : surface.fgMuted,
                  flexShrink: 0,
                }} />
                {action.label}
                {action.actionType === 'future' && (
                  <span style={{
                    marginLeft: 'auto',
                    fontSize: '9px',
                    color: surface.fgMuted,
                    fontStyle: 'italic',
                  }}>
                    future
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
