/**
 * Manufacturer Hub — Mode Switch
 * Explicit WORK | SYSTEM toggle. NOT Light | Dark.
 */

import { tokens } from '../../../ui/theme/tokens';
import type { ManufacturerHubMode } from '../../../lib/manufacturers/manufacturerHubTypes';
import { MODE_LABELS, MODE_DESCRIPTIONS } from '../../../lib/manufacturers/manufacturerHubMode';

const t = tokens;

interface ManufacturerModeSwitchProps {
  mode: ManufacturerHubMode;
  onModeChange: (mode: ManufacturerHubMode) => void;
  surface: Record<string, string>;
}

export function ManufacturerModeSwitch({ mode, onModeChange, surface }: ManufacturerModeSwitchProps) {
  const modes: ManufacturerHubMode[] = ['work', 'system'];

  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      gap: '2px',
      background: surface.border,
      borderRadius: t.radius.md,
      padding: '2px',
    }}>
      {modes.map(m => (
        <button
          key={m}
          onClick={() => onModeChange(m)}
          title={MODE_DESCRIPTIONS[m]}
          style={{
            padding: '6px 16px',
            border: 'none',
            borderRadius: t.radius.sm,
            cursor: 'pointer',
            fontSize: t.font.sizeXs,
            fontWeight: Number(mode === m ? t.font.weightBold : t.font.weightMedium),
            fontFamily: t.font.family,
            letterSpacing: '0.08em',
            color: mode === m ? '#ffffff' : surface.fgSecondary,
            background: mode === m ? surface.accent : 'transparent',
            transition: `all ${t.transition.fast}`,
          }}
        >
          {MODE_LABELS[m]}
        </button>
      ))}
    </div>
  );
}
