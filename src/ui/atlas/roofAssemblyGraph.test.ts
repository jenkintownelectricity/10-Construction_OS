/**
 * Assembly Relationship Graph — Tests
 *
 * Proves:
 *   - At least 4 graph nodes exist
 *   - At least 4 graph edges exist
 *   - All nodes reference existing assembly objects
 *   - All edges reference existing nodes
 *   - All edge kinds are valid
 *   - Graph validates successfully
 *   - getRelatedAssemblies returns correct neighbors
 *   - getRelatedAssemblies returns empty for unknown ID
 *   - Validation rejects unknown assembly references
 *   - Validation rejects unknown node references
 *   - Validation rejects invalid relationship kinds
 *   - No data duplication from roofAssemblyObjects
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect } from 'vitest';
import {
  GRAPH_NODES,
  GRAPH_EDGES,
  validateGraph,
  getRelatedAssemblies,
  getInverseKind,
  type AssemblyGraphNode,
  type AssemblyGraphEdge,
} from './roofAssemblyGraph';
import { ROOF_ASSEMBLY_OBJECTS } from './roofAssemblyObjects';

describe('GRAPH_NODES — static data', () => {
  it('has at least 4 graph nodes', () => {
    expect(GRAPH_NODES.length).toBeGreaterThanOrEqual(4);
  });

  it('all nodes have non-empty nodeId and assemblyObjectId', () => {
    for (const node of GRAPH_NODES) {
      expect(node.nodeId.trim().length).toBeGreaterThan(0);
      expect(node.assemblyObjectId.trim().length).toBeGreaterThan(0);
    }
  });

  it('all nodes have unique nodeIds', () => {
    const ids = GRAPH_NODES.map((n) => n.nodeId);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('all nodes reference existing assembly objects', () => {
    const assemblyIds = new Set(ROOF_ASSEMBLY_OBJECTS.map((o) => o.objectId));
    for (const node of GRAPH_NODES) {
      expect(assemblyIds.has(node.assemblyObjectId)).toBe(true);
    }
  });

  it('nodes do NOT duplicate label, manufacturer, or spec from assembly objects', () => {
    for (const node of GRAPH_NODES) {
      const n = node as Record<string, unknown>;
      expect(n).not.toHaveProperty('label');
      expect(n).not.toHaveProperty('manufacturer');
      expect(n).not.toHaveProperty('spec');
      expect(n).not.toHaveProperty('areaName');
    }
  });
});

describe('GRAPH_EDGES — static data', () => {
  it('has at least 4 graph edges', () => {
    expect(GRAPH_EDGES.length).toBeGreaterThanOrEqual(4);
  });

  it('all edges have non-empty edgeId, fromNodeId, toNodeId', () => {
    for (const edge of GRAPH_EDGES) {
      expect(edge.edgeId.trim().length).toBeGreaterThan(0);
      expect(edge.fromNodeId.trim().length).toBeGreaterThan(0);
      expect(edge.toNodeId.trim().length).toBeGreaterThan(0);
    }
  });

  it('all edges have unique edgeIds', () => {
    const ids = GRAPH_EDGES.map((e) => e.edgeId);
    expect(new Set(ids).size).toBe(ids.length);
  });

  it('all edges reference existing graph nodes', () => {
    const nodeIds = new Set(GRAPH_NODES.map((n) => n.nodeId));
    for (const edge of GRAPH_EDGES) {
      expect(nodeIds.has(edge.fromNodeId)).toBe(true);
      expect(nodeIds.has(edge.toNodeId)).toBe(true);
    }
  });

  it('all edge kinds are in the locked set', () => {
    const validKinds = new Set(['adjacent', 'up-slope', 'down-slope', 'service-linked']);
    for (const edge of GRAPH_EDGES) {
      expect(validKinds.has(edge.kind)).toBe(true);
    }
  });
});

describe('validateGraph', () => {
  it('validates the static graph successfully', () => {
    const result = validateGraph(GRAPH_NODES, GRAPH_EDGES);
    expect(result.valid).toBe(true);
  });

  it('FAIL_CLOSED on node referencing unknown assembly object', () => {
    const badNodes: AssemblyGraphNode[] = [
      ...GRAPH_NODES,
      { nodeId: 'GN-BAD', assemblyObjectId: 'RA-NONEXISTENT' },
    ];
    const result = validateGraph(badNodes, GRAPH_EDGES);
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('UNKNOWN_ASSEMBLY_OBJECT');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
  });

  it('FAIL_CLOSED on edge referencing unknown fromNodeId', () => {
    const badEdges: AssemblyGraphEdge[] = [
      ...GRAPH_EDGES,
      { edgeId: 'GE-BAD', fromNodeId: 'GN-NONEXISTENT', toNodeId: 'GN-001', kind: 'adjacent' },
    ];
    const result = validateGraph(GRAPH_NODES, badEdges);
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('UNKNOWN_NODE_REF');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
  });

  it('FAIL_CLOSED on edge referencing unknown toNodeId', () => {
    const badEdges: AssemblyGraphEdge[] = [
      ...GRAPH_EDGES,
      { edgeId: 'GE-BAD', fromNodeId: 'GN-001', toNodeId: 'GN-NONEXISTENT', kind: 'adjacent' },
    ];
    const result = validateGraph(GRAPH_NODES, badEdges);
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('UNKNOWN_NODE_REF');
  });

  it('FAIL_CLOSED on edge with invalid relationship kind', () => {
    const badEdges: AssemblyGraphEdge[] = [
      ...GRAPH_EDGES,
      { edgeId: 'GE-BAD', fromNodeId: 'GN-001', toNodeId: 'GN-002', kind: 'unknown-kind' as never },
    ];
    const result = validateGraph(GRAPH_NODES, badEdges);
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('INVALID_RELATIONSHIP_KIND');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
  });
});

describe('getRelatedAssemblies', () => {
  it('returns related assemblies for RA-001 (Main Roof)', () => {
    const related = getRelatedAssemblies('RA-001');
    expect(related.length).toBeGreaterThanOrEqual(2);
    const relatedIds = related.map((r) => r.assemblyObject.objectId);
    expect(relatedIds).toContain('RA-002'); // adjacent
    expect(relatedIds).toContain('RA-003'); // down-slope
  });

  it('returns related assemblies for RA-002 (Mech Penthouse)', () => {
    const related = getRelatedAssemblies('RA-002');
    expect(related.length).toBeGreaterThanOrEqual(2);
    const relatedIds = related.map((r) => r.assemblyObject.objectId);
    expect(relatedIds).toContain('RA-001'); // adjacent (reverse)
    expect(relatedIds).toContain('RA-004'); // service-linked
  });

  it('returns related assemblies for RA-004 (Service Wing)', () => {
    const related = getRelatedAssemblies('RA-004');
    expect(related.length).toBeGreaterThanOrEqual(2);
    const relatedIds = related.map((r) => r.assemblyObject.objectId);
    expect(relatedIds).toContain('RA-002'); // service-linked (reverse)
    expect(relatedIds).toContain('RA-001'); // adjacent
  });

  it('returns empty array for unknown assembly ID', () => {
    const related = getRelatedAssemblies('RA-NONEXISTENT');
    expect(related).toEqual([]);
  });

  it('each related assembly has assemblyObject, relationshipKind, and edgeId', () => {
    const related = getRelatedAssemblies('RA-001');
    for (const rel of related) {
      expect(rel.assemblyObject).toBeDefined();
      expect(rel.assemblyObject.objectId).toBeTruthy();
      expect(rel.relationshipKind).toBeTruthy();
      expect(rel.edgeId).toBeTruthy();
    }
  });

  it('related assemblies derive data from roofAssemblyObjects, not graph nodes', () => {
    const related = getRelatedAssemblies('RA-001');
    for (const rel of related) {
      expect(rel.assemblyObject.label).toBeTruthy();
      expect(rel.assemblyObject.manufacturer).toBeTruthy();
      expect(rel.assemblyObject.spec).toBeTruthy();
      expect(rel.assemblyObject.assemblyType).toBe('roofing');
    }
  });
});

// ─── Inverse Relationship Inference ──────────────────────────────────

describe('getInverseKind — deterministic inverse table', () => {
  it('adjacent → adjacent (symmetric)', () => {
    expect(getInverseKind('adjacent')).toBe('adjacent');
  });

  it('up-slope → down-slope', () => {
    expect(getInverseKind('up-slope')).toBe('down-slope');
  });

  it('down-slope → up-slope', () => {
    expect(getInverseKind('down-slope')).toBe('up-slope');
  });

  it('service-linked → service-linked (symmetric)', () => {
    expect(getInverseKind('service-linked')).toBe('service-linked');
  });

  it('returns null for unknown kind', () => {
    expect(getInverseKind('unknown' as never)).toBeNull();
  });
});

describe('getRelatedAssemblies — inverse inference', () => {
  it('down-slope stored edge returns up-slope when queried from target', () => {
    // GE-002: GN-001 (RA-001) → down-slope → GN-003 (RA-003)
    // Querying RA-003 should show RA-001 as up-slope
    const related = getRelatedAssemblies('RA-003');
    const fromMainRoof = related.find((r) => r.assemblyObject.objectId === 'RA-001');
    expect(fromMainRoof).toBeDefined();
    expect(fromMainRoof!.relationshipKind).toBe('up-slope');
    expect(fromMainRoof!.edgeId).toBe('GE-002');
  });

  it('up-slope stored edge returns down-slope when queried from target', () => {
    // GE-005: GN-003 (RA-003) → up-slope → GN-004 (RA-004)
    // Querying RA-004 should show RA-003 as down-slope
    const related = getRelatedAssemblies('RA-004');
    const fromPodium = related.find((r) => r.assemblyObject.objectId === 'RA-003');
    expect(fromPodium).toBeDefined();
    expect(fromPodium!.relationshipKind).toBe('down-slope');
    expect(fromPodium!.edgeId).toBe('GE-005');
  });

  it('adjacent stored edge remains adjacent when queried from target (symmetric)', () => {
    // GE-001: GN-001 (RA-001) → adjacent → GN-002 (RA-002)
    // Querying RA-002 should show RA-001 as adjacent
    const related = getRelatedAssemblies('RA-002');
    const fromMainRoof = related.find((r) => r.assemblyObject.objectId === 'RA-001');
    expect(fromMainRoof).toBeDefined();
    expect(fromMainRoof!.relationshipKind).toBe('adjacent');
  });

  it('service-linked stored edge remains service-linked when queried from target (symmetric)', () => {
    // GE-003: GN-002 (RA-002) → service-linked → GN-004 (RA-004)
    // Querying RA-004 should show RA-002 as service-linked
    const related = getRelatedAssemblies('RA-004');
    const fromMech = related.find((r) => r.assemblyObject.objectId === 'RA-002');
    expect(fromMech).toBeDefined();
    expect(fromMech!.relationshipKind).toBe('service-linked');
  });

  it('outgoing edges still use stored kind (not inverted)', () => {
    // GE-002: GN-001 (RA-001) → down-slope → GN-003 (RA-003)
    // Querying RA-001 should show RA-003 as down-slope (stored, not inverted)
    const related = getRelatedAssemblies('RA-001');
    const toPodium = related.find((r) => r.assemblyObject.objectId === 'RA-003');
    expect(toPodium).toBeDefined();
    expect(toPodium!.relationshipKind).toBe('down-slope');
  });

  it('no duplicate reverse edges exist in stored graph data', () => {
    // Verify that the stored GRAPH_EDGES count hasn't changed (still 5)
    expect(GRAPH_EDGES.length).toBe(5);
  });
});
