/**
 * Construction OS — Deterministic Mock Signals
 * Wave C1 — All values frozen in source. No random generation.
 */

export type SignalType =
  | 'ASSEMBLY_CREATED'
  | 'DETAIL_RESOLVED'
  | 'MATERIAL_LINKED'
  | 'PATTERN_MATCHED'
  | 'CONDITION_DETECTED'
  | 'ARTIFACT_RENDERED';

export interface MockSignal {
  id: string;
  type: SignalType;
  source: string;
  target: string;
  timestamp: string;
  payload: string;
  severity: 'INFO' | 'WARNING' | 'CRITICAL';
}

export const MOCK_SIGNALS: MockSignal[] = [
  {
    id: 'sig-001',
    type: 'ASSEMBLY_CREATED',
    source: 'Construction_Assembly_Kernel',
    target: 'Construction_OS_Registry',
    timestamp: '2026-03-28T09:00:00.000Z',
    payload: 'Assembly asm-003 created as DRAFT',
    severity: 'INFO',
  },
  {
    id: 'sig-002',
    type: 'DETAIL_RESOLVED',
    source: 'Construction_Atlas',
    target: 'Construction_Runtime',
    timestamp: '2026-03-28T09:05:00.000Z',
    payload: 'Detail DTL-017 resolved for edge condition',
    severity: 'INFO',
  },
  {
    id: 'sig-003',
    type: 'MATERIAL_LINKED',
    source: 'Construction_Material_Kernel',
    target: 'Construction_Assembly_Kernel',
    timestamp: '2026-03-28T09:10:00.000Z',
    payload: 'Material mat-003 linked to Assembly asm-001',
    severity: 'INFO',
  },
  {
    id: 'sig-004',
    type: 'PATTERN_MATCHED',
    source: 'Construction_ALEXANDER_Engine',
    target: 'Construction_Runtime',
    timestamp: '2026-03-28T09:15:00.000Z',
    payload: 'Pattern pat-001 matched with confidence 0.95',
    severity: 'INFO',
  },
  {
    id: 'sig-005',
    type: 'CONDITION_DETECTED',
    source: 'Construction_Atlas',
    target: 'Construction_Runtime',
    timestamp: '2026-03-28T09:20:00.000Z',
    payload: 'Moisture condition detected at Zone B-4',
    severity: 'WARNING',
  },
  {
    id: 'sig-006',
    type: 'ARTIFACT_RENDERED',
    source: 'Construction_Runtime',
    target: 'Construction_OS_Registry',
    timestamp: '2026-03-28T09:25:00.000Z',
    payload: 'DXF artifact rendered for detail DTL-017',
    severity: 'INFO',
  },
  {
    id: 'sig-007',
    type: 'CONDITION_DETECTED',
    source: 'Construction_Chemistry_Kernel',
    target: 'Construction_Runtime',
    timestamp: '2026-03-28T09:30:00.000Z',
    payload: 'Chemical incompatibility warning: chem-005 degraded',
    severity: 'CRITICAL',
  },
  {
    id: 'sig-008',
    type: 'ASSEMBLY_CREATED',
    source: 'Construction_Assembly_Kernel',
    target: 'Construction_OS_Registry',
    timestamp: '2026-03-28T09:35:00.000Z',
    payload: 'Assembly asm-005 created as DRAFT',
    severity: 'INFO',
  },
];
