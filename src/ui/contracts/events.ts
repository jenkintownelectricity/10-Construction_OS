/**
 * Construction OS — Typed Event Contracts
 *
 * Central typed event contract definitions for the event bus.
 * Panels communicate ONLY through these events — no direct panel-to-panel calls.
 */

// ─── Active Object Identity ─────────────────────────────────────────────────

export interface ActiveObjectIdentity {
  readonly id: string;
  readonly type: 'project' | 'zone' | 'document' | 'assembly' | 'element' | 'specification';
  readonly name: string;
  readonly parentId?: string;
  readonly metadata?: Record<string, unknown>;
}

// ─── Source Basis ────────────────────────────────────────────────────────────

export type SourceBasis = 'canonical' | 'derived' | 'draft' | 'compare' | 'mock';

export interface SourcedData<T> {
  readonly data: T;
  readonly basis: SourceBasis;
  readonly sourceAdapter: string;
  readonly timestamp: number;
  readonly isMock: boolean;
}

// ─── Event Payloads ─────────────────────────────────────────────────────────

export interface ObjectSelectedPayload {
  readonly object: ActiveObjectIdentity;
  readonly source: PanelId;
  readonly basis: SourceBasis;
}

export interface ZoneSelectedPayload {
  readonly zoneId: string;
  readonly zoneName: string;
  readonly source: PanelId;
  readonly containedObjects?: readonly string[];
}

export interface ReferenceRequestedPayload {
  readonly objectId: string;
  readonly referenceType: 'spec' | 'code' | 'citation' | 'document' | 'all';
  readonly source: PanelId;
}

export interface CompareRequestedPayload {
  readonly objectIdA: string;
  readonly objectIdB: string;
  readonly compareType: 'version' | 'state' | 'spatial';
  readonly source: PanelId;
}

export interface ArtifactRequestedPayload {
  readonly objectId: string;
  readonly artifactType: 'drawing' | 'report' | 'export';
  readonly format?: string;
  readonly source: PanelId;
}

export interface ValidationRequestedPayload {
  readonly objectId: string;
  readonly validationType: 'structural' | 'domain' | 'geometry' | 'full';
  readonly source: PanelId;
}

export interface ValidationUpdatedPayload {
  readonly objectId: string;
  readonly status: 'pending' | 'running' | 'passed' | 'failed' | 'error';
  readonly issues: readonly ValidationIssue[];
  readonly timestamp: number;
}

export interface ValidationIssue {
  readonly id: string;
  readonly severity: 'error' | 'warning' | 'info';
  readonly message: string;
  readonly rule?: string;
}

export interface ProposalCreatedPayload {
  readonly proposalId: string;
  readonly objectId: string;
  readonly title: string;
  readonly description: string;
  readonly source: PanelId;
}

export interface TaskCreatedPayload {
  readonly taskId: string;
  readonly objectId: string;
  readonly title: string;
  readonly assignee?: string;
  readonly source: PanelId;
}

export interface WorkspaceModeChangedPayload {
  readonly mode: WorkspaceMode;
  readonly previousMode: WorkspaceMode;
}

export interface PanelFollowChangedPayload {
  readonly panelId: PanelId;
  readonly following: boolean;
}

export interface CompanionPinnedPayload {
  readonly panelId: PanelId;
  readonly pinned: boolean;
  readonly deviceClass: DeviceClass;
}

export interface TruthEchoPropagatedPayload {
  readonly object: ActiveObjectIdentity;
  readonly originPanel: PanelId;
  readonly subscribedPanels: readonly PanelId[];
  readonly timestamp: number;
}

export interface TruthEchoFailedPayload {
  readonly reason: 'ambiguous_object' | 'missing_object' | 'propagation_error' | 'adapter_failure';
  readonly originPanel?: PanelId;
  readonly details: string;
  readonly timestamp: number;
}

// ─── Enums / Unions ─────────────────────────────────────────────────────────

export type PanelId = 'explorer' | 'work' | 'reference' | 'spatial' | 'system';

export type WorkspaceMode = 'default' | 'compare' | 'focus' | 'review';

export type DeviceClass = 'ultrawide' | 'desktop' | 'laptop' | 'tablet' | 'phone';

// ─── Event Map ──────────────────────────────────────────────────────────────

export interface EventMap {
  'object.selected': ObjectSelectedPayload;
  'zone.selected': ZoneSelectedPayload;
  'reference.requested': ReferenceRequestedPayload;
  'compare.requested': CompareRequestedPayload;
  'artifact.requested': ArtifactRequestedPayload;
  'validation.requested': ValidationRequestedPayload;
  'validation.updated': ValidationUpdatedPayload;
  'proposal.created': ProposalCreatedPayload;
  'task.created': TaskCreatedPayload;
  'workspace.mode.changed': WorkspaceModeChangedPayload;
  'panel.follow.changed': PanelFollowChangedPayload;
  'companion.pinned': CompanionPinnedPayload;
  'truth-echo.propagated': TruthEchoPropagatedPayload;
  'truth-echo.failed': TruthEchoFailedPayload;
}

export type EventName = keyof EventMap;
