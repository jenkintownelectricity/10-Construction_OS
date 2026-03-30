# Material Model — Construction Material Kernel

## Purpose

This model defines the core material entity — the foundational object in the kernel. A material is characterized by its class, form, physical properties, compatibility relationships, and standards references.

## Material Entity Structure

| Field | Type | Required | Description |
|---|---|---|---|
| material_id | string | Yes | Unique material identifier |
| name | string | Yes | Descriptive name (generic, no brand) |
| primary_material_class | enum | Yes | Taxonomy class (thermoplastic, etc.) |
| form | enum | No | Physical form (sheet, liquid, etc.) |
| status | enum | Yes | active, draft, deprecated |
| description | string | No | Plain-language material description |
| control_layers_served | array | No | Control layer IDs this material serves |
| typical_applications | array | No | Division 07 application areas |
| substrate_requirements | array | No | Compatible substrate types |
| temperature_range | object | No | Application and service temperature limits |
| notes | string | No | Additional context |

## Material Identity Rules

1. Materials are identified by generic description, never by brand or trade name
2. A "60-mil reinforced TPO membrane" is valid; "Manufacturer X TPO-60" is not
3. Material names describe composition and form: class + modifiers + form
4. Material IDs are stable across revisions — the ID persists; the revision number changes

## Material-to-Property Relationship

A material has zero or more property records. Each property record references the material by ID. Properties are stored as separate objects, not embedded in the material record. This allows independent property updates without modifying the material record.

## Material-to-Compatibility Relationship

Compatibility is a pairwise relationship between two materials. Compatibility records reference both materials by ID. A material may participate in many compatibility records.

## Material-to-Standards Relationship

Materials reference standards through their property records. Each property's `test_method_ref` points to a standards reference record. The material entity itself does not directly reference standards.

## Material-to-Control-Layer Mapping

Materials may serve one or more building envelope control layers. The `control_layers_served` field uses IDs from the shared control_layers.json registry. This mapping indicates capability, not specification — whether a material can serve a control layer, not whether it is specified to do so.

## Example Material Characterization

A thermoplastic polyolefin (TPO) roofing membrane is characterized as:
- Class: thermoplastic
- Form: membrane
- Properties: tensile strength, elongation, tear resistance, puncture resistance, permeance
- Control layers: water control, air control (when fully adhered)
- Standards: ASTM D6878 (material standard), ASTM D751 (test methods)
- Compatibility: tested against polyiso insulation, EPDM, PVC, adhesives
