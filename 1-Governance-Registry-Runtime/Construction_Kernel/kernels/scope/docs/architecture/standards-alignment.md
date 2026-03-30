# Standards Alignment

## Purpose

This document defines how the Scope Kernel aligns its object model to industry standards for classification, organization, and interoperability.

## CSI MasterFormat Alignment

The primary classification system is CSI MasterFormat 2018. All scope records reference CSI section numbers in the `csi_sections` field.

### Division 07 Mapping

| CSI Section | Scope Category | Typical Trades |
|---|---|---|
| 07 10 00 | Waterproofing | Waterproofing installer |
| 07 21 00 | Thermal Insulation | Insulation installer |
| 07 25 00 | Weather Barriers | Air barrier installer |
| 07 27 00 | Air Barriers | Air barrier installer |
| 07 50 00 | Membrane Roofing | Roofing contractor |
| 07 60 00 | Flashing and Sheet Metal | Sheet metal contractor |
| 07 81 00 | Applied Fireproofing | Fireproofing contractor |
| 07 84 00 | Firestopping | Firestopping contractor |
| 07 92 00 | Joint Sealants | Sealant applicator |

## UniFormat Alignment

UniFormat categories are used for building-system-level scope grouping:

- B2010 -- Exterior Walls
- B2020 -- Exterior Windows
- B3010 -- Roofing
- B3020 -- Roof Openings

## OmniClass Alignment

OmniClass Table 21 (Elements) and Table 22 (Work Results) provide supplementary classification when cross-system mapping is required.

## ASTM and Industry Standards

Scope records may reference ASTM standards for inspection and testing methods:

- ASTM E2357 -- Air Leakage of Building Envelope
- ASTM D4263 -- Moisture in Concrete
- ASTM E1105 -- Water Penetration of Windows
- SPRI/FM/UL standards for roofing wind uplift

These references are pointers only. The Scope Kernel does not interpret standard content.

## BECx Standards

Commissioning steps align to:

- ASTM E2813 -- Building Enclosure Commissioning
- NIBS Guideline 3 -- Exterior Enclosure Technical Requirements
