# Interpretation Limitations — Construction Specification Kernel

## Foundational Rule

This kernel records specification facts as written in source documents. It does not interpret, infer, extrapolate, or editorialize beyond what the source text states. Every specification record is a faithful representation of the source language, tagged with structured metadata.

## As-Written Fidelity

When a project specification states "membrane shall be mechanically attached at 12 inches on center in the field," this kernel records:

- The requirement (mechanical attachment at 12" o.c.)
- The obligation level (shall — mandatory)
- The applicable zone (field of roof)
- The source pointer (section, page, paragraph)

It does not infer that perimeter spacing should be tighter. It does not calculate wind uplift resistance from the stated spacing. Those are assembly and engineering concerns owned by other kernels and the intelligence layer.

## Obligation Language Mapping

Specification text uses precise obligation language:

- **"shall"** maps to `obligation_level: "shall"` — mandatory requirement
- **"should"** maps to `obligation_level: "should"` — recommended practice
- **"may"** maps to `obligation_level: "may"` — permissive allowance

When a specification uses non-standard obligation language (e.g., "must," "will," "is to be"), the closest obligation_level is assigned and `ambiguity_flag: true` is set with a note explaining the language deviation.

## Ambiguity Handling

Specifications frequently contain ambiguous language. Common patterns include:

- **Vague performance criteria** — "provide adequate drainage" without defining flow rates
- **Conflicting requirements** — section text contradicts referenced standard edition
- **Undefined terms** — "approved equal" without approval criteria
- **Missing conditions** — substrate preparation requirements not specified
- **Implicit references** — "per manufacturer's requirements" without citing a specific document
- **Conditional triggers without parameters** — "where required by code" without citing the specific code section
- **Unresolved RFI references** — specification references an RFI response that has not been incorporated

When ambiguity is detected, the kernel sets `ambiguity_flag: true` on the affected record. The record is committed with whatever facts can be extracted, and the ambiguous element is documented in the notes field. The kernel does not guess at intended meaning.

## Prohibited Interpretation Activities

The following activities are explicitly outside this kernel's scope:

1. **Gap-filling** — inferring requirements that the spec did not state
2. **Standard summarization** — restating what a referenced standard requires
3. **Equivalency judgments** — determining whether a substitution meets intent
4. **Performance calculation** — computing values from stated parameters
5. **Conflict resolution** — choosing which of two conflicting requirements governs
6. **Intent analysis** — determining what the specifier "meant" versus what they wrote

## Human Resolution Path

Ambiguity flags are surfaced to the intelligence layer, which may present them to human reviewers. When a human resolves an ambiguity, the resolution is recorded as a new specification fact (e.g., an addendum or RFI response) with its own source pointer. The original ambiguous record is not modified — it is superseded via the revision lineage model.

## Why This Matters

Specification disputes in construction frequently arise from interpretation disagreements. By recording facts as-written and flagging ambiguity without resolving it, this kernel provides a neutral, auditable record that supports dispute resolution without introducing bias.
