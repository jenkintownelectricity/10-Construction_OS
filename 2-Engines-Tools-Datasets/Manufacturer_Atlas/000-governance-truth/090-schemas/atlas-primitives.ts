/**
 * Atlas Graph Primitives
 *
 * Canonical type authority for the Manufacturer Atlas.
 * These types define the foundational node and edge structures
 * used across the entire manufacturer knowledge graph.
 *
 * This module defines TYPES ONLY — no execution, no rendering.
 *
 * _lineage:
 *   origin_repo: 10-Construction_OS
 *   origin_path: 2-Engines-Tools-Datasets/Manufacturer_Atlas/graph/atlas-primitives.ts
 *   origin_commit: 05a909260769de38eebe839494e2b00c277fbdff
 *   recreated_by: manufacturer-domain-os-taxonomy-wave
 *   recreated_date: 2026-03-31
 */

/** Honesty status classification for every atlas node */
export type AtlasNodeStatus =
  | "grounded"
  | "derived"
  | "scaffold"
  | "deferred"
  | "unverified";

/** Governance tier for atlas edges */
export type GovernanceTier =
  | "manufacturer_published"
  | "code_required"
  | "industry_standard"
  | "derived_inference"
  | "scaffold";

/** Domain classification for atlas nodes */
export type AtlasDomain = "building_envelope";

/** Supported node classes in the manufacturer atlas */
export type AtlasNodeClass =
  | "manufacturer"
  | "system_family"
  | "system"
  | "condition"
  | "assembly"
  | "product"
  | "rule"
  | "detail";

/** Supported relationship types between atlas nodes */
export type AtlasRelationship =
  | "contains"
  | "supports"
  | "uses"
  | "governed_by"
  | "compatible_with"
  | "resolved_by"
  | "references"
  | "outputs";

/**
 * AtlasNode — A single node in the manufacturer knowledge graph.
 */
export interface AtlasNode {
  node_id: string;
  domain: AtlasDomain;
  class: AtlasNodeClass;
  label: string;
  status: AtlasNodeStatus;
  metadata: Record<string, unknown>;
}

/**
 * AtlasEdge — A directed relationship between two atlas nodes.
 */
export interface AtlasEdge {
  edge_id: string;
  from_node: string;
  to_node: string;
  relationship: AtlasRelationship;
  governance_tier: GovernanceTier;
}

/**
 * AtlasGraph — The complete manufacturer atlas graph.
 */
export interface AtlasGraph {
  nodes: AtlasNode[];
  edges: AtlasEdge[];
}
