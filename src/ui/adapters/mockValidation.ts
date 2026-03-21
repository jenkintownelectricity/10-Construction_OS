/**
 * Construction OS — Mock Validation Adapter
 * MOCK: Provides simulated validation results for development.
 */

import type { ValidationAdapter, ValidationResult } from '../contracts/adapters';
import type { SourcedData, ValidationIssue } from '../contracts/events';

const MOCK_VALIDATION_RESULTS: Record<string, ValidationResult> = {
  'asm-001': {
    objectId: 'asm-001',
    status: 'passed',
    issues: [],
    validatedAt: Date.now() - 3600000,
    validationType: 'full',
  },
  'asm-002': {
    objectId: 'asm-002',
    status: 'failed',
    issues: [
      { id: 'vi-001', severity: 'error', message: 'Connection capacity insufficient for load case LC-3', rule: 'AISC-J3.6' },
      { id: 'vi-002', severity: 'warning', message: 'Bolt spacing below preferred minimum', rule: 'AISC-J3.3' },
    ],
    validatedAt: Date.now() - 1800000,
    validationType: 'structural',
  },
  'elem-001': {
    objectId: 'elem-001',
    status: 'passed',
    issues: [
      { id: 'vi-003', severity: 'info', message: 'Column utilization at 87% — review recommended', rule: 'ACI-318-10.3' },
    ],
    validatedAt: Date.now() - 7200000,
    validationType: 'domain',
  },
};

function sourced<T>(data: T): SourcedData<T> {
  return { data, basis: 'mock', sourceAdapter: 'mock-validation', timestamp: Date.now(), isMock: true };
}

export const mockValidation: ValidationAdapter = {
  adapterName: 'mock-validation',
  isMock: true,

  async validate(objectId, type) {
    // Simulate validation with a small delay
    await new Promise((r) => setTimeout(r, 100));
    const existing = MOCK_VALIDATION_RESULTS[objectId];
    if (existing) return sourced(existing);
    const result: ValidationResult = {
      objectId,
      status: 'passed',
      issues: [] as ValidationIssue[],
      validatedAt: Date.now(),
      validationType: type as ValidationResult['validationType'],
    };
    return sourced(result);
  },

  async getValidationStatus(objectId) {
    return sourced(MOCK_VALIDATION_RESULTS[objectId] ?? null);
  },
};
