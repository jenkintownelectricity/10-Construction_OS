/**
 * Construction OS — Deterministic Mock Assemblies
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface MockAssembly {
  id: string;
  name: string;
  version: string;
  status: 'CANONICAL' | 'DRAFT' | 'DEPRECATED';
  origin: string;
  purity: number;
  registrySource: string;
}

export const MOCK_ASSEMBLIES: MockAssembly[] = [
  {
    id: 'asm-001',
    name: 'Modified Bitumen Roof Assembly',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Assembly_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'asm-002',
    name: 'TPO Single-Ply Membrane Assembly',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Assembly_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'asm-003',
    name: 'Standing Seam Metal Roof Assembly',
    version: '0.9.0',
    status: 'DRAFT',
    origin: 'Construction_Assembly_Kernel',
    purity: 0.85,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'asm-004',
    name: 'EPDM Ballasted Roof Assembly',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Assembly_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'asm-005',
    name: 'Built-Up Roof Assembly',
    version: '0.8.0',
    status: 'DRAFT',
    origin: 'Construction_Assembly_Kernel',
    purity: 0.72,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'asm-006',
    name: 'Vegetative Green Roof Assembly',
    version: '0.7.0',
    status: 'DEPRECATED',
    origin: 'Construction_Assembly_Kernel',
    purity: 0.65,
    registrySource: 'Construction_OS_Registry',
  },
];
