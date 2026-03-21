/**
 * Construction OS — Mock Spatial Source Adapter
 * MOCK: Provides simulated spatial/plan data for development.
 */

import type { SpatialSourceAdapter, SpatialObject, SpatialZone } from '../contracts/adapters';
import type { SourcedData } from '../contracts/events';

const MOCK_ZONES: SpatialZone[] = [
  { id: 'zone-001', name: 'Zone A — Main Structure', bounds: { x: 0, y: 0, width: 400, height: 300 }, objects: ['asm-001', 'asm-002', 'elem-001', 'elem-002'] },
  { id: 'zone-002', name: 'Zone B — East Wing', bounds: { x: 400, y: 0, width: 300, height: 300 }, objects: ['asm-003', 'spec-001'] },
  { id: 'zone-003', name: 'Zone C — MEP Services', bounds: { x: 0, y: 300, width: 700, height: 200 }, objects: ['asm-004', 'elem-003'] },
];

const MOCK_SPATIAL_OBJECTS: SpatialObject[] = [
  { id: 'sp-001', objectId: 'asm-001', label: 'Steel Assembly A1', x: 50, y: 50, width: 80, height: 60, zoneId: 'zone-001', layer: 'structural' },
  { id: 'sp-002', objectId: 'asm-002', label: 'Steel Assembly A2', x: 180, y: 80, width: 80, height: 60, zoneId: 'zone-001', layer: 'structural' },
  { id: 'sp-003', objectId: 'elem-001', label: 'Column C-14', x: 100, y: 180, width: 30, height: 30, zoneId: 'zone-001', layer: 'structural' },
  { id: 'sp-004', objectId: 'elem-002', label: 'Beam B-22', x: 200, y: 200, width: 120, height: 20, zoneId: 'zone-001', layer: 'structural' },
  { id: 'sp-005', objectId: 'asm-003', label: 'Curtain Wall CW-1', x: 420, y: 40, width: 260, height: 200, zoneId: 'zone-002', layer: 'envelope' },
  { id: 'sp-006', objectId: 'asm-004', label: 'Duct Assembly DA-1', x: 100, y: 340, width: 200, height: 40, zoneId: 'zone-003', layer: 'mep' },
  { id: 'sp-007', objectId: 'elem-003', label: 'AHU Unit AH-01', x: 400, y: 350, width: 80, height: 80, zoneId: 'zone-003', layer: 'mep' },
];

function sourced<T>(data: T): SourcedData<T> {
  return { data, basis: 'mock', sourceAdapter: 'mock-spatial-source', timestamp: Date.now(), isMock: true };
}

export const mockSpatialSource: SpatialSourceAdapter = {
  adapterName: 'mock-spatial-source',
  isMock: true,

  async getSpatialObjects(zoneId) {
    const filtered = zoneId ? MOCK_SPATIAL_OBJECTS.filter((o) => o.zoneId === zoneId) : MOCK_SPATIAL_OBJECTS;
    return sourced(filtered);
  },

  async getZones() {
    return sourced(MOCK_ZONES);
  },

  async getObjectSpatialContext(objectId) {
    const obj = MOCK_SPATIAL_OBJECTS.find((o) => o.objectId === objectId);
    if (!obj) return sourced(null);
    const zone = MOCK_ZONES.find((z) => z.id === obj.zoneId);
    return sourced({ object: obj, zone });
  },
};
