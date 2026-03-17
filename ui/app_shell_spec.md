# App Shell Spec — Construction Application OS v0.1

## Status
Conceptual only. No UI implementation in this pass.

## Concept
A unified application shell hosting both first-class construction applications with shared navigation, status surfaces, and role-based access.

## Shell Components (Conceptual)
- Application launcher / selector
- Active workflow status display
- Role-based navigation filtering
- Deliverable output viewer
- Audit trail viewer

## Constraints
- Shell coordinates applications; it does not implement runtime logic
- Shell displays outputs from Construction_Runtime; it does not generate them
- Shell respects role model defined in `os/role_model.md`
