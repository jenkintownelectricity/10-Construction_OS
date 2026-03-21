/**
 * Construction OS — Truth Echo Orchestrator
 *
 * Truth Echo: when the active object changes in any subscribed live system,
 * the entire cockpit reorients around that same object in a governed way.
 *
 * - Listens for object.selected and zone.selected events
 * - Updates the canonical active object store
 * - Emits truth-echo.propagated to all subscribed panels
 * - Fails closed on ambiguous or missing active object state
 * - Does NOT allow direct panel-to-panel calls
 */

import { eventBus } from '../events/EventBus';
import { activeObjectStore } from '../stores/activeObjectStore';
import type {
  ObjectSelectedPayload,
  ZoneSelectedPayload,
  PanelId,
  TruthEchoPropagatedPayload,
  TruthEchoFailedPayload,
} from '../contracts/events';

let initialized = false;
const unsubscribers: Array<() => void> = [];

export function initTruthEcho(): void {
  if (initialized) return;
  initialized = true;

  // Listen for object selections from any panel
  unsubscribers.push(
    eventBus.on('object.selected', handleObjectSelected)
  );

  // Listen for zone selections (spatial → explorer context)
  unsubscribers.push(
    eventBus.on('zone.selected', handleZoneSelected)
  );
}

export function destroyTruthEcho(): void {
  for (const unsub of unsubscribers) {
    unsub();
  }
  unsubscribers.length = 0;
  initialized = false;
}

function handleObjectSelected(payload: ObjectSelectedPayload): void {
  const { object, source, basis } = payload;

  // Fail closed: reject null/ambiguous objects
  if (!object || !object.id) {
    const failure: TruthEchoFailedPayload = {
      reason: 'ambiguous_object',
      originPanel: source,
      details: `Object selected from ${source} has no valid identity`,
      timestamp: Date.now(),
    };
    eventBus.emit('truth-echo.failed', failure);
    activeObjectStore.setEchoFailure(failure.details);
    return;
  }

  // Update canonical active object
  const success = activeObjectStore.setActiveObject(object, source, basis);
  if (!success) {
    const failure: TruthEchoFailedPayload = {
      reason: 'missing_object',
      originPanel: source,
      details: `Failed to set active object from ${source}`,
      timestamp: Date.now(),
    };
    eventBus.emit('truth-echo.failed', failure);
    return;
  }

  // Propagate to all following panels except the source
  propagateEcho(object, source);
}

function handleZoneSelected(payload: ZoneSelectedPayload): void {
  const { zoneId, zoneName, source } = payload;

  if (!zoneId) {
    const failure: TruthEchoFailedPayload = {
      reason: 'ambiguous_object',
      originPanel: source,
      details: `Zone selected from ${source} has no valid id`,
      timestamp: Date.now(),
    };
    eventBus.emit('truth-echo.failed', failure);
    return;
  }

  // Convert zone selection to object identity
  const zoneObject = {
    id: zoneId,
    type: 'zone' as const,
    name: zoneName,
  };

  const success = activeObjectStore.setActiveObject(zoneObject, source, 'mock');
  if (!success) return;

  propagateEcho(zoneObject, source);
}

function propagateEcho(
  object: { id: string; type: string; name: string },
  originPanel: PanelId
): void {
  const state = activeObjectStore.getState();
  const subscribedPanels = Array.from(state.followingPanels).filter(
    (p) => p !== originPanel
  ) as PanelId[];

  const propagation: TruthEchoPropagatedPayload = {
    object: object as TruthEchoPropagatedPayload['object'],
    originPanel,
    subscribedPanels,
    timestamp: Date.now(),
  };

  eventBus.emit('truth-echo.propagated', propagation);
}
