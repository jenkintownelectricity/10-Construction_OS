# Kernel-to-Runtime Map — Construction Assembly Kernel

## Status: Reserved for Future

This map is reserved for documenting how runtime systems consume assembly truth from this kernel.

## Anticipated Runtime Consumers

| Runtime System | Consumption Pattern | Status |
|---|---|---|
| Assembly validation service | Schema validation of new assembly records | Not yet implemented |
| Continuity verification engine | Check assembly configurations against continuity requirements | Not yet implemented |
| Cross-kernel reference resolver | Resolve material_ref and spec_ref to sibling kernel entries | Not yet implemented |
| Query API | Structured queries against assembly truth | Not yet implemented |

## Design Principles for Runtime Integration

1. Runtime systems read kernel truth; they do not modify it.
2. All runtime access is through defined contracts and schemas.
3. Runtime validation failures are reported, not silently corrected.
4. No runtime system may bypass schema validation.

## Current State

The kernel is a static truth store with no runtime services. All validation is offline via JSON Schema tooling.
