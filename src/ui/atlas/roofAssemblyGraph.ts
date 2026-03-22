/**
 * Assembly Relationship Graph — First Construction Intelligence Layer
 *
 * Bounded graph of relationships between Roof Assembly objects.
 * UI-layer only. NOT kernel truth. NOT Atlas schema. NOT persisted.
 *
 * Graph nodes reference existing assembly objects from roofAssemblyObjects.ts.
 * Graph edges define deterministic relationships between nodes.
 * All display metadata (label, manufacturer, spec) is derived from
 * roofAssemblyObjects.ts, not duplicated into graph nodes.
 *
 * Governance: VKGL04R — Ring 3 TOUCH-ALLOWED
 */

import {
  ROOF_ASSEMBLY_OBJECTS,
  type RoofAssemblyObject,
} from './roofAssemblyObjects';

// ─── Graph Node Schema (locked) ─────────────────────────────────────

export interface AssemblyGraphNode {
  readonly nodeId: string;
  readonly assemblyObjectId: string;
}

// ─── Graph Edge Schema (locked) ─────────────────────────────────────

export type RelationshipKind = 'adjacent' | 'up-slope' | 'down-slope' | 'service-linked';

export interface AssemblyGraphEdge {
  readonly edgeId: string;
  readonly fromNodeId: string;
  readonly toNodeId: string;
  readonly kind: RelationshipKind;
}

// ─── Validation ─────────────────────────────────────────────────────

export interface GraphValidationResult {
  readonly valid: boolean;
  readonly errorCode?: string;
  readonly errorMessage?: string;
}

const VALID_KINDS: ReadonlySet<string> = new Set([
  'adjacent',
  'up-slope',
  'down-slope',
  'service-linked',
]);

/**
 * Validate graph integrity.
 * FAIL_CLOSED on:
 *   - node referencing unknown assemblyObjectId
 *   - edge referencing unknown nodeId
 *   - edge with invalid relationship kind
 */
export function validateGraph(
  nodes: readonly AssemblyGraphNode[],
  edges: readonly AssemblyGraphEdge[],
): GraphValidationResult {
  const assemblyIds = new Set(ROOF_ASSEMBLY_OBJECTS.map((o) => o.objectId));
  const nodeIds = new Set(nodes.map((n) => n.nodeId));

  // Validate nodes reference existing assembly objects
  for (const node of nodes) {
    if (!assemblyIds.has(node.assemblyObjectId)) {
      return {
        valid: false,
        errorCode: 'UNKNOWN_ASSEMBLY_OBJECT',
        errorMessage: `FAIL_CLOSED: Graph node '${node.nodeId}' references unknown assemblyObjectId '${node.assemblyObjectId}'.`,
      };
    }
  }

  // Validate edges reference existing nodes and use valid kinds
  for (const edge of edges) {
    if (!nodeIds.has(edge.fromNodeId)) {
      return {
        valid: false,
        errorCode: 'UNKNOWN_NODE_REF',
        errorMessage: `FAIL_CLOSED: Edge '${edge.edgeId}' references unknown fromNodeId '${edge.fromNodeId}'.`,
      };
    }
    if (!nodeIds.has(edge.toNodeId)) {
      return {
        valid: false,
        errorCode: 'UNKNOWN_NODE_REF',
        errorMessage: `FAIL_CLOSED: Edge '${edge.edgeId}' references unknown toNodeId '${edge.toNodeId}'.`,
      };
    }
    if (!VALID_KINDS.has(edge.kind)) {
      return {
        valid: false,
        errorCode: 'INVALID_RELATIONSHIP_KIND',
        errorMessage: `FAIL_CLOSED: Edge '${edge.edgeId}' has invalid kind '${edge.kind}'. Valid: ${[...VALID_KINDS].join(', ')}.`,
      };
    }
  }

  return { valid: true };
}

// ─── Deterministic Inverse Relationship Table ────────────────────────

/**
 * Maps each relationship kind to its directional inverse.
 * Symmetric kinds map to themselves. Directional kinds swap.
 * Used at query time only — stored edges remain canonical.
 */
const INVERSE_KIND: Readonly<Record<RelationshipKind, RelationshipKind>> = {
  'adjacent': 'adjacent',
  'up-slope': 'down-slope',
  'down-slope': 'up-slope',
  'service-linked': 'service-linked',
};

/**
 * Get the inverse relationship kind for an incoming edge.
 * FAIL_CLOSED: returns null for unknown kinds.
 */
export function getInverseKind(kind: RelationshipKind): RelationshipKind | null {
  return INVERSE_KIND[kind] ?? null;
}

// ─── Related Assembly Query ─────────────────────────────────────────

export interface RelatedAssembly {
  readonly assemblyObject: RoofAssemblyObject;
  readonly relationshipKind: RelationshipKind;
  readonly edgeId: string;
}

/**
 * Get related assemblies for a given assembly object ID.
 *
 * Traverses edges bidirectionally with deterministic inverse inference:
 *   - Outgoing edges (fromNodeId matches): use stored kind
 *   - Incoming edges (toNodeId matches): use inverse kind from INVERSE_KIND table
 *
 * Returns empty array for unknown or unconnected objects.
 */
export function getRelatedAssemblies(assemblyObjectId: string): readonly RelatedAssembly[] {
  // Find the graph node for this assembly
  const node = GRAPH_NODES.find((n) => n.assemblyObjectId === assemblyObjectId);
  if (!node) return [];

  const related: RelatedAssembly[] = [];

  for (const edge of GRAPH_EDGES) {
    let neighborNodeId: string | null = null;
    let effectiveKind: RelationshipKind | null = null;

    if (edge.fromNodeId === node.nodeId) {
      // Outgoing edge: use stored kind
      neighborNodeId = edge.toNodeId;
      effectiveKind = edge.kind;
    } else if (edge.toNodeId === node.nodeId) {
      // Incoming edge: use inverse kind
      neighborNodeId = edge.fromNodeId;
      effectiveKind = getInverseKind(edge.kind);
    }

    if (neighborNodeId && effectiveKind) {
      const neighborNode = GRAPH_NODES.find((n) => n.nodeId === neighborNodeId);
      if (neighborNode) {
        const assemblyObj = ROOF_ASSEMBLY_OBJECTS.find(
          (o) => o.objectId === neighborNode.assemblyObjectId,
        );
        if (assemblyObj) {
          related.push({
            assemblyObject: assemblyObj,
            relationshipKind: effectiveKind,
            edgeId: edge.edgeId,
          });
        }
      }
    }
  }

  return related;
}

// ─── Static Graph Nodes ─────────────────────────────────────────────

export const GRAPH_NODES: readonly AssemblyGraphNode[] = [
  { nodeId: 'GN-001', assemblyObjectId: 'RA-001' },
  { nodeId: 'GN-002', assemblyObjectId: 'RA-002' },
  { nodeId: 'GN-003', assemblyObjectId: 'RA-003' },
  { nodeId: 'GN-004', assemblyObjectId: 'RA-004' },
];

// ─── Static Graph Edges ─────────────────────────────────────────────

export const GRAPH_EDGES: readonly AssemblyGraphEdge[] = [
  // Main Roof (RA-001) is adjacent to Mechanical Penthouse (RA-002)
  { edgeId: 'GE-001', fromNodeId: 'GN-001', toNodeId: 'GN-002', kind: 'adjacent' },
  // Main Roof (RA-001) drains down-slope to Podium Level (RA-003)
  { edgeId: 'GE-002', fromNodeId: 'GN-001', toNodeId: 'GN-003', kind: 'down-slope' },
  // Mechanical Penthouse (RA-002) is service-linked to Service Wing (RA-004)
  { edgeId: 'GE-003', fromNodeId: 'GN-002', toNodeId: 'GN-004', kind: 'service-linked' },
  // Service Wing (RA-004) is adjacent to Main Roof (RA-001)
  { edgeId: 'GE-004', fromNodeId: 'GN-004', toNodeId: 'GN-001', kind: 'adjacent' },
  // Podium Level (RA-003) receives up-slope flow from Service Wing (RA-004)
  { edgeId: 'GE-005', fromNodeId: 'GN-003', toNodeId: 'GN-004', kind: 'up-slope' },
];
