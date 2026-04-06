/**
 * Construction OS Kernel Event Emitter
 * Authority: L0_ARMAND_LEFEBVRE
 * Date: 2026-04-06
 * FAIL_CLOSED on missing registry identity or schema violation.
 */

export type KernelEventType = 'kernel.condition_detected' | 'kernel.assembly_resolved' | 'kernel.validation_passed' | 'kernel.validation_failed' | 'kernel.detail_generated' | 'kernel.artifact_ready' | 'kernel.receipt_recorded' | 'kernel.state_changed';

export interface EntityRef { entity_id: string; entity_type: 'system' | 'assembly' | 'condition' | 'material' | 'rule' | 'detail' | 'artifact' | 'receipt'; registry_id: string; }

export interface KernelEvent { event_id: string; event_type: KernelEventType; schema_version: 'v1'; source_repo: '10-Construction_OS'; authority_level: 'L0' | 'L1' | 'L2' | 'L3'; emitted_at: string; entity_refs: EntityRef[]; payload: Record<string, unknown>; correlation_id?: string; idempotency_key: string; project_id?: string; }

export interface EmissionResult { emitted: boolean; event_id: string; errors: string[]; receipt_id: string | null; }

const VALID_TYPES: ReadonlySet<string> = new Set(['kernel.condition_detected','kernel.assembly_resolved','kernel.validation_passed','kernel.validation_failed','kernel.detail_generated','kernel.artifact_ready','kernel.receipt_recorded','kernel.state_changed']);

export function validateAndEmit(event: KernelEvent): EmissionResult {
  const errors: string[] = [];
  const rid = `RCP-EM-${Date.now()}-${Math.random().toString(36).substring(2, 8)}`;
  if (!VALID_TYPES.has(event.event_type)) errors.push(`Unknown event_type: ${event.event_type}. BLOCKED.`);
  if (event.schema_version !== 'v1') errors.push(`Invalid schema_version. BLOCKED.`);
  if (event.source_repo !== '10-Construction_OS') errors.push(`Invalid source_repo. BLOCKED.`);
  if (!event.entity_refs?.length) errors.push('No entity_refs. BLOCKED.');
  else { for (const ref of event.entity_refs) { if (!ref.registry_id?.trim()) errors.push(`Entity ${ref.entity_id} has no registry_id. BLOCKED.`); } }
  if (!event.event_id) errors.push('Missing event_id. BLOCKED.');
  if (!event.emitted_at) errors.push('Missing emitted_at. BLOCKED.');
  if (!event.idempotency_key) errors.push('Missing idempotency_key. BLOCKED.');
  if (errors.length > 0) return { emitted: false, event_id: event.event_id ?? 'UNKNOWN', errors, receipt_id: null };
  return { emitted: true, event_id: event.event_id, errors: [], receipt_id: rid };
}

export function buildKernelEvent(eventType: KernelEventType, entityRefs: EntityRef[], payload: Record<string, unknown>, opts?: { correlationId?: string; projectId?: string; authorityLevel?: 'L0'|'L1'|'L2'|'L3' }): KernelEvent {
  const id = `EVT-${Date.now()}-${Math.random().toString(36).substring(2, 10)}`;
  return { event_id: id, event_type: eventType, schema_version: 'v1', source_repo: '10-Construction_OS', authority_level: opts?.authorityLevel ?? 'L2', emitted_at: new Date().toISOString(), entity_refs: entityRefs, payload, correlation_id: opts?.correlationId, idempotency_key: `${eventType}-${id}`, project_id: opts?.projectId };
}
