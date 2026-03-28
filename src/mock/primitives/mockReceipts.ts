/**
 * Construction OS — Deterministic Mock Receipts
 * Wave C1 — All values frozen in source. No random generation.
 */

export type ReceiptCategory = 'EXECUTION' | 'SIGNAL' | 'REGISTRY' | 'RUNTIME';

export interface MockReceipt {
  id: string;
  category: ReceiptCategory;
  operation: string;
  timestamp: string;
  actor: string;
  status: 'SUCCESS' | 'FAILED' | 'PENDING';
  primitiveRef: string;
  detail: string;
}

export const MOCK_RECEIPTS: MockReceipt[] = [
  {
    id: 'rcpt-001',
    category: 'EXECUTION',
    operation: 'ASSEMBLY_MINT',
    timestamp: '2026-03-15T08:00:00.000Z',
    actor: 'system',
    status: 'SUCCESS',
    primitiveRef: 'asm-001',
    detail: 'Modified Bitumen Roof Assembly minted as CANONICAL v1.0.0',
  },
  {
    id: 'rcpt-002',
    category: 'EXECUTION',
    operation: 'MATERIAL_MINT',
    timestamp: '2026-03-15T08:01:00.000Z',
    actor: 'system',
    status: 'SUCCESS',
    primitiveRef: 'mat-001',
    detail: 'SBS Modified Bitumen Membrane minted as CANONICAL v1.0.0',
  },
  {
    id: 'rcpt-003',
    category: 'SIGNAL',
    operation: 'SIGNAL_EMIT',
    timestamp: '2026-03-28T09:00:00.000Z',
    actor: 'Construction_Assembly_Kernel',
    status: 'SUCCESS',
    primitiveRef: 'sig-001',
    detail: 'ASSEMBLY_CREATED signal emitted for asm-003',
  },
  {
    id: 'rcpt-004',
    category: 'REGISTRY',
    operation: 'REGISTRY_WRITE',
    timestamp: '2026-03-26T10:00:00.000Z',
    actor: 'governance',
    status: 'SUCCESS',
    primitiveRef: 'reg-008',
    detail: 'Version sealed for asm-002 at v1.0.0',
  },
  {
    id: 'rcpt-005',
    category: 'RUNTIME',
    operation: 'RUNTIME_BOOT',
    timestamp: '2026-03-28T08:00:00.000Z',
    actor: 'system',
    status: 'SUCCESS',
    primitiveRef: 'rt-001',
    detail: 'Construction Runtime booted successfully',
  },
  {
    id: 'rcpt-006',
    category: 'EXECUTION',
    operation: 'PATTERN_EVALUATE',
    timestamp: '2026-03-28T09:15:00.000Z',
    actor: 'Construction_ALEXANDER_Engine',
    status: 'SUCCESS',
    primitiveRef: 'pat-001',
    detail: 'Pattern evaluation completed with confidence 0.95',
  },
  {
    id: 'rcpt-007',
    category: 'SIGNAL',
    operation: 'SIGNAL_EMIT',
    timestamp: '2026-03-28T09:30:00.000Z',
    actor: 'Construction_Chemistry_Kernel',
    status: 'SUCCESS',
    primitiveRef: 'sig-007',
    detail: 'CONDITION_DETECTED signal emitted — chemical incompatibility',
  },
  {
    id: 'rcpt-008',
    category: 'RUNTIME',
    operation: 'MODULE_HEARTBEAT',
    timestamp: '2026-03-28T10:00:00.000Z',
    actor: 'system',
    status: 'SUCCESS',
    primitiveRef: 'rt-003',
    detail: 'Cognitive Bus heartbeat — all channels nominal',
  },
];
