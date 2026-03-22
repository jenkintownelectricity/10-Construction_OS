/**
 * Tests for the Detail Generation Adapter
 *
 * Validates:
 * 1. Roofing generation produces SVG + DXF from same lineage
 * 2. Fireproofing fails closed with diagnostics
 * 3. Empty assembly fails closed
 * 4. SVG content is real SVG markup
 * 5. Artifact metadata is correctly populated
 *
 * Governance: VKGL04R
 */

import { describe, it, expect } from 'vitest';
import { generateDetailPreview } from './detailGenerationAdapter';
import { getSampleRoofingDraft } from '../assembly-builder/roofingSourceAdapter';
import { getSampleFireproofingDraft } from '../assembly-builder/fireproofingSourceAdapter';
import type { CanonicalAssemblyDraft } from '../assembly-builder/types';

// ─── Roofing Generation ─────────────────────────────────────────────

describe('Roofing detail generation', () => {
  it('produces a successful result with SVG and DXF', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    expect(result.success).toBe(true);
    expect(result.generation_status).toBe('success');
    expect(result.svg_content).not.toBe('');
    expect(result.dxf_available).toBe(true);
    expect(result.dxf_content).not.toBe('');
  });

  it('produces real SVG markup', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    expect(result.svg_content).toContain('<svg');
    expect(result.svg_content).toContain('xmlns');
    expect(result.svg_content).toContain('</svg>');
  });

  it('populates artifact metadata', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    expect(result.detail_id).toBe('DRAFT-ROOF-SDC-001');
    expect(result.artifact_type).toBe('roofing_detail');
    expect(result.artifact_filename).toContain('.dxf');
    expect(result.generator_seam).toBe('detail_preview_seam_v1');
    expect(result.seam_id).toBe('detail_preview_seam_v1');
  });

  it('has lineage data for both SVG and DXF', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    expect(result.manifest_id).not.toBe('');
    expect(result.svg_artifact_id).not.toBe('');
    expect(result.dxf_artifact_id).not.toBe('');
    expect(result.svg_content_hash).not.toBe('');
    expect(result.dxf_content_hash).not.toBe('');
  });

  it('includes diagnostics', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    expect(result.diagnostics.length).toBeGreaterThan(0);
    expect(result.diagnostics[0]).toContain('detail_preview_seam_v1');
  });

  it('SVG contains layer labels from the assembly', () => {
    const { draft } = getSampleRoofingDraft();
    const result = generateDetailPreview(draft, 'roofing');
    expect(result.svg_content).toContain('TPO');
    expect(result.svg_content).toContain('BULK WATER CONTROL');
  });
});

// ─── Fireproofing Fail-Closed ────────────────────────────────────────

describe('Fireproofing fail-closed', () => {
  it('returns unsupported status', () => {
    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');
    expect(result.success).toBe(false);
    expect(result.generation_status).toBe('unsupported');
  });

  it('includes FAIL_CLOSED diagnostic', () => {
    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');
    expect(result.diagnostics.length).toBeGreaterThan(0);
    expect(result.diagnostics[0]).toContain('FAIL_CLOSED');
    expect(result.diagnostics[0]).toContain('fireproofing');
  });

  it('includes error with UNSUPPORTED_CATEGORY code', () => {
    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');
    expect(result.errors.length).toBeGreaterThan(0);
    expect(result.errors[0].code).toBe('UNSUPPORTED_CATEGORY');
  });

  it('does not produce SVG or DXF content', () => {
    const { draft } = getSampleFireproofingDraft();
    const result = generateDetailPreview(draft, 'fireproofing');
    expect(result.svg_content).toBe('');
    expect(result.dxf_content).toBe('');
    expect(result.dxf_available).toBe(false);
  });
});

// ─── Empty Draft Fail-Closed ─────────────────────────────────────────

describe('Empty draft fail-closed', () => {
  it('fails with no layers', () => {
    const emptyDraft: CanonicalAssemblyDraft = {
      schema_version: 'v1',
      system_id: 'EMPTY',
      title: 'Empty',
      assembly_type: 'roof_assembly',
      status: 'draft',
      layers: [],
    };
    const result = generateDetailPreview(emptyDraft, 'roofing');
    expect(result.success).toBe(false);
    expect(result.generation_status).toBe('validation_failed');
    expect(result.diagnostics[0]).toContain('FAIL_CLOSED');
  });
});
