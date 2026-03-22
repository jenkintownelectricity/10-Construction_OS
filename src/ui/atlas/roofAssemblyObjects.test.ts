/**
 * Roof Assembly Objects — Tests
 *
 * Proves:
 *   - At least 3 static objects exist
 *   - All objects have assemblyType = "roofing"
 *   - All objects match locked schema shape
 *   - All objects use supported manufacturer/spec set
 *   - All objects use UI canvas rect geometry
 *   - Projection to sourceContext matches locked contract
 *   - Validation rejects malformed objects
 *   - Validation rejects non-roofing types
 *   - Validation rejects unsupported manufacturer/spec
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect } from 'vitest';
import {
  ROOF_ASSEMBLY_OBJECTS,
  BUILDINGS,
  LEVELS,
  validateRoofAssemblyObject,
  projectToSourceContext,
  type RoofAssemblyObject,
} from './roofAssemblyObjects';

describe('ROOF_ASSEMBLY_OBJECTS — static data', () => {
  it('has at least 3 static objects', () => {
    expect(ROOF_ASSEMBLY_OBJECTS.length).toBeGreaterThanOrEqual(3);
  });

  it('all objects have assemblyType = "roofing"', () => {
    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      expect(obj.assemblyType).toBe('roofing');
    }
  });

  it('all objects have non-empty required string fields', () => {
    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      expect(obj.objectId.trim().length).toBeGreaterThan(0);
      expect(obj.label.trim().length).toBeGreaterThan(0);
      expect(obj.areaName.trim().length).toBeGreaterThan(0);
      expect(obj.manufacturer.trim().length).toBeGreaterThan(0);
      expect(obj.spec.trim().length).toBeGreaterThan(0);
      expect(obj.project.trim().length).toBeGreaterThan(0);
    }
  });

  it('all objects have valid rect geometry', () => {
    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      expect(obj.geometry.kind).toBe('rect');
      expect(typeof obj.geometry.x).toBe('number');
      expect(typeof obj.geometry.y).toBe('number');
      expect(typeof obj.geometry.width).toBe('number');
      expect(typeof obj.geometry.height).toBe('number');
      expect(obj.geometry.width).toBeGreaterThan(0);
      expect(obj.geometry.height).toBeGreaterThan(0);
    }
  });

  it('all objects use supported manufacturer/spec combinations', () => {
    const supported = new Set([
      'Carlisle SynTec::07 52 16',
      'GAF::07 54 23',
      'Johns Manville::07 54 19',
      'Henry Company::07 52 13',
    ]);
    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      expect(supported.has(`${obj.manufacturer}::${obj.spec}`)).toBe(true);
    }
  });

  it('all objects have unique objectIds', () => {
    const ids = ROOF_ASSEMBLY_OBJECTS.map((o) => o.objectId);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe('validateRoofAssemblyObject', () => {
  it('accepts valid roof assembly objects', () => {
    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      const result = validateRoofAssemblyObject(obj);
      expect(result.valid).toBe(true);
    }
  });

  it('FAIL_CLOSED on null', () => {
    const result = validateRoofAssemblyObject(null);
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MALFORMED_OBJECT');
  });

  it('FAIL_CLOSED on missing objectId', () => {
    const result = validateRoofAssemblyObject({
      ...ROOF_ASSEMBLY_OBJECTS[0],
      objectId: '',
    });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MALFORMED_OBJECT');
  });

  it('FAIL_CLOSED on non-roofing assemblyType', () => {
    const result = validateRoofAssemblyObject({
      ...ROOF_ASSEMBLY_OBJECTS[0],
      assemblyType: 'fireproofing',
    });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('NON_ROOFING_TYPE');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
  });

  it('FAIL_CLOSED on malformed geometry', () => {
    const result = validateRoofAssemblyObject({
      ...ROOF_ASSEMBLY_OBJECTS[0],
      geometry: { kind: 'circle', cx: 0, cy: 0, r: 5 },
    });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MALFORMED_GEOMETRY');
  });

  it('FAIL_CLOSED on unsupported manufacturer/spec', () => {
    const result = validateRoofAssemblyObject({
      ...ROOF_ASSEMBLY_OBJECTS[0],
      manufacturer: 'Acme Corp',
      spec: '07 99 99',
    });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('UNSUPPORTED_MANUFACTURER_SPEC');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
  });
});

describe('projectToSourceContext', () => {
  it('projects to locked sourceContext schema', () => {
    const obj = ROOF_ASSEMBLY_OBJECTS[0];
    const ctx = projectToSourceContext(obj);
    expect(ctx).not.toBeNull();
    expect(ctx!.submittalId).toBe(obj.objectId);
    expect(ctx!.title).toBe(obj.areaName);
    expect(ctx!.manufacturer).toBe(obj.manufacturer);
    expect(ctx!.spec).toBe(obj.spec);
    expect(ctx!.project).toBe(obj.project);
  });

  it('projects all static objects successfully', () => {
    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      const ctx = projectToSourceContext(obj);
      expect(ctx).not.toBeNull();
      expect(Object.keys(ctx!).sort()).toEqual([
        'manufacturer', 'project', 'spec', 'submittalId', 'title',
      ]);
    }
  });

  it('returns null for invalid object', () => {
    const invalid = {
      ...ROOF_ASSEMBLY_OBJECTS[0],
      assemblyType: 'fireproofing',
    } as unknown as RoofAssemblyObject;
    const ctx = projectToSourceContext(invalid);
    expect(ctx).toBeNull();
  });
});

// ─── Building and Level metadata ─────────────────────────────────────

describe('BUILDINGS — static data', () => {
  it('has at least 1 building', () => {
    expect(BUILDINGS.length).toBeGreaterThanOrEqual(1);
  });

  it('all buildings have non-empty id and name', () => {
    for (const b of BUILDINGS) {
      expect(b.id.trim().length).toBeGreaterThan(0);
      expect(b.name.trim().length).toBeGreaterThan(0);
    }
  });

  it('all buildings have unique ids', () => {
    const ids = BUILDINGS.map((b) => b.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe('LEVELS — static data', () => {
  it('has at least 1 level', () => {
    expect(LEVELS.length).toBeGreaterThanOrEqual(1);
  });

  it('all levels have non-empty id, buildingId, and name', () => {
    for (const l of LEVELS) {
      expect(l.id.trim().length).toBeGreaterThan(0);
      expect(l.buildingId.trim().length).toBeGreaterThan(0);
      expect(l.name.trim().length).toBeGreaterThan(0);
    }
  });

  it('all levels reference a valid buildingId', () => {
    const buildingIds = new Set(BUILDINGS.map((b) => b.id));
    for (const l of LEVELS) {
      expect(buildingIds.has(l.buildingId)).toBe(true);
    }
  });

  it('all levels have unique ids', () => {
    const ids = LEVELS.map((l) => l.id);
    expect(new Set(ids).size).toBe(ids.length);
  });
});
