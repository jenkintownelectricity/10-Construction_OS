# Operator Truth Report

## What Armand Should Trust

1. **10-Construction_OS** — This is your production system. Assembly records, parametric generator, export tools, condition atlas, Barrett source data. Everything that actually produces printable details lives here.

2. **The parametric generator** (`generators/pmma/pmma_flash_generator.py`) — This is the repeatable path. Feed it calibration data, get normalized geometry for all 10 PMMA conditions. Don't hand-draw details when this exists.

3. **The export tools** (`tools/export_svg_to_pdf.py`, `tools/export_assembly_to_dxf.py`) — These produce real PDF and DXF. They work. They're installed. Use them.

4. **The PRINT_STANDARD SVGs** in `output/barrett_pmma_packet/print/` — These are the white-background, printer-ready detail sheets. Open in browser, print to PDF, hand to Craig.

5. **GPC_Shop_Drawings** — When you need real production CAD DXF generation, this repo has the most mature DXF code (28.8KB `dxf_generator.py`). It's real engineering.

## What Armand Should Stop Using

1. **Stop searching for "the right pipeline" across 31 repos.** There is one production path. It's in Construction_OS.

2. **Stop expecting ALEXANDER, WLV, ShopDrawing_Compiler, or Construction_Runtime to produce packets without manual wiring.** They have real code but are not connected to each other. Each was built independently.

3. **Stop rebuilding the same generators.** There are 4 SVG exporters, 4 DXF generators, 3 PDF writers across the ecosystem. Pick one canonical owner per function and freeze it.

4. **Stop treating satellite kernels (Material, Chemistry, Scope, Spec) as production systems.** They're JSON schemas. They don't generate anything.

5. **Stop treating empty repos as future promise.** `architect-reasoning-workspace` and `schematic-digital-twin` have been empty README stubs. Either build them or delete them.

## What Is Real Production

```
10-Construction_OS/generators/pmma/pmma_flash_generator.py
  → calibration specimen + DNA template
    → normalized geometry JSON
      → SVG (PRINT_STANDARD)
        → PDF (cairosvg + pypdf)
        → DXF (ezdxf)
```

**That's it.** One repo, three scripts, ten conditions, verified output.

## What Is Smoke

| System | Claim | Reality |
|--------|-------|---------|
| "ALEXANDER resolves conditions into geometry" | Advisory proposals only — nothing consumes them |
| "WLV exports real DXF/PDF" | Has renderers but requires running Next.js app interactively |
| "ShopDrawing_Compiler compiles packets" | Has pipeline stages but no evidence of end-to-end run |
| "Construction_Runtime generates drawings" | Has writers but needs DrawingInstructionSet nobody generates |
| "Digital twin renders schematics" | Empty repo with a README |
| "Sales Command Center generates proposals" | Scaffold with zero implemented generators |
| "Manufacturer mirror is source truth" | Explicitly states it is NOT source truth |

## The One Next Hardening Target

**Build a geometry-to-SVG renderer adapter that consumes the parametric generator's normalized geometry JSON and outputs PRINT_STANDARD SVG sheets automatically.**

Today: generator → geometry JSON (works) → SVG (manual/Claude-authored)
Target: generator → geometry JSON → SVG renderer → automatic SVG

This closes the last manual gap in the production path. Once this adapter exists, the entire chain from condition selection to client PDF is automated.

## What Should Never Be Rebuilt Again

1. The Barrett PMMA assembly records (10 JSON files) — done, validated, pushed
2. The calibration specimen with measured dimensions — done
3. The parametric generator with 10 condition functions — done, proof-of-life passed
4. The PDF and DXF export functions — done, installed, working
5. The condition family map tying everything together — done

**If someone tries to "redesign the architecture" instead of wiring what exists, point them to this report.**
