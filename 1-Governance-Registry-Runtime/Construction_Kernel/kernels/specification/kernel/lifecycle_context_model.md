# Lifecycle Context Model — Construction Specification Kernel

## Purpose

This model defines how specification requirements relate to project lifecycle stages. Not all requirements are relevant at all stages — insulation R-value requirements are established at design but verified at installation, while warranty requirements are exercised at commissioning and throughout operation.

## Lifecycle Stages

From `shared_enum_registry.json`:

- **design** — specification authoring, coordination, design review
- **procurement** — bidding, submittal review, material ordering
- **installation** — field execution, mock-ups, in-progress testing
- **commissioning** — system verification, performance testing
- **operation** — normal building use, warranty period
- **maintenance** — scheduled and reactive maintenance activities
- **failure** — performance failure, investigation, forensic analysis
- **replacement** — system replacement, re-specification

## Requirement-to-Stage Mapping

| Requirement Type | Primary Stage | Secondary Stages |
|---|---|---|
| Material performance criteria | design | procurement, installation |
| Submittal requirements | procurement | design |
| Qualification requirements | procurement | installation |
| Installation method requirements | installation | design |
| Testing requirements (mock-up) | installation | design |
| Testing requirements (field test) | installation | commissioning |
| Warranty requirements | commissioning | operation, maintenance |
| Maintenance obligations | operation | maintenance |
| Performance criteria verification | commissioning | operation |

## Recording Lifecycle Context

The `lifecycle_stage` field on requirement records indicates the primary lifecycle stage where the requirement is exercised. This field uses values from the shared enum registry.

When a requirement spans multiple stages, the primary stage is recorded in `lifecycle_stage` and secondary stages are noted in the `notes` field. The kernel does not support array-valued lifecycle_stage to maintain schema simplicity.

## Lifecycle and Evidence

Evidence requirements are lifecycle-sensitive:

- Design stage: evidence is specification text and referenced standards
- Procurement stage: evidence is submittals, qualifications, and certifications
- Installation stage: evidence is test reports, inspection records, and mock-up results
- Commissioning stage: evidence is performance test results
- Operation stage: evidence is warranty documentation and maintenance records

## Stage-Dependent Specification Sections

Some specification sections are primarily relevant at specific stages:

- Part 1 (General) — design and procurement
- Part 2 (Products) — procurement
- Part 3 (Execution) — installation and commissioning

This three-part CSI format aligns with lifecycle stages, though the kernel records the stage explicitly rather than inferring from section structure.

## Lifecycle Gaps

When a specification does not address a lifecycle stage that should be covered (e.g., no maintenance requirements for a system with a 20-year warranty), this gap can be flagged via `ambiguity_flag` on related records.
