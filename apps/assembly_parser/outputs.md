# Assembly Parser Outputs

## Primary Outputs
| Output | Format | Description |
|--------|--------|-------------|
| DXF Drawing | `.dxf` | AutoCAD-compatible shop drawing |
| SVG Drawing | `.svg` | Web-viewable shop drawing |
| JSON Preview | `.json` | Machine-readable assembly summary |
| Runtime Report | structured | Pipeline execution summary |
| Audit Log | structured | Append-only execution trail |

## Output Contract
- Deliverable conforms to `contracts/deliverable.schema.json` (v0.2)
- DXF and SVG derive from identical DrawingInstructionSet
- Dimensions include provenance metadata (EXPLICIT/DERIVED/INFERRED/UNAPPROVED)
