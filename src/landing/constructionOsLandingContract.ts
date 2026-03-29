import { loadFabricSessionEnvelope } from "./loadFabricSessionEnvelope";
import { resolveLandingSurface } from "./resolveLandingSurface";
import type { LandingSurface } from "./resolveLandingSurface";

/**
 * Construction OS Fabric Session Landing Contract.
 *
 * Orchestrates: loader → validator → surface resolver.
 * Returns a bounded landing result in metadata form only.
 *
 * This contract does NOT:
 * - Execute runtime actions
 * - Mutate topology
 * - Import Fabric runtime modules
 * - Depend on environment variables
 * - Perform cross-repo writes or invocations
 * - Accept identity, auth tokens, secrets, or permission grants
 *
 * Construction OS remains standalone-valid and may execute independently of Fabric.
 */

/** Accepted Fabric session envelope fields for landing. */
export interface FabricSessionLandingEnvelope {
  readonly envelope_id: string;
  readonly domain_id: "construction-os";
  readonly domain_key: "construction_os";
  readonly launch_origin: "fabric_domain_surface" | "fabric_control_tower" | "fabric_tenant_surface";
  readonly target_surface: "construction_application_os";
  readonly initial_view: "workspace" | "dashboard" | "atlas" | "inspector";
  readonly observer_mode: true;
  readonly branding_ref: string;
  readonly registry_ref: string;
  readonly launch_route: string;
  readonly return_route: string;
  readonly session_scope: "metadata_only";
  readonly readiness_state: "not_ready" | "registry_validated" | "launch_ready" | "launched" | "suspended";
  readonly standalone_valid: true;
  readonly created_from: "fabric_launch_bridge" | "fabric_domain_attachment" | "manual_declaration";
  readonly notes: readonly string[];
}

/** Bounded landing result. Metadata only. */
export interface ConstructionOsLandingResult {
  readonly success: boolean;
  readonly envelope_id: string | null;
  readonly landing_surface: LandingSurface | null;
  readonly branding_ref: string | null;
  readonly return_route: string | null;
  readonly observer_mode: true | null;
  readonly standalone_valid: true | null;
  readonly errors: readonly string[];
}

/**
 * Processes a raw Fabric session envelope JSON string and resolves
 * the Construction OS landing surface.
 *
 * Returns a bounded metadata-only landing result with:
 * - resolved landing surface
 * - preserved return_route for later Fabric return navigation
 * - branding reference for display
 * - observer_mode and standalone_valid confirmation
 *
 * No runtime invocation. No Fabric runtime import. No external invocation.
 */
export function processLanding(rawEnvelope: string): ConstructionOsLandingResult {
  // Load and validate the envelope
  const loadResult = loadFabricSessionEnvelope(rawEnvelope);

  if (!loadResult.success || !loadResult.envelope) {
    return {
      success: false,
      envelope_id: null,
      landing_surface: null,
      branding_ref: null,
      return_route: null,
      observer_mode: null,
      standalone_valid: null,
      errors: [
        "FAIL_CLOSED: Landing contract cannot process envelope.",
        ...loadResult.errors,
      ],
    };
  }

  const envelope = loadResult.envelope;

  // Resolve landing surface from initial_view
  const surfaceResult = resolveLandingSurface(envelope.initial_view);

  if (!surfaceResult.success || !surfaceResult.surface) {
    return {
      success: false,
      envelope_id: envelope.envelope_id,
      landing_surface: null,
      branding_ref: envelope.branding_ref,
      return_route: envelope.return_route,
      observer_mode: envelope.observer_mode,
      standalone_valid: envelope.standalone_valid,
      errors: [
        "FAIL_CLOSED: Landing surface resolution failed.",
        ...surfaceResult.errors,
      ],
    };
  }

  // Return bounded landing result — metadata only
  return {
    success: true,
    envelope_id: envelope.envelope_id,
    landing_surface: surfaceResult.surface,
    branding_ref: envelope.branding_ref,
    return_route: envelope.return_route,
    observer_mode: envelope.observer_mode,
    standalone_valid: envelope.standalone_valid,
    errors: [],
  };
}
