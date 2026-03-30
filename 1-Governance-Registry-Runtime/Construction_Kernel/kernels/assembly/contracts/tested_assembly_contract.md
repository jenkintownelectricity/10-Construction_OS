# Tested Assembly Contract

## Purpose

Defines the truth exchange contract for tested_assembly_record entries. Tested assembly records document specific configurations validated by specific tests under specific standards.

## Schema

`schemas/tested_assembly_record.schema.json`

## Required Fields

| Field | Type | Constraint |
|---|---|---|
| schema_version | string | Must be "v1" |
| record_id | string | Unique, non-empty |
| title | string | Describes the tested configuration |
| test_type | enum | fire_rating, wind_uplift, structural, air_leakage, water_penetration, thermal |
| test_standard_ref | string | Valid standards reference ID |
| result | string | Test outcome |
| status | enum | active, draft, deprecated |

## Invariants

1. Tested assembly records are immutable once status is `active`. They cannot be modified.
2. The test_standard_ref must reference a valid standard from the shared standards registry.
3. The result field must accurately reflect the test outcome without interpretation.
4. If assembly_ref is provided, it must reference a valid assembly_system.
5. If evidence_ref is provided, it should point to the actual test report.
6. A test record does not imply that substituted configurations also pass.

## Immutability Rule

Once a tested assembly record achieves `active` status, no field may be changed. If a test is invalidated, the record is set to `deprecated` and a note explains the reason. A new test creates a new record.

## Consumers

- Assembly system records — reference via tested_assembly_refs
- Construction_Reference_Intelligence — test coverage gap analysis
- Specification compliance verification tools

## Change Policy

Immutable. No amendments. Deprecation only with documented justification.
