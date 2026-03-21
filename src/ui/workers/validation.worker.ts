/**
 * Construction OS — Validation Worker
 * Worker-backed seam for expensive validation computation off the main thread.
 * MOCK: Currently simulates validation. Real worker would run actual validation logic.
 */

interface ValidationWorkerRequest {
  type: 'validate';
  objectId: string;
  validationType: string;
  data?: unknown;
}

interface ValidationWorkerResponse {
  type: 'validation-result';
  objectId: string;
  status: 'passed' | 'failed' | 'error';
  issues: Array<{ id: string; severity: string; message: string; rule?: string }>;
  computeTimeMs: number;
}

self.onmessage = function (e: MessageEvent<ValidationWorkerRequest>) {
  const { objectId, validationType } = e.data;
  const start = performance.now();

  // Simulate expensive validation computation
  // In production, this would run actual structural/domain/geometry checks
  let result: ValidationWorkerResponse;

  // Simulate computation by doing actual work (not just setTimeout)
  let sum = 0;
  for (let i = 0; i < 100000; i++) {
    sum += Math.sqrt(i) * Math.sin(i);
  }

  const elapsed = performance.now() - start;

  // Mock result based on objectId patterns
  if (objectId.includes('asm-002')) {
    result = {
      type: 'validation-result',
      objectId,
      status: 'failed',
      issues: [
        { id: `w-vi-${Date.now()}`, severity: 'error', message: `[Worker] Connection capacity check failed for ${validationType}`, rule: 'AISC-J3.6' },
      ],
      computeTimeMs: elapsed,
    };
  } else {
    result = {
      type: 'validation-result',
      objectId,
      status: 'passed',
      issues: [],
      computeTimeMs: elapsed,
    };
  }

  self.postMessage(result);
};

export {};
