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
});
