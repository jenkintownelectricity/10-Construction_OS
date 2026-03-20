# Transfer Directory: GCP Shop Drawing Mirror

**Mirror ID:** `gcp_shopdrawing`
**Last Updated:** 2026-03-20

---

## Purpose

This directory contains artifacts related to data transfer operations for the `gcp_shopdrawing` mirror. Transfer encompasses the movement of reflected data between environments, the migration of reflections during mirror replacement, and the handoff of mirror ownership between teams.

---

## Types of Transfer

### 1. Environment Transfer

Moving reflected data between Construction OS environments (development, staging, production). This is needed for:

- Testing mirror configuration in non-production environments.
- Promoting mirror configuration from staging to production.
- Seeding development environments with representative reflected data.

**Rules:**
- Reflected data transfers between environments use the canonical format only.
- No GCP-native data is transferred. The mediation layer runs in each environment independently.
- Production data transferred to non-production environments must be anonymized (opaque actor tokens are already anonymized; no additional PII exists in reflections).

### 2. Mirror Replacement Transfer

Migrating consumers from one mirror to a replacement mirror (e.g., when GCP is replaced by a different source system). This is the most architecturally significant type of transfer.

**Rules:**
- Old mirror data and new mirror data coexist during the transition period.
- Consumer migration is explicit and tracked. No silent cutover.
- The old mirror's data remains available as historical record.
- The new mirror produces data in the same canonical format. Consumer-side changes should be minimal or zero.

### 3. Ownership Transfer

Transferring responsibility for the mirror from one team to another within the Construction OS organization.

**Rules:**
- All documentation, credentials, and operational knowledge are transferred.
- The receiving team must pass the activation checklist before accepting ownership.
- A transition period with shared responsibility is required.

---

## Directory Structure

```
transfer/
  environment/             # Environment transfer procedures and logs
  replacement/             # Mirror replacement transfer plans
  ownership/               # Ownership transfer records
  templates/               # Transfer plan templates
```

---

## Transfer Principles

1. **Canonical format only.** All transfers use the Construction OS canonical format. GCP-native formats never appear in transfer artifacts.
2. **Idempotent operations.** Transfer operations can be safely repeated without creating duplicates or inconsistencies.
3. **Audited.** Every transfer operation is logged with who, what, when, and why.
4. **Reversible.** Transfers can be rolled back within a defined window.
5. **Non-destructive.** The source of the transfer is never modified or deleted by the transfer operation.
