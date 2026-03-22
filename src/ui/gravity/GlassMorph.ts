/**
 * Construction OS — Glass Morph Panel Style
 *
 * Professional glass styling for secondary panels only.
 * Workspace controls remain crisp, not glassy.
 *
 * No flashy/glowing effects. Subtle, professional.
 */

import type { CSSProperties } from 'react';

/** Glass morph style for secondary/edge panels */
export const glassMorphStyle: CSSProperties = {
  background: 'rgba(22,26,34,0.65)',
  backdropFilter: 'blur(12px)',
  WebkitBackdropFilter: 'blur(12px)',
  border: '1px solid rgba(255,255,255,0.06)',
};

/** Glass morph style for dock panels */
export const glassMorphDockStyle: CSSProperties = {
  background: 'rgba(22,26,34,0.72)',
  backdropFilter: 'blur(12px)',
  WebkitBackdropFilter: 'blur(12px)',
  border: '1px solid rgba(255,255,255,0.06)',
  borderBottom: 'none',
};

/** Glass morph style for the fan-out deck */
export const glassMorphFanStyle: CSSProperties = {
  background: 'rgba(22,26,34,0.6)',
  backdropFilter: 'blur(10px)',
  WebkitBackdropFilter: 'blur(10px)',
  border: '1px solid rgba(255,255,255,0.05)',
};

/** Glass morph card style */
export const glassMorphCardStyle: CSSProperties = {
  background: 'rgba(30,37,56,0.55)',
  backdropFilter: 'blur(8px)',
  WebkitBackdropFilter: 'blur(8px)',
  border: '1px solid rgba(255,255,255,0.04)',
};
