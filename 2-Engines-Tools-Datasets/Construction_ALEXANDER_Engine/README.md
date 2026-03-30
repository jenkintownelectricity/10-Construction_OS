Construction_ALEXANDER_Engine

Ring-2 advisory pattern-resolution engine for Construction OS.

Responsibilities:
- Consume pattern truth from Construction_Pattern_Language_OS
- Evaluate context conditions
- Produce resolution_result outputs
- Emit advisory proposal and observation events to Construction_Cognitive_Bus

Explicit Boundaries:
- Does not own truth
- Does not mutate kernels
- Does not execute runtime
- Does not render UI
- Does not own registry state