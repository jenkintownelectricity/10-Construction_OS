# Standards Reference Model — Construction Specification Kernel

## Citation-Only Protocol

This kernel references standards by citation only. It records that a specification cites a standard, which standard is cited, and for what purpose. It never reproduces, summarizes, or paraphrases the standard's text.

## Reference Structure

A standards reference in this kernel contains:

- **standard_id** — identifier from `shared_standards_registry.json` (e.g., "ASTM", "IBC", "NFPA_285")
- **title** — human-readable title of the standard
- **issuing_body** — organization that publishes the standard
- **relevance** — description of why this standard is referenced (e.g., "test method for adhesion pull-off testing")
- **edition** — specific edition year, if stated in the specification
- **applicable_sections** — CSI sections where this standard is referenced

## Standards Referenced in Division 07

### Building Codes
- **IBC** — International Building Code. Chapters 14 and 15 generate mandatory requirements for exterior walls and roof assemblies.
- **IECC/ASHRAE 90.1** — Energy code requirements driving insulation values, air barrier performance, and continuous insulation.

### Test Method Standards
- **ASTM D4541** — Pull-off strength of coatings using portable adhesion testers (field adhesion testing)
- **ASTM E2357** — Air leakage of air barrier assemblies
- **ASTM E1105** — Field determination of water penetration of installed windows, curtain walls, and doors
- **ASTM E96** — Water vapor transmission of materials
- **ASTM D903** — Peel or stripping strength of adhesive bonds
- **ASTM D5147** — Sampling and testing modified bituminous sheet material
- **ASTM C1549** — Solar reflectance near ambient temperature

### Performance Standards
- **AAMA 501** — Methods of test for metal curtain walls
- **AAMA 711** — Voluntary specification for self-adhering flashing
- **NFPA 285** — Fire propagation characteristics of exterior wall assemblies

### Classification Standards
- **CSI MasterFormat** — Section numbering and classification authority

## How Standards Link to Requirements

A specification requirement may reference one or more standards. The linkage is recorded in the requirement's `standards_refs` and `test_method_refs` fields. The reference is a string citation (e.g., "ASTM D4541") that can be resolved against the shared standards registry.

## Edition Conflicts

When a specification cites a specific edition of a standard and a more recent edition exists, the kernel records exactly what the specification cites. It does not substitute newer editions. If the specification says "ASTM D4541-17," that is the reference recorded. Edition conflicts between specification citations and current editions are flagged with `ambiguity_flag: true` only if the specification itself creates the conflict (e.g., citing two different editions of the same standard).

## Standards Not in Shared Registry

If a specification references a standard not listed in `shared_standards_registry.json`, the reference is recorded with a note identifying the gap. The standard should be added to the shared registry through the family governance process.
