"""
ALEXANDER Engine configuration constants.

Ring 2 authority boundary — advisory pattern resolution only.
"""

import os
from pathlib import Path

# Engine identity
ENGINE_NAME = "Construction_ALEXANDER_Engine"
SOURCE_COMPONENT = "Construction_ALEXANDER_Engine"
SOURCE_REPO = "Construction_ALEXANDER_Engine"
RING = 2
SCHEMA_VERSION = "1.0.0"

# Cognitive Bus integration
BUS_SCHEMA_VERSION = "0.1"
MAX_PAYLOAD_BYTES = 65536  # 64 KiB
ALLOWED_EVENT_CLASSES = frozenset({"Proposal", "Observation"})
FORBIDDEN_EVENT_CLASSES = frozenset({"ExternallyValidatedEvent"})

# Resolution statuses
STATUS_RESOLVED = "RESOLVED"
STATUS_UNRESOLVED = "UNRESOLVED"
STATUS_BLOCKED = "BLOCKED"
STATUS_CONFLICT = "CONFLICT"
VALID_STATUSES = frozenset({STATUS_RESOLVED, STATUS_UNRESOLVED, STATUS_BLOCKED, STATUS_CONFLICT})

# Stage statuses
STAGE_PASS = "PASS"
STAGE_FAIL = "FAIL"
STAGE_SKIP = "SKIP"

# Fail reason codes
FAIL_INVALID_CONDITION = "INVALID_CONDITION"
FAIL_MISSING_REQUIRED_FIELD = "MISSING_REQUIRED_FIELD"
FAIL_UNKNOWN_CONDITION_TYPE = "UNKNOWN_CONDITION_TYPE"
FAIL_NO_FAMILY_MATCH = "NO_FAMILY_MATCH"
FAIL_AMBIGUOUS_FAMILY = "AMBIGUOUS_FAMILY"
FAIL_NO_PATTERN_MATCH = "NO_PATTERN_MATCH"
FAIL_AMBIGUOUS_PATTERN = "AMBIGUOUS_PATTERN"
FAIL_NO_VARIANT_MATCH = "NO_VARIANT_MATCH"
FAIL_AMBIGUOUS_VARIANT = "AMBIGUOUS_VARIANT"
FAIL_CONSTRAINT_VIOLATION = "CONSTRAINT_VIOLATION"
FAIL_CONFLICT_DETECTED = "CONFLICT_DETECTED"
FAIL_MISSING_TRUTH = "MISSING_TRUTH"
FAIL_INCOMPATIBLE_CONTEXT = "INCOMPATIBLE_CONTEXT"
FAIL_SCORING_FAILURE = "SCORING_FAILURE"
FAIL_INTERNAL_ERROR = "INTERNAL_ERROR"

# Pipeline stages (ordered)
PIPELINE_STAGES = [
    "intake",
    "normalization",
    "family_classification",
    "pattern_resolution",
    "variant_selection",
    "constraint_enforcement",
    "conflict_detection",
    "scoring",
]

# Condition type to family domain mapping
CONDITION_TYPE_MAP = {
    "roof_edge": "EDGE",
    "parapet": "PARAPET",
    "drain": "DRAIN",
    "penetration": "PIPE",
    "expansion_joint": "JOINT",
    "interface": None,  # requires further classification
    "transition": None,  # requires further classification
}

VALID_CONDITION_TYPES = frozenset(CONDITION_TYPE_MAP.keys())

# Paths
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCHEMAS_DIR = BASE_DIR / "schemas"

# Pattern Language OS path (read-only consumer)
PATTERN_LANGUAGE_OS_DIR = Path(
    os.environ.get(
        "PATTERN_LANGUAGE_OS_DIR",
        str(BASE_DIR.parent / "Construction_Pattern_Language_OS"),
    )
)

# ID format patterns (from Construction_Pattern_Language_OS)
FAMILY_ID_PATTERN = r"^DNA-CONSTR-FAM-[A-Z]+-\d{3}-R\d+$"
PATTERN_ID_PATTERN = r"^DNA-CONSTR-PAT-[A-Z]+-[A-Z]+-\d{3}-R\d+$"
VARIANT_ID_PATTERN = r"^CHEM-CONSTR-VAR-[A-Z]+-\d{3}-R\d+$"
ARTIFACT_ID_PATTERN = r"^COLOR-CONSTR-ART-[A-Z]+-\d{3}-R\d+$"
CONSTRAINT_ID_PATTERN = r"^(TEXTURE|CLIMATE)-CONSTR-CNS-[A-Z]+-\d{3}-R\d+$"
RELATIONSHIP_ID_PATTERN = r"^SOUND-CONSTR-REL-[A-Z]+-\d{3}-R\d+$"
