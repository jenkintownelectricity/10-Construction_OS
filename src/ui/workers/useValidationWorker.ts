/**
 * Construction OS — Validation Worker Hook
 * React hook for off-main-thread validation via Web Worker.
 */

import { useCallback, useEffect, useRef, useState } from 'react';

interface WorkerValidationResult {
  objectId: string;
  status: 'passed' | 'failed' | 'error';
  issues: Array<{ id: string; severity: string; message: string; rule?: string }>;
  computeTimeMs: number;
}

export function useValidationWorker() {
  const workerRef = useRef<Worker | null>(null);
  const [result, setResult] = useState<WorkerValidationResult | null>(null);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    workerRef.current = new Worker(
      new URL('./validation.worker.ts', import.meta.url),
      { type: 'module' }
    );

    workerRef.current.onmessage = (e: MessageEvent<WorkerValidationResult>) => {
      setResult(e.data);
      setIsRunning(false);
    };

    workerRef.current.onerror = (err) => {
      console.error('[ValidationWorker] Error:', err);
      setIsRunning(false);
    };

    return () => {
      workerRef.current?.terminate();
    };
  }, []);

  const validate = useCallback((objectId: string, validationType: string) => {
    if (!workerRef.current) return;
    setIsRunning(true);
    workerRef.current.postMessage({ type: 'validate', objectId, validationType });
  }, []);

  return { validate, result, isRunning };
}
