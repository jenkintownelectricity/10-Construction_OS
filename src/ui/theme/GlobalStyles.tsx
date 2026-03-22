/**
 * Construction OS — Global Styles
 *
 * Includes cockpit typography scale, density modes, layout rules,
 * and visual hierarchy refinement for the enterprise command interface.
 * Root font-size: 16px. No cockpit text smaller than 0.85rem (~13.6px).
 */

import { tokens } from './tokens';

export function GlobalStyles() {
  return (
    <style>{`
      :root {
        /* ─── Color tokens ────────────────────────────────────────── */
        --cos-bg-deep: ${tokens.color.bgDeep};
        --cos-bg-base: ${tokens.color.bgBase};
        --cos-bg-surface: ${tokens.color.bgSurface};
        --cos-bg-elevated: ${tokens.color.bgElevated};
        --cos-bg-hover: ${tokens.color.bgHover};
        --cos-bg-active: ${tokens.color.bgActive};
        --cos-fg-primary: ${tokens.color.fgPrimary};
        --cos-fg-secondary: ${tokens.color.fgSecondary};
        --cos-fg-muted: ${tokens.color.fgMuted};
        --cos-accent: ${tokens.color.accentPrimary};
        --cos-accent-hover: ${tokens.color.accentHover};
        --cos-border: ${tokens.color.border};
        --cos-border-active: ${tokens.color.borderActive};
        --cos-echo-active: ${tokens.color.echoActive};
        --cos-echo-trace: ${tokens.color.echoTrace};
        --cos-echo-pulse: ${tokens.color.echoPulse};
        --cos-success: ${tokens.color.success};
        --cos-warning: ${tokens.color.warning};
        --cos-error: ${tokens.color.error};
        --cos-mock: ${tokens.color.mock};
        --cos-font: ${tokens.font.family};
        --cos-font-mono: ${tokens.font.familyMono};

        /* ─── Cockpit typography scale ────────────────────────────── */
        --font-xs: ${tokens.font.sizeXs};
        --font-sm: ${tokens.font.sizeSm};
        --font-md: ${tokens.font.sizeMd};
        --font-lg: ${tokens.font.sizeLg};
        --line-tight: ${tokens.font.lineTight};
        --line-normal: ${tokens.font.lineNormal};
        --space-row-y: ${tokens.space.rowY};
        --space-row-x: ${tokens.space.rowX};

        /* ─── Authority colors ────────────────────────────────────── */
        --cos-authority-l3: ${tokens.color.authorityL3};
        --cos-authority-l2: ${tokens.color.authorityL2};
        --cos-authority-l1: ${tokens.color.authorityL1};
      }

      *, *::before, *::after {
        box-sizing: border-box;
      }

      html {
        font-size: 16px;
      }

      html, body, #root {
        width: 100%;
        height: 100%;
        margin: 0;
        padding: 0;
        overflow: hidden;
        font-family: var(--cos-font);
        background: var(--cos-bg-deep);
        color: var(--cos-fg-primary);
        font-size: ${tokens.font.sizeBase};
        line-height: var(--line-normal);
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      /* ─── Density Modes ──────────────────────────────────────── */
      body.readable {
        font-size: 1.1rem;
      }
      body.compact {
        font-size: 0.95rem;
      }

      /* ─── Cockpit Typography Classes ─────────────────────────── */
      .panel-title, .panel-header, .panel-tab-title {
        font-size: var(--font-md);
        font-weight: 600;
        line-height: var(--line-tight);
      }

      .panel-subtitle {
        font-size: var(--font-xs);
        font-weight: 400;
        line-height: var(--line-normal);
        color: var(--cos-fg-muted);
        letter-spacing: 0.03em;
      }

      .panel-content, .panel-body, .panel-text, .panel-label,
      .panel-value, .tree-node, .list-item, .table-cell,
      .proposal-text, .assistant-text, .reference-text,
      .awareness-text, .spatial-text, .system-text {
        font-size: var(--font-sm);
        line-height: var(--line-normal);
      }

      .status-line, .meta-text, .caption, .badge, .chip,
      .table-row, .diagnostics-row, .tree-meta,
      .panel-subtitle, .small-text {
        font-size: var(--font-xs);
        line-height: var(--line-normal);
      }

      button, .btn, .tab, .pill, .action-chip {
        font-size: 0.85rem;
        line-height: 1.2;
      }

      .panel-row, .table-row, .list-row, .tree-row,
      .diagnostics-row, .proposal-row {
        padding: var(--space-row-y) var(--space-row-x);
        line-height: var(--line-normal);
      }

      /* ─── Workspace Layout (prevents lower panel compression) ─ */
      .workspace-shell {
        display: grid;
        grid-template-rows: 56px 1fr 320px;
        min-height: 0;
      }

      .workspace-main, .workspace-center, .workspace-content {
        min-height: 0;
      }

      .workspace-bottom, .workspace-lower-panels {
        min-height: 320px;
      }

      .app-shell, .cockpit-shell, .cockpit-layout {
        min-height: 0;
      }

      .grid-cell, .panel-container, .workspace-panel {
        min-height: 0;
        overflow: hidden;
      }

      /* ─── Dockview Theme Overrides ───────────────────────────── */
      .dockview-theme-dark {
        --dv-activegroup-visiblepanel-tab-background-color: var(--cos-bg-elevated);
        --dv-activegroup-hiddenpanel-tab-background-color: var(--cos-bg-surface);
        --dv-inactivegroup-visiblepanel-tab-background-color: var(--cos-bg-surface);
        --dv-inactivegroup-hiddenpanel-tab-background-color: var(--cos-bg-base);
        --dv-tab-divider-color: var(--cos-border);
        --dv-activegroup-visiblepanel-tab-color: var(--cos-fg-primary);
        --dv-activegroup-hiddenpanel-tab-color: var(--cos-fg-secondary);
        --dv-separator-border: var(--cos-border);
        --dv-paneview-header-border-color: var(--cos-border);
        --dv-group-view-background-color: var(--cos-bg-base);
        --dv-activegroup-visiblepanel-tab-font-size: var(--font-xs);
        --dv-activegroup-hiddenpanel-tab-font-size: var(--font-xs);
      }

      /* ─── Scrollbar Styling ──────────────────────────────────── */
      ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
      }
      ::-webkit-scrollbar-track {
        background: transparent;
      }
      ::-webkit-scrollbar-thumb {
        background: var(--cos-bg-hover);
        border-radius: 3px;
      }
      ::-webkit-scrollbar-thumb:hover {
        background: var(--cos-fg-muted);
      }

      /* ─── Truth Echo Animation ───────────────────────────────── */
      @keyframes truthEchoPulse {
        0% { box-shadow: 0 0 0 0 var(--cos-echo-pulse); }
        50% { box-shadow: 0 0 0 3px var(--cos-echo-trace); }
        100% { box-shadow: 0 0 0 0 transparent; }
      }

      .truth-echo-active {
        animation: truthEchoPulse 600ms ease-out;
        border-color: var(--cos-echo-active) !important;
      }

      /* ─── Context Collapse Animation ─────────────────────────── */
      @keyframes contextCollapse {
        from { opacity: 1; }
        to { opacity: 0.4; }
      }

      @keyframes contextExpand {
        from { opacity: 0.4; }
        to { opacity: 1; }
      }

      /* ─── Command Palette Backdrop ───────────────────────────── */
      @keyframes paletteSlideIn {
        from {
          opacity: 0;
          transform: translateY(-8px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
    `}</style>
  );
}
