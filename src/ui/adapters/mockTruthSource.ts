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
        {
          id: 'asm-001',
          name: 'Main Roof Assembly R-1',
          type: 'assembly',
          metadata: {
            category: 'roofing',
            layers: {
              assembly_roof_area: 'Main Roof',
              manufacturer: 'Carlisle',
              system: 'TPO',
              membrane_1: '60-mil Sure-Weld TPO membrane',
              membrane_1_attachment: 'adhered with Sure-Weld Low-VOC Bonding Adhesive',
              coverboard_1: 'DensDeck Prime: 1/2"',
              coverboard_1_attachment: 'adhered with Flexible FAST Adhesive',
              insulation_layer_1: '2.6" thick InsulBase Polyisocyanurate insulation',
              insulation_layer_1_attachment: 'adhered with Flexible FAST Adhesive',
              insulation_layer_2: '2.6" thick Tapered InsulBase Polyisocyanurate insulation',
              insulation_layer_2_attachment: 'adhered with Flexible FAST Adhesive',
              vapor_barrier: 'VapAir Seal SA self-adhered vapor barrier',
              vapor_barrier_attachment: 'self-adhered',
              deck_slope: 'Existing Concrete deck',
              deck_slope_attachment: 'structural',
            },
            project: {
              name: 'Highland Medical Center',
              location: 'Baltimore, MD',
            },
          },
        },
        {
          id: 'asm-002',
          name: 'Penthouse Roof Assembly R-2',
          type: 'assembly',
          metadata: {
            category: 'roofing',
            layers: {
              assembly_roof_area: 'Penthouse Roof',
              manufacturer: 'Carlisle',
              system: 'TPO',
              membrane_1: '80-mil Sure-Weld TPO membrane',
              membrane_1_attachment: 'mechanically fastened at 12" on center',
              coverboard_1: 'DensDeck Prime: 5/8"',
              coverboard_1_attachment: 'mechanically fastened',
              insulation_layer_1: '3.0" thick InsulBase Polyisocyanurate insulation',
              insulation_layer_1_attachment: 'mechanically fastened',
              deck_slope: 'Steel deck 22 gauge',
              deck_slope_attachment: 'structural',
            },
            project: {
              name: 'Highland Medical Center',
              location: 'Baltimore, MD',
            },
          },
        },
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
      name: 'Zone C — Fireproofing',
      type: 'zone',
      children: [
        { id: 'doc-003', name: 'Fireproofing Specifications', type: 'document' },
        {
          id: 'asm-004',
          name: 'Structural Fireproofing FP-1',
          type: 'assembly',
          metadata: {
            category: 'fireproofing',
            layers: {
              assembly_roof_area: 'Steel Column Fireproofing',
              manufacturer: 'Isolatek',
              system: 'Spray-applied',
              membrane_1: 'CAFCO 300 spray-applied fireproofing',
              deck_slope: 'W14x90 Steel Column',
            },
            project: {
              name: 'Highland Medical Center',
              location: 'Baltimore, MD',
            },
          },
        },
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
