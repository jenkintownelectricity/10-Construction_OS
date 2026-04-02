# Manufacturer Detail System Input Manual

**Document Type:** External Manufacturer Guide
**Audience:** Manufacturers supplying detail systems to the platform
**Version:** 1.0
**Date:** April 2026

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Required Input Package](#2-required-input-package)
3. [DXF Requirements](#3-dxf-requirements)
4. [Three Ownership Classes](#4-three-ownership-classes)
5. [Assembly Definition Requirements](#5-assembly-definition-requirements)
6. [Quality Guidelines](#6-quality-guidelines)
7. [Submission Checklist](#7-submission-checklist)
8. [What Happens After Submission](#8-what-happens-after-submission)
9. [Privacy](#9-privacy)

---

## 1. Introduction

### 1.1 What the Platform Does

This platform generates construction details for roofing, waterproofing, and
envelope assemblies. It takes manufacturer-specific system data and produces
accurate, standards-compliant detail drawings that architects, specifiers, and
contractors can use directly in their project documentation.

The platform understands the layered composition of building envelope systems.
It knows which materials belong to which manufacturer, how they relate to
adjacent construction, and how to annotate them correctly. The result is a
library of details that faithfully represents your system as installed in
real-world conditions.

### 1.2 Why Manufacturers Participate

Participation gives your systems direct representation in the detail generation
pipeline. When a specifier selects your system, the platform produces details
that show your specific products, layer sequences, and installation
configurations. This means:

- Your products appear by name in generated details.
- Your system assemblies are drawn with correct layer order and geometry.
- Your installation requirements are reflected in the output.
- Your systems are available for selection alongside industry peers.

### 1.3 What You Get

As a participating manufacturer, you receive:

- **Accurate representation.** Your system details are generated from your own
  source drawings, preserving the geometry and naming you control.
- **Broad coverage.** The platform generates details across multiple condition
  types (parapet, field, drain, penetration, edge, transition, and more) for
  each system family you supply.
- **Consistency.** All details generated for your system follow the same
  conventions, reducing errors and rework for specifiers.
- **No drafting burden.** Once your input package is submitted, the platform
  handles detail generation. You do not need to maintain a library of condition-
  specific drawings.

---

## 2. Required Input Package

To onboard a system family, submit the following materials.

### 2.1 Representative Detail DXF Files

Provide at least **5 DXF files per system family**. These should represent
different installation conditions and show your system as it would appear in a
typical construction detail.

Good representative details include:

- Field membrane section
- Parapet termination
- Roof drain
- Pipe penetration
- Edge condition or perimeter termination
- Expansion joint
- Wall flashing
- Transition between roof types

More details are better. A complete submission might include 15 to 25 details
covering the full range of conditions your system supports.

### 2.2 Product Data Sheets

Provide current product data sheets (PDF format preferred) for each component
in the system. Data sheets should include:

- Product name (matching the names used in your DXF layers)
- Material composition
- Thickness or application rate
- Key physical properties
- Application method

### 2.3 Installation Instructions

Submit installation guides or application instructions for the system family.
These help the platform understand layer sequencing, substrate preparation
requirements, and critical installation constraints.

### 2.4 Warranty Terms

Provide warranty documentation that describes:

- Warranty types offered (material-only, system, labor-and-material)
- Duration and coverage tiers
- Conditions or limitations

This information is used for classification purposes only and is not published
to end users without your approval.

### 2.5 System Compatibility Information

Include any compatibility notes, such as:

- Approved substrate types (concrete, metal deck, plywood, gypsum board)
- Approved insulation types and attachment methods
- Restrictions on adjacent materials or chemical exposure
- Wind uplift ratings or tested assemblies
- Fire rating information

---

## 3. DXF Requirements

The quality of your DXF files directly affects the quality of generated details.
Follow these requirements to ensure smooth ingestion.

### 3.1 Clean Layer Naming

Every layer in your DXF file should have a descriptive name that identifies the
material or component it represents.

**Good layer names:**

- `RAM Black Pearl Sheet`
- `Protection Course`
- `Hot Rubberized Asphalt`
- `Reinforcing Fleece`
- `Primer Coat`
- `Metal Flashing - Coping`
- `Cant Strip`
- `Adhesive Layer`

**Poor layer names:**

- `Layer1`
- `0`
- `Copy of Layer 3`
- `TEMP`
- `Misc`

Layer names are the primary mechanism by which the platform identifies what
each piece of geometry represents. Descriptive names reduce manual classification
work and improve accuracy.

### 3.2 Supported Entity Types

The platform supports the following DXF entity types:

| Entity Type   | Usage                                      |
|---------------|---------------------------------------------|
| LWPOLYLINE    | Closed and open shapes, outlines, profiles  |
| HATCH         | Filled areas, material patterns             |
| LINE          | Individual line segments                    |
| ARC           | Curved segments                             |
| CIRCLE        | Circular elements (pipes, fasteners)        |
| MULTILEADER   | Callout leaders with text                   |
| TEXT          | Single-line text annotations                |
| MTEXT         | Multi-line text annotations                 |

Other entity types (SPLINE, ELLIPSE, INSERT, BLOCK, DIMENSION, etc.) may be
present in your files but are not guaranteed to be processed. Where possible,
explode blocks and convert splines to polylines before submission.

### 3.3 Actual Scale Geometry

All geometry must be drawn at **actual scale** (1:1). The platform interprets
coordinates as real-world dimensions. A membrane that is 60 mils thick should
be drawn at 0.060 inches in the DXF, not scaled up for visual clarity.

If your standard practice is to draw details at exaggerated scale for
readability, please also provide a note indicating the scale factor used, or
provide a separate set of files at true scale.

### 3.4 One Detail Per File

Each DXF file should contain **one detail**. If a single file contains multiple
details arranged side by side, the platform cannot reliably distinguish between
them. Separate each condition into its own file.

File naming should identify the system and condition:

- `RAM_BlackPearl_Parapet.dxf`
- `RAM_BlackPearl_Drain.dxf`
- `RAM_BlackPearl_Penetration_Pipe.dxf`
- `Siplast_Paradiene_FieldMembrane.dxf`

### 3.5 System-Owned Layer Identification

Your layer names should make it clear which layers belong to your system
assembly. This is the most important aspect of layer naming.

The platform uses layer names to determine ownership. If a layer is named
`Protection Course`, the platform can identify it as a system-owned material.
If a layer is named `Layer 7`, the platform cannot.

See Section 4 for a full explanation of ownership classes.

---

## 4. Three Ownership Classes

Every layer in a submitted DXF file is classified into one of three ownership
classes. Understanding these classes helps you prepare cleaner submissions.

### 4.1 SYSTEM_OWNED

**Definition:** Geometry that belongs to your roofing, waterproofing, or
envelope assembly. These are the materials and components that you manufacture,
supply, or specify as part of your warranted system.

**Examples of SYSTEM_OWNED layers:**

- Membranes (sheet goods, fluid-applied membranes, self-adhered sheets)
- Primers and primer coats
- Flashings (membrane flashings, liquid flashings)
- Adhesive layers and bonding agents
- Topcoats and basecoats
- Reinforcing fleece and fabric
- Protection courses included in your system
- Cant strips specified as part of your assembly
- Sealants and termination materials you supply

**Guidance for manufacturers:** If a component is listed on your product data
sheet, appears in your installation instructions, or is covered by your system
warranty, it is SYSTEM_OWNED.

### 4.2 CONTEXT_ONLY

**Definition:** Geometry shown in the detail for readability and context but
not owned by your system. This is the surrounding construction that your
system is installed against, on top of, or adjacent to.

**Examples of CONTEXT_ONLY layers:**

- Structural concrete slab or deck
- Metal roof deck
- Backup wall (CMU, concrete, stud framing)
- Wood blocking or nailers (unless supplied by manufacturer)
- Insulation (unless supplied by manufacturer)
- Overburden (pavers, soil, ballast)
- Adjacent construction (window frames, door thresholds)
- Substrate materials

**Default behavior:** A layer named `Others` or any unrecognized generic name
is classified as CONTEXT_ONLY by default.

**Guidance for manufacturers:** If a component is part of the building
structure or is supplied by a different trade, it is CONTEXT_ONLY. Your
details should still show these elements for context, but label them clearly
so the platform knows they are not part of your system.

### 4.3 ANNOTATION

**Definition:** Text, dimensions, callouts, leaders, and other non-geometric
annotation elements. These convey information about the detail but do not
represent physical materials.

**Examples of ANNOTATION layers:**

- Callout text identifying materials
- Dimension lines and dimension text
- Leader lines pointing to components
- Notes and specifications text
- Title block text
- Drawing borders

**Default behavior:** Entities of type MULTILEADER, TEXT, and MTEXT are
classified as ANNOTATION regardless of their layer name. Layers named `Text`,
`Defpoints`, or `MULTILEADER` are treated as ANNOTATION by default.

**Guidance for manufacturers:** You do not need to take special action for
annotation layers. The platform handles them automatically. However, keeping
annotation on dedicated layers (rather than mixed with geometry) improves
processing quality.

### 4.4 Why Ownership Classes Matter

The ownership classification drives how the platform handles your geometry:

- **SYSTEM_OWNED** layers are preserved, adapted, and regenerated when the
  platform produces details for different conditions. These are the core of
  your system representation.
- **CONTEXT_ONLY** layers are used for spatial reference but can be swapped or
  adjusted to match the target building configuration.
- **ANNOTATION** layers are regenerated with correct callout text and
  positioning for each output detail.

Accurate classification means accurate details. When ownership is ambiguous,
the platform defaults to CONTEXT_ONLY and flags the layer for review.

---

## 5. Assembly Definition Requirements

Beyond the DXF files themselves, the platform needs structured information
about your system assemblies.

### 5.1 System Family Name

Provide the official marketing name for the system family. This is the name
specifiers will see when selecting your system.

Examples:

- Siplast Paradiene 20/30 FR GS
- RAM Black Pearl System
- Tremco AlphaGuard BIO
- Carlisle SynTec FleeceBACK TPO

### 5.2 Product Components List with Roles

For each component in the system, provide:

| Field         | Description                                    |
|---------------|------------------------------------------------|
| Product Name  | The commercial name of the product             |
| Role          | The function it serves (membrane, primer, etc.)|
| Layer Name    | The DXF layer name used for this component     |
| Required      | Whether the component is always present        |
| Conditionally Present | Conditions under which it appears       |

Example component list:

| Product Name            | Role              | Layer Name             | Required |
|-------------------------|-------------------|------------------------|----------|
| Black Pearl Sheet       | Primary membrane  | RAM Black Pearl Sheet  | Yes      |
| BP Primer               | Primer            | Primer Coat            | Yes      |
| Reinforcing Fleece      | Reinforcement     | Reinforcing Fleece     | No       |
| Hot Rubberized Asphalt  | Adhesive/Membrane | Hot Rubberized Asphalt | Yes      |
| Protection Course       | Protection        | Protection Course      | Yes      |

### 5.3 Supported Condition Types

Indicate which installation conditions your system supports. Check all that
apply:

- [ ] Field membrane (horizontal application)
- [ ] Parapet termination (vertical to horizontal transition with coping)
- [ ] Base flashing (wall-to-roof transition)
- [ ] Roof drain
- [ ] Scupper
- [ ] Pipe penetration
- [ ] Equipment curb
- [ ] Expansion joint
- [ ] Edge metal / perimeter termination
- [ ] Area divider
- [ ] Roof-to-wall transition
- [ ] Skylight curb
- [ ] Interior corner
- [ ] Exterior corner
- [ ] Green roof / overburden assembly
- [ ] Plaza / paver assembly

### 5.4 Layer Ownership Summary

Provide a summary table mapping each layer name used in your DXF files to its
ownership class:

| Layer Name             | Ownership Class | Notes                          |
|------------------------|----------------|--------------------------------|
| RAM Black Pearl Sheet  | SYSTEM_OWNED   | Primary membrane               |
| Hot Rubberized Asphalt | SYSTEM_OWNED   | Applied waterproofing          |
| Primer Coat            | SYSTEM_OWNED   | Surface primer                 |
| Protection Course      | SYSTEM_OWNED   | Protective layer               |
| Concrete Slab          | CONTEXT_ONLY   | Structural substrate           |
| Metal Deck             | CONTEXT_ONLY   | Structural substrate           |
| Wood Blocking          | CONTEXT_ONLY   | Nailer by others               |
| Others                 | CONTEXT_ONLY   | Miscellaneous context          |
| Text                   | ANNOTATION     | Callout text                   |
| Defpoints              | ANNOTATION     | AutoCAD reference points       |

---

## 6. Quality Guidelines

The following guidelines help ensure your submission processes smoothly and
produces high-quality output.

### 6.1 Minimize Noise Layers

Remove layers that are not needed for the detail. Common noise layers include:

- Unused default layers (`0`, `Defpoints` with geometry)
- Temporary construction layers
- Layers from xrefs that were not cleaned up
- Duplicate layers with slightly different names
- Viewport-specific layers

Fewer layers means faster processing and fewer classification decisions.

### 6.2 Use Consistent Layer Naming Across Detail Families

If your membrane is called `RAM Black Pearl Sheet` in one detail, it should be
called `RAM Black Pearl Sheet` in every detail. Do not use variations like:

- `BP Sheet`
- `Black Pearl`
- `RAM BP Sheet Membrane`
- `Membrane - BP`

Consistency allows the platform to automatically recognize the same material
across all details in a family.

### 6.3 Provide at Least One "Golden" Clean Detail

Every system family should include at least one detail that meets all of the
following criteria:

- **Low layer count.** Ten or fewer layers is ideal.
- **Clean geometry.** No overlapping entities, no stray lines, no duplicate
  polylines on top of each other.
- **Descriptive layer names.** Every layer is named after its material or
  function.
- **Correct ownership.** System-owned layers are clearly distinguishable from
  context layers.
- **Complete annotation.** Callouts identify all visible materials.
- **One condition.** The detail shows a single, well-defined condition (such
  as a parapet termination or a field membrane section).

This golden detail serves as the reference point for configuring your system
in the platform. It is processed first and used to establish the baseline
layer mapping for all subsequent details in the family.

### 6.4 Avoid Embedded Images and External References

DXF files should not contain:

- Embedded raster images (company logos, photos)
- External references (xrefs) that will not resolve
- OLE objects
- Proxy entities from third-party applications

These elements cannot be processed and may cause parsing errors.

### 6.5 Purge Before Submission

Run the AutoCAD `PURGE` command (or equivalent in your CAD application) before
saving the DXF. This removes:

- Unused layers
- Unused blocks
- Unused text styles
- Unused dimension styles

A purged file is smaller, cleaner, and faster to process.

---

## 7. Submission Checklist

Use this checklist to verify your submission is complete before sending.

1. [ ] System family name is clearly stated.
2. [ ] At least 5 representative DXF files are included for the system family.
3. [ ] Each DXF file contains one detail only.
4. [ ] All DXF files are drawn at actual scale (1:1).
5. [ ] Layer names are descriptive and identify each material or component.
6. [ ] Layer names are consistent across all DXF files in the family.
7. [ ] At least one "golden" clean detail is identified and marked.
8. [ ] Product data sheets are included for all system components (PDF).
9. [ ] Installation instructions are included for the system family (PDF).
10. [ ] Warranty terms documentation is included (PDF).
11. [ ] System compatibility information is provided (substrates, insulation,
    restrictions).
12. [ ] Product components list is provided with roles and layer names.
13. [ ] Supported condition types are identified.
14. [ ] Layer ownership summary table is completed (SYSTEM_OWNED, CONTEXT_ONLY,
    ANNOTATION for each layer).
15. [ ] DXF files have been purged of unused layers and blocks.
16. [ ] No embedded images, xrefs, or OLE objects are present in DXF files.
17. [ ] Files are named with system and condition identifiers.
18. [ ] All files are organized in a single folder or archive for submission.

---

## 8. What Happens After Submission

Once your input package is received, the following process takes place.

### 8.1 Ingestion

Your DXF files are parsed and analyzed. The platform extracts:

- Layer names and entity counts per layer
- Entity types and geometry characteristics
- Spatial relationships between layers

This step is automated and typically completes within minutes.

### 8.2 Validation

The parsed data is validated against the requirements described in this manual.
The platform checks for:

- Supported entity types
- Layer naming quality
- Scale consistency
- File completeness

Issues found during validation are documented and communicated back to you if
corrections are needed.

### 8.3 Layer Classification

Each layer is mapped to an ownership class (SYSTEM_OWNED, CONTEXT_ONLY,
ANNOTATION) using the layer ownership summary you provided and the platform's
automated classification rules.

### 8.4 Readiness Classification

Each system family is assigned a readiness status:

| Status     | Meaning                                                    |
|------------|------------------------------------------------------------|
| READY      | System is fully configured and can generate details.       |
| PARTIAL    | System is partially configured. Some conditions available. |
| BLOCKED    | Critical information is missing. Cannot proceed.           |
| NO_SOURCE  | No DXF files received for this system family.              |

You will receive a receipt confirming the readiness status of your submission
and any action items required to reach READY status.

---

## 9. Privacy

### 9.1 Competitive Separation

Your system details, product data, and assembly definitions are not exposed to
competing manufacturers. Each manufacturer's data is stored and processed
independently.

### 9.2 System Internals Not Shared

The internal architecture, algorithms, and classification methods used by the
platform are not disclosed to manufacturers. This manual describes input
requirements and expected behavior, not implementation details.

### 9.3 Output Control

Generated details that include your system are produced for use by specifiers
and project teams. Your product names, layer sequences, and system
configurations appear in the output as you defined them. The platform does not
alter your product names or misrepresent your system composition.

### 9.4 Data Handling

Submitted files are stored securely and used only for the purpose of
configuring your system within the platform. Files are not shared with third
parties, used for purposes outside the platform, or retained beyond the active
service period without your consent.

---

## Contact

For questions about this manual or the submission process, contact your
assigned platform representative. Include your manufacturer name and system
family name in all correspondence.

---

*End of Manufacturer Detail System Input Manual*
