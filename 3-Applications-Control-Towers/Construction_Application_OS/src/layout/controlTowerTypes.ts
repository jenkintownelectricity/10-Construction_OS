/**
 * Construction OS — Control Tower Route Types
 * Wave C1 + VTI Absorption + Manufacturer Hub — Grouped navigation with absorbed feature families.
 */

export type ControlTowerRoute =
  // Core
  | 'dashboard'
  | 'mirror-builder'
  // Foundry
  | 'foundry'
  | 'birth-planner'
  | 'kernels'
  // Atlas
  | 'atlas'
  | 'topology'
  | 'assemblies'
  // Runtime
  | 'runtime'
  | 'engines'
  | 'signals'
  | 'capabilities'
  // Governance
  | 'governance'
  | 'contracts'
  | 'doctrine'
  | 'truth-spine'
  // Registry
  | 'registry'
  | 'receipts'
  | 'mirrors'
  // Platform
  | 'viewer'
  | 'plans'
  | 'materials'
  | 'specifications'
  | 'chemistry'
  | 'scope'
  | 'patterns'
  | 'pmma-generator'
  | 'manufacturers'
  // Admin
  | 'branding'
  | 'admin';

export interface ControlTowerNavItem {
  id: ControlTowerRoute;
  label: string;
  icon: string;
}

export interface ControlTowerNavGroup {
  label: string;
  items: ControlTowerNavItem[];
}

/**
 * Grouped navigation families.
 * Absorbed VTI features are integrated into coherent groups
 * rather than exposed as a flat overloaded nav.
 */
export const CONTROL_TOWER_NAV_GROUPS: ControlTowerNavGroup[] = [
  {
    label: 'Core',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: '\u2630' },
      { id: 'mirror-builder', label: 'Mirror Builder', icon: '\u25C9' },
    ],
  },
  {
    label: 'Foundry',
    items: [
      { id: 'foundry', label: 'Kernel Foundry', icon: '\u2692' },
      { id: 'birth-planner', label: 'Birth Planner', icon: '\u2726' },
      { id: 'kernels', label: 'Kernel Vault', icon: '\u25A3' },
    ],
  },
  {
    label: 'Atlas',
    items: [
      { id: 'atlas', label: 'Atlas', icon: '\u25C7' },
      { id: 'topology', label: 'Topology', icon: '\u25C8' },
      { id: 'assemblies', label: 'Assemblies', icon: '\u25A0' },
    ],
  },
  {
    label: 'Runtime',
    items: [
      { id: 'runtime', label: 'Runtime', icon: '\u25B7' },
      { id: 'engines', label: 'Engines', icon: '\u2B21' },
      { id: 'signals', label: 'Signals', icon: '\u25AA' },
      { id: 'capabilities', label: 'Capabilities', icon: '\u25C6' },
    ],
  },
  {
    label: 'Governance',
    items: [
      { id: 'governance', label: 'Governance', icon: '\u25C8' },
      { id: 'contracts', label: 'Contracts', icon: '\u25AB' },
      { id: 'doctrine', label: 'Doctrine', icon: '\u25A1' },
      { id: 'truth-spine', label: 'Truth Spine', icon: '\u25CB' },
    ],
  },
  {
    label: 'Registry',
    items: [
      { id: 'registry', label: 'Registry', icon: '\u25A1' },
      { id: 'receipts', label: 'Receipts', icon: '\u25AB' },
      { id: 'mirrors', label: 'Mirrors', icon: '\u25D1' },
    ],
  },
  {
    label: 'Platform',
    items: [
      { id: 'viewer', label: 'Viewer', icon: '\u25CE' },
      { id: 'plans', label: 'Plans & Upgrades', icon: '\u2605' },
      { id: 'materials', label: 'Materials', icon: '\u25A0' },
      { id: 'specifications', label: 'Specifications', icon: '\u25B6' },
      { id: 'chemistry', label: 'Chemistry', icon: '\u25CF' },
      { id: 'scope', label: 'Scope', icon: '\u25CB' },
      { id: 'patterns', label: 'Patterns', icon: '\u2726' },
      { id: 'pmma-generator', label: 'PMMA Generator', icon: '\u25E9' },
      { id: 'manufacturers', label: 'Manufacturer Hub', icon: '\u2302' },
    ],
  },
  {
    label: 'Admin',
    items: [
      { id: 'branding', label: 'Branding', icon: '\u25C6' },
      { id: 'admin', label: 'Admin', icon: '\u229E' },
    ],
  },
];

/** Flat nav array for backwards compatibility. */
export const CONTROL_TOWER_NAV: ControlTowerNavItem[] = CONTROL_TOWER_NAV_GROUPS.flatMap((g) => g.items);
