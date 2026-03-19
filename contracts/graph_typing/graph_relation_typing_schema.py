"""Kernel-owned graph relation typing schema.

Defines typing rules for how graph edges relate node types.
This is a structural contract — runtime enforces it during materialization.
"""

# Valid (from_node_type, edge_type, to_node_type) triples.
# Runtime must validate materialized edges against this set.
VALID_EDGE_RELATIONS = frozenset({
    # Dependency and blocking
    ("condition", "depends_on", "condition"),
    ("condition", "blocked_by", "blocker"),
    ("condition", "blocked_by", "issue"),
    ("blocker", "resolved_by", "remediation"),
    ("issue", "resolved_by", "remediation"),
    # Interface relationships
    ("assembly", "interfaces_with", "assembly"),
    ("condition", "interfaces_with", "interface"),
    # Implementation and derivation
    ("detail", "implemented_by", "assembly"),
    ("condition", "derived_from", "evidence"),
    ("artifact", "derived_from", "package"),
    # Classification (enrichment-derived)
    ("condition", "classified_as", "pattern"),
    # Inclusion / containment
    ("assembly", "included_in", "package"),
    ("artifact", "included_in", "package"),
    ("detail", "included_in", "assembly"),
    ("condition", "included_in", "assembly"),
    # Revision lineage
    ("condition", "revised_by", "revision"),
    ("assembly", "revised_by", "revision"),
    ("package", "revised_by", "revision"),
    ("artifact", "revised_by", "revision"),
    # Ownership
    ("condition", "owned_by", "owner"),
    ("assembly", "owned_by", "owner"),
    # Support
    ("evidence", "supported_by", "artifact"),
    ("remediation", "supported_by", "evidence"),
})
