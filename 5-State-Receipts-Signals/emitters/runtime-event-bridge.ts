/**
 * Construction OS Runtime Event Bridge
 * Authority: L0_ARMAND_LEFEBVRE
 * Wires kernel-event-emitter into runtime. FAIL_CLOSED on schema mismatch.
 */

import { buildKernelEvent, validateAndEmit } from './kernel-event-emitter';
import type { KernelEventType, EntityRef, KernelEvent } from './kernel-event-emitter';

export interface EventSink { send(event: KernelEvent): Promise<{ accepted: boolean; error?: string }>; }
export interface RuntimeEventBridgeConfig { sink: EventSink; onEmissionBlocked?: (event: KernelEvent, errors: string[]) => void; }

export class RuntimeEventBridge {
  private sink: EventSink;
  private onBlocked?: (event: KernelEvent, errors: string[]) => void;
  private emittedCount = 0;
  private blockedCount = 0;

  constructor(config: RuntimeEventBridgeConfig) { this.sink = config.sink; this.onBlocked = config.onEmissionBlocked; }

  async emit(eventType: KernelEventType, entityRefs: EntityRef[], payload: Record<string, unknown>, options?: { correlationId?: string; projectId?: string }): Promise<{ emitted: boolean; event_id: string; errors: string[] }> {
    const event = buildKernelEvent(eventType, entityRefs, payload, options);
    const validation = validateAndEmit(event);
    if (!validation.emitted) { this.blockedCount++; this.onBlocked?.(event, validation.errors); return { emitted: false, event_id: validation.event_id, errors: validation.errors }; }
    const result = await this.sink.send(event);
    if (!result.accepted) { this.blockedCount++; return { emitted: false, event_id: event.event_id, errors: [result.error ?? 'Sink rejected'] }; }
    this.emittedCount++;
    return { emitted: true, event_id: event.event_id, errors: [] };
  }

  async emitSystemCreated(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.condition_detected', [ref], { ...payload, sub_type: 'system_created' }, { correlationId: cid }); }
  async emitAssemblyCreated(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.assembly_resolved', [ref], payload, { correlationId: cid }); }
  async emitConditionDetected(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.condition_detected', [ref], payload, { correlationId: cid }); }
  async emitRuleAdded(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.validation_passed', [ref], { ...payload, sub_type: 'rule_added' }, { correlationId: cid }); }
  async emitMaterialAdded(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.condition_detected', [ref], { ...payload, sub_type: 'material_added' }, { correlationId: cid }); }
  async emitDetailGenerated(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.detail_generated', [ref], payload, { correlationId: cid }); }
  async emitPipelineStageChanged(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.state_changed', [ref], payload, { correlationId: cid }); }
  async emitReceiptCreated(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.receipt_recorded', [ref], payload, { correlationId: cid }); }
  async emitArtifactReady(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.artifact_ready', [ref], payload, { correlationId: cid }); }
  async emitValidationFailed(ref: EntityRef, payload: Record<string, unknown>, cid?: string) { return this.emit('kernel.validation_failed', [ref], payload, { correlationId: cid }); }

  getStats() { return { emitted: this.emittedCount, blocked: this.blockedCount }; }
}
