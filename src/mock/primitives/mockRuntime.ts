/**
 * Construction OS — Deterministic Mock Runtime
 * Wave C1 — All values frozen in source. No random generation.
 */

export interface MockRuntimeModule {
  id: string;
  name: string;
  status: 'ACTIVE' | 'IDLE' | 'OFFLINE';
  version: string;
  lastHeartbeat: string;
  description: string;
}

export const MOCK_RUNTIME_MODULES: MockRuntimeModule[] = [
  {
    id: 'rt-001',
    name: 'Construction Runtime',
    status: 'ACTIVE',
    version: '1.0.0',
    lastHeartbeat: '2026-03-28T10:00:00.000Z',
    description: 'Core execution runtime for Construction OS operations.',
  },
  {
    id: 'rt-002',
    name: 'Alexander Engine',
    status: 'ACTIVE',
    version: '1.0.0',
    lastHeartbeat: '2026-03-28T10:00:00.000Z',
    description: 'Pattern language evaluation and matching engine.',
  },
  {
    id: 'rt-003',
    name: 'Cognitive Bus',
    status: 'ACTIVE',
    version: '0.9.0',
    lastHeartbeat: '2026-03-28T09:58:00.000Z',
    description: 'Inter-module communication and signal routing bus.',
  },
  {
    id: 'rt-004',
    name: 'Awareness Cache',
    status: 'IDLE',
    version: '0.8.0',
    lastHeartbeat: '2026-03-28T09:45:00.000Z',
    description: 'Contextual awareness and state caching layer.',
  },
  {
    id: 'rt-005',
    name: 'Workers',
    status: 'IDLE',
    version: '0.9.0',
    lastHeartbeat: '2026-03-28T09:50:00.000Z',
    description: 'Background task workers for async operations.',
  },
  {
    id: 'rt-006',
    name: 'Assistant',
    status: 'OFFLINE',
    version: '0.7.0',
    lastHeartbeat: '2026-03-28T08:00:00.000Z',
    description: 'AI-assisted construction intelligence module.',
  },
];
