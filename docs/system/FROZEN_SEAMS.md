# Frozen Seams — Construction_Application_OS

## Frozen Seams

| Seam | Description | Frozen Since |
|------|-------------|-------------|
| Two-app inventory | Only Assembly Parser and Spec Intelligence are first-class v0.1 apps | v0.1 |
| App-to-runtime mapping structure | Maps app capabilities to real Construction_Runtime v0.2 components | v0.1 |
| App-to-kernel mapping structure | Maps app needs to real Construction_Kernel domain kernels | v0.1 |
| Stack position | Layer 7 — Application, above Construction_Runtime, below user apps | v0.1 |
| Truth consumption posture | Consumes truth; does not originate, redefine, or contradict | v0.1 |
| Role model structure | Four roles: Project Manager, Estimator, Detailer, System | v0.1 |

## Boundary Rules

- Application layer coordinates; it does not execute runtime logic
- Application layer references kernel truth; it does not define it
- Application layer consumes governance; it does not define governance doctrine
- Apps must map to real runtime components; speculative mappings are invalid
- Apps must map to real kernel domains; speculative domain references are invalid

## What Must Not Be Casually Redefined

- The two-app v0.1 inventory (do not add speculative apps)
- App-to-runtime mappings (must match Construction_Runtime v0.2 actual state)
- App-to-kernel mappings (must match Construction_Kernel actual domains)
- Truth consumption posture (layer 7 consumes; never originates)
- Stack position and layer number

## What May Evolve

- App specification details (workflow refinements, input/output details)
- UI specs (from conceptual toward implementation)
- Role model details (new roles, refined permissions)
- New workflows for existing apps
- New apps in future versions (with explicit versioning)

## Invalid Drift Patterns

- App layer defining construction truth
- App layer implementing runtime execution logic
- App layer redefining kernel domain boundaries
- App-to-runtime maps referencing nonexistent runtime components
- App-to-kernel maps referencing nonexistent kernel domains
- Adding unlisted first-class apps without version increment

## Safe Change Patterns

- Refining existing app specs
- Extending workflow documentation
- Moving UI specs toward implementation
- Adding roles to role model
- Updating mappings to track runtime/kernel changes
