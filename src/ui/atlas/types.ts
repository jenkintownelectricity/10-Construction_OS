/**
 * Construction Atlas — Layout types
 *
 * Route and navigation types for the primary application shell.
 */

export type AtlasRoute =
  | 'dashboard'
  | 'atlas'
  | 'projects'
  | 'details'
  | 'shop-drawings'
  | 'manufacturers'
  | 'observations'
  | 'artifacts'
  | 'tools'
  | 'viewer'
  | 'ai-settings'
  | 'branding';

export interface NavItem {
  id: AtlasRoute;
  label: string;
  icon: string;
}

export interface NavGroup {
  label: string;
  items: NavItem[];
}

export const NAV_GROUPS: NavGroup[] = [
  {
    label: 'PRODUCT',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: '\u2630' },
      { id: 'atlas', label: 'Atlas', icon: '\u25C7' },
      { id: 'projects', label: 'Projects', icon: '\u25A0' },
      { id: 'details', label: 'Details', icon: '\u2726' },
      { id: 'shop-drawings', label: 'Shop Drawings', icon: '\u25A1' },
      { id: 'manufacturers', label: 'Manufacturers', icon: '\u25AA' },
      { id: 'observations', label: 'Observations', icon: '\u25CB' },
      { id: 'artifacts', label: 'Artifacts', icon: '\u25B7' },
    ],
  },
  {
    label: 'TOOLS',
    items: [
      { id: 'tools', label: 'Tools', icon: '\u2692' },
      { id: 'viewer', label: 'Viewer', icon: '\u2B1A' },
    ],
  },
  {
    label: 'CONFIG',
    items: [
      { id: 'ai-settings', label: 'AI Settings', icon: '\u25AA' },
      { id: 'branding', label: 'Branding', icon: '\u25CF' },
    ],
  },
];
