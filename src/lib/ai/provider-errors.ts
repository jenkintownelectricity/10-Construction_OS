import type { AIError, ErrorType, ProviderId } from "./provider-types";

export class ProviderError extends Error {
  public readonly provider: ProviderId;
  public readonly errorType: ErrorType;
  public readonly retryable: boolean;
  public readonly statusCode?: number;
  public readonly rawCategory?: string;

  constructor(error: AIError) {
    super(error.message);
    this.name = "ProviderError";
    this.provider = error.provider;
    this.errorType = error.errorType;
    this.retryable = error.retryable;
    this.statusCode = error.statusCode;
    this.rawCategory = error.rawCategory;
  }

  toJSON(): AIError {
    return {
      provider: this.provider,
      errorType: this.errorType,
      message: this.message,
      retryable: this.retryable,
      statusCode: this.statusCode,
      rawCategory: this.rawCategory,
    };
  }
}

export function normalizeError(provider: ProviderId, err: unknown): ProviderError {
  if (err instanceof ProviderError) return err;

  const raw = err instanceof Error ? err : new Error(String(err));
  const message = raw.message.toLowerCase();
  const statusCode = (err as { status?: number })?.status;

  let errorType: ErrorType = "provider_error";
  let retryable = false;

  if (statusCode === 401 || statusCode === 403 || message.includes("api key") || message.includes("unauthorized") || message.includes("authentication")) {
    errorType = "auth_error";
  } else if (statusCode === 429 || message.includes("rate limit") || message.includes("quota")) {
    errorType = "quota_error";
    retryable = true;
  } else if (message.includes("timeout") || message.includes("timed out") || message.includes("ETIMEDOUT")) {
    errorType = "timeout_error";
    retryable = true;
  } else if (statusCode === 503 || statusCode === 502 || message.includes("unavailable") || message.includes("ECONNREFUSED")) {
    errorType = "unavailable_error";
    retryable = true;
  } else if (statusCode === 400 || message.includes("invalid")) {
    errorType = "validation_error";
  } else if (statusCode && statusCode >= 500) {
    errorType = "provider_error";
    retryable = true;
  }

  return new ProviderError({
    provider,
    errorType,
    message: raw.message,
    retryable,
    statusCode,
    rawCategory: raw.name,
  });
}
