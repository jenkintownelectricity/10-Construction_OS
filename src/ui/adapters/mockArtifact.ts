/**
 * Construction OS — Mock Artifact Adapter
 * MOCK: Provides simulated artifact generation for development.
 */

import type { ArtifactAdapter, ArtifactResult } from '../contracts/adapters';
import type { SourcedData } from '../contracts/events';

function sourced<T>(data: T): SourcedData<T> {
  return { data, basis: 'mock', sourceAdapter: 'mock-artifact', timestamp: Date.now(), isMock: true };
}

export const mockArtifact: ArtifactAdapter = {
  adapterName: 'mock-artifact',
  isMock: true,

  async requestArtifact(objectId, type, format) {
    const result: ArtifactResult = {
      artifactId: `art-${Date.now()}`,
      objectId,
      type: type as ArtifactResult['type'],
      format: format ?? 'pdf',
      status: 'pending',
    };
    return sourced(result);
  },

  async getArtifactStatus(artifactId) {
    return sourced(null);
  },
};
