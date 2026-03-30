# Detail Training Corpus

**Authority:** Construction_Kernel (read-only consumer)
**Wave:** 13A
**Status:** Active

## Purpose

The Detail Training Corpus generates structured training data for automated detail generation systems. It reads from Construction_Kernel detail families, tags, and route graphs to produce training pairs.

## Isolation Rules

1. This subsystem may **READ** Construction_Kernel data.
2. This subsystem may **NOT MODIFY** any kernel datasets.
3. All outputs are written exclusively to `detail_training_corpus/`.
4. Training data is a **derived artifact** — it has no authority over kernel definitions.

## Output Format

Training pairs are emitted in JSONL format to `training_pairs.jsonl`.

Each line contains a JSON object with:

```json
{
  "input": {
    "system": "LOW_SLOPE",
    "class": "TERMINATION",
    "condition": "PARAPET",
    "assembly_family": "EPDM",
    "tags": ["fn-termination", "fn-waterproofing"],
    "compatible_materials": ["EPDM"],
    "risk_tags": ["UV_EXPOSURE", "WIND_UPLIFT"]
  },
  "output": {
    "detail_id": "LOW_SLOPE-TERMINATION-PARAPET-COUNTERFLASHING-EPDM-01",
    "display_name": "EPDM Parapet Termination with Counterflashing",
    "variant": "COUNTERFLASHING",
    "relationships": [
      {
        "target": "LOW_SLOPE-TRANSITION-ROOF_TO_WALL-REGLET-PVC-01",
        "type": "adjacent_to"
      }
    ]
  },
  "metadata": {
    "source": "Construction_Kernel",
    "wave": "13A",
    "generated_at": "ISO-8601 timestamp"
  }
}
```

## Generation Rules

1. One training pair per detail family.
2. Relationships are included from `detail_route_index.json` where the family appears as source.
3. Material compatibility is sourced from the detail family record.
4. Tags are sourced from the detail family record.
5. No data augmentation or synthesis — training data reflects kernel truth only.
