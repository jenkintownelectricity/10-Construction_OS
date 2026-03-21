# Adapter Contracts — Construction OS

## Architecture

Adapters provide the seam between the UI and real/mock data sources. UI code never invents source truth — it always flows through adapters. Every adapter declares `isMock` and `adapterName`.

## Adapter Catalog

| Adapter | Interface | Current Implementation | Mock? |
|---------|-----------|----------------------|-------|
| Truth Source | `TruthSourceAdapter` | `mockTruthSource` | Yes |
| Reference Source | `ReferenceSourceAdapter` | `mockReferenceSource` | Yes |
| Spatial Source | `SpatialSourceAdapter` | `mockSpatialSource` | Yes |
| Validation | `ValidationAdapter` | `mockValidation` | Yes |
| Artifact | `ArtifactAdapter` | `mockArtifact` | Yes |
| Voice | `VoiceAdapter` | `mockVoice` | Yes |

## Adapter Output Classification

All adapter outputs use `SourcedData<T>` wrapper:

```typescript
interface SourcedData<T> {
  data: T;
  basis: 'canonical' | 'derived' | 'draft' | 'compare' | 'mock';
  sourceAdapter: string;
  timestamp: number;
  isMock: boolean;
}
```

## Swappability

Mock adapters are assembled in `src/ui/adapters/index.ts` via the `AdapterRegistry` interface. To swap a mock for a real adapter:

1. Implement the typed interface (e.g., `TruthSourceAdapter`)
2. Set `isMock: false` and `adapterName` to the real adapter name
3. Replace the mock in the registry

No panel code needs to change — panels only interact with the typed interface.

## Code Location

Machine-readable typed contracts: `src/ui/contracts/adapters.ts`
Mock implementations: `src/ui/adapters/mock*.ts`
Registry: `src/ui/adapters/index.ts`
