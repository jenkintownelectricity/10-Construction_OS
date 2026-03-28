/**
 * Construction OS — Deterministic Mock Specifications
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface MockSpecification {
  id: string;
  name: string;
  version: string;
  status: 'CANONICAL' | 'DRAFT' | 'DEPRECATED';
  origin: string;
  purity: number;
  registrySource: string;
}

export const MOCK_SPECIFICATIONS: MockSpecification[] = [
  {
    id: 'spec-001',
    name: 'ASTM D6162 — SBS Modified Bitumen',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Specification_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'spec-002',
    name: 'ASTM D6878 — TPO Membrane',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Specification_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'spec-003',
    name: 'ASTM C1289 — Polyisocyanurate Board',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Specification_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'spec-004',
    name: 'ASTM D4637 — EPDM Sheet',
    version: '0.9.0',
    status: 'DRAFT',
    origin: 'Construction_Specification_Kernel',
    purity: 0.91,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'spec-005',
    name: 'FM 4470 — Wind Uplift Resistance',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Specification_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'spec-006',
    name: 'UL 790 — Fire Resistance',
    version: '0.8.0',
    status: 'DRAFT',
    origin: 'Construction_Specification_Kernel',
    purity: 0.82,
    registrySource: 'Construction_OS_Registry',
  },
];
