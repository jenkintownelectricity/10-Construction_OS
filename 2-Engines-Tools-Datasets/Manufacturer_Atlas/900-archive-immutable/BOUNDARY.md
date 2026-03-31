# 900-archive-immutable — Boundary

| Property | Value |
|----------|-------|
| Layer | 900-archive-immutable |
| Purpose | Append-only lineage archive |
| Write Access | Append-only (no overwrite, no delete) |
| Read Access | All layers (read-only reference) |

## Rules

- APPEND-ONLY: Never overwrite existing files
- NEVER DELETE: No file may be removed
- IMMUTABLE: Once written, content is permanent record
