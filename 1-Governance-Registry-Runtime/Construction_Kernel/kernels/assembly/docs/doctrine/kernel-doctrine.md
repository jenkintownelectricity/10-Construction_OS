# Kernel Doctrine — Construction Assembly Kernel

## Purpose

The Construction Assembly Kernel is the single source of truth for assembly-domain knowledge within the construction-kernel family. It captures how building enclosure systems are composed, layered, connected, and validated.

## Core Principles

### 1. Assemblies Are Layered Systems, Not Product Lists

An assembly is an ordered stack of layers, each assigned to one or more control-layer functions. The kernel records layer position, control-layer assignment, attachment method, and continuity status. Product selection is downstream of assembly design.

### 2. Control-Layer Continuity Is the Organizing Principle

Every assembly exists to maintain one or more of the 11 control layers defined in the shared registry. The kernel tracks whether each control layer is continuous, interrupted, terminated, or transitioned at every boundary, transition, and penetration.

### 3. Fail-Closed Posture

When assembly data is incomplete, ambiguous, or conflicting, the kernel does not guess. It records the known state and flags the gap. No assembly record is promoted to `active` status without all required fields populated and validated against schema.

### 4. Division 07 as Control-Layer System

CSI Division 07 — Building Envelope Systems — is the initial domain focus. The kernel treats Division 07 not as a product catalog but as a system of control layers that must be maintained across roofs, walls, below-grade assemblies, transitions, penetrations, and edge conditions.

### 5. Interface Zones Are First-Class Objects

Transitions, penetrations, edge conditions, and tie-ins are not secondary details. They are where assemblies succeed or fail. The kernel models these as distinct objects with their own schemas, risk postures, and evidence requirements.

### 6. Standards-Aware, Not Standards-Reproducing

The kernel references IBC, NFPA 285, ASHRAE 90.1, ASTM test standards, and FM Global requirements by citation. It does not reproduce standards text. Compliance is tracked as a property of tested assembly records.

### 7. Evidence-Linked

Every assembly configuration, test result, and continuity claim should be traceable to evidence: test reports, field observations, manufacturer data, or forensic findings. Evidence is referenced, not duplicated.

## Governance

- Schema validation is mandatory before any record enters the kernel.
- All enums are drawn from the shared registry at `Construction_Reference_Intelligence/shared/`.
- Records use append-only revision with full lineage tracking.
- No kernel record may contradict a validated tested assembly record without explicit override justification.
