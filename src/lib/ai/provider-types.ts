// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// AI Control Plane — Type Definitions
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

export type ProviderId = "openai" | "anthropic" | "gemini" | "groq";

export type CapabilityClass =
  | "detail_explainer"
  | "observation_classifier"
  | "related_detail_suggester"
  | "manufacturer_note_drafter"
  | "assembly_summarizer"
  | "field_note_cleaner"
  | "artifact_summary"
  | "premium_reasoning"
  | "fast_classification";

export type ProviderPreset = "fast" | "low_cost" | "balanced" | "premium_reasoning" | "multimodal_ready";

export type HealthStatus = "healthy" | "degraded" | "unavailable" | "misconfigured";

export type ErrorType =
  | "auth_error"
  | "config_error"
  | "timeout_error"
  | "quota_error"
  | "provider_error"
  | "validation_error"
  | "unavailable_error";

export type FinishReason = "stop" | "length" | "content_filter" | "error" | "unknown";

// ─── Provider Configuration ─────────────────

export interface ProviderConfig {
  id: ProviderId;
  name: string;
  enabled: boolean;
  apiKeySet: boolean;
  apiKeyMasked: string;
  defaultModel: string;
  baseUrl?: string;
  models: ModelInfo[];
  healthStatus: HealthStatus;
  lastHealthCheck?: string;
  lastLatencyMs?: number;
}

export interface ModelInfo {
  id: string;
  name: string;
  capabilities: CapabilityClass[];
  contextWindow: number;
  supportsStreaming: boolean;
}

// ─── Request / Response ─────────────────────

export interface AIRequest {
  provider: ProviderId;
  model: string;
  capability?: CapabilityClass;
  system?: string;
  messages: AIMessage[];
  temperature?: number;
  maxTokens?: number;
  timeoutMs?: number;
}

export interface AIMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export interface AIResponse {
  provider: ProviderId;
  model: string;
  text: string;
  usage: TokenUsage;
  latencyMs: number;
  finishReason: FinishReason;
  metadata: Record<string, unknown>;
}

export interface TokenUsage {
  promptTokens: number;
  completionTokens: number;
  totalTokens: number;
}

// ─── Errors ─────────────────────────────────

export interface AIError {
  provider: ProviderId;
  errorType: ErrorType;
  message: string;
  retryable: boolean;
  statusCode?: number;
  rawCategory?: string;
}

// ─── Settings ───────────────────────────────

export interface AISettings {
  defaultProvider: ProviderId;
  fallbackProvider: ProviderId;
  activePreset: ProviderPreset;
  defaultTemperature: number;
  defaultMaxTokens: number;
  timeoutMs: number;
  streamingEnabled: boolean;
  providers: Record<ProviderId, ProviderSettings>;
  routing: RoutingPolicy;
}

export interface ProviderSettings {
  enabled: boolean;
  defaultModel: string;
  baseUrl?: string;
}

// ─── Routing ────────────────────────────────

export interface RoutingPolicy {
  presets: Record<ProviderPreset, RoutingPresetConfig>;
  capabilityMap: Record<CapabilityClass, CapabilityRouting>;
  fallbackChain: ProviderId[];
}

export interface RoutingPresetConfig {
  preferredProviders: ProviderId[];
  description: string;
}

export interface CapabilityRouting {
  preferredProvider: ProviderId;
  fallbacks: ProviderId[];
  preset: ProviderPreset;
}

// ─── Health ─────────────────────────────────

export interface ProviderHealth {
  provider: ProviderId;
  status: HealthStatus;
  lastCheck: string;
  latencyMs?: number;
  consecutiveFailures: number;
  circuitOpen: boolean;
  reason?: string;
}
