# Domain Bridge Boundary v0.1

**SYSTEM PLANE:** domain_plane
**ROLE:** consume_manufacturer_truth

---

## Boundary Definition

This bridge consumes upstream manufacturer truth. It does not own it.

### Consumed Truth Categories (from upstream)

| Category | Local Path | Upstream Owner |
|----------|-----------|----------------|
| Manufacturers | truth-cache/manufacturers/ | 10-building-envelope-manufacturer-os |
| Products | truth-cache/products/ | 10-building-envelope-manufacturer-os |
| Systems | truth-cache/systems/ | 10-building-envelope-manufacturer-os |
| Installation Rules | truth-cache/rules/installation/ | 10-building-envelope-manufacturer-os |
| Certification Rules | truth-cache/rules/certification/ | 10-building-envelope-manufacturer-os |
| Compatibility | truth-cache/compatibility/ | 10-building-envelope-manufacturer-os |

### Not Owned (consumed from elsewhere)

| Responsibility | Owner |
|---------------|-------|
| Canonical manufacturer truth | 10-building-envelope-manufacturer-os |
| Runtime execution | Construction_Runtime |
| UI rendering | Construction_Application_OS |
| Governance doctrine | ValidKernel-Governance |
| Signal routing | ValidKernelOS_VKBUS |
| Registry topology | Construction_OS_Registry |

### Schemas

`schemas/` contains local read-validation helpers for consumer-side
consistency checks. They are not canonical manufacturer authority schemas.
They exist to validate the shape of consumed records at the bridge boundary.

### Projection

`projection/` contains read-only translation maps and downstream
mapping definitions. Projection does not mutate truth.
