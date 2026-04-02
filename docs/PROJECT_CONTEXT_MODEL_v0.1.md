# Project Context Model v0.1

## Authority
10-Construction_OS (domain execution plane)

## Purpose
Define the neutral project context aggregation model for construction project intelligence. Context is a snapshot of current project state — not a judgment, not a recommendation, not a decision.

## Object Families

| Object | Purpose |
|--------|---------|
| project_record | Project identity, parties, status |
| project_party | Stakeholder with role (owner, architect, GC, sub, manufacturer) |
| project_document_record | Document reference with revision tracking |
| project_email_record | Communication record (inbound/outbound) |
| project_thread_record | Communication thread grouping |
| project_submittal_record | Submittal package with items and status |
| project_decision_record | Recorded decision with authority and evidence |
| project_action_item | Action with owner, due date, status |
| project_milestone_record | Schedule milestone with status |
| project_context_snapshot | Aggregated point-in-time summary |

## Rules

1. Context snapshots aggregate — they do not invent or infer
2. UI consumes context snapshots — UI does not own context truth
3. Context does not replace evidence, claims, posture, or reconciliation
4. Context carries counts and summaries, not full records
5. Every snapshot carries lineage with generation timestamp

## Current State (2026-04-02)

- Schema: schemas/project_context_snapshot.schema.json
- Tool: tools/context_snapshot_builder.py
- Example: output/project_context/context_snapshot_demo.json (STAGED)
