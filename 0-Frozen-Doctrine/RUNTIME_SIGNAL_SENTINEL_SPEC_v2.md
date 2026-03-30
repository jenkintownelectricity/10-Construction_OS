# Construction OS v2 — Runtime Signal Sentinel Specification

## Authority

Armand Lefebvre, L0 — Lefebvre Design Solutions LLC

## Purpose

Defines how runtime signals are observed, validated, and gated by sentinels
at seam boundaries within Construction OS v2.

## Sentinel Model

Sentinels are non-authoritative observers positioned at seam boundaries.
They do not own truth. They observe transitions and produce receipts.

## Signal Types

| Signal Type | Description |
|-------------|-------------|
| doctrine_activation | Doctrine file loaded and validated |
| authority_transition | Control passes from governance to engine |
| truth_relay | Truth data moves between planes |
| state_admission | State change proposed for admission |
| publication_event | Data surfaces to application layer |
| boundary_exit | Data leaves the system boundary |

## Sentinel Responsibilities

1. Observe signal at seam boundary
2. Validate signal against seam contract
3. Produce observation receipt
4. Tag signal with observation metadata
5. Block, tag, or downgrade signal based on seam posture

## Sentinel Prohibitions

- Sentinels must not create truth
- Sentinels must not modify signal content
- Sentinels must not self-authorize
- Sentinels must not bypass seam contracts

## Doctrine Lock

Seam-Gated Sentinel Observation
