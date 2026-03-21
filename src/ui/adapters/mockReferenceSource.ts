/**
 * Construction OS — Mock Reference Source Adapter
 * MOCK: Provides simulated reference/spec data for development.
 */

import type { ReferenceSourceAdapter, ReferenceEntry } from '../contracts/adapters';
import type { SourcedData } from '../contracts/events';

const MOCK_REFERENCES: Record<string, ReferenceEntry[]> = {
  'asm-001': [
    { id: 'ref-001', objectId: 'asm-001', type: 'spec', title: 'AISC 360-22 Section J3 — Bolted Connections', content: 'High-strength bolts shall conform to ASTM F3125...', sourceBasis: 'mock', sourceDocument: 'AISC 360-22' },
    { id: 'ref-002', objectId: 'asm-001', type: 'document', title: 'Assembly Drawing A1-SD-001', content: 'Shop drawing reference for Steel Assembly A1.', sourceBasis: 'mock', sourceDocument: 'Project Drawings' },
  ],
  'elem-001': [
    { id: 'ref-003', objectId: 'elem-001', type: 'spec', title: 'Column Design — ACI 318-19 Ch.10', content: 'Reinforced concrete columns shall be designed for combined axial and bending...', sourceBasis: 'mock', sourceDocument: 'ACI 318-19' },
    { id: 'ref-004', objectId: 'elem-001', type: 'citation', title: 'Structural Calc Report C-14', content: 'Column C-14 verified for 1.2D + 1.6L load combination.', sourceBasis: 'mock' },
  ],
  'spec-001': [
    { id: 'ref-005', objectId: 'spec-001', type: 'spec', title: 'Section 08 44 13 — Glazed Curtain Walls', content: 'Furnish and install unitized curtain wall system...', sourceBasis: 'mock', sourceDocument: 'Project Specifications' },
  ],
};

function sourced<T>(data: T): SourcedData<T> {
  return { data, basis: 'mock', sourceAdapter: 'mock-reference-source', timestamp: Date.now(), isMock: true };
}

export const mockReferenceSource: ReferenceSourceAdapter = {
  adapterName: 'mock-reference-source',
  isMock: true,

  async getReferences(objectId, type) {
    const refs = MOCK_REFERENCES[objectId] ?? [
      { id: `ref-gen-${objectId}`, objectId, type: 'document' as const, title: `Reference for ${objectId}`, content: 'No specific references found. Adapter seam ready for real integration.', sourceBasis: 'mock' as const },
    ];
    const filtered = type ? refs.filter((r) => r.type === type) : refs;
    return sourced(filtered);
  },

  async getCompareReferences(objectIdA, objectIdB) {
    const a = MOCK_REFERENCES[objectIdA] ?? [];
    const b = MOCK_REFERENCES[objectIdB] ?? [];
    return sourced({ a, b });
  },
};
