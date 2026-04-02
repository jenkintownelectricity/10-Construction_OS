# Contractor Lens Reply Drafting Doctrine v0.1

## Authority
10-Construction_OS (domain execution plane)

## Purpose
Define the rules for AI-assisted reply drafting within the Contractor Lens workspace. Replies are shaped from project context, not invented from imagination.

## Reply Context Inputs

Every reply draft is shaped from:
1. **Project context snapshot** — current project state summary
2. **Claims** — active assertions by parties with evidence links
3. **Posture** — detected project position on the topic
4. **Reconciliation** — intent vs reality status for the topic
5. **Communications** — relevant thread history
6. **Submittals** — related submittal status
7. **Assembly readiness** — compilation and library admission status

## Reply Output Shape

| Field | Purpose |
|-------|---------|
| target_party_id | Who receives the reply |
| topic | Subject of the reply |
| claims_to_address | Which claims this reply responds to |
| evidence_to_cite | Which evidence supports the reply |
| posture_context | Relevant posture assessments |
| tone_guidance | NEUTRAL / FIRM / COLLABORATIVE / ESCALATION |
| risk_level | LOW / MEDIUM / HIGH / CRITICAL |
| draft_body | Proposed reply text |
| status | DRAFT / PROPOSED / REQUIRES_HUMAN_REVIEW / APPROVED / SENT |

## Rules

1. Every reply MUST be labeled DRAFT or REQUIRES_HUMAN_REVIEW until a human approves
2. No autonomous sending — human is final sender and approver
3. Draft body must cite specific evidence and claims, not make unsupported assertions
4. Tone guidance is a suggestion, not a mandate — human adjusts final wording
5. Risk level reflects the assessed project risk of the topic, not the reply risk
6. No legal advice — system surfaces facts, humans make legal judgments

## Current State (2026-04-02)

- Schema: `schemas/project_reply_draft.schema.json`
- Tool: `tools/reply_context_builder.py`
- Example: `output/project_replies/drf_demo_001.json` (STAGED)
- Status: Tool produces context-shaped drafts. No live email integration.
