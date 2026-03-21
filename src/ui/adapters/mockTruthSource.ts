/**
 * Construction OS — Mock Truth Source Adapter
 * MOCK: This adapter provides simulated project data for development.
 * It must be replaced with a real truth source adapter for production.
 */

import type { TruthSourceAdapter, ProjectNode } from '../contracts/adapters';
import type { ActiveObjectIdentity, SourcedData } from '../contracts/events';

const MOCK_PROJECT_TREE: ProjectNode = {
  id: 'proj-001',
  name: 'Highland Medical Center',
  type: 'project',
  children: [
    {
      id: 'zone-001',
      name: 'Zone A — Main Structure',
      type: 'zone',
      children: [
        { id: 'doc-001', name: 'Structural Specifications', type: 'document' },
        { id: 'asm-001', name: 'Steel Assembly A1', type: 'assembly' },
        { id: 'asm-002', name: 'Steel Assembly A2', type: 'assembly' },
        { id: 'elem-001', name: 'Column C-14', type: 'element' },
        { id: 'elem-002', name: 'Beam B-22', type: 'element' },
      ],
    },
    {
      id: 'zone-002',
      name: 'Zone B — East Wing',
      type: 'zone',
      children: [
        { id: 'doc-002', name: 'Curtain Wall Specifications', type: 'document' },
        { id: 'asm-003', name: 'Curtain Wall Panel CW-1', type: 'assembly' },
        { id: 'spec-001', name: 'Glazing Specification GL-100', type: 'specification' },
      ],
    },
    {
      id: 'zone-003',
      name: 'Zone C — MEP Services',
      type: 'zone',
      children: [
        { id: 'doc-003', name: 'HVAC Specifications', type: 'document' },
        { id: 'asm-004', name: 'Duct Assembly DA-1', type: 'assembly' },
        { id: 'elem-003', name: 'AHU Unit AH-01', type: 'element' },
      ],
    },
  ],
};

function flattenNodes(node: ProjectNode): ActiveObjectIdentity[] {
  const result: ActiveObjectIdentity[] = [{
    id: node.id,
    name: node.name,
    type: node.type as ActiveObjectIdentity['type'],
  }];
  if (node.children) {
    for (const child of node.children) {
      result.push(...flattenNodes(child));
    }
  }
  return result;
}

const ALL_OBJECTS = flattenNodes(MOCK_PROJECT_TREE);

function sourced<T>(data: T): SourcedData<T> {
  return {
    data,
    basis: 'mock',
    sourceAdapter: 'mock-truth-source',
    timestamp: Date.now(),
    isMock: true,
  };
}

export const mockTruthSource: TruthSourceAdapter = {
  adapterName: 'mock-truth-source',
  isMock: true,

  async getProjectTree() {
    return sourced(MOCK_PROJECT_TREE);
  },

  async getObject(id: string) {
    const found = ALL_OBJECTS.find((o) => o.id === id) ?? null;
    return sourced(found);
  },

  async searchObjects(query: string) {
    const q = query.toLowerCase();
    const results = ALL_OBJECTS.filter(
      (o) => o.name.toLowerCase().includes(q) || o.id.toLowerCase().includes(q)
    );
    return sourced(results);
  },
};
