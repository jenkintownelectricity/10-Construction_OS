/**
 * Construction OS — Panel Registry
 *
 * Central registry for all panel system definitions.
 * Panels declare their state ownership, event subscriptions,
 * and Truth Echo participation here.
 */

import type { PanelId, EventName } from '../contracts/events';

export interface PanelDefinition {
  id: PanelId;
  title: string;
  description: string;
  /** Events this panel subscribes to */
  subscribesTo: readonly EventName[];
  /** Events this panel may emit */
  emits: readonly EventName[];
  /** Whether this panel participates in Truth Echo */
  truthEchoSubscriber: boolean;
  /** State this panel owns */
  ownedState: readonly string[];
  /** Default size weight for dockview */
  defaultSizeWeight: number;
}

export const PANEL_DEFINITIONS: Record<PanelId, PanelDefinition> = {
  explorer: {
    id: 'explorer',
    title: 'Explorer',
    description: 'Project hierarchy, search, filter, object/document/zone selection',
    subscribesTo: ['truth-echo.propagated', 'zone.selected', 'validation.updated'],
    emits: ['object.selected', 'zone.selected', 'reference.requested'],
    truthEchoSubscriber: true,
    ownedState: ['selectedNodeId', 'expandedNodes', 'searchQuery', 'filterState'],
    defaultSizeWeight: 200,
  },
  work: {
    id: 'work',
    title: 'Work',
    description: 'Primary live work surface — detail, drawing, artifact workspace',
    subscribesTo: ['truth-echo.propagated', 'object.selected', 'validation.updated', 'workspace.mode.changed'],
    emits: ['object.selected', 'validation.requested', 'artifact.requested', 'compare.requested'],
    truthEchoSubscriber: true,
    ownedState: ['activeTab', 'draftState', 'localCommands'],
    defaultSizeWeight: 400,
  },
  reference: {
    id: 'reference',
    title: 'Reference',
    description: 'Specs, code, source docs, citations — compare-ready, source basis visibility',
    subscribesTo: ['truth-echo.propagated', 'reference.requested', 'compare.requested'],
    emits: ['object.selected', 'compare.requested'],
    truthEchoSubscriber: true,
    ownedState: ['activeReferences', 'compareState', 'referenceFilter'],
    defaultSizeWeight: 250,
  },
  spatial: {
    id: 'spatial',
    title: 'Spatial',
    description: 'Atlas, plan, zone, location — selected object spatial context',
    subscribesTo: ['truth-echo.propagated', 'object.selected', 'zone.selected'],
    emits: ['object.selected', 'zone.selected'],
    truthEchoSubscriber: true,
    ownedState: ['viewportState', 'activeZoneId', 'selectedSpatialObject', 'layerVisibility'],
    defaultSizeWeight: 300,
  },
  system: {
    id: 'system',
    title: 'System',
    description: 'Validation summary, alerts, mailbox/proposals, tasks, activity log, intelligence',
    subscribesTo: ['truth-echo.propagated', 'validation.updated', 'proposal.created', 'task.created', 'truth-echo.failed'],
    emits: ['validation.requested', 'task.created', 'proposal.created'],
    truthEchoSubscriber: true,
    ownedState: ['activeTab', 'validationSummary', 'tasks', 'proposals', 'alerts'],
    defaultSizeWeight: 200,
  },
  awareness: {
    id: 'awareness',
    title: 'Awareness',
    description: 'Awareness Cache snapshot — conditions, artifacts, proposals, FAIL_CLOSED log',
    subscribesTo: ['truth-echo.propagated'],
    emits: [],
    truthEchoSubscriber: true,
    ownedState: ['awarenessState', 'activeTab'],
    defaultSizeWeight: 250,
  },
  proposals: {
    id: 'proposals',
    title: 'Proposal Mailbox',
    description: 'Proposal review — approve/reject/elaborate workflow routed to Ring 1',
    subscribesTo: ['truth-echo.propagated', 'proposal.created'],
    emits: ['proposal.created'],
    truthEchoSubscriber: true,
    ownedState: ['proposals', 'filter', 'actionInFlight'],
    defaultSizeWeight: 250,
  },
  diagnostics: {
    id: 'diagnostics',
    title: 'Runtime Diagnostics',
    description: 'Pipeline state, runtime events, artifact lifecycle, FAIL_CLOSED visibility',
    subscribesTo: ['truth-echo.propagated'],
    emits: [],
    truthEchoSubscriber: true,
    ownedState: ['diagnosticsState', 'activeTab'],
    defaultSizeWeight: 300,
  },
  assistant: {
    id: 'assistant',
    title: 'Assistant Console',
    description: 'Bounded assistant output — no execution authority, proposals route to mailbox',
    subscribesTo: ['truth-echo.propagated'],
    emits: ['proposal.created'],
    truthEchoSubscriber: true,
    ownedState: ['responses', 'query', 'submitting'],
    defaultSizeWeight: 250,
  },
  'detail-viewer': {
    id: 'detail-viewer',
    title: 'Detail Viewer',
    description: 'Runtime-derived detail artifact viewer — SVG preview, DXF download, artifact metadata, fail-closed diagnostics',
    subscribesTo: ['truth-echo.propagated', 'generation.completed'],
    emits: ['artifact.requested'],
    truthEchoSubscriber: true,
    ownedState: ['previewResult', 'activeTab', 'selectedCategory'],
    defaultSizeWeight: 400,
  },
};

export const ALL_PANELS: PanelId[] = ['explorer', 'work', 'reference', 'spatial', 'system', 'awareness', 'proposals', 'diagnostics', 'assistant', 'detail-viewer'];
