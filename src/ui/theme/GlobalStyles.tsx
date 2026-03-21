/**
 * Construction OS — Global Styles
 */

import { tokens } from './tokens';

export function GlobalStyles() {
  return (
    <style>{`
      :root {
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
      }

      *, *::before, *::after {
        box-sizing: border-box;
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
        line-height: 1.5;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
      }

      /* Dockview theme overrides for Construction OS */
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
      }

      /* Scrollbar styling */
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

      /* Truth Echo animation */
      @keyframes truthEchoPulse {
        0% { box-shadow: 0 0 0 0 var(--cos-echo-pulse); }
        50% { box-shadow: 0 0 0 3px var(--cos-echo-trace); }
        100% { box-shadow: 0 0 0 0 transparent; }
      }

      .truth-echo-active {
        animation: truthEchoPulse 600ms ease-out;
        border-color: var(--cos-echo-active) !important;
      }
    `}</style>
  );
}
