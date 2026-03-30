# Interpretation Limitations — Construction Assembly Kernel

## Posture

The Construction Assembly Kernel records assembly configurations as-designed and as-built. It does not interpret ambiguous conditions, predict performance, or substitute judgment for missing data.

## Recording vs. Interpreting

| Action | Kernel Does | Kernel Does NOT |
|---|---|---|
| Layer stack definition | Records ordered layers with positions and assignments | Infer missing layers from context |
| Control-layer continuity | Records continuity status at each boundary | Predict continuity where data is absent |
| Transition details | Records how assemblies connect at interface zones | Assume connection method if undocumented |
| Test results | Records test configuration and result | Extrapolate results to untested configurations |
| Material references | Stores reference pointer to material entry | Assume material properties from reference |

## Ambiguity Handling

When assembly data is ambiguous, the kernel applies these rules:

1. **Flag, do not resolve.** If a layer's control-layer assignment is unclear, record the layer and set `control_layer_id` to the most conservative assignment with a note documenting the ambiguity.

2. **Draft status for incomplete records.** Any assembly record missing required evidence or containing flagged ambiguities remains in `draft` status. It is not promoted to `active` until resolved.

3. **No inference across kernels.** If material properties would resolve an assembly question (e.g., whether a membrane serves as both air and vapor control), the kernel does not infer from material data. It records the assembly as documented and notes the dependency.

4. **Conflicting sources.** When design documents and field conditions conflict, both are recorded. The kernel does not choose between them. The `notes` field documents the conflict and its source.

5. **Standard interpretation.** The kernel records which standards a tested assembly complies with. It does not interpret whether compliance with one standard implies compliance with another.

## Limitations of Tested Assembly Records

- A tested assembly record documents a specific configuration tested under specific conditions.
- The kernel does not certify that substituting one component makes the assembly non-compliant; it records only what was tested.
- Interpolation and extrapolation of test results are outside kernel scope. Those judgments belong to the intelligence layer or qualified professionals.

## Climate and Geometry Context

Climate and geometry affect assembly design (vapor retarder position, drainage slope, wind exposure). The kernel records these contexts as metadata. It does not contain climate models or structural analysis tools.
