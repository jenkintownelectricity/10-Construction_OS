/**
 * Construction OS — Typed Adapter Contracts
 *
 * Adapters provide the seam between the UI and real/mock data sources.
 * UI code never invents source truth — it always flows through adapters.
 * Mock adapters must be explicitly labeled.
 */

import type { ActiveObjectIdentity, SourceBasis, SourcedData, ValidationIssue } from './events';

// ─── Truth Source Adapter ───────────────────────────────────────────────────

export interface ProjectNode {
  readonly id: string;
  readonly name: string;
  readonly type: 'project' | 'zone' | 'folder' | 'document' | 'assembly' | 'element' | 'specification';
  readonly children?: readonly ProjectNode[];
  readonly metadata?: Record<string, unknown>;
}

export interface TruthSourceAdapter {
  readonly adapterName: string;
  readonly isMock: boolean;
  getProjectTree(): Promise<SourcedData<ProjectNode>>;
  getObject(id: string): Promise<SourcedData<ActiveObjectIdentity | null>>;
  searchObjects(query: string): Promise<SourcedData<readonly ActiveObjectIdentity[]>>;
}

// ─── Reference Source Adapter ───────────────────────────────────────────────

export interface ReferenceEntry {
  readonly id: string;
  readonly objectId: string;
  readonly type: 'spec' | 'code' | 'citation' | 'document';
  readonly title: string;
  readonly content: string;
  readonly sourceBasis: SourceBasis;
  readonly sourceDocument?: string;
}

export interface ReferenceSourceAdapter {
  readonly adapterName: string;
  readonly isMock: boolean;
  getReferences(objectId: string, type?: string): Promise<SourcedData<readonly ReferenceEntry[]>>;
  getCompareReferences(objectIdA: string, objectIdB: string): Promise<SourcedData<{ a: readonly ReferenceEntry[]; b: readonly ReferenceEntry[] }>>;
}

// ─── Spatial Source Adapter ─────────────────────────────────────────────────

export interface SpatialObject {
  readonly id: string;
  readonly objectId: string;
  readonly label: string;
  readonly x: number;
  readonly y: number;
  readonly width: number;
  readonly height: number;
  readonly zoneId?: string;
  readonly layer?: string;
}

export interface SpatialZone {
  readonly id: string;
  readonly name: string;
  readonly bounds: { x: number; y: number; width: number; height: number };
  readonly objects: readonly string[];
}

export interface SpatialSourceAdapter {
  readonly adapterName: string;
  readonly isMock: boolean;
  getSpatialObjects(zoneId?: string): Promise<SourcedData<readonly SpatialObject[]>>;
  getZones(): Promise<SourcedData<readonly SpatialZone[]>>;
  getObjectSpatialContext(objectId: string): Promise<SourcedData<{ object: SpatialObject; zone?: SpatialZone } | null>>;
}

// ─── Validation Adapter ─────────────────────────────────────────────────────

export interface ValidationResult {
  readonly objectId: string;
  readonly status: 'pending' | 'running' | 'passed' | 'failed' | 'error';
  readonly issues: readonly ValidationIssue[];
  readonly validatedAt: number;
  readonly validationType: 'structural' | 'domain' | 'geometry' | 'full';
}

export interface ValidationAdapter {
  readonly adapterName: string;
  readonly isMock: boolean;
  validate(objectId: string, type: string): Promise<SourcedData<ValidationResult>>;
  getValidationStatus(objectId: string): Promise<SourcedData<ValidationResult | null>>;
}

// ─── Artifact Adapter ───────────────────────────────────────────────────────

export interface ArtifactResult {
  readonly artifactId: string;
  readonly objectId: string;
  readonly type: 'drawing' | 'report' | 'export';
  readonly format: string;
  readonly status: 'pending' | 'generating' | 'ready' | 'error';
  readonly url?: string;
}

export interface ArtifactAdapter {
  readonly adapterName: string;
  readonly isMock: boolean;
  requestArtifact(objectId: string, type: string, format?: string): Promise<SourcedData<ArtifactResult>>;
  getArtifactStatus(artifactId: string): Promise<SourcedData<ArtifactResult | null>>;
}

// ─── Voice Adapter Seam ─────────────────────────────────────────────────────

export interface VoiceCommand {
  readonly transcript: string;
  readonly confidence: number;
  readonly intent?: string;
  readonly parameters?: Record<string, unknown>;
}

export interface VoiceAdapter {
  readonly adapterName: string;
  readonly isMock: boolean;
  readonly isAvailable: boolean;
  startListening(): Promise<void>;
  stopListening(): Promise<void>;
  onCommand(handler: (command: VoiceCommand) => void): () => void;
}

// ─── Adapter Registry ───────────────────────────────────────────────────────

export interface AdapterRegistry {
  readonly truth: TruthSourceAdapter;
  readonly reference: ReferenceSourceAdapter;
  readonly spatial: SpatialSourceAdapter;
  readonly validation: ValidationAdapter;
  readonly artifact: ArtifactAdapter;
  readonly voice: VoiceAdapter;
}
