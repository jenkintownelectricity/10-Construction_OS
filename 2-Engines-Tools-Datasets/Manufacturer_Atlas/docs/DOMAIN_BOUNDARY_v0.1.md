# Domain Boundary v0.1

**SYSTEM PLANE:** domain_plane
**AUTHORITY:** produce_truth

---

## Boundary Definition

This domain owns manufacturer truth for building envelope systems.

### Owned Truth Categories

| Category | Registry Location | Status |
|----------|------------------|--------|
| Manufacturers | registry/manufacturers/ | scaffold |
| Products | registry/products/ | scaffold |
| Systems | registry/systems/ | scaffold |
| Installation Rules | registry/rules/installation/ | grounded |
| Certification Rules | registry/rules/certification/ | grounded |
| Compatibility | registry/compatibility/ | mixed |

### Not Owned (Consumed From Elsewhere)

| Responsibility | Owner |
|---------------|-------|
| Runtime execution | Construction_Runtime |
| UI rendering | Construction_Application_OS |
| Spatial context | Construction_Atlas |
| Governance doctrine | ValidKernel-Governance |
| Signal routing | ValidKernelOS_VKBUS |
| Registry topology | Construction_OS_Registry |

### Projection Surface

`projection/` contains read-only truth-to-consumer translations.
Projection does not mutate truth. It is a downstream convenience surface.

### Schema Surface

`schemas/` contains the canonical truth schemas that govern the
structure of records in `registry/`. Schemas are isolated from records.
