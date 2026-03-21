/**
 * Construction OS — Adapter Registry
 * Assembles all adapters (mock or real) into a single registry.
 * Mock adapters are clearly labeled.
 */

import type { AdapterRegistry } from '../contracts/adapters';
import { mockTruthSource } from './mockTruthSource';
import { mockReferenceSource } from './mockReferenceSource';
import { mockSpatialSource } from './mockSpatialSource';
import { mockValidation } from './mockValidation';
import { mockArtifact } from './mockArtifact';
import { mockVoice } from './mockVoice';

export const adapters: AdapterRegistry = {
  truth: mockTruthSource,
  reference: mockReferenceSource,
  spatial: mockSpatialSource,
  validation: mockValidation,
  artifact: mockArtifact,
  voice: mockVoice,
};
