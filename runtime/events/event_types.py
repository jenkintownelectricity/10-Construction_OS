"""Runtime event type constants.

These five event types are the exact governed event names.
Do not rename. Do not add alternative primary event names.
"""


# Required event type constants — exact names per doctrine
ConditionDetected = "ConditionDetected"
DetailResolved = "DetailResolved"
ArtifactRendered = "ArtifactRendered"
ValidationFailed = "ValidationFailed"
RuntimeError = "RuntimeError"

EVENT_TYPES = frozenset({
    ConditionDetected,
    DetailResolved,
    ArtifactRendered,
    ValidationFailed,
    RuntimeError,
})

# Pipeline stage constants for checkpoint mapping
PIPELINE_STAGES = frozenset({
    "pipeline_entry",
    "input_validation",
    "detail_resolution",
    "parameterization",
    "ir_emission",
    "rendering",
    "artifact_rendering",
    "pipeline_complete",
})
