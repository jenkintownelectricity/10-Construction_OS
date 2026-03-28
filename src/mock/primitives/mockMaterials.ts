/**
 * Construction OS — Deterministic Mock Materials
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface MockMaterial {
  id: string;
  name: string;
  version: string;
  status: 'CANONICAL' | 'DRAFT' | 'DEPRECATED';
  origin: string;
  purity: number;
  registrySource: string;
}

export const MOCK_MATERIALS: MockMaterial[] = [
  {
    id: 'mat-001',
    name: 'SBS Modified Bitumen Membrane',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Material_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'mat-002',
    name: 'TPO Thermoplastic Membrane',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Material_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'mat-003',
    name: 'Polyisocyanurate Insulation Board',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Material_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'mat-004',
    name: 'Glass Fiber Reinforcement',
    version: '0.9.0',
    status: 'DRAFT',
    origin: 'Construction_Material_Kernel',
    purity: 0.88,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'mat-005',
    name: 'EPDM Synthetic Rubber Membrane',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Material_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'mat-006',
    name: 'Aluminum Standing Seam Panel',
    version: '0.8.0',
    status: 'DRAFT',
    origin: 'Construction_Material_Kernel',
    purity: 0.78,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'mat-007',
    name: 'Vapor Retarder Film',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Material_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
];
