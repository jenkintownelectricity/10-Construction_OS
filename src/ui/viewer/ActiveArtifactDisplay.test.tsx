/**
 * Active Artifact Display — Tests
 *
 * Proves:
 *   - Holds current successful SVG payload only
 *   - Clears on sourceContext.submittalId change
 *   - Clears on generation failure
 *   - Contains no history
 *   - Contains no persistence
 *   - Rejects empty SVG content
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect, beforeEach } from 'vitest';
import {
  activeArtifactDisplay,
  type ActiveArtifactPayload,
} from './ActiveArtifactDisplay';
import { generationStore } from '../stores/generationStore';

const SAMPLE_PAYLOAD: ActiveArtifactPayload = {
  svgContent: '<svg viewBox="0 0 1080 720"><rect width="100" height="100"/></svg>',
  detailId: 'DRAFT-ROOF-SD-002',
  sourceSubmittalId: 'SD-002',
  artifactType: 'roofing_detail',
  filename: 'DRAFT-ROOF-SD-002.dxf',
};

beforeEach(() => {
  generationStore.clear();
  activeArtifactDisplay.reset();
});

describe('ActiveArtifactDisplay — payload management', () => {
  it('initializes with null payload', () => {
    expect(activeArtifactDisplay.getPayload()).toBeNull();
  });

  it('stores payload on setPayload', () => {
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    expect(activeArtifactDisplay.getPayload()).toEqual(SAMPLE_PAYLOAD);
  });

  it('clears payload on clear()', () => {
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    activeArtifactDisplay.clear();
    expect(activeArtifactDisplay.getPayload()).toBeNull();
  });

  it('rejects empty SVG content', () => {
    activeArtifactDisplay.setPayload({ ...SAMPLE_PAYLOAD, svgContent: '' });
    expect(activeArtifactDisplay.getPayload()).toBeNull();
  });

  it('contains only current payload — no history', () => {
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    const second: ActiveArtifactPayload = {
      ...SAMPLE_PAYLOAD,
      detailId: 'DRAFT-ROOF-SD-003',
      sourceSubmittalId: 'SD-003',
    };
    activeArtifactDisplay.setPayload(second);
    expect(activeArtifactDisplay.getPayload()).toEqual(second);
  });
});

describe('ActiveArtifactDisplay — generationStore binding', () => {
  it('clears on sourceContext.submittalId change', async () => {
    // Set initial context and payload
    generationStore.setSourceContext({
      submittalId: 'SD-002',
      title: 'Roof Membrane',
      manufacturer: 'Carlisle SynTec',
      spec: '07 52 16',
      project: 'Heritage Plaza',
    });
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    expect(activeArtifactDisplay.getPayload()).not.toBeNull();

    // Change submittalId → payload cleared
    generationStore.setSourceContext({
      submittalId: 'SD-099',
      title: 'Different Submittal',
      manufacturer: 'Carlisle SynTec',
      spec: '07 52 16',
      project: 'Heritage Plaza',
    });

    // Wait for microtask notification
    await new Promise((r) => setTimeout(r, 20));
    expect(activeArtifactDisplay.getPayload()).toBeNull();
  });

  it('clears on generation failure', async () => {
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    expect(activeArtifactDisplay.getPayload()).not.toBeNull();

    // Simulate failure
    generationStore.beginRequest();
    generationStore.completeError('GENERATION_FAILED', 'test failure');

    await new Promise((r) => setTimeout(r, 20));
    expect(activeArtifactDisplay.getPayload()).toBeNull();
  });

  it('does NOT clear when same submittalId is re-set', async () => {
    generationStore.setSourceContext({
      submittalId: 'SD-002',
      title: 'Roof Membrane',
      manufacturer: 'Carlisle SynTec',
      spec: '07 52 16',
      project: 'Heritage Plaza',
    });
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);

    // Re-set same context
    generationStore.setSourceContext({
      submittalId: 'SD-002',
      title: 'Roof Membrane Updated',
      manufacturer: 'Carlisle SynTec',
      spec: '07 52 16',
      project: 'Heritage Plaza',
    });

    await new Promise((r) => setTimeout(r, 20));
    expect(activeArtifactDisplay.getPayload()).not.toBeNull();
  });
});

describe('ActiveArtifactDisplay — subscribe', () => {
  it('notifies subscribers on setPayload', async () => {
    let notified = false;
    activeArtifactDisplay.subscribe(() => {
      notified = true;
    });
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    await new Promise((r) => setTimeout(r, 20));
    expect(notified).toBe(true);
  });

  it('notifies subscribers on clear', async () => {
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    await new Promise((r) => setTimeout(r, 20));

    let notified = false;
    activeArtifactDisplay.subscribe(() => {
      notified = true;
    });
    activeArtifactDisplay.clear();
    await new Promise((r) => setTimeout(r, 20));
    expect(notified).toBe(true);
  });

  it('unsubscribe stops notifications', async () => {
    let count = 0;
    const unsub = activeArtifactDisplay.subscribe(() => {
      count++;
    });
    activeArtifactDisplay.setPayload(SAMPLE_PAYLOAD);
    await new Promise((r) => setTimeout(r, 20));
    expect(count).toBe(1);

    unsub();
    activeArtifactDisplay.clear();
    await new Promise((r) => setTimeout(r, 20));
    expect(count).toBe(1);
  });
});
