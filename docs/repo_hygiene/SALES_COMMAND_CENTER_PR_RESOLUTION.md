# Sales Command Center PR Resolution

## PR Details
- **PR:** #8 — "Install Claude planetary context — slim repo-specific CLAUDE.md"
- **Repo:** Construction_OS_Sales_Command_Center
- **Branch:** claude/ecosystem-website-build-ZLrKF
- **Conflicting file:** .claude/CLAUDE.md

## Root Cause of Conflict
Both `main` and the PR branch created `.claude/CLAUDE.md` independently with overlapping but slightly different content.

**Main branch version** (already merged):
- Title: "CLAUDE SYSTEM CONTEXT — Construction_OS_Sales_Command_Center"
- Has ECOSYSTEM and POSTURE sections
- No ROLE or NOTES sections

**PR branch version:**
- Title: "CLAUDE SYSTEM CONTEXT — SALES COMMAND"
- Has ROLE, NOTES, ECOSYSTEM, and POSTURE sections
- Adds: `ROLE: Sales intelligence command center` and `NOTES: Support tool`

## Merged Content Strategy

The correct merged version preserves the repo-specific title from main, adds the ROLE and NOTES from the PR, and keeps the shared ECOSYSTEM/POSTURE sections. Result:

```markdown
# CLAUDE SYSTEM CONTEXT — Construction_OS_Sales_Command_Center

## ROLE
Sales intelligence command center — governed commercial observer surface.

## NOTES
Non-production scaffold. Generators declared but not yet implemented.
Observes upstream truth from Construction_OS. Does not mutate canonical data.

## ECOSYSTEM
Governance: 00-validkernel-governance (platform intelligence lives there)
Mainframe: https://30-validkernel-platform-production.up.railway.app
UTK: "The system is bounded by truth."

## POSTURE
Claude operates as advisory analysis agent.
Claude may read, analyze, trace, propose.
Claude may NOT mutate canonical doctrine.
```

## Branch Merge Status
The PR can be merged by resolving the conflict with the content above. Since the main branch already has the file, the operator should:

1. Check out the PR branch locally
2. Replace `.claude/CLAUDE.md` with the merged content above
3. Commit and push
4. Merge the PR

## Exact Next Operator Step
```bash
git fetch origin claude/ecosystem-website-build-ZLrKF
git checkout claude/ecosystem-website-build-ZLrKF
# Edit .claude/CLAUDE.md with merged content
git add .claude/CLAUDE.md
git commit -m "Resolve CLAUDE.md conflict — merge main + PR content"
git push origin claude/ecosystem-website-build-ZLrKF
# Then merge PR #8 via GitHub UI
```
