/**
 * Construction OS — Deterministic Mock Truth Spine
 * Wave C1 — Fixed node positions, deterministic edges. No force-directed layout.
 */

export interface TruthSpineNode {
  id: string;
  name: string;
  type: 'KERNEL' | 'RUNTIME' | 'REGISTRY' | 'ENGINE' | 'ATLAS';
  status: 'ACTIVE' | 'IDLE' | 'OFFLINE';
  x: number;
  y: number;
  description: string;
}

export interface TruthSpineEdge {
  id: string;
  source: string;
  target: string;
  relationship: string;
}

export const TRUTH_SPINE_NODES: TruthSpineNode[] = [
  {
    id: 'node-kernel',
    name: 'Construction Kernel',
    type: 'KERNEL',
    status: 'ACTIVE',
    x: 400,
    y: 80,
    description: 'Core truth authority. Defines all construction primitives and governance rules.',
  },
  {
    id: 'node-assembly',
    name: 'Assembly Kernel',
    type: 'KERNEL',
    status: 'ACTIVE',
    x: 160,
    y: 220,
    description: 'Governs construction assembly composition, layering, and structural integrity.',
  },
  {
    id: 'node-material',
    name: 'Material Kernel',
    type: 'KERNEL',
    status: 'ACTIVE',
    x: 340,
    y: 220,
    description: 'Material truth authority. Tracks material properties, chemistry, and compatibility.',
  },
  {
    id: 'node-specification',
    name: 'Specification Kernel',
    type: 'KERNEL',
    status: 'ACTIVE',
    x: 520,
    y: 220,
    description: 'Specification governance. ASTM, FM, UL standards enforcement.',
  },
  {
    id: 'node-chemistry',
    name: 'Chemistry Kernel',
    type: 'KERNEL',
    status: 'ACTIVE',
    x: 160,
    y: 360,
    description: 'Chemical composition and compatibility analysis engine.',
  },
  {
    id: 'node-scope',
    name: 'Scope Kernel',
    type: 'KERNEL',
    status: 'ACTIVE',
    x: 340,
    y: 360,
    description: 'Project scope definition and boundary governance.',
  },
  {
    id: 'node-runtime',
    name: 'Construction Runtime',
    type: 'RUNTIME',
    status: 'ACTIVE',
    x: 640,
    y: 300,
    description: 'Core execution runtime. Orchestrates all kernel operations.',
  },
  {
    id: 'node-registry',
    name: 'Construction Registry',
    type: 'REGISTRY',
    status: 'ACTIVE',
    x: 640,
    y: 140,
    description: 'Immutable ledger for all primitive registrations and state transitions.',
  },
  {
    id: 'node-atlas',
    name: 'Construction Atlas',
    type: 'ATLAS',
    status: 'ACTIVE',
    x: 520,
    y: 360,
    description: 'Spatial intelligence surface for building context and detail resolution.',
  },
  {
    id: 'node-alexander',
    name: 'Alexander Engine',
    type: 'ENGINE',
    status: 'ACTIVE',
    x: 400,
    y: 480,
    description: 'Pattern language evaluation engine. Drives construction intelligence.',
  },
];

export const TRUTH_SPINE_EDGES: TruthSpineEdge[] = [
  { id: 'edge-001', source: 'node-kernel', target: 'node-assembly', relationship: 'GOVERNS' },
  { id: 'edge-002', source: 'node-kernel', target: 'node-material', relationship: 'GOVERNS' },
  { id: 'edge-003', source: 'node-kernel', target: 'node-specification', relationship: 'GOVERNS' },
  { id: 'edge-004', source: 'node-kernel', target: 'node-registry', relationship: 'REGISTERS_TO' },
  { id: 'edge-005', source: 'node-assembly', target: 'node-material', relationship: 'CONSUMES' },
  { id: 'edge-006', source: 'node-assembly', target: 'node-specification', relationship: 'VALIDATED_BY' },
  { id: 'edge-007', source: 'node-material', target: 'node-chemistry', relationship: 'COMPOSED_OF' },
  { id: 'edge-008', source: 'node-chemistry', target: 'node-specification', relationship: 'CONSTRAINED_BY' },
  { id: 'edge-009', source: 'node-scope', target: 'node-assembly', relationship: 'SCOPES' },
  { id: 'edge-010', source: 'node-runtime', target: 'node-kernel', relationship: 'EXECUTES' },
  { id: 'edge-011', source: 'node-runtime', target: 'node-registry', relationship: 'WRITES_TO' },
  { id: 'edge-012', source: 'node-atlas', target: 'node-assembly', relationship: 'SPATIALIZES' },
  { id: 'edge-013', source: 'node-atlas', target: 'node-runtime', relationship: 'QUERIES' },
  { id: 'edge-014', source: 'node-alexander', target: 'node-assembly', relationship: 'EVALUATES' },
  { id: 'edge-015', source: 'node-alexander', target: 'node-runtime', relationship: 'ADVISES' },
];
