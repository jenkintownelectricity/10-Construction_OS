/**
 * Preview/Test Compiler Adapter
 *
 * Bounded adapter that accepts canonical assembly drafts and runs them
 * through a preview/test validation loop. Does NOT mutate any source repo.
 *
 * This adapter simulates the compiler-facing handoff:
 * 1. Receives a validated canonical draft
 * 2. Re-validates against Assembly Kernel schema (fail-closed)
 * 3. Maps to a compiler-consumable representation
 * 4. Returns preview/test diagnostics
 *
 * Governance: VKGL04R — Ring 2: "Preview/test adapter bounded, no source mutation."
 */

import type { CanonicalAssemblyDraft, PreviewTestResult, FieldDiagnostic } from './types';
import { validateAssemblyDraft } from './assemblyDraftValidator';

// ─── Compiler IR shape (aligned to ShopDrawing_Compiler detail_analysis_contract) ──

interface CompilerPreviewIR {
  readonly detail_id: string;
  readonly source_assembly_id: string;
  readonly assembly_type: string;
  readonly layer_count: number;
  readonly control_layers_addressed: readonly string[];
  readonly interface_zones_declared: readonly string[];
  readonly continuity_map: Readonly<Record<string, string>>;
  readonly validation_gate: 'PASS' | 'FAIL';
  readonly diagnostics: readonly string[];
}

// ─── Compiler-facing preview checks ─────────────────────────────────────

function checkCompilerReadiness(draft: CanonicalAssemblyDraft): readonly string[] {
  const issues: string[] = [];

  // Check: assembly must have at least one layer
  if (!draft.layers || draft.layers.length === 0) {
    issues.push('COMPILER: No layers defined — cannot generate drawing output.');
  }

  // Check: roofing assemblies need bulk_water_control
  if (draft.assembly_type === 'roof_assembly') {
    const hasBulkWater = draft.layers?.some((l) => l.control_layer_id === 'bulk_water_control');
    if (!hasBulkWater) {
      issues.push('COMPILER: Roof assembly missing bulk_water_control layer.');
    }
    const hasThermal = draft.layers?.some((l) => l.control_layer_id === 'thermal_control');
    if (!hasThermal) {
      issues.push('COMPILER: Roof assembly missing thermal_control layer.');
    }
  }

  // Check: fire-rated assemblies need fire_smoke_control
  if (draft.layers?.some((l) => l.control_layer_id === 'fire_smoke_control')) {
    const hasContinuity = draft.control_layer_continuity?.['fire_smoke_control'];
    if (!hasContinuity) {
      issues.push('COMPILER: Fire protection layer present but fire_smoke_control continuity not declared.');
    }
  }

  // Check: all layers have material_ref
  const missingMaterial = draft.layers?.filter((l) => !l.material_ref);
  if (missingMaterial && missingMaterial.length > 0) {
    issues.push(`COMPILER: ${missingMaterial.length} layer(s) missing material_ref.`);
  }

  // Check: layer positions are sequential
  if (draft.layers && draft.layers.length > 0) {
    const positions = draft.layers.map((l) => l.position).sort((a, b) => a - b);
    for (let i = 0; i < positions.length; i++) {
      if (positions[i] !== i + 1) {
        issues.push(`COMPILER: Layer positions not sequential (expected ${i + 1}, got ${positions[i]}).`);
        break;
      }
    }
  }

  return issues;
}

// ─── Map draft to compiler IR ───────────────────────────────────────────

function toCompilerIR(draft: CanonicalAssemblyDraft): CompilerPreviewIR {
  const controlLayers = [...new Set(draft.layers?.map((l) => l.control_layer_id) ?? [])];
  const compilerDiagnostics = checkCompilerReadiness(draft);

  return {
    detail_id: `PREVIEW-${draft.system_id}`,
    source_assembly_id: draft.system_id,
    assembly_type: draft.assembly_type,
    layer_count: draft.layers?.length ?? 0,
    control_layers_addressed: controlLayers,
    interface_zones_declared: draft.interface_zones ?? [],
    continuity_map: draft.control_layer_continuity ?? {},
    validation_gate: compilerDiagnostics.length === 0 ? 'PASS' : 'FAIL',
    diagnostics: compilerDiagnostics,
  };
}

// ─── Public API ─────────────────────────────────────────────────────────

/**
 * Run preview/test on a canonical assembly draft.
 * Returns a complete test result with pass/fail status and diagnostics.
 *
 * Fail-closed: if schema validation fails, preview fails.
 * Bounded: no source repo is mutated.
 */
export function runPreviewTest(draft: CanonicalAssemblyDraft): PreviewTestResult {
  // Step 1: Schema validation (fail-closed)
  const schemaValidation = validateAssemblyDraft(draft);
  if (!schemaValidation.valid) {
    const schemaErrors = schemaValidation.diagnostics
      .filter((d) => d.severity === 'error')
      .map((d) => `SCHEMA: ${d.field} — ${d.message}`);
    return {
      draftId: draft.system_id,
      status: 'fail',
      compilerAdapter: 'previewTestAdapter',
      diagnostics: schemaErrors,
      timestamp: Date.now(),
      payload: draft,
    };
  }

  // Step 2: Compiler readiness check
  const ir = toCompilerIR(draft);

  if (ir.validation_gate === 'FAIL') {
    return {
      draftId: draft.system_id,
      status: 'fail',
      compilerAdapter: 'previewTestAdapter',
      diagnostics: [...ir.diagnostics],
      timestamp: Date.now(),
      payload: draft,
    };
  }

  // Step 3: Preview passed
  return {
    draftId: draft.system_id,
    status: 'pass',
    compilerAdapter: 'previewTestAdapter',
    diagnostics: [
      `PREVIEW PASS: ${ir.layer_count} layers, ${ir.control_layers_addressed.length} control layers, ${ir.interface_zones_declared.length} interface zones.`,
      `Compiler IR generated: ${ir.detail_id}`,
      `Continuity map: ${Object.entries(ir.continuity_map).map(([k, v]) => `${k}=${v}`).join(', ')}`,
    ],
    timestamp: Date.now(),
    payload: draft,
  };
}

/**
 * Get the compiler IR representation for display/diagnostics.
 */
export function getCompilerIR(draft: CanonicalAssemblyDraft): CompilerPreviewIR {
  return toCompilerIR(draft);
}
