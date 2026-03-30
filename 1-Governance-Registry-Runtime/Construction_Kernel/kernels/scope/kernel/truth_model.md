# Truth Model

## Purpose

Defines what constitutes scope truth in the Construction Scope Kernel. Scope truth is the authoritative record of defined work boundaries with trade assignments.

## Definition of Scope Truth

Scope truth is a structured assertion about what work is included, what is excluded, who is responsible, in what order, and how it is verified. Scope truth is:

1. **Defined, not inferred.** Every scope assertion originates from an explicit definition. The kernel never infers scope from context, convention, or adjacent records.
2. **Bounded, not open-ended.** Every scope record has explicit boundaries. Work not addressed by a scope record is not "implicitly included" -- it is unscoped.
3. **Assigned, not assumed.** Trade responsibility is explicitly assigned. If no trade is assigned, a scope gap exists.
4. **Versioned, not overwritten.** Scope changes create new versions. Prior scope truth is deprecated, not deleted.

## Truth Categories

### Boundary Truth
What is in scope and what is out of scope. Expressed through `inclusions` and `exclusions` on scope of work records.

### Responsibility Truth
Which trade owns which scope items. Expressed through trade responsibility records linked to scopes.

### Sequence Truth
What order operations must follow. Expressed through sequence steps with predecessor/successor relationships.

### Verification Truth
How scope completion is verified. Expressed through inspection steps, commissioning steps, and closeout requirements.

### Interface Truth
Where scope boundaries meet between trades. Expressed through interface zone references on scope and trade responsibility records.

## Truth Lifecycle

| State | Meaning |
|---|---|
| `draft` | Proposed scope truth, not yet authoritative |
| `active` | Current authoritative scope truth |
| `deprecated` | Superseded scope truth, retained for lineage |

## Truth Integrity Rules

1. Every scope of work must have at least one trade responsibility assignment.
2. Every interface zone referenced must have trade assignments on all sides.
3. Every hold point in a sequence must have an associated inspection step.
4. Scope gaps are truth -- the absence of an assignment is itself a scope fact that must be recorded and surfaced.
