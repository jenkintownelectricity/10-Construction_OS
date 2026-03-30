# Construction OS v2 — Intent Identity Sentinel Specification

## Authority

Armand Lefebvre, L0 — Lefebvre Design Solutions LLC

## Purpose

Defines how intent identity is preserved and validated as truth flows
through the Construction OS v2 system.

## Intent Identity

Every governed action carries an intent identity that traces back to:

1. The authorizing governance command
2. The truth plane that sourced the data
3. The seam boundary it crossed

## Identity Preservation Rules

1. Intent identity must be present on every signal
2. Intent identity must not be stripped during processing
3. Intent identity must be verifiable at any point in the flow
4. Intent identity must trace to a governance command

## Sentinel Role

The Intent Identity Sentinel validates that:

- Signals carry valid intent identity
- Intent identity matches the authorizing command
- Intent identity has not been tampered with
- Intent identity is recorded in the observation receipt

## Doctrine Lock

Seam-Gated Sentinel Observation
