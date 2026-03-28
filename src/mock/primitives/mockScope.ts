/**
 * Construction OS — Deterministic Mock Scope
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface MockScope {
  id: string;
  name: string;
  version: string;
  status: 'CANONICAL' | 'DRAFT' | 'DEPRECATED';
  origin: string;
  purity: number;
  registrySource: string;
}

export const MOCK_SCOPE: MockScope[] = [
  {
    id: 'scope-001',
    name: 'Full Roof Replacement — Commercial',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Scope_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'scope-002',
    name: 'Roof Overlay — TPO over BUR',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Scope_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'scope-003',
    name: 'Repair — Flashing and Penetration',
    version: '0.9.0',
    status: 'DRAFT',
    origin: 'Construction_Scope_Kernel',
    purity: 0.87,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'scope-004',
    name: 'New Construction — Metal Roof',
    version: '0.8.0',
    status: 'DRAFT',
    origin: 'Construction_Scope_Kernel',
    purity: 0.75,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'scope-005',
    name: 'Maintenance — Coating Application',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Scope_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
];
