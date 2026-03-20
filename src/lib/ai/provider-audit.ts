import type { ProviderId, CapabilityClass, ProviderPreset } from "./provider-types";
import type { RoutingDecision } from "./provider-routing";

export interface AuditEntry {
  timestamp: string;
  action: "request" | "response" | "error" | "fallback" | "routing_decision" | "config_change" | "health_change";
  provider: ProviderId;
  detail: string;
  metadata?: Record<string, unknown>;
}

const auditLog: AuditEntry[] = [];
const MAX_ENTRIES = 1000;

export function logAudit(entry: Omit<AuditEntry, "timestamp">): void {
  auditLog.push({ ...entry, timestamp: new Date().toISOString() });
  if (auditLog.length > MAX_ENTRIES) {
    auditLog.splice(0, auditLog.length - MAX_ENTRIES);
  }
}

export function logRoutingDecision(decision: RoutingDecision, capability?: CapabilityClass, preset?: ProviderPreset): void {
  logAudit({
    action: decision.isFallback ? "fallback" : "routing_decision",
    provider: decision.provider,
    detail: decision.reason,
    metadata: {
      capability,
      preset,
      isFallback: decision.isFallback,
      originalProvider: decision.originalProvider,
    },
  });
}

export function getRecentAuditEntries(limit = 50): AuditEntry[] {
  return auditLog.slice(-limit);
}
