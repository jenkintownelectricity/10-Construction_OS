/**
 * Source Context Validator — Tests
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect } from 'vitest';
import { validateSourceContext } from './validateSourceContext';
import type { GenerationSourceContext } from '../stores/generationStore';

const VALID_CONTEXT: GenerationSourceContext = {
  submittalId: 'SD-002',
  title: 'Roof Membrane Assembly — Full Plan',
  manufacturer: 'Carlisle SynTec',
  spec: '07 52 16',
  project: 'Heritage Plaza',
};

describe('validateSourceContext', () => {
  it('accepts valid roofing source context', () => {
    const result = validateSourceContext(VALID_CONTEXT);
    expect(result.valid).toBe(true);
    expect(result.errorCode).toBeUndefined();
  });

  it('FAIL_CLOSED on null context', () => {
    const result = validateSourceContext(null);
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('NO_SOURCE_CONTEXT');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
  });

  it('FAIL_CLOSED on missing submittalId', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, submittalId: '' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MISSING_FIELD');
    expect(result.errorMessage).toContain("'submittalId'");
  });

  it('FAIL_CLOSED on missing title', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, title: '' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MISSING_FIELD');
    expect(result.errorMessage).toContain("'title'");
  });

  it('FAIL_CLOSED on missing manufacturer', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, manufacturer: '' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MISSING_FIELD');
    expect(result.errorMessage).toContain("'manufacturer'");
  });

  it('FAIL_CLOSED on missing spec', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MISSING_FIELD');
    expect(result.errorMessage).toContain("'spec'");
  });

  it('FAIL_CLOSED on missing project', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, project: '' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('MISSING_FIELD');
    expect(result.errorMessage).toContain("'project'");
  });

  it('FAIL_CLOSED on non-roofing spec (curtain wall 08 44 13)', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '08 44 13' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('NON_ROOFING_SPEC');
    expect(result.errorMessage).toContain('FAIL_CLOSED');
    expect(result.errorMessage).toContain('08 44 13');
  });

  it('FAIL_CLOSED on non-roofing spec (metal panels 07 42 43)', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '07 42 43' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('NON_ROOFING_SPEC');
  });

  it('FAIL_CLOSED on non-roofing spec (waterproofing 07 11 13)', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '07 11 13' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('NON_ROOFING_SPEC');
  });

  it('FAIL_CLOSED on non-roofing spec (windows 08 51 13)', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '08 51 13' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('NON_ROOFING_SPEC');
  });

  it('accepts TPO spec 07 54 23', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '07 54 23' });
    expect(result.valid).toBe(true);
  });

  it('accepts EPDM spec 07 53 23', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '07 53 23' });
    expect(result.valid).toBe(true);
  });

  it('accepts PVC spec 07 54 19', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '07 54 19' });
    expect(result.valid).toBe(true);
  });

  it('accepts protected membrane spec 07 55 56', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '07 55 56' });
    expect(result.valid).toBe(true);
  });

  // ─── New submittal contexts validate correctly ──────────────────

  it('accepts GAF TPO submittal (SD-007, 07 54 23)', () => {
    const result = validateSourceContext({
      submittalId: 'SD-007',
      title: 'TPO Roof Assembly — Building A',
      manufacturer: 'GAF',
      spec: '07 54 23',
      project: 'Riverside Commerce Center',
    });
    expect(result.valid).toBe(true);
  });

  it('accepts Johns Manville PVC submittal (SD-008, 07 54 19)', () => {
    const result = validateSourceContext({
      submittalId: 'SD-008',
      title: 'PVC Membrane Roofing — Tower Podium',
      manufacturer: 'Johns Manville',
      spec: '07 54 19',
      project: 'Metro Station',
    });
    expect(result.valid).toBe(true);
  });

  it('accepts Henry Company SBS submittal (SD-009, 07 52 13)', () => {
    const result = validateSourceContext({
      submittalId: 'SD-009',
      title: 'SBS Modified Bitumen Roof — Mechanical Area',
      manufacturer: 'Henry Company',
      spec: '07 52 13',
      project: 'Heritage Plaza',
    });
    expect(result.valid).toBe(true);
  });

  it('accepts GAF protected membrane submittal (SD-010, 07 55 56)', () => {
    const result = validateSourceContext({
      submittalId: 'SD-010',
      title: 'Protected Membrane Roof — Green Roof Area',
      manufacturer: 'GAF',
      spec: '07 55 56',
      project: 'Airport Terminal',
    });
    expect(result.valid).toBe(true);
  });

  it('FAIL_CLOSED on expansion joints spec (07 95 13) even after coverage expansion', () => {
    const result = validateSourceContext({ ...VALID_CONTEXT, spec: '07 95 13' });
    expect(result.valid).toBe(false);
    expect(result.errorCode).toBe('NON_ROOFING_SPEC');
  });
});
