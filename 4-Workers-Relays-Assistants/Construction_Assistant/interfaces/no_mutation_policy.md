# No-Mutation Policy

## Purpose

Explicit policy prohibiting the assistant from mutating any canonical state in any system.

## Policy Statement

Construction_Assistant performs no writes, updates, deletions, insertions, state transitions, approvals, certifications, or any other form of state mutation against any upstream, downstream, or lateral system.

## Scope

This policy applies to:

1. **All upstream systems:** Construction_Kernel (Layer 5), Construction_Runtime (Layer 6), Construction_Application_OS (Layer 7), Universal_Truth_Kernel (Layer 0).
2. **All truth surfaces:** Every surface listed in `maps/truth_surface_map.md`.
3. **All data stores:** Any database, file system, registry, cache, or artifact store owned by any governed system.
4. **All workflow engines:** The assistant does not advance, revert, pause, or modify any workflow state.
5. **All validation pipelines:** The assistant does not trigger, re-trigger, override, or modify any validation result.
6. **All governance records:** The assistant does not create, modify, or delete any governance record.

## What the Assistant May Write

1. **Transient responses to operators.** These are not canonical records. They are bounded emissions that exist only in the query-response session.
2. **Internal classification metadata.** Emission class labels and routing decisions used to produce the response. These are internal to the assistant and not written to any external system.

## Enforcement

This policy is enforced by architecture. The assistant has no write credentials, no write API access, and no write path to any upstream system. If a code path is discovered that permits mutation, it is a defect and must be resolved immediately.

## No Exceptions

There are no exceptions to this policy. Operator requests for mutation are declined with an insufficiency emission that redirects the operator to the appropriate governed system interface.
