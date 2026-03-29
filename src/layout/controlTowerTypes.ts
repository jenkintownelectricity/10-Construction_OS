/**
 * Construction OS — Control Tower Route Types
 * Wave C1 — Route definitions for the Control Tower sidebar.
 */

export type ControlTowerRoute =
  | 'dashboard'
  | 'foundry'
  | 'truth-spine'
  | 'atlas'
  | 'assemblies'
  | 'materials'
  | 'specifications'
  | 'chemistry'
  | 'scope'
  | 'patterns'
  | 'runtime'
  | 'registry'
  | 'signals'
  | 'receipts'
  | 'branding'
  | 'mirror-builder';

export interface ControlTowerNavItem {
  id: ControlTowerRoute;
  label: string;
  icon: string;
}

export const CONTROL_TOWER_NAV: ControlTowerNavItem[] = [
  { id: 'dashboard', label: 'Dashboard', icon: '\u2630' },
  { id: 'mirror-builder', label: 'Mirror Builder', icon: '\u25C9' },
  { id: 'foundry', label: 'Foundry', icon: '\u2692' },
  { id: 'truth-spine', label: 'Truth Spine', icon: '\u25C8' },
  { id: 'atlas', label: 'Atlas', icon: '\u25C7' },
  { id: 'assemblies', label: 'Assemblies', icon: '\u25A3' },
  { id: 'materials', label: 'Materials', icon: '\u25A0' },
  { id: 'specifications', label: 'Specifications', icon: '\u25B6' },
  { id: 'chemistry', label: 'Chemistry', icon: '\u25CF' },
  { id: 'scope', label: 'Scope', icon: '\u25CB' },
  { id: 'patterns', label: 'Patterns', icon: '\u2726' },
  { id: 'runtime', label: 'Runtime', icon: '\u25B7' },
  { id: 'registry', label: 'Registry', icon: '\u25A1' },
  { id: 'signals', label: 'Signals', icon: '\u25AA' },
  { id: 'receipts', label: 'Receipts', icon: '\u25AB' },
  { id: 'branding', label: 'Branding', icon: '\u25C6' },
];
