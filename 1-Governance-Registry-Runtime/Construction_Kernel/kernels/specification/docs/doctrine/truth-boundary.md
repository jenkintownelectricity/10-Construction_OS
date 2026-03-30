# Truth Boundary — Construction Specification Kernel

## Owned Truth Surface

This kernel owns specification-domain truth and nothing else. Specification truth includes:

- **Specification documents** — project manuals, addenda, RFIs, bulletins
- **Specification sections** — CSI-formatted sections with their content structure
- **Requirements** — mandatory (shall), recommended (should), and permissive (may) obligations
- **Prohibitions** — explicitly forbidden materials, methods, or conditions
- **Allowances** — explicitly permitted alternatives or substitutions
- **Submittal requirements** — product data, shop drawings, samples, test reports, certificates
- **Testing requirements** — field tests, lab tests, mock-ups, preconstruction testing
- **Warranty requirements** — manufacturer, system, NDL, and workmanship warranties
- **Qualification requirements** — manufacturer, installer, testing agency, inspector qualifications
- **Standards references** — citations to IBC, ASTM, AAMA, NFPA, ASHRAE (by citation only)
- **Source pointers** — traceable references to originating documents
- **Specification revisions** — addenda and revision lineage

## Not Owned — Assembly Truth

Assembly configurations, layering sequences, attachment methods, and system compositions are owned by the Construction Assembly Kernel. This kernel may reference assemblies via pointers but does not define them. A specification requirement may mandate "fully adhered membrane roofing system" but the layer-by-layer assembly definition lives in the assembly kernel.

## Not Owned — Material Truth

Material properties, compatibility data, physical characteristics, and degradation behavior are owned by the Construction Material Kernel. Specification requirements may reference material properties as performance criteria (e.g., "tensile strength not less than 200 psi"), but the actual material property values live elsewhere.

## Not Owned — Chemistry Truth

Chemical interactions, adhesion mechanisms, cure behavior, and solvent compatibility are owned by the Construction Chemistry Kernel. This kernel does not store or interpret chemistry. A spec prohibition against contact between incompatible materials is recorded here; the chemistry explaining why is not.

## Not Owned — Scope Truth

Project scope boundaries, trade responsibilities, division of work, and exclusion clauses are owned by the Construction Scope Kernel. Specification sections identify scope by reference, but scope truth is not duplicated here.

## Not Owned — Reference Intelligence

Pattern analysis, cross-kernel correlation, risk scoring, and design guidance generation are performed by Construction_Reference_Intelligence. This kernel provides structured truth that the intelligence layer reads. It does not perform intelligence operations.

## Boundary Enforcement

Any record that crosses a truth boundary is rejected at schema validation. Fields belonging to other kernels are not present in specification schemas. Cross-kernel relationships use pointer references only. When a specification fact implies truth that belongs to another kernel, only the specification-side fact is recorded here with a reference pointer.
