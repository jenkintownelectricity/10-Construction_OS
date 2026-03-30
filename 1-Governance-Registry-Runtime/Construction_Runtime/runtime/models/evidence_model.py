"""Evidence and candidate object models.

Evidence records are non-canonical inputs extracted from source documents.
Candidate objects represent inferred construction elements pending resolution.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EvidenceRecord:
    """A record of evidence extracted from a source document.

    Evidence is a non-canonical input — it does not define doctrine.
    It is used to inform assembly inference and candidate generation.
    """

    evidence_id: str = ""
    source_document: str = ""
    extraction_method: str = ""
    confidence: float = 0.0
    extracted_entities: list[dict] = field(default_factory=list)
    source_page: Optional[int] = None
    source_section: str = ""
    timestamp: str = ""


@dataclass
class CandidateObject:
    """A candidate construction element inferred from evidence.

    Candidates are proposed assemblies, interfaces, parameters, or conditions
    that require resolution before becoming part of the project model.
    """

    candidate_id: str = ""
    candidate_type: str = ""  # assembly | interface | parameter | condition
    confidence: float = 0.0
    source_evidence_refs: list[str] = field(default_factory=list)
    extraction_method: str = ""
    resolved: bool = False
