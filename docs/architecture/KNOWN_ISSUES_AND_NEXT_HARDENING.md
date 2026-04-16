# Known Issues and Next Hardening

## Non-Blocking Issues

1. **Leader line routing** — Callout leaders fan out to the right side but don't use sophisticated non-crossing algorithms. Occasional visual overlap possible on dense details.

2. **Viewport padding** — Bounding box normalization centers geometry but doesn't always optimize whitespace distribution. Some details may appear shifted.

3. **Title block styling** — Current title block is functional but doesn't match Barrett's branded format (Barrett logo, detail number grid, PREP/CLEAN boxes). This is a styling pass, not a structural issue.

4. **Full 10-condition parametric render** — The SVG section renderer is proven on equipment curb. The remaining 9 conditions need to be run through the renderer to produce the full parametric-rendered set.

5. **Manufacturer sign-off** — Barrett Company has not reviewed or approved the generated details. All outputs are marked DRAFT FOR REVIEW.

6. **Null calibration dimensions** — 7 project-specific dimensions (joint gap, overburden depth, bellows width, etc.) are null in the calibration specimen and need operator fill per project.

## Next Hardening Target

Run `svg_section_renderer.py` on all 10 parametric geometry JSONs to produce the full rendered packet. This proves the complete pipeline is automated.

## Future Hardening (Not Blocking)

- Add Barrett-branded title block with logo zone and detail number grid
- Implement non-crossing leader routing algorithm
- Add viewport padding optimization per condition family
- Wire Construction_Runtime's svg_writer.py as alternative rendering backend
- Connect manufacturer-mirror for live product data updates
