# System Map

## Architecture Overview

```
+---------------------------------------------------------------+
|                    Construction Stack                          |
|                                                                |
|  Layer 0: Universal_Truth_Kernel (root doctrine)               |
|     |                                                          |
|  Layer 5: Construction_Kernel (domain truth)                   |
|     |  7 domain kernels:                                       |
|     |  Governance, Geometry, Chemistry, Assembly,              |
|     |  Reality, Deliverable, Intelligence                      |
|     |                                                          |
|  Layer 6: Construction_Runtime (execution engine)              |
|     |  Pipeline: parse > normalize > validate > generate > audit|
|     |                                                          |
|  Layer 7: Construction_Application_OS (app coordination)       |
|     |  Apps: Assembly Parser, Spec Intelligence                |
|     |                                                          |
+-------+-----------+-------------------------------------------+
        |           |
        | truth     | truth
        | surfaces  | surfaces
        |           |
+-------v-----------v-------------------------------------------+
|                                                                |
|  Construction_Assistant (beside stack)                          |
|                                                                |
|  Reads: governed truth from Layers 5, 6, 7                     |
|  Emits: bounded truth, uncertainty, insufficiency,             |
|         next valid action                                      |
|  Writes: nothing to canonical state                            |
|                                                                |
+------------------------+--------------------------------------+
                         |
                         | bounded emissions
                         v
                    [ Operator ]
```

## Key Relationships

- **Upstream (read-only):** Construction_Kernel, Construction_Runtime, Construction_Application_OS.
- **Conceptual reference:** Universal_Truth_Kernel (Layer 0). Not consumed directly; referenced for doctrinal alignment.
- **Downstream (output-only):** Operator-facing query responses. All emissions are bounded and classified.
- **No lateral peers.** The assistant does not communicate with or depend on other assistant-tier systems.

## Data Flow Direction

All data flows one direction: from governed stack systems to the assistant to the operator. There is no reverse flow. The assistant does not write back to any upstream system.
