# Kernel-to-Assistant Map — Construction Assembly Kernel

## Status: Reserved for Future

This map is reserved for documenting how AI assistants interact with assembly kernel truth.

## Anticipated Assistant Interactions

| Interaction | Description | Status |
|---|---|---|
| Assembly query | Assistant queries kernel for assembly configurations by type, climate, or control layer | Not yet implemented |
| Transition lookup | Assistant retrieves transition details for a given interface zone | Not yet implemented |
| Continuity check | Assistant verifies whether a proposed assembly meets continuity requirements | Not yet implemented |
| Evidence gap identification | Assistant identifies assembly records lacking evidence support | Not yet implemented |

## Assistant Interaction Rules

1. Assistants read kernel truth; they do not modify it without human approval.
2. Assistants must respect the fail-closed posture: absence of data is not negative evidence.
3. Assistants must not extrapolate tested assembly results to untested configurations.
4. Assistants must flag ambiguity rather than resolve it.
5. Assistants reference kernel schemas for structured output formatting.

## AI Readiness

See `docs/architecture/ai-readiness-posture.md` for the kernel's structural and semantic readiness for AI consumption.

## Current State

No assistant integrations are implemented. The kernel's schema-first design and enum-based classification prepare it for future AI consumption.
