# Navigation Spec — Construction Application OS v0.1

## Status
Conceptual only. No UI implementation in this pass.

## Navigation Structure (Conceptual)

```
Home
├── Assembly Parser
│   ├── New Assembly (input)
│   ├── Active Workflows
│   └── Deliverables (DXF/SVG outputs)
├── Spec Intelligence
│   ├── New Specification (input)
│   ├── Active Workflows
│   └── Intelligence Reports
├── Audit
│   └── Execution Trail Viewer
└── Settings
    └── Role / Preferences
```

## Navigation Rules
- Navigation items filtered by user role
- Estimators see Spec Intelligence only
- Detailers see Assembly Parser only
- Project Managers see all applications
- System role has no UI navigation (API only)
