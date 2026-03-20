# Mirror Activation Checklist — gcp_shopdrawing

**Mirror ID:** gcp_shopdrawing
**Checklist Date:** 2026-03-20
**Checklist Version:** L0.6

## L0.6 Validity Checks

| #  | Check                                | Status  | Notes                                              |
|----|--------------------------------------|---------|----------------------------------------------------|
| 1  | Reflection inventory present         | PASS    | reflection-inventory.yaml created and populated    |
| 2  | All ACTIVE slices have contracts     | PASS    | 5 ACTIVE slices each declare contracts             |
| 3  | All ACTIVE slices have schemas       | PASS    | Schemas defined for all 5 ACTIVE slices            |
| 4  | All ACTIVE slices have fixtures      | PASS    | 3 fixtures per ACTIVE slice (15 total)             |
| 5  | All ACTIVE slices have mappings      | PASS    | GCP-specific mappings declared per ACTIVE slice    |
| 6  | Dependency graph is acyclic          | PASS    | slice-dependency-graph.json verified cycle-free    |
| 7  | Parity baseline recorded             | PASS    | parity-baseline.yaml created with measurements    |
| 8  | STAGED slices enumerated             | PASS    | 10 STAGED slices listed in inventory               |
| 9  | Transfer detachment plan exists      | PASS    | transfer/detachment-test-plan.md authored          |
| 10 | Directory structure complete         | PASS    | All 9 subdirectories present with README files     |
| 11 | No circular dependency in ACTIVE set | PASS    | ACTIVE edges form a DAG (layers 0-4)               |
| 12 | Drift baseline initializable         | PENDING | Awaiting first canonical-kernel sync to establish  |

## Summary

- **Passed:** 11 / 12
- **Pending:** 1 / 12 (drift baseline requires first sync event)
- **Failed:** 0 / 12

## Next Steps

1. Execute first canonical-kernel sync to establish drift baseline (check 12).
2. Promote STAGED slices to ACTIVE as contracts and fixtures are finalized.
3. Run full parity test suite once all ACTIVE slices reach FULL parity level.
