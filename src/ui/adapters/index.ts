/**
 * Construction OS — Adapter Registry
 * Assembles all adapters (mock or real) into a single registry.
 * Mock adapters are clearly labeled.
 *
 * Cockpit adapters (awareness, proposal, runtimeDiagnostics, assistant) are
 * bounded UI facades that consume upstream system data through assumed payload
 * shapes. See docs/ui/cockpit-adapters.md for full documentation.
 */

import type { AdapterRegistry } from '../contracts/adapters';
import { mockTruthSource } from './mockTruthSource';
import { mockReferenceSource } from './mockReferenceSource';
import { mockSpatialSource } from './mockSpatialSource';
import { mockValidation } from './mockValidation';
import { mockArtifact } from './mockArtifact';
import { mockVoice } from './mockVoice';
import { mockAwarenessAdapter } from './awarenessAdapter';
import { mockProposalAdapter } from './proposalAdapter';
import { mockRuntimeDiagnosticsAdapter } from './runtimeDiagnosticsAdapter';
import { mockAssistantAdapter } from './assistantAdapter';
import { dxfGenerationAdapter } from './dxfGenerationAdapter';

export { dxfGenerationAdapter } from './dxfGenerationAdapter';

export const adapters: AdapterRegistry = {
  truth: mockTruthSource,
  reference: mockReferenceSource,
  spatial: mockSpatialSource,
  validation: mockValidation,
  artifact: mockArtifact,
  voice: mockVoice,
};

/**
 * Cockpit-specific adapters — bounded UI facades for governance panels.
 * These are separate from the core AdapterRegistry because they consume
 * Construction OS system-level data (Awareness Cache, Cognitive Bus,
 * Runtime, Assistant) rather than project-level data.
 */
export const cockpitAdapters = {
  awareness: mockAwarenessAdapter,
  proposal: mockProposalAdapter,
  runtimeDiagnostics: mockRuntimeDiagnosticsAdapter,
  assistant: mockAssistantAdapter,
};
