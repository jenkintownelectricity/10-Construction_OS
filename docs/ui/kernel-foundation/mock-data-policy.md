# Mock Data Policy — Construction OS

## Policy

1. **All mock adapters declare `isMock: true`.** This is a typed contract field, not optional.
2. **All mock adapter outputs set `basis: 'mock'` in SourcedData.** This flows through to UI display.
3. **The PanelShell displays a visible MOCK indicator** when the adapter is mock.
4. **The workspace status bar displays "MOCK ADAPTERS"** when any mock adapter is active.
5. **Mock data is realistic but explicitly fictional.** The mock project "Highland Medical Center" contains realistic construction objects but is not real production data.
6. **Mock adapters are swappable** without re-architecting panels.

## Current Mock Adapters

| Adapter | File | Data Description |
|---------|------|-----------------|
| mockTruthSource | `src/ui/adapters/mockTruthSource.ts` | Project tree with 3 zones, 13 objects |
| mockReferenceSource | `src/ui/adapters/mockReferenceSource.ts` | Spec references, citations for select objects |
| mockSpatialSource | `src/ui/adapters/mockSpatialSource.ts` | Spatial objects with zones and layers |
| mockValidation | `src/ui/adapters/mockValidation.ts` | Validation results (pass/fail examples) |
| mockArtifact | `src/ui/adapters/mockArtifact.ts` | Artifact generation seam (pending results) |
| mockVoice | `src/ui/adapters/mockVoice.ts` | Voice seam (not available, no-op) |

## What Mock Data Must NOT Do

1. Must not be presented as canonical truth
2. Must not be hidden behind production-looking UI
3. Must not be the only indicator of system capability
4. Must not be used for validation of real business logic
