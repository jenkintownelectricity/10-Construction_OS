/**
 * Construction OS — Deterministic Mock Chemistry
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface MockChemistry {
  id: string;
  name: string;
  version: string;
  status: 'CANONICAL' | 'DRAFT' | 'DEPRECATED';
  origin: string;
  purity: number;
  registrySource: string;
}

export const MOCK_CHEMISTRY: MockChemistry[] = [
  {
    id: 'chem-001',
    name: 'Styrene-Butadiene-Styrene Polymer',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Chemistry_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'chem-002',
    name: 'Thermoplastic Olefin Compound',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Chemistry_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'chem-003',
    name: 'Polyisocyanurate Foam Chemistry',
    version: '1.0.0',
    status: 'CANONICAL',
    origin: 'Construction_Chemistry_Kernel',
    purity: 1.0,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'chem-004',
    name: 'Ethylene Propylene Diene Monomer',
    version: '0.9.0',
    status: 'DRAFT',
    origin: 'Construction_Chemistry_Kernel',
    purity: 0.90,
    registrySource: 'Construction_OS_Registry',
  },
  {
    id: 'chem-005',
    name: 'Asphalt Oxidation Compound',
    version: '0.7.0',
    status: 'DEPRECATED',
    origin: 'Construction_Chemistry_Kernel',
    purity: 0.60,
    registrySource: 'Construction_OS_Registry',
  },
];
