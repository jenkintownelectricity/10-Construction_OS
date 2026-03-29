import { validateFabricSessionEnvelope } from "./validateFabricSessionEnvelope";
import type { FabricSessionLandingEnvelope } from "./constructionOsLandingContract";

/**
 * Loads and parses an incoming Fabric session envelope for landing.
 *
 * Deterministic parsing only. No environment-variable dependency.
 * No Fabric runtime import. Fails closed on missing or invalid data.
 *
 * Construction OS remains standalone-valid and may execute independently of Fabric.
 */

export interface LoadEnvelopeResult {
  readonly success: boolean;
  readonly envelope: FabricSessionLandingEnvelope | null;
  readonly errors: readonly string[];
}

/**
 * Parses a raw JSON string into a validated Fabric session landing envelope.
 *
 * This function does NOT:
 * - read from process.env
 * - import Fabric runtime modules
 * - invoke external systems
 * - perform cross-repo operations
 */
export function loadFabricSessionEnvelope(raw: string): LoadEnvelopeResult {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return {
      success: false,
      envelope: null,
      errors: ["FAIL_CLOSED: Invalid JSON in Fabric session envelope."],
    };
  }

  if (typeof parsed !== "object" || parsed === null || Array.isArray(parsed)) {
    return {
      success: false,
      envelope: null,
      errors: ["FAIL_CLOSED: Fabric session envelope must be a non-null object."],
    };
  }

  const validation = validateFabricSessionEnvelope(parsed);
  if (!validation.valid) {
    return {
      success: false,
      envelope: null,
      errors: validation.errors,
    };
  }

  return {
    success: true,
    envelope: parsed as FabricSessionLandingEnvelope,
    errors: [],
  };
}
