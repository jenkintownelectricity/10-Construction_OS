# Spec Intelligence Outputs

## Primary Outputs
| Output | Format | Description |
|--------|--------|-------------|
| Intelligence Report | structured | Opportunities, requirement summaries, reference analysis |
| Runtime Report | structured | Pipeline execution summary |
| Audit Log | structured | Append-only execution trail |

## Output Contract
- Intelligence conforms to `contracts/runtime_spec.schema.json` (v0.2)
- Fields: opportunities[], requirement_summary, reference_summary, intelligence_status
