/**
 * Construction OS — DXF Generation Adapter
 *
 * Real adapter that sends canonical assembly drafts to the
 * dxf_Generatior_Assembly_Letter_Parser /generate-from-draft endpoint
 * and returns generation results.
 *
 * Fail-closed: any network error, validation failure, or generation error
 * is surfaced explicitly. No silent fallback or preview-only substitution.
 */

import type {
  CanonicalAssemblyDraft,
  GenerationResult,
  GenerationDiagnostic,
} from '../contracts/assemblyDraft';
import { validateAssemblyDraft } from '../contracts/assemblyDraft';

// ─── Configuration ─────────────────────────────────────────────────────────

const DXF_GENERATOR_BASE_URL =
  (typeof import.meta !== 'undefined' && (import.meta as unknown as Record<string, Record<string, string>>).env?.VITE_DXF_GENERATOR_URL)
  || 'http://localhost:5000';

// ─── Generation Adapter ────────────────────────────────────────────────────

export interface DxfGenerationAdapter {
  readonly adapterName: string;
  readonly isMock: false;

  /**
   * Validate and generate a DXF detail from a canonical assembly draft.
   * Performs client-side validation first (fail-closed), then sends to
   * the real generator endpoint.
   */
  generateDetail(draft: CanonicalAssemblyDraft): Promise<GenerationResult>;

  /**
   * Get the download URL for a generated DXF file.
   */
  getDownloadUrl(dxfFilename: string): string;
}

function makeFailedResult(
  draftId: string,
  status: 'validation_failed' | 'generation_error',
  diagnostics: GenerationDiagnostic[],
): GenerationResult {
  return {
    status,
    draftId,
    generatorSeam: null,
    dxfFilename: null,
    dxfPath: null,
    diagnostics,
    timestamp: Date.now(),
  };
}

export const dxfGenerationAdapter: DxfGenerationAdapter = {
  adapterName: 'dxf-generation-adapter',
  isMock: false,

  async generateDetail(draft: CanonicalAssemblyDraft): Promise<GenerationResult> {
    // ── Client-side pre-flight validation (fail-closed) ────────────────
    const preValidation = validateAssemblyDraft(draft);
    if (!preValidation.valid) {
      return makeFailedResult(draft.id, 'validation_failed', [...preValidation.errors]);
    }

    // ── Send to real generator endpoint ────────────────────────────────
    try {
      const response = await fetch(`${DXF_GENERATOR_BASE_URL}/generate-from-draft`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(draft),
      });

      const data = await response.json();

      if (response.ok && data.status === 'success') {
        return {
          status: 'success',
          draftId: data.draftId ?? draft.id,
          generatorSeam: data.generatorSeam ?? 'AssemblyDXFGenerator._generate_single_assembly',
          dxfFilename: data.dxfFilename,
          dxfPath: data.dxfPath,
          diagnostics: [],
          timestamp: Date.now(),
        };
      }

      // Server returned validation failure or generation error
      const diagnostics: GenerationDiagnostic[] = (data.diagnostics ?? []).map(
        (msg: string) => ({ code: 'SERVER_DIAGNOSTIC', message: msg })
      );

      if (data.validation?.errors) {
        for (const err of data.validation.errors) {
          diagnostics.push({
            code: err.code ?? 'SERVER_VALIDATION',
            message: err.message,
            field: err.field,
          });
        }
      }

      return makeFailedResult(
        draft.id,
        data.status === 'validation_failed' ? 'validation_failed' : 'generation_error',
        diagnostics,
      );
    } catch (err) {
      // Network error or JSON parse failure — fail closed
      const message = err instanceof Error ? err.message : String(err);
      return makeFailedResult(draft.id, 'generation_error', [
        {
          code: 'NETWORK_ERROR',
          message: `Failed to reach DXF generator: ${message}. `
            + `Ensure dxf_Generatior_Assembly_Letter_Parser is running at ${DXF_GENERATOR_BASE_URL}`,
        },
      ]);
    }
  },

  getDownloadUrl(dxfFilename: string): string {
    return `${DXF_GENERATOR_BASE_URL}/generate-from-draft/download/${encodeURIComponent(dxfFilename)}`;
  },
};
