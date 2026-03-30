# Scope Model

## Purpose

Defines the scope of work object -- the root object in the Scope Kernel's object graph. A scope of work record defines work boundaries with explicit inclusions, exclusions, and trade responsibility assignments.

## Definition

A scope of work is a bounded definition of work to be performed under a specific CSI division, trade package, interface zone, or project phase. It is the authoritative record of what is included, what is excluded, and who is responsible.

## Scope Types

| Type | Description |
|---|---|
| `division_scope` | Scope defined at the CSI division level (e.g., all of Division 07) |
| `trade_scope` | Scope defined for a specific trade contractor's package |
| `interface_scope` | Scope defined specifically for an interface zone between trades |
| `phased_scope` | Scope defined for a specific project phase |

## Core Fields

### Inclusions
An explicit list of work items that are part of this scope. If an item is not listed in inclusions, it is not in scope (fail-closed principle).

### Exclusions
An explicit list of work items that are deliberately excluded from this scope. Exclusions prevent ambiguity by calling out items that might reasonably be assumed to be included.

### Trade Responsibilities
References to trade responsibility records that define which trades perform which portions of this scope.

### Operations
References to work operation records that define the activities within this scope.

### Inspection Steps
References to inspection step records that define quality verification for this scope.

### Commissioning Steps
References to commissioning step records that define BECx activities for this scope.

### Closeout Requirements
References to closeout requirement records that define handoff deliverables for this scope.

## Scope Boundaries

Every scope record has boundaries defined by:
1. **CSI sections**: Which specification sections are covered
2. **Control layers affected**: Which functional layers of the building envelope
3. **Interface zones**: Where this scope meets adjacent scopes
4. **Physical extent**: Described in inclusions (e.g., "all roof areas above level 5")

## Scope Gap Detection

A scope gap exists when:
- A work item appears in no scope record's inclusions
- An interface zone has no scope record addressing it
- A control layer has no scope record covering it in a given area
- A trade is referenced but has no trade responsibility record

## Schema Reference

See `schemas/scope_of_work.schema.json` for the formal schema definition.
