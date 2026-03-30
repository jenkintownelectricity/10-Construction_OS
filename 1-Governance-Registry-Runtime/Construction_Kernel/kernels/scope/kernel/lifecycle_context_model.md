# Lifecycle Context Model

## Purpose

Defines how scope spans the full project lifecycle from design through closeout. Different scope objects are primary at different lifecycle phases, and this model maps those relationships.

## Lifecycle Phases

### Design
Scope is being defined. Documents produced during design establish the initial scope truth:
- Contract drawings define work boundaries
- Specifications define inclusions and exclusions
- Bid packages define trade responsibility boundaries

**Primary scope objects**: Scope of Work, Trade Responsibility

### Preconstruction
Scope is refined through coordination:
- Trade contractors review scope assignments
- Interface zones are identified and discussed
- Sequencing is planned
- Scope gaps are identified and resolved

**Primary scope objects**: Trade Responsibility, Sequence Steps, Interface references

### Construction
Scope is executed. Work operations occur per the defined sequence:
- Trades perform work per scope assignments
- Hold points trigger inspections
- Scope changes are documented through revision lineage
- BECx construction observations occur

**Primary scope objects**: Work Operations, Sequence Steps, Inspection Steps

### Commissioning
Scope verification occurs:
- Pre-cover inspections before concealment
- Performance testing (air, water)
- Seasonal observations across weather conditions
- Deficiency documentation and resolution

**Primary scope objects**: Commissioning Steps, Inspection Steps

### Closeout
Scope deliverables are collected and transferred:
- Warranty submissions from all envelope trades
- As-built documentation reflecting actual construction
- Maintenance manuals for ongoing care
- Training for facility staff
- Final inspections and punch list resolution

**Primary scope objects**: Closeout Requirements, Warranty Handoff Records

## Phase Transitions

| Transition | Trigger | Scope Impact |
|---|---|---|
| Design to Preconstruction | Contract award | Scope becomes contractual |
| Preconstruction to Construction | Notice to proceed | Scope becomes executable |
| Construction to Commissioning | Substantial completion approaching | Verification scope activates |
| Commissioning to Closeout | Performance tests passed | Handoff scope activates |

## Phase-Scope Integrity Rules

1. Scope of work records should not remain in `draft` status past the preconstruction phase.
2. Inspection steps must be defined before the construction phase for hold-point items.
3. Closeout requirements must be defined before substantial completion.
4. Warranty handoff records must be finalized before final completion.
