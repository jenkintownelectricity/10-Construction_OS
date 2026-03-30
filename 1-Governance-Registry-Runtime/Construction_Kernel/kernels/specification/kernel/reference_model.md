# Reference Model — Construction Specification Kernel

## Purpose

This model defines how the specification kernel handles cross-references to standards, codes, manufacturer literature, and other external documents. References are citations, not content.

## Reference Types

### Standards References
Citations to published standards from recognized standards bodies (ASTM, AAMA, NFPA, ASHRAE, ISO). Recorded with standard identifier, title, issuing body, and relevance to the specification requirement.

### Code References
Citations to building codes (IBC, IECC, local amendments). Code references establish mandatory compliance requirements that flow into specification obligations.

### Manufacturer Literature
References to manufacturer product data sheets, installation instructions, technical bulletins, and warranty documents. Recorded as source pointers with `source_type: standards_body` when published by a recognized body, or noted in the requirement's `notes` field when manufacturer-specific.

### Industry Guidance
References to design guides, best practice documents, and industry publications (WBDG, NRCA Manual, SMACNA guidelines). These are advisory references and do not create mandatory obligations unless the specification explicitly adopts them.

## Reference Resolution

References in this kernel are pointers, not content. A reference to "ASTM D4541" tells the consumer:

1. A standard with this identifier exists
2. The specification cites it for a specific purpose (e.g., test method for adhesion)
3. The consumer must obtain the actual standard for its content

The kernel does not resolve references — it does not retrieve, display, or summarize the referenced document.

## Cross-Kernel References

Specification records may reference entities in sibling kernels via pointer:

- Assembly kernel: specification requires a specific assembly type (pointer to assembly_id)
- Material kernel: specification requires a material property threshold (pointer to material property)
- Scope kernel: specification references scope boundary (pointer to scope definition)

These cross-kernel references use ID strings, not embedded objects. The referenced kernel owns the truth about the referenced entity.

## Reference Validation

References to standards in `shared_standards_registry.json` can be validated against the registry. References to standards not in the registry are flagged for registry update. Cross-kernel references are validated by the intelligence layer, not by this kernel.

## Reference Freshness

The kernel records the edition or version of a referenced standard as stated in the specification. It does not track whether a newer edition has been published. Standards currency analysis is an intelligence layer function.
