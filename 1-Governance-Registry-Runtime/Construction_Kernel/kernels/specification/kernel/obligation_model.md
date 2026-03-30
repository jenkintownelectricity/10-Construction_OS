# Obligation Model — Construction Specification Kernel

## Purpose

This model defines the three obligation levels used in specification documents and how they are recorded in the kernel. Obligation levels determine the binding force of a specification statement.

## Obligation Levels

### Shall — Mandatory

The word "shall" in specification language indicates a mandatory requirement. The contractor is obligated to comply. Non-compliance constitutes a specification violation that may require remediation at the contractor's expense.

**Recording:** `obligation_level: "shall"`

**Examples in Division 07:**
- "Membrane roofing shall be installed by a manufacturer-authorized installer"
- "Air barrier shall achieve maximum air leakage rate of 0.04 cfm/sf at 1.57 psf"
- "Insulation shall have minimum R-30 thermal resistance"
- "Flashing shall extend minimum 4 inches above finished roof surface"

### Should — Recommended

The word "should" indicates a recommended practice. Compliance is expected but deviation is permitted with justification. Non-compliance is not automatically a violation but may be questioned during submittal review or inspection.

**Recording:** `obligation_level: "should"`

**Examples in Division 07:**
- "Installer should have completed manufacturer's training within the past 24 months"
- "Adhesive application should be performed when substrate temperature is above 40 deg F"
- "Test cuts should be taken at minimum two locations per 10,000 square feet"

### May — Permissive

The word "may" indicates permission. It establishes what is allowed, not what is required. May-statements create allowances and alternatives.

**Recording:** `obligation_level: "may"`

**Examples in Division 07:**
- "Contractor may propose alternative fastener pattern with supporting wind uplift calculations"
- "Membrane color may be selected from manufacturer's standard color range"
- "Preconstruction conference may be conducted via video conference"

## Non-Standard Obligation Language

Specifications sometimes use obligation language that does not map cleanly to shall/should/may:

| Spec Language | Mapped Level | Ambiguity Flag |
|---|---|---|
| "must" | shall | false (generally synonymous) |
| "will" | shall | true (ambiguous — may indicate future tense, not obligation) |
| "is to be" | shall | true (non-standard phrasing) |
| "is required" | shall | false |
| "is recommended" | should | false |
| "is permitted" | may | false |
| "is acceptable" | may | false |
| "as directed" | shall | true (authority not specified) |
| "as approved" | shall | true (approval criteria not specified) |

## Obligation and Enforcement

The kernel records obligation levels but does not enforce them. Enforcement is the responsibility of contract administration (architect, engineer, owner's representative). The kernel provides the structured data needed to identify what obligations exist and at what level.

## Compound Obligations

When a single specification clause contains multiple obligation levels, each obligation is recorded separately:
- "Membrane shall be fully adhered at perimeter and corners; membrane may be mechanically attached in the field" produces one `shall` requirement and one `may` allowance.
