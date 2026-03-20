# Compatibility Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory contains compatibility testing artifacts for the `gcp_shopdrawing` mirror. Compatibility testing verifies that the mirror works correctly with its environment: the Construction Kernel version, consumer systems, the GCP source APIs, and the trust boundary mediation layer.

---

## What Is Compatibility Testing

Compatibility testing ensures that:

1. **Kernel compatibility.** The mirror operates correctly with the current Construction Kernel version and will continue to work across the supported kernel version range (0.6.0 to 1.x).

2. **Source API compatibility.** The mirror's sync agent correctly communicates with GCP's current API version. Schema changes at GCP are detected and handled.

3. **Consumer compatibility.** Canonical records produced by the mirror are consumable by all registered consumers without transformation errors.

4. **Trust boundary compatibility.** The mediation layer correctly transforms all data types currently flowing through the boundary.

---

## Testing Categories

### Kernel Version Compatibility

| Test | Description | Frequency |
|------|-------------|-----------|
| Minimum version | Mirror operates on kernel 0.6.0 | On kernel upgrade |
| Current version | Mirror operates on current kernel | Continuous |
| Forward compatibility | Mirror handles deprecated kernel APIs gracefully | On kernel pre-release |

### Source API Compatibility

| Test | Description | Frequency |
|------|-------------|-----------|
| API response schema | GCP API responses match expected schema | Every sync cycle |
| API version negotiation | Sync agent correctly negotiates API version | Weekly |
| Rate limit compliance | Sync agent respects rate limits | Continuous |
| Error response handling | Sync agent handles all GCP error codes | Monthly |

### Consumer Compatibility

| Test | Description | Frequency |
|------|-------------|-----------|
| Schema validation | Canonical records pass consumer schema validation | Every sync cycle |
| Backward compatibility | Schema changes are backward-compatible with existing consumers | On schema change |
| Null handling | Consumers handle optional fields correctly | Monthly |

### Trust Boundary Compatibility

| Test | Description | Frequency |
|------|-------------|-----------|
| Transform correctness | All mediation transforms produce valid canonical output | Every sync cycle |
| Vocabulary mapping | All source enumerations map to valid OS vocabulary | On vocabulary change |
| ID mapping | All source IDs map to valid mirror-scoped IDs | Every sync cycle |

---

## Directory Structure

```
compatibility/
  kernel/                  # Kernel version compatibility test results
  source-api/              # GCP API compatibility test results
  consumers/               # Consumer compatibility test results
  trust-boundary/          # Trust boundary compatibility test results
  reports/                 # Aggregate compatibility reports
```

---

## Compatibility Failure Response

If a compatibility test fails:

1. **Isolate** the incompatibility. Is it kernel, source, consumer, or boundary?
2. **Assess** the impact. Is data flowing incorrectly, or is the failure a future risk?
3. **Remediate** at the appropriate layer. Do not patch around incompatibilities.
4. **Re-test** after remediation.
5. **Document** the incompatibility and resolution for future reference.
