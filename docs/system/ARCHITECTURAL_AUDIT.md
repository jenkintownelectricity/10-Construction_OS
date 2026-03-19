# Architectural Audit — Construction_Intelligence_Workers

**Audit date:** 2026-03-19
**Auditor:** Architectural audit pass (pre-map-freeze)
**Repo:** jenkintownelectricity/Construction_Intelligence_Workers
**Version audited:** v0.1 (baseline_commit: PENDING)

---

## 1. Repo Identity

Construction_Intelligence_Workers is a governance and doctrine repository that specifies a fleet of five workers for extracting structured intelligence from construction documents. It defines worker behavior, output contracts, routing rules, and boundaries — but contains zero executable code.

## 2. Audit Context

Provisional classification described this as "execution-layer workers running automation pipelines" with tags `workers, automation, pipeline` and `grown_from: Construction_Runtime`. This audit checks that classification against actual repo contents.

## 3. Current Observed Purpose

**Worker fleet specification and doctrine repository** that defines:
- Five workers: assembly_interpreter, spec_parser, detail_extractor, material_intelligence, compliance_signal
- Output contracts: observation, extracted_structure, proposal, signal
- Routing rules to governed validation surfaces (Construction_Runtime, Construction_Application_OS)
- Four frozen seams: no truth definition, no self-canonicalization, proposal-only outputs, handoff-required posture
- Kernel bindings per worker

Self-identifies as sitting "beside the stack" (not a numbered layer). All worker outputs are non-canonical proposals that must be validated by downstream surfaces before consumption.

Contains **zero executable code**. All content is doctrine, architecture documentation, contracts, and maps.

## 4. Recommended Layer

**execution**

Rationale: Despite containing no executable code in v0.1, the repo defines workers whose purpose is to execute document extraction pipelines. The workers process inputs and produce structured outputs — this is execution-layer work. The specification-only status is a maturity artifact, not a classification signal. When implemented, these workers will run automation pipelines.

## 5. Recommended primary_area

**execution**

## 6. What It Owns

- Worker doctrine and behavioral boundaries
- Worker inventory (5 workers) and per-worker specifications
- Output contracts and schemas (proposal, observation, extracted_structure, signal)
- Handoff requirements and routing rules
- Confidence scoring methodology
- Kernel bindings per worker
- Signal surface mapping
- Frozen seams (4 non-negotiable constraints)

## 7. What It Does Not Own

- Truth definition (Universal_Truth_Kernel, Construction_Kernel)
- Validation logic (Construction_Runtime)
- Upstream kernel schemas (Construction_Kernel)
- Downstream consumer logic (Construction_Assistant, Opportunity_Intelligence)
- Actual document/drawing processing implementation (no code exists)
- Application orchestration (Construction_Application_OS)
- State persistence (workers are stateless by design)

## 8. Recommended grown_from

`Construction_Runtime`

Evidence: Workers consume Construction_Runtime validation pipelines and signal audit surfaces. Worker-to-runtime maps document specific routing to Construction_Runtime components. The worker fleet concept is an extraction layer that feeds into the runtime's validation infrastructure.

## 9. Recommended upstream_affinity

`Construction_Runtime`

Rationale: Workers route outputs to Construction_Runtime validation surfaces. Workers also reference Construction_Kernel for domain schemas and Construction_Application_OS for proposal review surfaces, but the primary operational dependency is on Construction_Runtime's validation infrastructure.

## 10. Suggested Tags

`workers, extraction, proposals, doctrine, signal-generation, execution`

## 11. Confidence Scores

| Dimension | Score |
|---|---|
| Repo understanding | 88 |
| Role fit | 75 |
| Lineage confidence | 80 |
| Affinity confidence | 80 |
| Tag confidence | 80 |

Note: Role fit score is lower because the repo currently contains only specifications, not implementations. The execution-layer classification is based on intended purpose rather than current content. If the repo remains specification-only, it may be better classified as a design artifact.

## 12. Provisional Understanding Assessment

**Refined.**

The provisional classification of "execution-layer workers running automation pipelines" was directionally correct but overstated:
- **Layer:** Correct (execution), but the repo does not currently run anything — it only specifies.
- **Characterization:** "Running automation pipelines" implies active execution. The repo defines worker specifications and doctrine with zero executable code.
- **grown_from:** `Construction_Runtime` is confirmed correct.
- **Tags:** `automation` and `pipeline` overstate current maturity. More accurate: `extraction, proposals, doctrine`.
- **Key correction:** Workers do not run automation pipelines — they extract intelligence and emit proposals. The "beside the stack" self-positioning and proposal-only output model differ from traditional pipeline workers.

## 13. Follow-up Recommendation

- Determine where worker implementation code will live (this repo or separate implementation repos).
- Clarify the "beside the stack" positioning — if workers are execution-layer, they should be in the stack, not beside it.
- Monitor whether the proposal-only output model holds as implementation progresses, or whether workers eventually gain direct write capabilities.
- Role fit confidence will increase once executable code exists.
