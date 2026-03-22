/**
 * Construction OS — Design Token System
 *
 * Premium workstation aesthetic. Dark, structured, technically potent.
 * NOT generic admin SaaS. NOT a toy AI app. NOT a dashboard.
 *
 * Typography scale: readable cockpit scale (html root = 16px).
 * No font size smaller than 0.85rem (13.6px) in cockpit panels.
 */

export const tokens = {
  // ─── Colors ─────────────────────────────────────────────────────────
  color: {
    // Background hierarchy (depth layers)
    bgDeep: '#080a0e',         // deepest background
    bgBase: '#0c0f15',         // primary workspace surface
    bgSurface: '#121620',      // panel surface
    bgElevated: '#181d2a',     // elevated surface (headers, toolbars)
    bgHover: '#1e2538',        // hover state
    bgActive: '#252d42',       // active/selected state

    // Foreground hierarchy
    fgPrimary: '#e0e4ec',      // primary text
    fgSecondary: '#8b93a8',    // secondary text
    fgMuted: '#555d73',        // muted/disabled text
    fgInverse: '#0c0f15',      // inverse text

    // Accent — restrained power
    accentPrimary: '#3b82f6',  // primary accent (blue)
    accentHover: '#2563eb',    // accent hover
    accentMuted: '#1e3a5f',    // accent muted

    // Truth Echo visual language
    echoActive: '#3b82f6',     // Truth Echo active indicator
    echoTrace: 'rgba(59,130,246,0.12)', // Echo propagation trace
    echoPulse: 'rgba(59,130,246,0.25)', // Echo pulse highlight

    // Semantic
    success: '#22c55e',
    warning: '#eab308',
    error: '#ef4444',
    info: '#3b82f6',

    // State indicators
    canonical: '#22c55e',       // canonical/source truth data
    derived: '#8b93a8',         // derived UI data
    draft: '#eab308',           // draft/unsaved state
    compare: '#a855f7',         // compare mode
    mock: '#f97316',            // mock data indicator

    // Panel borders
    border: '#1e2538',
    borderActive: '#3b82f6',
    borderSubtle: '#151a26',
  },

  // ─── Typography ─────────────────────────────────────────────────────
  // Readable cockpit scale. All sizes >= 0.85rem (13.6px at 16px root).
  font: {
    family: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif",
    familyMono: "'JetBrains Mono', 'Fira Code', 'SF Mono', monospace",
    sizeXs: '0.85rem',       // ~13.6px — rows, status, meta, badges
    sizeSm: '0.95rem',       // ~15.2px — panel body, content, lists
    sizeBase: '1rem',        // 16px — base readable size
    sizeMd: '1.05rem',       // ~16.8px — panel titles, headings
    sizeLg: '1.25rem',       // 20px — section headings
    sizeXl: '1.5rem',        // 24px — page headings
    weightNormal: '400',
    weightMedium: '500',
    weightSemibold: '600',
    weightBold: '700',
    lineNormal: '1.4',       // line-height for content/lists/diagnostics
    lineTight: '1.25',       // line-height for headings/titles
  },

  // ─── Spacing ────────────────────────────────────────────────────────
  space: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    lg: '16px',
    xl: '24px',
    xxl: '32px',
    rowY: '8px',              // vertical row padding
    rowX: '12px',             // horizontal row padding
  },

  // ─── Borders & Radii ───────────────────────────────────────────────
  radius: {
    sm: '4px',
    md: '6px',
    lg: '8px',
  },

  // ─── Shadows ────────────────────────────────────────────────────────
  shadow: {
    panel: '0 1px 3px rgba(0,0,0,0.4)',
    elevated: '0 4px 12px rgba(0,0,0,0.5)',
    echo: '0 0 0 1px rgba(59,130,246,0.3), 0 0 8px rgba(59,130,246,0.15)',
  },

  // ─── Transitions ──────────────────────────────────────────────────
  transition: {
    fast: '120ms ease',
    normal: '200ms ease',
    echo: '300ms ease-out',
  },
} as const;
