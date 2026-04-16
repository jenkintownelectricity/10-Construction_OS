# Print Standard Enablement Report

## Status: ENABLED

## Export Modes Defined

| Mode | Background | Lines | Use Case | Status |
|------|-----------|-------|----------|--------|
| SCREEN_MODE | Dark (#0A0D11) | Cyan/Orange | Workstation viewing | Active |
| PRINT_STANDARD | White (#FFFFFF) | Black/Gray | Client deliverables | **ACTIVE** |
| CAD_MODE | N/A | Layer-based | DXF export | Active |

## PRINT_STANDARD Rules
- Background: #FFFFFF (white)
- Primary lines: #000000 (black), 1.5px
- Secondary lines: #555555 (dark gray), 1px
- PMMA system: #0088BB (Barrett blue) per manufacturer standard
- Fleece: dashed stroke, diagonal hatch pattern
- Dimensions: #666666, 0.5px dashed
- Text: Arial/Helvetica, #000000
- Titleblock: required, bottom of sheet
- Callout legend: required, right side
- Draft watermark: 48px, #CCCCCC, 30% opacity

## Barrett PMMA Packet Re-Export
- 10 PRINT_STANDARD SVGs generated in `print/` subdirectory
- Combined 10-page PDF compiled: `client/Barrett_PMMA_Detail_Packet_v1.pdf`
- Individual page PDFs in `client/` directory
- White background validated on all sheets

## Fireproofing Packet Export
- 10 PRINT_STANDARD SVGs generated in `print/` subdirectory
- Combined 10-page PDF compiled: `client/Fireproofing_Starter_Packet_v1.pdf`

## Export Functions Installed
- `tools/export_svg_to_pdf.py` — SVG-to-PDF conversion (cairosvg + pypdf)
- `tools/export_assembly_to_dxf.py` — Assembly JSON-to-DXF (ezdxf)

## Packet Compile Forces PRINT_STANDARD
The PDF export function only reads from the `print/` subdirectory, ensuring all client-facing PDFs use white-background PRINT_STANDARD format.
