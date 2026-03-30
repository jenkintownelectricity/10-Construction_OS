# Non-Goals — Construction Specification Kernel

## What This Kernel Is Not

### Not a Runtime System

This kernel stores structured specification truth. It does not execute workflows, trigger notifications, manage approvals, or run business logic. Runtime consumption of specification data is the responsibility of future runtime layers that read from this kernel. The kernel itself has no execution surface.

### Not an Application

There is no user interface, no API endpoints, no authentication layer, and no session management. This kernel is a structured data repository with schemas and validation rules. Applications that present specification data to users must be built separately and must read from this kernel without modifying its truth surface.

### Not a Standards Text Repository

This kernel references standards by citation only. It does not store, reproduce, summarize, or paraphrase copyrighted standards text from ASTM, IBC, NFPA, AAMA, ASHRAE, or any other standards body. Users who need standards text must obtain it from the issuing organization.

### Not a CAD System

This kernel does not store drawings, geometric models, BIM objects, or spatial coordinates. Specification requirements may reference geometry contexts (wind uplift zones, slope requirements) using structured fields, but geometric representation is out of scope entirely.

### Not a Document Management System

While this kernel tracks specification documents and revisions, it is not a general-purpose document management system. It does not store PDF files, manage file versioning, handle check-in/check-out workflows, or provide full-text search across document content.

### Not a Compliance Engine

This kernel records specification requirements and their obligation levels. It does not evaluate whether a project is in compliance. Compliance assessment requires cross-referencing specification truth with assembly truth, material truth, and field evidence — a function belonging to the intelligence layer.

### Not a Cost Estimating Tool

Specification data may inform cost decisions, but this kernel does not store unit costs, labor rates, quantity takeoffs, or budget estimates. Cost intelligence is outside the construction-kernel family scope.

### Not a Specification Writing Tool

This kernel records specification facts from existing documents. It does not generate, author, or recommend specification language. Specification writing tools may consume kernel data as input, but the kernel itself is not an authoring system.

### Not an Interpretation Service

When specification language is ambiguous, this kernel flags the ambiguity. It does not resolve ambiguity, provide expert opinions, or suggest interpretations. Human judgment is required for ambiguity resolution, and the result of that judgment is recorded as a new specification fact with its own source pointer.

## Why Non-Goals Matter

Clearly defined non-goals prevent scope creep that would compromise the kernel's role as a clean, schema-validated, single-source-of-truth data structure. Every non-goal listed here represents a capability that belongs to a different layer or system.
