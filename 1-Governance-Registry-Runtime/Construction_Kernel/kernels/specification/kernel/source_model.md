# Source Model — Construction Specification Kernel

## Purpose

Every specification fact in this kernel must trace to a source document. The source model defines the types of source documents and the pointer structure that establishes traceability.

## Source Types

### Project Manual
The primary specification document for a construction project. Contains Division 07 specification sections with requirements, prohibitions, allowances, and associated obligations. This is the most common source type.

### Addendum
A formal modification to the project manual issued before contract award. Addenda change, add, or delete specification content. Each addendum is numbered sequentially and has an issue date.

### RFI (Request for Information)
A formal request for clarification and the response to it. When an RFI response modifies specification intent, the response becomes a source document for the revised specification fact.

### Bulletin
A supplementary instruction issued during construction that clarifies or modifies specification requirements. Bulletins may be issued by the architect, engineer, or owner.

### Standards Body
A reference to a published standard (ASTM, IBC, NFPA, AAMA, ASHRAE). Standards body sources are cited by reference only — the standard's text is not a source stored in this kernel.

## Source Pointer Structure

A source pointer contains:

- `source_id` — unique identifier for the source
- `source_type` — enum: project_manual, addendum, rfi, bulletin, standards_body
- `title` — descriptive title of the source document
- `document_ref` — external document reference (project number, addendum number)
- `page_ref` — page, paragraph, or clause reference within the source
- `date` — date of the source document
- `notes` — supplementary context

## Traceability Rules

1. Every specification record must reference at least one source pointer
2. Source pointers are immutable once committed
3. A source pointer may be referenced by multiple specification records
4. Source pointers do not contain specification content — they point to where content was extracted from
5. When a source document is superseded (e.g., by an addendum), both the original and superseding sources are retained

## Source Hierarchy

When multiple sources address the same specification topic, the following hierarchy governs (most authoritative first):

1. Most recent addendum
2. Most recent RFI response
3. Most recent bulletin
4. Original project manual

This hierarchy is industry convention. The kernel records all sources; the intelligence layer may apply the hierarchy for conflict analysis.

## Source Quality

The kernel does not assess source quality or reliability. A project manual and a manufacturer's data sheet are both valid sources. The distinction between authoritative and supplementary sources is metadata (`source_type`), not a quality judgment.
