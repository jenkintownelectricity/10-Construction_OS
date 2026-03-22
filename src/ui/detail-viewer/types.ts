/**
 * Detail Viewer — Types
 *
 * Aligned to Construction_Runtime detail_preview_seam contract.
 * No invented fields. All fields map to runtime output.
 *
 * Governance: VKGL04R
 */

// ─── Detail Preview Result (mirrors runtime DetailPreviewResult) ──────

export interface DetailPreviewResult {
  readonly success: boolean;
  readonly category: string;
  readonly detail_id: string;
  readonly seam_id: string;

  // Artifact metadata
  readonly artifact_type: string;
  readonly artifact_filename: string;
  readonly generation_status: GenerationStatus;
  readonly generator_seam: string;

  // SVG preview (same lineage as DXF)
  readonly svg_content: string;
  readonly svg_artifact_id: string;
  readonly svg_content_hash: string;

  // DXF availability
  readonly dxf_available: boolean;
  readonly dxf_artifact_id: string;
  readonly dxf_content: string;
  readonly dxf_content_hash: string;

  // Lineage
  readonly manifest_id: string;
  readonly instruction_set_id: string;
  readonly lineage: Record<string, unknown>;

  // Diagnostics
  readonly diagnostics: readonly string[];
  readonly errors: readonly DetailError[];
}

export interface DetailError {
  readonly code: string;
  readonly message: string;
}

export type GenerationStatus =
  | 'pending'
  | 'generating'
  | 'success'
  | 'validation_failed'
  | 'generation_error'
  | 'unsupported';

// ─── Viewer Tab ───────────────────────────────────────────────────────

export type ViewerTab = 'preview' | 'artifacts' | 'diagnostics';

// ─── Category ─────────────────────────────────────────────────────────

export type DetailCategory = 'roofing' | 'fireproofing';
