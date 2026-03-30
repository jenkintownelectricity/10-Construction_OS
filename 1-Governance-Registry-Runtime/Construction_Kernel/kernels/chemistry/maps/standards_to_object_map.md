# Standards-to-Object Map

## Purpose

Maps ASTM and industry standards to chemistry kernel objects they govern or inform.

## Standard Mappings

| Standard | Chemistry Object | Relationship |
|---|---|---|
| ASTM C920 | Chemical System (sealant) | Defines classification for elastomeric joint sealants. Systems of type `sealant` align to C920 types. |
| ASTM C794 | Adhesion Rule | Standard test method for adhesion-in-peel of elastomeric joint sealants. Referenced in `test_method_ref`. |
| ASTM C719 | Adhesion Rule | Cyclic movement capability test for joint sealants. Informs adhesion status determination. |
| ASTM C1193 | Chemical System (sealant) | Guide for use of joint sealants. Governs system type and substrate pairing selection. |
| ASTM C1382 | Incompatibility Rule | Test method for determining compatibility of sealant/substrate combinations. |
| ASTM D412 | Polymer Family | Tensile testing of vulcanized rubber. Informs characteristic properties of elastomeric families. |
| ASTM D2240 | Degradation Mechanism | Durometer hardness testing. Used to detect plasticizer loss and UV degradation. |
| ASTM E96 | Chemical System (coating) | Water vapor transmission testing. Relevant to coating and membrane system performance. |
| ASTM C836 | Chemical System (sealant) | Specification for high-solids-content cold liquid-applied elastomeric waterproofing membrane. |
| ASTM D4541 | Adhesion Rule | Pull-off strength of coatings. Referenced for coating adhesion verification. |

## Usage

- `test_method_ref` fields in adhesion rules reference ASTM test method designations.
- Standards inform the enum values and validation rules in contracts.
- Evidence records (`evidence_refs`) cite specific test results per these standards.

## Notes

- This map covers primary Division 07 standards. Additional standards may apply to specific chemistries.
- Standard references are informational. The kernel does not embed standard text.
- Standard revision years are tracked in evidence records, not in kernel schemas.
