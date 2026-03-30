# Intent-to-Repo Map

## Purpose

Maps each intent class to the upstream repo(s) that hold the truth required to answer queries of that type.

## Map

| Intent Class | Primary Repo | Secondary Repo | Notes |
|---|---|---|---|
| Truth lookup | Construction_Kernel | — | Domain facts live in Layer 5 kernels. |
| Status lookup | Construction_Runtime | Construction_Application_OS | Pipeline state in Layer 6; application/workflow state in Layer 7. |
| Lineage lookup | Construction_Kernel | — | Source lineage is governed at the kernel level. |
| Conflict question | Construction_Kernel | Construction_Runtime | Domain truth from Layer 5; validation from Layer 6. |
| Completeness question | Construction_Runtime | Construction_Application_OS | Validation completeness in Layer 6; package completeness in Layer 7. |
| Routing question | Construction_Assistant (internal) | — | Resolved from assistant routing model. No upstream query required. |
| Next-step question | Construction_Application_OS | — | Workflow state and next actions governed at Layer 7. |

## Repo References

| Repo | Layer | Role |
|---|---|---|
| Universal_Truth_Kernel | Layer 0 | Root doctrine. Conceptual reference only. |
| Construction_Kernel | Layer 5 | Domain truth (7 kernels). |
| Construction_Runtime | Layer 6 | Execution engine (pipeline state, validation). |
| Construction_Application_OS | Layer 7 | Application coordination (Assembly Parser, Spec Intelligence). |
| Construction_Assistant | Beside stack | This repo. Query routing and emission. |
