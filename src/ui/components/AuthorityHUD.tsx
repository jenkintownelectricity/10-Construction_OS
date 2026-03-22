/**
 * Construction OS — Adaptive Authority HUD
 *
 * Compact authority indicator in the top shell/header.
 * Shows current authority/agency display state:
 *   L3 Read-Only (blue)
 *   L2 Propose (purple)
 *   L1 Execute (gold)
 *
 * AWARENESS ONLY — this component does NOT enforce authority logic.
 * It reflects the current display state from the activeObjectStore.
 * Subtle signal colors; does NOT theme-shift the whole app.
 */

import { tokens } from '../theme/tokens';
import { useActiveObject } from '../stores/useSyncExternalStore';
import type { AuthorityLevel } from '../stores/activeObjectStore';

const AUTHORITY_CONFIG: Record<AuthorityLevel, { label: string; color: string; description: string }> = {
  L3: { label: 'L3', color: tokens.color.authorityL3, description: 'Read-Only' },
  L2: { label: 'L2', color: tokens.color.authorityL2, description: 'Propose' },
  L1: { label: 'L1', color: tokens.color.authorityL1, description: 'Execute' },
};

export function AuthorityHUD() {
  const { authorityLevel } = useActiveObject();
  const config = AUTHORITY_CONFIG[authorityLevel];

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: tokens.space.xs,
        padding: `${tokens.space.xs} ${tokens.space.sm}`,
        borderRadius: tokens.radius.sm,
        background: `${config.color}12`,
        border: `1px solid ${config.color}30`,
        cursor: 'default',
        userSelect: 'none',
      }}
      title={`Authority: ${config.label} — ${config.description}`}
    >
      {/* Signal dot */}
      <span
        style={{
          width: '6px',
          height: '6px',
          borderRadius: '50%',
          background: config.color,
          boxShadow: `0 0 4px ${config.color}60`,
          flexShrink: 0,
        }}
      />
      <span
        style={{
          fontSize: tokens.font.sizeXs,
          fontWeight: tokens.font.weightSemibold,
          color: config.color,
          fontFamily: tokens.font.familyMono,
          letterSpacing: '0.05em',
          lineHeight: tokens.font.lineTight,
        }}
      >
        {config.label}
      </span>
      <span
        style={{
          fontSize: tokens.font.sizeXs,
          color: `${config.color}99`,
          lineHeight: tokens.font.lineTight,
        }}
      >
        {config.description}
      </span>
    </div>
  );
}
