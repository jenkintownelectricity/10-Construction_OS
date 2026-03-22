/**
 * Construction OS — Canonical Assembly Draft Contracts
 *
 * Defines the canonical assembly draft shape used by the Assembly Builder
 * to communicate with the DXF generator. These types map 1:1 to the
 * recognised layer fields in dxf_Generatior_Assembly_Letter_Parser.
 *
 * No fields are invented. All fields match the existing generator input.
 */

// ─── Assembly Category ─────────────────────────────────────────────────────

export type AssemblyCategory = 'roofing' | 'fireproofing';

// ─── Assembly Layer Fields ─────────────────────────────────────────────────

export interface AssemblyLayers {
  readonly assembly_roof_area?: string;
  readonly manufacturer?: string;
  readonly system?: string;
  readonly spec_number?: string;
  readonly membrane_1: string;
  readonly membrane_1_attachment?: string;
  readonly membrane_2?: string;
  readonly membrane_2_attachment?: string;
  readonly membrane_3?: string;
  readonly membrane_3_attachment?: string;
  readonly insulation_layer_1?: string;
  readonly insulation_layer_1_attachment?: string;
  readonly insulation_layer_2?: string;
  readonly insulation_layer_2_attachment?: string;
  readonly insulation_layer_3?: string;
  readonly insulation_layer_3_attachment?: string;
  readonly coverboard_1?: string;
  readonly coverboard_1_attachment?: string;
  readonly coverboard_2?: string;
  readonly coverboard_2_attachment?: string;
  readonly vapor_barrier?: string;
  readonly vapor_barrier_attachment?: string;
  readonly deck_slope: string;
  readonly deck_slope_attachment?: string;
}

// ─── Canonical Assembly Draft ──────────────────────────────────────────────

export interface CanonicalAssemblyDraft {
  readonly id: string;
  readonly name: string;
  readonly type: 'assembly';
  readonly category: AssemblyCategory;
  readonly layers: AssemblyLayers;
  readonly project?: {
    readonly name: string;
    readonly location: string;
  };
}

// ─── Generation Request / Response ─────────────────────────────────────────

export type GenerationStatus =
  | 'idle'
  | 'validating'
  | 'generating'
  | 'success'
  | 'validation_failed'
  | 'generation_error';

export interface GenerationDiagnostic {
  readonly code: string;
  readonly message: string;
  readonly field?: string;
}

export interface GenerationResult {
  readonly status: GenerationStatus;
  readonly draftId: string;
  readonly generatorSeam: string | null;
  readonly dxfFilename: string | null;
  readonly dxfPath: string | null;
  readonly diagnostics: readonly GenerationDiagnostic[];
  readonly timestamp: number;
}

// ─── Draft Validation (client-side pre-flight) ────────────────────────────

export interface DraftValidationResult {
  readonly valid: boolean;
  readonly errors: readonly GenerationDiagnostic[];
}

/**
 * Validate a canonical assembly draft before sending to the generator.
 * Fail-closed: any issue returns valid=false with diagnostics.
 */
export function validateAssemblyDraft(draft: CanonicalAssemblyDraft): DraftValidationResult {
  const errors: GenerationDiagnostic[] = [];

  if (!draft.id) {
    errors.push({ code: 'MISSING_FIELD', message: 'Draft ID is required', field: 'id' });
  }
  if (!draft.name) {
    errors.push({ code: 'MISSING_FIELD', message: 'Draft name is required', field: 'name' });
  }
  if (draft.type !== 'assembly') {
    errors.push({ code: 'INVALID_TYPE', message: `Draft type must be "assembly", got "${draft.type}"`, field: 'type' });
  }
  if (!draft.category) {
    errors.push({ code: 'MISSING_FIELD', message: 'Draft category is required', field: 'category' });
  }
  if (!draft.layers) {
    errors.push({ code: 'MISSING_FIELD', message: 'Draft layers are required', field: 'layers' });
    return { valid: false, errors };
  }

  // Roofing requires at minimum deck_slope and membrane_1
  if (draft.category === 'roofing') {
    if (!draft.layers.deck_slope) {
      errors.push({ code: 'MISSING_REQUIRED_LAYER', message: 'Roofing draft requires deck_slope', field: 'deck_slope' });
    }
    if (!draft.layers.membrane_1) {
      errors.push({ code: 'MISSING_REQUIRED_LAYER', message: 'Roofing draft requires membrane_1', field: 'membrane_1' });
    }
  }

  // Fireproofing is not supported by current generator — flag early
  if (draft.category === 'fireproofing') {
    errors.push({
      code: 'UNSUPPORTED_CATEGORY',
      message: 'Fireproofing assemblies are not supported by the current DXF generator. '
        + 'The generator only handles roofing layer structures (membrane, insulation, '
        + 'coverboard, vapor barrier, deck). Fireproofing requires a different layer model.',
      field: 'category',
    });
  }

  return { valid: errors.length === 0, errors };
}
