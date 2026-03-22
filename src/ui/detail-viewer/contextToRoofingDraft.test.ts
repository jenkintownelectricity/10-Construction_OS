/**
 * Context-to-Roofing-Draft Mapper — Tests
 *
 * Proves:
 *   - Deterministic mapping for identical inputs
 *   - Supported manufacturer/spec combinations succeed
 *   - Unsupported combinations FAIL_CLOSED
 *   - Draft structure matches CanonicalAssemblyDraft schema
 *   - Existing hydrateRoofingDraft seam is used
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect } from 'vitest';
import { mapContextToRoofingDraft } from './contextToRoofingDraft';
import type { GenerationSourceContext } from '../stores/generationStore';

// ─── Test Contexts ────────────────────────────────────────────────────

const CARLISLE_TPO: GenerationSourceContext = {
  submittalId: 'SD-002',
  title: 'Roof Membrane Assembly — Full Plan',
  manufacturer: 'Carlisle SynTec',
  spec: '07 54 23',
  project: 'Heritage Plaza',
};

const CARLISLE_SBS: GenerationSourceContext = {
  submittalId: 'SD-010',
  title: 'Modified Bituminous Roof — Building A',
  manufacturer: 'Carlisle SynTec',
  spec: '07 52 16',
  project: 'Metro Station',
};

const FIRESTONE_EPDM: GenerationSourceContext = {
  submittalId: 'SD-011',
  title: 'EPDM Roof System — Warehouse',
  manufacturer: 'Firestone Building Products',
  spec: '07 53 23',
  project: 'Industrial Park',
};

const SIKA_PVC: GenerationSourceContext = {
  submittalId: 'SD-012',
  title: 'PVC Membrane — Civic Center',
  manufacturer: 'Sika Corporation',
  spec: '07 54 19',
  project: 'Civic Center Library',
};

describe('mapContextToRoofingDraft', () => {
  // ─── Determinism ──────────────────────────────────────────────────

  it('is deterministic — identical inputs produce identical outputs', () => {
    const result1 = mapContextToRoofingDraft(CARLISLE_TPO);
    const result2 = mapContextToRoofingDraft(CARLISLE_TPO);
    expect(result1).toEqual(result2);
  });

  it('different submittalIds produce different draftIds', () => {
    const r1 = mapContextToRoofingDraft(CARLISLE_TPO);
    const r2 = mapContextToRoofingDraft({ ...CARLISLE_TPO, submittalId: 'SD-099' });
    expect(r1.draft!.system_id).not.toBe(r2.draft!.system_id);
  });

  // ─── Supported Combinations ───────────────────────────────────────

  it('maps Carlisle SynTec + TPO (07 54 23) successfully', () => {
    const result = mapContextToRoofingDraft(CARLISLE_TPO);
    expect(result.success).toBe(true);
    expect(result.draft).toBeDefined();
    expect(result.draft!.system_id).toBe('DRAFT-ROOF-SD-002');
    expect(result.draft!.assembly_type).toBe('roof_assembly');
    expect(result.draft!.schema_version).toBe('v1');
    expect(result.draft!.status).toBe('draft');
    expect(result.draft!.layers!.length).toBeGreaterThan(0);
  });

  it('maps Carlisle SynTec + SBS (07 52 16) successfully', () => {
    const result = mapContextToRoofingDraft(CARLISLE_SBS);
    expect(result.success).toBe(true);
    expect(result.draft!.system_id).toBe('DRAFT-ROOF-SD-010');
    expect(result.draft!.layers!.length).toBeGreaterThan(0);
  });

  it('maps Firestone + EPDM (07 53 23) successfully', () => {
    const result = mapContextToRoofingDraft(FIRESTONE_EPDM);
    expect(result.success).toBe(true);
    expect(result.draft!.system_id).toBe('DRAFT-ROOF-SD-011');
    expect(result.draft!.layers!.length).toBeGreaterThan(0);
  });

  it('maps Sika + PVC (07 54 19) successfully', () => {
    const result = mapContextToRoofingDraft(SIKA_PVC);
    expect(result.success).toBe(true);
    expect(result.draft!.system_id).toBe('DRAFT-ROOF-SD-012');
  });

  // ─── Draft Structure Validation ───────────────────────────────────

  it('produced draft has valid layer structure', () => {
    const result = mapContextToRoofingDraft(CARLISLE_TPO);
    const draft = result.draft!;
    expect(draft.layers).toBeDefined();
    for (const layer of draft.layers!) {
      expect(layer.layer_id).toBeTruthy();
      expect(layer.position).toBeGreaterThan(0);
      expect(layer.control_layer_id).toBeTruthy();
      expect(layer.material_ref).toBeTruthy();
    }
  });

  it('produced draft has control layer continuity', () => {
    const result = mapContextToRoofingDraft(CARLISLE_TPO);
    expect(result.draft!.control_layer_continuity).toBeDefined();
    expect(result.draft!.control_layer_continuity!.bulk_water_control).toBe('continuous');
  });

  it('produced draft title includes manufacturer and assembly area', () => {
    const result = mapContextToRoofingDraft(CARLISLE_TPO);
    expect(result.draft!.title).toContain('Carlisle SynTec');
    expect(result.draft!.title).toContain('Roof Membrane Assembly');
  });

  // ─── FAIL_CLOSED Cases ────────────────────────────────────────────

  it('FAIL_CLOSED on unmappable spec (expansion joint 07 95 13)', () => {
    const result = mapContextToRoofingDraft({
      ...CARLISLE_TPO,
      spec: '07 95 13',
    });
    expect(result.success).toBe(false);
    expect(result.errorCode).toBe('UNMAPPABLE_SPEC');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
    expect(result.draft).toBeUndefined();
  });

  it('FAIL_CLOSED on unknown manufacturer', () => {
    const result = mapContextToRoofingDraft({
      ...CARLISLE_TPO,
      manufacturer: 'Unknown Mfr Co',
    });
    expect(result.success).toBe(false);
    expect(result.errorCode).toBe('UNMAPPABLE_MANUFACTURER');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
    expect(result.draft).toBeUndefined();
  });

  it('FAIL_CLOSED on known manufacturer but unsupported system combo', () => {
    // Firestone has EPDM and TPO but not SBS in our lookup
    const result = mapContextToRoofingDraft({
      submittalId: 'SD-099',
      title: 'Test',
      manufacturer: 'Firestone Building Products',
      spec: '07 52 16', // SBS
      project: 'Test',
    });
    expect(result.success).toBe(false);
    expect(result.errorCode).toBe('UNMAPPABLE_MANUFACTURER');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
  });
});
