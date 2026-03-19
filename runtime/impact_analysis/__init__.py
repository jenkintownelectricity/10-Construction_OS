"""Impact analysis — condition graph traversal for downstream/upstream impact assessment.

Consumes a ConditionGraph without modifying it.  May NOT redefine revision
doctrine or package doctrine.
"""

from runtime.impact_analysis.analyzer import ImpactAnalyzer
from runtime.impact_analysis.get_downstream_impacts import get_downstream_impacts
from runtime.impact_analysis.get_upstream_dependencies import get_upstream_dependencies
from runtime.impact_analysis.get_artifact_impacts import get_artifact_impacts
from runtime.impact_analysis.get_revision_impacts import get_revision_impacts

__all__ = [
    "ImpactAnalyzer",
    "get_downstream_impacts",
    "get_upstream_dependencies",
    "get_artifact_impacts",
    "get_revision_impacts",
]
