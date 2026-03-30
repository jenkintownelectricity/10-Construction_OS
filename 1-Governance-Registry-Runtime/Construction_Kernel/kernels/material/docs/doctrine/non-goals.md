# Non-Goals — Construction Material Kernel

## What This Kernel Is Not

### Not a Product Database

This kernel does not store manufacturer names, brand names, trade names, product numbers, or pricing. Materials are characterized by their physical properties and tested performance against standard test methods. Product-specific data belongs to manufacturer databases and procurement systems.

### Not a Runtime System

This kernel stores structured material truth. It does not execute workflows, trigger notifications, manage approvals, or run business logic. Runtime consumption of material data is the responsibility of future runtime layers that read from this kernel.

### Not a Standards Text Repository

This kernel references ASTM test methods and material standards by citation only. It does not store, reproduce, summarize, or paraphrase copyrighted standards text. Users who need standards text must obtain it from the issuing organization.

### Not a Material Science Textbook

This kernel records published material properties from test data and manufacturer TDS. It does not explain the science behind material behavior, polymer chemistry, thermodynamics, or failure mechanisms. Scientific explanations belong to educational resources and the chemistry kernel.

### Not a Predictive Performance Engine

This kernel records published and tested material properties. It does not predict behavior beyond published data, model long-term performance through simulation, or extrapolate properties to untested conditions. Predictive modeling belongs to engineering analysis tools.

### Not a Specification Writing Tool

Material data from this kernel may inform specifications, but this kernel does not generate specification language. Specification authoring belongs to separate tools that may consume kernel data as input.

### Not a CAD or BIM System

This kernel does not store drawings, geometric models, BIM objects, or spatial coordinates. Material geometry context (low-slope roof, steep-slope wall) is captured as metadata for property applicability, not as geometric representation.

### Not a Cost Estimating Tool

Material data may inform cost decisions, but this kernel does not store unit costs, labor rates, quantity takeoffs, or budget estimates. Cost intelligence is outside the construction-kernel family scope.

### Not a Testing Laboratory

This kernel records test results and references test methods. It does not perform tests, interpret test results beyond pass/fail against stated criteria, or recommend testing programs.

## Why Non-Goals Matter

Clearly defined non-goals prevent scope creep that would compromise the kernel's role as a clean, schema-validated, single-source-of-truth data structure. Every non-goal listed here represents a capability that belongs to a different layer or system.
