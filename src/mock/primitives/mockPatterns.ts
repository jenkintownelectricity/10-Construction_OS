/**
 * Construction OS — Deterministic Mock Patterns
 * Wave C1 — Pattern Language reference data. No random generation.
 */

export interface MockPattern {
  id: string;
  name: string;
  category: string;
  description: string;
  confidence: number;
  relatedPatterns: string[];
  x: number;
  y: number;
}

export const MOCK_PATTERNS: MockPattern[] = [
  {
    id: 'pat-001',
    name: 'Layered Membrane Defense',
    category: 'Assembly',
    description: 'Multi-layer membrane system providing redundant waterproofing protection through material diversity.',
    confidence: 0.95,
    relatedPatterns: ['pat-002', 'pat-003'],
    x: 200,
    y: 100,
  },
  {
    id: 'pat-002',
    name: 'Thermal Envelope Continuity',
    category: 'Performance',
    description: 'Unbroken insulation plane ensuring thermal performance across all assembly transitions.',
    confidence: 0.92,
    relatedPatterns: ['pat-001', 'pat-004'],
    x: 400,
    y: 100,
  },
  {
    id: 'pat-003',
    name: 'Drainage Plane Hierarchy',
    category: 'Water Management',
    description: 'Tiered drainage system directing water away from critical assembly junctions.',
    confidence: 0.88,
    relatedPatterns: ['pat-001', 'pat-005'],
    x: 200,
    y: 250,
  },
  {
    id: 'pat-004',
    name: 'Vapor Drive Mediation',
    category: 'Moisture',
    description: 'Strategic vapor retarder placement based on climate zone analysis and dew point calculation.',
    confidence: 0.90,
    relatedPatterns: ['pat-002'],
    x: 400,
    y: 250,
  },
  {
    id: 'pat-005',
    name: 'Edge Termination Protocol',
    category: 'Detail',
    description: 'Systematic approach to membrane termination at edges, ensuring wind uplift resistance.',
    confidence: 0.85,
    relatedPatterns: ['pat-003', 'pat-006'],
    x: 300,
    y: 400,
  },
  {
    id: 'pat-006',
    name: 'Penetration Seal Doctrine',
    category: 'Detail',
    description: 'Governed protocol for sealing around pipes, vents, and mechanical penetrations.',
    confidence: 0.87,
    relatedPatterns: ['pat-005'],
    x: 500,
    y: 400,
  },
];
