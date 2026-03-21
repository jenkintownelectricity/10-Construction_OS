# Worker Strategy — Construction OS

## Purpose

Panels are live systems with potential for expensive computation. Workers keep the main thread responsive.

## Worker-Backed Seam: Validation Worker

### Implementation
- **File**: `src/ui/workers/validation.worker.ts`
- **Hook**: `src/ui/workers/useValidationWorker.ts`
- **Consumer**: WorkPanel (validation tab, "Validate (Worker)" button)

### Architecture
```
Main Thread                          Worker Thread
─────────────                        ─────────────
WorkPanel                            validation.worker.ts
  │                                    │
  ├── useValidationWorker hook         │
  │   ├── Creates Worker on mount      │
  │   ├── Sends validate message ─────▶│ Receives message
  │   │                                │ Performs computation
  │   │                                │ (100K iterations simulation)
  │   ◀── Receives result ────────────│ Posts result
  │   └── Updates React state          │
  │                                    │
  └── Emits validation.updated event   │
```

### Worker Protocol
```typescript
// Request
{ type: 'validate', objectId: string, validationType: string }

// Response
{ type: 'validation-result', objectId: string, status: string, issues: [], computeTimeMs: number }
```

### Performance Evidence
The worker performs 100,000 iterations of `Math.sqrt * Math.sin` to simulate real computation. The `computeTimeMs` field reports actual computation time, visible in the WorkPanel validation tab.

## Worker-Ready Boundaries

The following areas are designed for future worker offload:
1. **Validation computation** — IMPLEMENTED via validation.worker.ts
2. **Spatial view rendering** — SVG computation could be offloaded to worker for complex scenes
3. **Search/filter** — Large project tree filtering could be worker-backed
4. **Reference resolution** — Cross-referencing large document sets

## Performance Rules

1. **Lazy loading**: Non-primary panel systems can be lazily loaded (Dockview handles this via component registration).
2. **Microtask event delivery**: The event bus uses `queueMicrotask` to prevent synchronous cascade storms.
3. **Panel isolation**: Each panel manages its own state — no cross-panel rerender storms.
4. **Truth Echo efficiency**: Propagation events are lightweight (IDs + metadata, not full objects). Panels decide independently what to refetch.
5. **Scalability**: The panel registry pattern supports N panels. Adding a 6th+ panel requires only a new registry entry, component, and adapter.
