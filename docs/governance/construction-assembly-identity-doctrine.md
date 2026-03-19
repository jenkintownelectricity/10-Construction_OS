# Construction Assembly Identity Doctrine

## Purpose

Define governed rules for object identity continuity within the Construction domain. Identity anchors the continuity of construction objects across revisions, enabling reliable truth history and event attachment.

---

## Core Principle

Identity is the governed basis for asserting that a construction object persists across time, revisions, and document versions. Without governed identity, truth events cannot be reliably attributed to a continuous object.

---

## Identity Rule

Every construction object that participates in truth history must carry a governed identity. Identity is assigned, tracked, and resolved through governed processes. Identity is not inherited from document metadata, file paths, or presentation artifacts.

---

## Non-Equivalence Rule

The following are not identity:

- Labels
- Drawing callouts
- Titles
- Sheet positions
- Document paths
- File names
- Revision markers

These are **representation artifacts**. They may change without affecting identity. They may remain stable while identity changes. No representation artifact may be treated as a substitute for governed identity.

---

## Provisional Identity Rule

When an object enters the system without sufficient evidence to establish governed identity, it must receive a provisional identity. Provisional identities must be explicitly marked. Provisional identities must not be treated as established for continuity claims. Provisional identities must be resolved through governed evaluation before final truth assertions depend on them.

---

## Explicit Correction Rule

Identity assignments, once established, may only be corrected through explicit governed operations. Silent reassignment of identity is a governance violation. Every identity correction must produce an auditable record.

---

## Supersession Relationship Rule

When one object supersedes another, the relationship must be explicit and recorded. The prior identity and the resulting identity must both be preserved. Supersession chains must be traversable for audit purposes. Implicit supersession through document replacement is not valid.

---

## Evidence Rule

Identity continuity across revisions must be supported by governed evidence. The system must not assert identity continuity based solely on positional, naming, or structural similarity. Evidence supporting identity continuity must be traceable to source artifacts.

---

## Relationship to Truth Spine

Truth events attach to identities, not to documents. The Construction Truth Spine records events against governed object identities. If identity is unresolved, truth events must be recorded provisionally and must fail closed on final continuity claims.

Identity merges, splits, replacements, and retirements must be explicit and auditable within the truth spine. No truth event may silently reassign the object it references.

---

## Safety Note

- This document defines construction-domain governance only
- No runtime code, schemas, or implementations are modified
- This doctrine is specific to the Construction domain and does not modify root ValidKernel governance
