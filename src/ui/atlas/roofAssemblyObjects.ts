/**
 * Roof Assembly Objects — Bounded UI-layer object data
 *
 * Static Roof Assembly objects for the first construction map surface.
 * NOT kernel truth. NOT Atlas schema. NOT persisted. NOT cross-session.
 *
 * Each object:
 *   - Has assemblyType = "roofing" only
 *   - Projects deterministically into the locked sourceContext schema
 *   - Uses UI canvas pixel coordinates (origin top-left)
 *   - Uses manufacturer/spec from the locked supported set
 *
 * Building and Level metadata are UI-only spatial context.
 * They are NOT kernel truth, NOT Atlas schema, NOT persisted.
 *
 * Governance: VKGL04R — Ring 3 TOUCH-ALLOWED
 */

import type { GenerationSourceContext } from '../stores/generationStore';

// ─── Building (UI-only spatial metadata) ─────────────────────────────

export interface Building {
  readonly id: string;
  readonly name: string;
}

// ─── Level (UI-only spatial metadata) ────────────────────────────────

export interface Level {
  readonly id: string;
  readonly buildingId: string;
  readonly name: string;
}

// ─── Roof Assembly Object Schema (locked) ────────────────────────────

export interface RoofAssemblyGeometry {
  readonly kind: 'rect';
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
}

export interface RoofAssemblyObject {
  readonly objectId: string;
  readonly label: string;
  readonly assemblyType: 'roofing';
  readonly areaName: string;
  readonly manufacturer: string;
  readonly spec: string;
  readonly project: string;
  readonly geometry: RoofAssemblyGeometry;
}

// ─── Validation ──────────────────────────────────────────────────────

export interface RoofAssemblyValidationResult {
  readonly valid: boolean;
  readonly errorCode?: string;
  readonly errorMessage?: string;
}

const SUPPORTED_MANUFACTURER_SPECS: ReadonlySet<string> = new Set([
  'Carlisle SynTec::07 52 16',
  'GAF::07 54 23',
  'Johns Manville::07 54 19',
  'Henry Company::07 52 13',
]);

/**
 * Validate a Roof Assembly object shape and supported coverage.
 * FAIL_CLOSED on malformed or unsupported objects.
 */
export function validateRoofAssemblyObject(
  obj: unknown,
): RoofAssemblyValidationResult {
  if (!obj || typeof obj !== 'object') {
    return {
      valid: false,
      errorCode: 'MALFORMED_OBJECT',
      errorMessage: 'FAIL_CLOSED: Assembly object is null or not an object.',
    };
  }

  const o = obj as Record<string, unknown>;

  // Required string fields
  for (const field of ['objectId', 'label', 'assemblyType', 'areaName', 'manufacturer', 'spec', 'project']) {
    if (typeof o[field] !== 'string' || (o[field] as string).trim().length === 0) {
      return {
        valid: false,
        errorCode: 'MALFORMED_OBJECT',
        errorMessage: `FAIL_CLOSED: Assembly object field '${field}' is missing or empty.`,
      };
    }
  }

  // assemblyType must be "roofing"
  if (o.assemblyType !== 'roofing') {
    return {
      valid: false,
      errorCode: 'NON_ROOFING_TYPE',
      errorMessage: `FAIL_CLOSED: Assembly type '${o.assemblyType}' is not 'roofing'. Non-roofing objects are not supported.`,
    };
  }

  // Geometry check
  const geo = o.geometry as Record<string, unknown> | undefined;
  if (!geo || geo.kind !== 'rect' || typeof geo.x !== 'number' || typeof geo.y !== 'number' || typeof geo.width !== 'number' || typeof geo.height !== 'number') {
    return {
      valid: false,
      errorCode: 'MALFORMED_GEOMETRY',
      errorMessage: 'FAIL_CLOSED: Assembly object geometry is malformed. Expected { kind: "rect", x, y, width, height }.',
    };
  }

  // Supported manufacturer/spec check
  const mfrSpec = `${o.manufacturer}::${o.spec}`;
  if (!SUPPORTED_MANUFACTURER_SPECS.has(mfrSpec)) {
    return {
      valid: false,
      errorCode: 'UNSUPPORTED_MANUFACTURER_SPEC',
      errorMessage: `FAIL_CLOSED: Manufacturer/spec '${mfrSpec}' is not in the supported set: ${[...SUPPORTED_MANUFACTURER_SPECS].join(', ')}.`,
    };
  }

  return { valid: true };
}

// ─── Source Context Projection (locked) ──────────────────────────────

/**
 * Deterministic projection: RoofAssemblyObject → GenerationSourceContext.
 * Returns null if object is invalid.
 */
export function projectToSourceContext(
  obj: RoofAssemblyObject,
): GenerationSourceContext | null {
  const validation = validateRoofAssemblyObject(obj);
  if (!validation.valid) return null;

  return {
    submittalId: obj.objectId,
    title: obj.areaName,
    manufacturer: obj.manufacturer,
    spec: obj.spec,
    project: obj.project,
  };
}

// ─── Static Roof Assembly Objects (bounded local data) ───────────────

export const ROOF_ASSEMBLY_OBJECTS: readonly RoofAssemblyObject[] = [
  {
    objectId: 'RA-001',
    label: 'Main Roof Area A',
    assemblyType: 'roofing',
    areaName: 'Main Roof — Low-Slope Area A',
    manufacturer: 'Carlisle SynTec',
    spec: '07 52 16',
    project: 'Heritage Plaza',
    geometry: { kind: 'rect', x: 20, y: 30, width: 200, height: 120 },
  },
  {
    objectId: 'RA-002',
    label: 'Mechanical Penthouse',
    assemblyType: 'roofing',
    areaName: 'Mechanical Penthouse Roof',
    manufacturer: 'GAF',
    spec: '07 54 23',
    project: 'Heritage Plaza',
    geometry: { kind: 'rect', x: 240, y: 30, width: 140, height: 80 },
  },
  {
    objectId: 'RA-003',
    label: 'Podium Level Roof',
    assemblyType: 'roofing',
    areaName: 'Podium Level Roof — Plaza Deck',
    manufacturer: 'Johns Manville',
    spec: '07 54 19',
    project: 'Heritage Plaza',
    geometry: { kind: 'rect', x: 20, y: 170, width: 360, height: 90 },
  },
  {
    objectId: 'RA-004',
    label: 'Service Wing Roof',
    assemblyType: 'roofing',
    areaName: 'Service Wing — Modified Bitumen',
    manufacturer: 'Henry Company',
    spec: '07 52 13',
    project: 'Heritage Plaza',
    geometry: { kind: 'rect', x: 240, y: 125, width: 140, height: 30 },
  },
];

// ─── Static Building Data (UI-only) ─────────────────────────────────

export const BUILDINGS: readonly Building[] = [
  { id: 'BLD-001', name: 'Heritage Plaza' },
];

// ─── Static Level Data (UI-only) ────────────────────────────────────

export const LEVELS: readonly Level[] = [
  { id: 'LVL-ROOF', buildingId: 'BLD-001', name: 'Roof Level' },
];
