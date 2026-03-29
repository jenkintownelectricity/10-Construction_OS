/**
 * Resolves the Construction Application OS landing surface from
 * the initial_view field in a Fabric session envelope.
 *
 * Maps initial_view to allowed control-tower surfaces only.
 * Unknown views are rejected fail-closed.
 *
 * No Fabric runtime imports. No environment-variable dependency.
 * No runtime execution logic. No topology mutation.
 *
 * Construction OS remains standalone-valid and may execute independently of Fabric.
 */

/** Allowed landing views from the Fabric session envelope. */
export type LandingView = "workspace" | "dashboard" | "atlas" | "inspector";

/** Resolved landing surface descriptor. Metadata only. */
export interface LandingSurface {
  readonly view: LandingView;
  readonly surface_label: string;
  readonly surface_id: string;
}

export interface ResolveSurfaceResult {
  readonly success: boolean;
  readonly surface: LandingSurface | null;
  readonly errors: readonly string[];
}

const SURFACE_MAP: Record<LandingView, LandingSurface> = {
  workspace: {
    view: "workspace",
    surface_label: "Control Tower Workspace",
    surface_id: "control-tower-workspace",
  },
  dashboard: {
    view: "dashboard",
    surface_label: "Control Tower Dashboard",
    surface_id: "control-tower-dashboard",
  },
  atlas: {
    view: "atlas",
    surface_label: "Atlas Navigation",
    surface_id: "atlas-navigation",
  },
  inspector: {
    view: "inspector",
    surface_label: "Inspector",
    surface_id: "inspector-surface",
  },
};

const ALLOWED_VIEWS = new Set<string>(Object.keys(SURFACE_MAP));

/**
 * Resolves the initial_view string to a bounded landing surface.
 * Rejects unknown views fail-closed.
 */
export function resolveLandingSurface(initialView: string): ResolveSurfaceResult {
  if (!ALLOWED_VIEWS.has(initialView)) {
    return {
      success: false,
      surface: null,
      errors: [
        `FAIL_CLOSED: Unknown initial_view '${initialView}'. Allowed: ${[...ALLOWED_VIEWS].join(", ")}.`,
      ],
    };
  }

  return {
    success: true,
    surface: SURFACE_MAP[initialView as LandingView],
    errors: [],
  };
}
