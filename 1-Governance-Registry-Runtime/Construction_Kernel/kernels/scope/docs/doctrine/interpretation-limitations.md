# Interpretation Limitations

## Purpose

The Construction Scope Kernel records scope boundaries as-defined. It does not infer, extend, or interpret scope beyond what is explicitly stated. This document defines the limitations on scope interpretation.

## Core Limitation

Scope is recorded, not interpreted. When a scope boundary is ambiguous, the kernel flags the ambiguity rather than resolving it.

## Ambiguity Categories

### 1. Undefined Responsibility
When no trade is explicitly assigned to a scope item, the kernel creates a **scope gap** record. It does not assign responsibility by inference from adjacent trades or common practice.

### 2. Overlapping Scope
When two or more trades appear to have responsibility for the same work item, the kernel creates a **scope overlap** record. It does not arbitrate which trade should prevail.

### 3. Missing Exclusions
When a scope definition includes work items but does not explicitly state exclusions, the kernel does not infer exclusions. It flags the absence of explicit exclusion language.

### 4. Implied Sequencing
When documents reference work that "follows" or "precedes" other work without explicit sequencing, the kernel records the reference but flags the absence of a formal sequence dependency.

### 5. Interface Zone Ambiguity
When the physical boundary between two trades' work is not precisely defined (e.g., "flashing at the roof-to-wall transition" without specifying who terminates the membrane), the kernel flags the interface as ambiguous.

## Flagging Protocol

All ambiguities are recorded with:

- **Flag type**: `undefined_responsibility`, `scope_overlap`, `missing_exclusion`, `implied_sequence`, `interface_ambiguity`
- **Source reference**: the document or record where the ambiguity was detected
- **Affected trades**: trades potentially impacted
- **Resolution status**: `open`, `under_review`, `resolved`

## Resolution Path

1. Ambiguity is detected and flagged during scope entry.
2. Flag is surfaced to human reviewers.
3. Reviewer provides explicit scope definition.
4. Scope record is updated with resolution and revision lineage.

## What This Means for Consumers

Any system consuming scope data from this kernel must handle scope gaps. A missing scope assignment is not "no work required" -- it is "work assignment undefined." Consumers must treat scope gaps as blocking conditions.
