# 300-tools

**Purpose:** Operator-facing tools and UI surfaces.

## Subdirectories

| Directory | Purpose |
|-----------|----------|
| 310-manufacturer-atlas-ui | Interactive atlas explorer and surface contract |
| 320-detail-inspector | Detail inspection tool |
| 330-coverage-explorer | Coverage analysis tool |
| 340-system-browser | System hierarchy browser |
| 350-rule-browser | Rule and constraint browser |
| 360-operator-workstation | Integrated operator workstation |

## Dependency Rules

- **Calls:** 200-engines only
- **MUST NOT write to:** 000, 100, or 200
- **Consumed by:** 400-adapters
