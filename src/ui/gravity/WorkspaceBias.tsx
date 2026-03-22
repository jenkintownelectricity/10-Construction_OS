/**
 * Construction OS — Workspace Bias Controls
 *
 * Four controls in workspace header:
 *   + expand workspace (increase dominance)
 *   - shrink workspace (increase surrounding visibility)
 *   ← visual/spatial bias (expand right visual usage)
 *   → document/reference bias (expand left document usage)
 *
 * No freeform manual resizing. Deterministic bias steps.
 */

import { useCallback } from 'react';
import { tokens } from '../theme/tokens';
import { PROXIMITY } from './ProximityConstants';

export interface BiasState {
  /** Workspace share percentage (40-90) */
  workspaceShare: number;
  /** Horizontal bias: negative = visual/spatial, positive = document/reference */
  horizontalBias: number;
}

interface WorkspaceBiasProps {
  bias: BiasState;
  onBiasChange: (bias: BiasState) => void;
}

export function WorkspaceBiasControls({ bias, onBiasChange }: WorkspaceBiasProps) {
  const handleExpand = useCallback(() => {
    onBiasChange({
      ...bias,
      workspaceShare: Math.min(bias.workspaceShare + PROXIMITY.biasStep, PROXIMITY.workspaceMaxShare),
    });
  }, [bias, onBiasChange]);

  const handleShrink = useCallback(() => {
    onBiasChange({
      ...bias,
      workspaceShare: Math.max(bias.workspaceShare - PROXIMITY.biasStep, PROXIMITY.workspaceMinShare),
    });
  }, [bias, onBiasChange]);

  const handleVisualBias = useCallback(() => {
    onBiasChange({
      ...bias,
      horizontalBias: Math.max(bias.horizontalBias - PROXIMITY.biasStep, -40),
    });
  }, [bias, onBiasChange]);

  const handleDocBias = useCallback(() => {
    onBiasChange({
      ...bias,
      horizontalBias: Math.min(bias.horizontalBias + PROXIMITY.biasStep, 40),
    });
  }, [bias, onBiasChange]);

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '1px',
      background: tokens.color.border,
      borderRadius: tokens.radius.sm,
      overflow: 'hidden',
    }}>
      <BiasButton
        label={'\u2190'}
        title="Visual/spatial bias — expand right panels"
        onClick={handleVisualBias}
        active={bias.horizontalBias < 0}
      />
      <BiasButton
        label={'\u2212'}
        title="Shrink workspace — increase surrounding panel visibility"
        onClick={handleShrink}
        active={bias.workspaceShare < PROXIMITY.workspaceDefaultShare}
      />
      <BiasButton
        label={'\u002B'}
        title="Expand workspace — increase workspace dominance"
        onClick={handleExpand}
        active={bias.workspaceShare > PROXIMITY.workspaceDefaultShare}
      />
      <BiasButton
        label={'\u2192'}
        title="Document/reference bias — expand left panels"
        onClick={handleDocBias}
        active={bias.horizontalBias > 0}
      />
    </div>
  );
}

function BiasButton({ label, title, onClick, active }: {
  label: string;
  title: string;
  onClick: () => void;
  active: boolean;
}) {
  return (
    <button
      onClick={onClick}
      title={title}
      style={{
        width: '28px',
        height: '26px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        background: active ? tokens.color.bgActive : tokens.color.bgElevated,
        color: active ? tokens.color.accentPrimary : tokens.color.fgMuted,
        border: 'none',
        cursor: 'pointer',
        fontSize: tokens.font.sizeSm,
        fontWeight: tokens.font.weightSemibold,
        padding: 0,
        transition: `all ${tokens.transition.fast}`,
      }}
    >
      {label}
    </button>
  );
}

export function getDefaultBias(): BiasState {
  return {
    workspaceShare: PROXIMITY.workspaceDefaultShare,
    horizontalBias: 0,
  };
}
