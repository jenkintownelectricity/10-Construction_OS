# Standards-to-Object Map — Construction Specification Kernel

## How Standards Map to Specification Objects

Standards are referenced by specification objects through citation pointers. This map shows the typical mapping between standards bodies and the specification entities that reference them.

## IBC (International Building Code)

| Spec Entity | Relationship | Example |
|---|---|---|
| requirement | Mandatory compliance | "Roof assembly shall comply with IBC Section 1504.1" |
| prohibition | Code prohibition | "Combustible materials prohibited per IBC Section 1403" |
| testing_requirement | Code-required testing | "NFPA 285 testing required per IBC Section 1403.5" |

## ASTM International

| Spec Entity | Relationship | Example |
|---|---|---|
| requirement | Performance criterion | "Membrane tensile strength per ASTM D5147" |
| testing_requirement | Test method | "Field adhesion testing per ASTM D4541" |
| submittal_requirement | Test report | "Submit lab test report per ASTM E2357" |
| requirement | Material standard | "Vapor retarder conforming to ASTM E1745" |

## AAMA

| Spec Entity | Relationship | Example |
|---|---|---|
| requirement | Performance standard | "Flashing per AAMA 711" |
| testing_requirement | Test method | "Water penetration testing per AAMA 501.1" |

## NFPA 285

| Spec Entity | Relationship | Example |
|---|---|---|
| requirement | Fire test compliance | "Assembly shall have passed NFPA 285 testing" |
| submittal_requirement | Test report | "Submit NFPA 285 test report" |
| testing_requirement | Fire test | "Preconstruction NFPA 285 assembly review" |

## ASHRAE 90.1

| Spec Entity | Relationship | Example |
|---|---|---|
| requirement | Energy performance | "Continuous insulation per ASHRAE 90.1 Table 5.5-5" |
| requirement | Air barrier performance | "Air barrier per ASHRAE 90.1 Section 5.4.3" |

## CSI MasterFormat

| Spec Entity | Relationship | Example |
|---|---|---|
| specification_section | Classification | "Section 07 54 00 per MasterFormat" |
| specification_document | Organization | "Division 07 per MasterFormat" |

## Standards Reference Flow

1. Specification text cites a standard
2. The citation is recorded in the requirement's `standards_refs` or `test_method_refs` array
3. A `reference_standard` record is created with the standard's metadata
4. The standard ID is validated against `shared_standards_registry.json`
5. The standard's actual text is never stored in the kernel
