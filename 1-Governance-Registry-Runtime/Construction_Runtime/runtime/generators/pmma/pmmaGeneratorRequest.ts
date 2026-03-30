/**
 * PMMA Generator Input Contract — Fail-Closed Request Validation
 *
 * L0-CMD-BARRETT-PMMA-GEN-005
 * Wave 5 — Generator Input Contract
 *
 * Defines the input parameters for the PMMA detail generator.
 * All fields validate fail-closed: unknown or missing values are rejected.
 */

// ─── Enumerated Input Values ─────────────────────────────────────

export const VALID_SUBSTRATES = [
  'concrete',
  'plywood',
  'metal deck',
  'existing membrane',
  'masonry',
  'metal',
  'wood',
] as const;
export type Substrate = (typeof VALID_SUBSTRATES)[number];

export const VALID_WALL_TYPES = [
  'masonry',
  'metal stud',
  'concrete',
  'wood frame',
  'curtain wall',
  'none',
] as const;
export type WallType = (typeof VALID_WALL_TYPES)[number];

export const VALID_EXPOSURES = [
  'exposed',
  'covered',
  'semi-exposed',
  'buried',
] as const;
export type Exposure = (typeof VALID_EXPOSURES)[number];

export const VALID_REINFORCEMENTS = [
  'standard fleece',
  'heavy fleece',
  'dual fleece',
  'none',
] as const;
export type Reinforcement = (typeof VALID_REINFORCEMENTS)[number];

export const VALID_DRAIN_TYPES = [
  'interior drain',
  'scupper',
  'overflow drain',
  'gutter',
  'none',
] as const;
export type DrainType = (typeof VALID_DRAIN_TYPES)[number];

export const VALID_PENETRATION_TYPES = [
  'pipe',
  'conduit',
  'mechanical curb',
  'vent',
  'none',
] as const;
export type PenetrationType = (typeof VALID_PENETRATION_TYPES)[number];

export const VALID_CURB_TYPES = [
  'mechanical curb',
  'skylight curb',
  'raised curb',
  'none',
] as const;
export type CurbType = (typeof VALID_CURB_TYPES)[number];

export const VALID_JOINT_TYPES = [
  'expansion joint',
  'area divider',
  'control joint',
  'none',
] as const;
export type JointType = (typeof VALID_JOINT_TYPES)[number];

export const VALID_CANT_CONDITIONS = [
  'pre-formed cant',
  'field-built cant',
  'no cant',
] as const;
export type CantCondition = (typeof VALID_CANT_CONDITIONS)[number];

export const VALID_BRANDS = [
  'Barrett PMMA',
  'PUMA PROOF',
  'Generic PMMA',
  'HIPPA COAT',
] as const;
export type Brand = (typeof VALID_BRANDS)[number];

// ─── Dimensions ──────────────────────────────────────────────────

export interface GeneratorDimensions {
  readonly width_mm?: number;
  readonly height_mm?: number;
  readonly depth_mm?: number;
  readonly flashing_height_mm?: number;
}

// ─── Generator Request ───────────────────────────────────────────

export interface PMMAGeneratorRequest {
  readonly substrate: Substrate;
  readonly wall_type: WallType;
  readonly exposure: Exposure;
  readonly reinforcement: Reinforcement;
  readonly drain_type: DrainType;
  readonly penetration_type: PenetrationType;
  readonly curb_type: CurbType;
  readonly joint_type: JointType;
  readonly cant_condition: CantCondition;
  readonly dimensions: GeneratorDimensions;
  readonly brand: Brand;
}

// ─── Validation ──────────────────────────────────────────────────

export interface ValidationResult {
  readonly valid: boolean;
  readonly errors: readonly string[];
}

function includes<T>(arr: readonly T[], value: unknown): value is T {
  return (arr as readonly unknown[]).includes(value);
}

export function validateGeneratorRequest(input: Record<string, unknown>): ValidationResult {
  const errors: string[] = [];

  if (!includes(VALID_SUBSTRATES, input.substrate)) {
    errors.push(`Invalid substrate: "${String(input.substrate ?? '')}"`);
  }
  if (!includes(VALID_WALL_TYPES, input.wall_type)) {
    errors.push(`Invalid wall_type: "${String(input.wall_type ?? '')}"`);
  }
  if (!includes(VALID_EXPOSURES, input.exposure)) {
    errors.push(`Invalid exposure: "${String(input.exposure ?? '')}"`);
  }
  if (!includes(VALID_REINFORCEMENTS, input.reinforcement)) {
    errors.push(`Invalid reinforcement: "${String(input.reinforcement ?? '')}"`);
  }
  if (!includes(VALID_DRAIN_TYPES, input.drain_type)) {
    errors.push(`Invalid drain_type: "${String(input.drain_type ?? '')}"`);
  }
  if (!includes(VALID_PENETRATION_TYPES, input.penetration_type)) {
    errors.push(`Invalid penetration_type: "${String(input.penetration_type ?? '')}"`);
  }
  if (!includes(VALID_CURB_TYPES, input.curb_type)) {
    errors.push(`Invalid curb_type: "${String(input.curb_type ?? '')}"`);
  }
  if (!includes(VALID_JOINT_TYPES, input.joint_type)) {
    errors.push(`Invalid joint_type: "${String(input.joint_type ?? '')}"`);
  }
  if (!includes(VALID_CANT_CONDITIONS, input.cant_condition)) {
    errors.push(`Invalid cant_condition: "${String(input.cant_condition ?? '')}"`);
  }
  if (!includes(VALID_BRANDS, input.brand)) {
    errors.push(`Invalid brand: "${String(input.brand ?? '')}"`);
  }
  if (input.dimensions === null || input.dimensions === undefined || typeof input.dimensions !== 'object') {
    errors.push('dimensions must be an object');
  }

  return { valid: errors.length === 0, errors };
}
