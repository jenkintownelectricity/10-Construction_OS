/**
 * Validates an incoming Fabric session envelope against the
 * construction_os_session_landing.schema.json contract.
 *
 * Rejects identity/auth/secret fields.
 * Rejects unknown authority-escalation fields.
 * Enforces observer_mode === true.
 * Enforces standalone_valid === true.
 * Enforces session_scope === "metadata_only".
 * Fails closed on invalid envelope.
 *
 * No Fabric runtime imports. No environment-variable dependency.
 *
 * Construction OS remains standalone-valid and may execute independently of Fabric.
 */

const ALLOWED_FIELDS = new Set([
  "envelope_id",
  "domain_id",
  "domain_key",
  "launch_origin",
  "target_surface",
  "initial_view",
  "observer_mode",
  "branding_ref",
  "registry_ref",
  "launch_route",
  "return_route",
  "session_scope",
  "readiness_state",
  "standalone_valid",
  "created_from",
  "notes",
]);

const FORBIDDEN_FIELDS = new Set([
  "user_id", "user_identity", "identity", "auth_token", "token",
  "secret", "password", "credential", "permission", "permissions",
  "session_state", "mutable_state", "write_permission", "execution_command",
  "runtime_command", "topology_mutation", "kernel_authority", "atlas_authority",
  "cognitive_authority", "runtime_authority",
]);

const VALID_LAUNCH_ORIGINS = new Set(["fabric_domain_surface", "fabric_control_tower", "fabric_tenant_surface"]);
const VALID_INITIAL_VIEWS = new Set(["workspace", "dashboard", "atlas", "inspector"]);
const VALID_READINESS_STATES = new Set(["not_ready", "registry_validated", "launch_ready", "launched", "suspended"]);
const VALID_CREATED_FROM = new Set(["fabric_launch_bridge", "fabric_domain_attachment", "manual_declaration"]);

const ENVELOPE_ID_PATTERN = /^session-envelope-construction-os-[a-z0-9-]+$/;
const ROUTE_PATTERN = /^\/[a-z0-9/_-]+$/;
const REGISTRY_REF_PATTERN = /^construction_os_registry::/;

export interface EnvelopeValidationResult {
  readonly valid: boolean;
  readonly errors: readonly string[];
}

export function validateFabricSessionEnvelope(data: unknown): EnvelopeValidationResult {
  const errors: string[] = [];

  if (typeof data !== "object" || data === null || Array.isArray(data)) {
    return { valid: false, errors: ["FAIL_CLOSED: Session envelope must be a non-null object."] };
  }

  const record = data as Record<string, unknown>;

  // Reject forbidden fields — identity/auth/secret guard
  for (const key of Object.keys(record)) {
    if (FORBIDDEN_FIELDS.has(key)) {
      errors.push(`FAIL_CLOSED: Forbidden field '${key}' detected. Identity/auth/secret fields are prohibited.`);
    }
  }

  // Reject unknown fields — authority-escalation guard
  for (const key of Object.keys(record)) {
    if (!ALLOWED_FIELDS.has(key) && !FORBIDDEN_FIELDS.has(key)) {
      errors.push(`FAIL_CLOSED: Unknown field '${key}' detected. Possible authority escalation — rejected.`);
    }
  }

  // Required: envelope_id
  if (typeof record.envelope_id !== "string" || !ENVELOPE_ID_PATTERN.test(record.envelope_id)) {
    errors.push("FAIL_CLOSED: envelope_id must match 'session-envelope-construction-os-{key}'.");
  }

  // Required: domain_id
  if (record.domain_id !== "construction-os") {
    errors.push(`FAIL_CLOSED: domain_id must be 'construction-os'.`);
  }

  // Required: domain_key
  if (record.domain_key !== "construction_os") {
    errors.push(`FAIL_CLOSED: domain_key must be 'construction_os'.`);
  }

  // Required: launch_origin
  if (typeof record.launch_origin !== "string" || !VALID_LAUNCH_ORIGINS.has(record.launch_origin)) {
    errors.push(`FAIL_CLOSED: launch_origin must be one of: ${[...VALID_LAUNCH_ORIGINS].join(", ")}.`);
  }

  // Required: target_surface
  if (record.target_surface !== "construction_application_os") {
    errors.push("FAIL_CLOSED: target_surface must be 'construction_application_os'.");
  }

  // Required: initial_view
  if (typeof record.initial_view !== "string" || !VALID_INITIAL_VIEWS.has(record.initial_view)) {
    errors.push(`FAIL_CLOSED: initial_view must be one of: ${[...VALID_INITIAL_VIEWS].join(", ")}.`);
  }

  // Enforced: observer_mode must be true
  if (record.observer_mode !== true) {
    errors.push("FAIL_CLOSED: observer_mode must be true. Construction OS must not enter elevated execution mode via Fabric handoff.");
  }

  // Required: branding_ref
  if (typeof record.branding_ref !== "string" || record.branding_ref.length === 0) {
    errors.push("FAIL_CLOSED: branding_ref must be a non-empty string.");
  }

  // Required: registry_ref
  if (typeof record.registry_ref !== "string" || !REGISTRY_REF_PATTERN.test(record.registry_ref)) {
    errors.push("FAIL_CLOSED: registry_ref must start with 'construction_os_registry::'.");
  }

  // Required: launch_route
  if (typeof record.launch_route !== "string" || !ROUTE_PATTERN.test(record.launch_route)) {
    errors.push("FAIL_CLOSED: launch_route must match '/[a-z0-9/_-]+'.");
  }

  // Required: return_route
  if (typeof record.return_route !== "string" || !ROUTE_PATTERN.test(record.return_route)) {
    errors.push("FAIL_CLOSED: return_route must match '/[a-z0-9/_-]+'.");
  }

  // Enforced: session_scope must be metadata_only
  if (record.session_scope !== "metadata_only") {
    errors.push("FAIL_CLOSED: session_scope must be 'metadata_only'.");
  }

  // Required: readiness_state
  if (typeof record.readiness_state !== "string" || !VALID_READINESS_STATES.has(record.readiness_state)) {
    errors.push(`FAIL_CLOSED: readiness_state must be one of: ${[...VALID_READINESS_STATES].join(", ")}.`);
  }

  // Enforced: standalone_valid must be true
  if (record.standalone_valid !== true) {
    errors.push("FAIL_CLOSED: standalone_valid must be true. Construction OS standalone validity is non-negotiable.");
  }

  // Required: created_from
  if (typeof record.created_from !== "string" || !VALID_CREATED_FROM.has(record.created_from)) {
    errors.push(`FAIL_CLOSED: created_from must be one of: ${[...VALID_CREATED_FROM].join(", ")}.`);
  }

  // Required: notes
  if (!Array.isArray(record.notes) || !record.notes.every((n: unknown) => typeof n === "string")) {
    errors.push("FAIL_CLOSED: notes must be an array of strings.");
  }

  return { valid: errors.length === 0, errors };
}
