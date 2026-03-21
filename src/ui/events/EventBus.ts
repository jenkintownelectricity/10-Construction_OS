/**
 * Construction OS — Central Event Bus
 *
 * All panel-to-panel communication flows through this bus.
 * Direct panel-to-panel calls are forbidden.
 * Events use lightweight typed payloads (IDs + metadata).
 * Ambiguous or missing targets fail closed.
 */

import type { EventMap, EventName } from '../contracts/events';

type Handler<T> = (payload: T) => void;

interface EventBusOptions {
  /** Enable debug logging of all events */
  debug?: boolean;
}

class EventBusImpl {
  private handlers = new Map<string, Set<Handler<unknown>>>();
  private debug: boolean;
  private eventLog: Array<{ event: string; payload: unknown; timestamp: number }> = [];
  private maxLogSize = 200;

  constructor(options: EventBusOptions = {}) {
    this.debug = options.debug ?? false;
  }

  on<E extends EventName>(event: E, handler: Handler<EventMap[E]>): () => void {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, new Set());
    }
    const set = this.handlers.get(event)!;
    set.add(handler as Handler<unknown>);

    // Return unsubscribe function
    return () => {
      set.delete(handler as Handler<unknown>);
      if (set.size === 0) {
        this.handlers.delete(event);
      }
    };
  }

  emit<E extends EventName>(event: E, payload: EventMap[E]): void {
    if (this.debug) {
      console.debug(`[EventBus] ${event}`, payload);
    }

    this.eventLog.push({ event, payload, timestamp: Date.now() });
    if (this.eventLog.length > this.maxLogSize) {
      this.eventLog.shift();
    }

    const set = this.handlers.get(event);
    if (!set || set.size === 0) {
      // No handlers — this is acceptable, not an error.
      return;
    }

    // Use microtask to prevent synchronous cascade storms
    for (const handler of set) {
      queueMicrotask(() => {
        try {
          handler(payload);
        } catch (err) {
          console.error(`[EventBus] Handler error for ${event}:`, err);
        }
      });
    }
  }

  /** Get recent event log for debugging */
  getLog() {
    return [...this.eventLog];
  }

  /** Clear all handlers (for testing) */
  clear() {
    this.handlers.clear();
    this.eventLog = [];
  }

  /** Get handler count for a given event (for testing) */
  listenerCount(event: EventName): number {
    return this.handlers.get(event)?.size ?? 0;
  }
}

// Singleton event bus instance
export const eventBus = new EventBusImpl({ debug: import.meta.env?.DEV ?? false });

// Export class for testing
export { EventBusImpl };
