/**
 * React hook for subscribing to the active object store
 */

import { useSyncExternalStore } from 'react';
import { activeObjectStore, type ActiveObjectState } from './activeObjectStore';

export function useActiveObject(): ActiveObjectState {
  return useSyncExternalStore(
    activeObjectStore.subscribe,
    activeObjectStore.getState,
    activeObjectStore.getState
  );
}
