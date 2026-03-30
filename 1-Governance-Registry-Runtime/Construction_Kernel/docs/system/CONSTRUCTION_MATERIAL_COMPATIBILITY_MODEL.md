# Construction Material Compatibility Model

## Purpose

Define the canonical model for material compatibility within the Construction domain. Compatibility rules govern which materials may be placed in contact, proximity, or functional relationship with each other within assembly compositions.

---

## Position in Architecture

```
Universal_Truth_Kernel
  → Construction_Kernel
    → Assembly Composition Model
    → Material Taxonomy
    → Material Compatibility Model  ← this document
    → Interface Model
    → Scope Boundary Model
    → Construction_Runtime
```

The Compatibility Model consumes the Material Taxonomy as its canonical vocabulary. Compatibility rules are expressed between canonical material classes, not manufacturer products.

---

## Compatibility Types

| Type | Description |
|---|---|
| `compatible` | Materials may be placed in contact or functional relationship without adverse interaction |
| `conditionally_compatible` | Materials may coexist under specific conditions (separation layer, coating, drainage path) |
| `incompatible` | Materials must not be placed in contact or functional relationship due to adverse interaction |

---

## Compatibility Rule Structure

Each compatibility rule must specify:

| Field | Description |
|---|---|
| `material_a` | First canonical material class |
| `material_b` | Second canonical material class |
| `compatibility_type` | One of: `compatible`, `conditionally_compatible`, `incompatible` |
| `interaction_mechanism` | The physical or chemical mechanism (corrosion, plasticizer migration, solvent attack, etc.) |
| `condition` | For `conditionally_compatible`: the required mitigation condition |
| `evidence_basis` | Reference to standard, test data, or authoritative guidance |

---

## Known Compatibility Rules

### Incompatible Pairs

| Material A | Material B | Mechanism |
|---|---|---|
| `pvc_membrane` | `bituminous_adhesive` | Plasticizer migration from bitumen degrades PVC |
| `pvc_membrane` | `mod_bit_membrane` | Plasticizer migration; direct contact prohibited |
| `pvc_membrane` | `xps_insulation` | Plasticizer migration into polystyrene |
| `pvc_membrane` | `eps_insulation` | Plasticizer migration into polystyrene |
| `epdm_membrane` | `bituminous_adhesive` | Petroleum solvents attack EPDM |
| `copper_sheet` | `galvanized_steel` | Galvanic corrosion; copper accelerates zinc dissolution |
| `copper_sheet` | `aluminum_sheet` | Galvanic corrosion in presence of electrolyte |
| `lead_sheet` | `aluminum_sheet` | Galvanic corrosion |

### Conditionally Compatible Pairs

| Material A | Material B | Condition |
|---|---|---|
| `copper_sheet` | `galvanized_steel` | Permitted with isolation layer preventing galvanic contact and drainage separation preventing copper runoff onto zinc |
| `aluminum_sheet` | `concrete_deck` | Permitted with separation layer preventing alkaline attack on aluminum |
| `tpo_membrane` | `polyiso_insulation` | Compatible when adhered per manufacturer specification; adhesive type must be verified |
| `pvc_membrane` | `polyiso_insulation` | Compatible with approved separation sheet if insulation facer is incompatible |
| `stainless_fastener` | `galvanized_steel` | Conditionally compatible; galvanic risk low in dry environments, requires evaluation in wet or coastal exposure |

### Compatible Pairs (Representative)

| Material A | Material B | Note |
|---|---|---|
| `tpo_membrane` | `tpo_membrane` | Self-compatible; heat-weldable |
| `epdm_membrane` | `epdm_membrane` | Self-compatible; adhesive or tape bonded |
| `galvanized_steel` | `galvanized_steel` | Self-compatible |
| `polyiso_insulation` | `steel_deck` | Standard substrate relationship |
| `mineral_wool_insulation` | `steel_deck` | Standard substrate relationship |

---

## Compatibility Evaluation Rule

When an assembly composition places two materials in contact or functional relationship:

1. Both materials must be identified by canonical material class.
2. The compatibility rule for the pair must be evaluated.
3. If `incompatible`: the composition must be flagged and must not proceed to buildability claims.
4. If `conditionally_compatible`: the required condition must be verified as present in the composition.
5. If `compatible`: no additional action required.
6. If no rule exists for the pair: the condition must be flagged as `unknown_compatibility` and fail closed.

---

## Unknown Compatibility Rule

If a material pair has no defined compatibility rule, the system must not assume compatibility. Unknown compatibility must be flagged and must fail closed on buildability and drawing generation claims until the compatibility is governed and determined.

---

## Compatibility Scope

This model covers material compatibility for commercial building envelope and roofing applications. It does not cover:
- Structural material compatibility (weld compatibility, concrete reinforcement)
- MEP material compatibility (pipe material, fluid compatibility)
- Interior finish compatibility

Expansion requires governed admission.

---

## Safety Note

- This document defines architecture documentation only
- No runtime code, schemas, or implementations are modified
- No existing registry entries are changed
- Material Taxonomy: `Construction_Kernel/docs/system/CONSTRUCTION_MATERIAL_TAXONOMY.md`
- Governance doctrine: `Construction_Kernel/docs/governance/construction-material-doctrine.md`
