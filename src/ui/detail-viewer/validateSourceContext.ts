/**
 * Source Context Validator
 *
 * Validates generationStore.sourceContext before mapper execution.
 * FAIL_CLOSED on any missing or invalid field.
 *
 * Schema (locked):
 *   { submittalId: string, title: string, manufacturer: string, spec: string, project: string }
 *
 * Governance: VKGL04R — Ring 3 TOUCH-ALLOWED
 */

import type { GenerationSourceContext } from '../stores/generationStore';

// ─── Validation Result ────────────────────────────────────────────────

export interface SourceContextValidationResult {
  readonly valid: boolean;
  readonly errorCode?: string;
  readonly errorMessage?: string;
}

// ─── Roofing spec prefix check ────────────────────────────────────────

/**
 * CSI Division 07 roofing membrane spec codes.
 * Only these prefixes are valid roofing generation sources.
 */
const ROOFING_SPEC_PREFIXES: ReadonlySet<string> = new Set([
  '07 52',  // Modified Bituminous Membrane Roofing
  '07 53',  // Elastomeric Membrane Roofing (EPDM)
  '07 54',  // Thermoplastic Membrane Roofing (TPO/PVC)
  '07 55',  // Protected Membrane Roofing
]);

// ─── Validator ────────────────────────────────────────────────────────

/**
 * Validate a source context for roofing generation.
 *
 * Checks:
 *   1. Context is non-null
 *   2. All required string fields are present and non-empty
 *   3. Spec code maps to a roofing membrane division
 *
 * FAIL_CLOSED on any check failure.
 */
export function validateSourceContext(
  context: GenerationSourceContext | null,
): SourceContextValidationResult {
  // Gate: null context
  if (context === null || context === undefined) {
    return {
      valid: false,
      errorCode: 'NO_SOURCE_CONTEXT',
      errorMessage: 'FAIL_CLOSED: No source context provided. Select a submittal from Shop Drawings first.',
    };
  }

  // Gate: required string fields
  const requiredFields: ReadonlyArray<keyof GenerationSourceContext> = [
    'submittalId',
    'title',
    'manufacturer',
    'spec',
    'project',
  ];

  for (const field of requiredFields) {
    const value = context[field];
    if (typeof value !== 'string' || value.trim().length === 0) {
      return {
        valid: false,
        errorCode: 'MISSING_FIELD',
        errorMessage: `FAIL_CLOSED: Source context field '${field}' is missing or empty.`,
      };
    }
  }

  // Gate: spec must be a roofing membrane spec
  const specPrefix = context.spec.slice(0, 5); // e.g. "07 52"
  if (!ROOFING_SPEC_PREFIXES.has(specPrefix)) {
    return {
      valid: false,
      errorCode: 'NON_ROOFING_SPEC',
      errorMessage: `FAIL_CLOSED: Spec '${context.spec}' is not a roofing membrane specification. Supported CSI divisions: ${[...ROOFING_SPEC_PREFIXES].sort().join(', ')}.`,
    };
  }

  return { valid: true };
}
