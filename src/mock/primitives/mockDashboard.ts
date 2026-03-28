/**
 * Construction OS — Deterministic Mock Dashboard Data
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface DashboardMetric {
  label: string;
  value: string | number;
  status: 'NOMINAL' | 'WARNING' | 'CRITICAL' | 'OFFLINE';
}

export const DASHBOARD_METRICS: DashboardMetric[] = [
  { label: 'Kernel Count', value: 6, status: 'NOMINAL' },
  { label: 'Assembly Count', value: 6, status: 'NOMINAL' },
  { label: 'Material Count', value: 7, status: 'NOMINAL' },
  { label: 'Specification Count', value: 6, status: 'NOMINAL' },
  { label: 'Active Signals', value: 8, status: 'NOMINAL' },
  { label: 'Recent Receipts', value: 8, status: 'NOMINAL' },
  { label: 'Runtime Status', value: 'ACTIVE', status: 'NOMINAL' },
  { label: 'Atlas Status', value: 'ACTIVE', status: 'NOMINAL' },
];

export interface GovernedOperation {
  id: string;
  operation: string;
  actor: string;
  timestamp: string;
  status: 'SUCCESS' | 'FAILED' | 'PENDING';
}

export const GOVERNED_OPERATIONS: GovernedOperation[] = [
  {
    id: 'gov-001',
    operation: 'Assembly asm-002 version sealed at v1.0.0',
    actor: 'governance',
    timestamp: '2026-03-26T10:00:00.000Z',
    status: 'SUCCESS',
  },
  {
    id: 'gov-002',
    operation: 'Assembly asm-006 deprecated',
    actor: 'system',
    timestamp: '2026-03-25T16:00:00.000Z',
    status: 'SUCCESS',
  },
  {
    id: 'gov-003',
    operation: 'Chemistry chem-005 deprecated',
    actor: 'system',
    timestamp: '2026-03-25T16:05:00.000Z',
    status: 'SUCCESS',
  },
  {
    id: 'gov-004',
    operation: 'Material mat-004 draft created',
    actor: 'architect',
    timestamp: '2026-03-22T09:15:00.000Z',
    status: 'SUCCESS',
  },
  {
    id: 'gov-005',
    operation: 'Pattern pat-001 evaluated — confidence 0.95',
    actor: 'Construction_ALEXANDER_Engine',
    timestamp: '2026-03-28T09:15:00.000Z',
    status: 'SUCCESS',
  },
];

export interface PrimitiveSummary {
  type: string;
  total: number;
  canonical: number;
  draft: number;
  deprecated: number;
}

export const PRIMITIVE_SUMMARY: PrimitiveSummary[] = [
  { type: 'Assemblies', total: 6, canonical: 3, draft: 2, deprecated: 1 },
  { type: 'Materials', total: 7, canonical: 5, draft: 2, deprecated: 0 },
  { type: 'Specifications', total: 6, canonical: 4, draft: 2, deprecated: 0 },
  { type: 'Chemistry', total: 5, canonical: 3, draft: 1, deprecated: 1 },
  { type: 'Scope', total: 5, canonical: 3, draft: 2, deprecated: 0 },
  { type: 'Patterns', total: 6, canonical: 6, draft: 0, deprecated: 0 },
];
