# Condition Pattern Library

**Authority**: Construction_Kernel  
**Wave**: 8.5  
**Status**: Canonical

## Purpose

The Condition Pattern Library defines reusable construction condition patterns that represent known, recurring construction issues. These patterns encode domain expertise about common failure modes, coordination gaps, and material incompatibilities found in building envelope construction.

## Governance Rules

1. **Kernel owns pattern truth.** All pattern definitions, blocker archetypes, remediation archetypes, and issue signatures are canonical kernel artifacts.
2. **Runtime may reference but not author patterns.** Runtime modules may attach pattern_candidate_refs to condition packets as enrichment, but may never create, modify, or delete pattern definitions.
3. **Pattern candidates are enrichment only.** Pattern matching results attached to condition packets may NOT modify: readiness_state, issue_state, blocker_state, ownership_state, package_state, revision_state, release_state.
4. **Patterns are graph-compatible.** All patterns reference assemblies, interfaces, and details by canonical identifiers that are graph-addressable.

## Contents

| File | Description |
|------|-------------|
| pattern_schema.json | JSON Schema for condition pattern definitions |
| patterns/ | Individual pattern definitions |
| blocker_archetypes.json | Catalog of canonical blocker archetype definitions |
| remediation_archetypes.json | Catalog of canonical remediation archetype definitions |
| issue_signatures.json | Catalog of issue signature definitions for pattern matching |

## Patterns

| Pattern ID | Description |
|------------|-------------|
| PARAPET_FLASHING_GAP | Flashing discontinuity at parapet transition |
| TERMINATION_BAR_FAILURE | Mechanical termination bar missing or failed |
| COUNTERFLASHING_SCOPE_GAP | Counterflashing scope gap between trades |
| SLOPE_TO_DRAIN_MISMATCH | Slope specification misaligned with drainage |
| INSULATION_COMPRESSIBILITY_MISMATCH | Insulation compressibility does not meet requirements |
