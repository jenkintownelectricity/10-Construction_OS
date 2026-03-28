/**
 * Construction OS — Deterministic Mock Registry
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface MockRegistryEntry {
  id: string;
  primitiveId: string;
  primitiveType: string;
  action: string;
  timestamp: string;
  actor: string;
  version: string;
}

export const MOCK_REGISTRY_ENTRIES: MockRegistryEntry[] = [
  {
    id: 'reg-001',
    primitiveId: 'asm-001',
    primitiveType: 'Assembly',
    action: 'REGISTERED',
    timestamp: '2026-03-15T08:00:00.000Z',
    actor: 'system',
    version: '1.0.0',
  },
  {
    id: 'reg-002',
    primitiveId: 'mat-001',
    primitiveType: 'Material',
    action: 'REGISTERED',
    timestamp: '2026-03-15T08:01:00.000Z',
    actor: 'system',
    version: '1.0.0',
  },
  {
    id: 'reg-003',
    primitiveId: 'spec-001',
    primitiveType: 'Specification',
    action: 'REGISTERED',
    timestamp: '2026-03-15T08:02:00.000Z',
    actor: 'system',
    version: '1.0.0',
  },
  {
    id: 'reg-004',
    primitiveId: 'asm-003',
    primitiveType: 'Assembly',
    action: 'DRAFT_CREATED',
    timestamp: '2026-03-20T14:30:00.000Z',
    actor: 'architect',
    version: '0.9.0',
  },
  {
    id: 'reg-005',
    primitiveId: 'mat-004',
    primitiveType: 'Material',
    action: 'DRAFT_CREATED',
    timestamp: '2026-03-22T09:15:00.000Z',
    actor: 'architect',
    version: '0.9.0',
  },
  {
    id: 'reg-006',
    primitiveId: 'asm-006',
    primitiveType: 'Assembly',
    action: 'DEPRECATED',
    timestamp: '2026-03-25T16:00:00.000Z',
    actor: 'system',
    version: '0.7.0',
  },
  {
    id: 'reg-007',
    primitiveId: 'chem-005',
    primitiveType: 'Chemistry',
    action: 'DEPRECATED',
    timestamp: '2026-03-25T16:05:00.000Z',
    actor: 'system',
    version: '0.7.0',
  },
  {
    id: 'reg-008',
    primitiveId: 'asm-002',
    primitiveType: 'Assembly',
    action: 'VERSION_SEALED',
    timestamp: '2026-03-26T10:00:00.000Z',
    actor: 'governance',
    version: '1.0.0',
  },
];

export interface MockRegistryHealth {
  totalEntries: number;
  canonical: number;
  draft: number;
  deprecated: number;
  lastSyncTimestamp: string;
  integrityStatus: 'HEALTHY' | 'DEGRADED' | 'OFFLINE';
}

export const MOCK_REGISTRY_HEALTH: MockRegistryHealth = {
  totalEntries: 29,
  canonical: 18,
  draft: 8,
  deprecated: 3,
  lastSyncTimestamp: '2026-03-28T10:00:00.000Z',
  integrityStatus: 'HEALTHY',
};
