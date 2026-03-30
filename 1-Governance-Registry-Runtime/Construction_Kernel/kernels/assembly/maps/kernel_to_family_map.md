# Kernel-to-Family Map — Construction Assembly Kernel

## Purpose

Maps this kernel's position and relationships within the construction-kernel family.

## Family Architecture

```
                  ValidKernel_Registry
                         |
        Construction_Reference_Intelligence
           (reference-intelligence layer)
                         |
     +---------+---------+---------+---------+
     |         |         |         |         |
  Spec      Assembly  Material  Chemistry  Scope
  Kernel    Kernel    Kernel    Kernel     Kernel
            (this)
```

## Relationship to Each Sibling

### Construction_Specification_Kernel

- **Direction**: Assembly references specification by spec_ref
- **Exchange**: Assembly components may reference specification sections. Assembly configurations are constrained by specification requirements.
- **Boundary**: This kernel records what the assembly is; Spec Kernel records what the specification requires.

### Construction_Material_Kernel

- **Direction**: Assembly references materials by material_ref
- **Exchange**: Every assembly layer has a material_ref pointing to the Material Kernel. Assembly configurations depend on material properties but do not store them.
- **Boundary**: This kernel records layer position and control-layer assignment; Material Kernel records material properties.

### Construction_Chemistry_Kernel

- **Direction**: Indirect — via material_ref through Material Kernel
- **Exchange**: Chemistry compatibility between adjacent layers affects assembly viability. This kernel records the layer stack; Chemistry Kernel determines compatibility.
- **Boundary**: This kernel does not assess chemical compatibility.

### Construction_Scope_Kernel

- **Direction**: Scope references assembly IDs
- **Exchange**: Scope boundaries may align with assembly transitions. Trade handoff points often coincide with interface zones.
- **Boundary**: This kernel records assembly configurations; Scope Kernel records who builds what.

### Construction_Reference_Intelligence

- **Direction**: Intelligence reads assembly truth
- **Exchange**: Intelligence layer reads all assembly objects for pattern analysis, failure correlation, and cross-domain insight.
- **Boundary**: Intelligence observes and annotates; it does not modify assembly truth.

## Shared Artifact Consumption

All siblings consume the same shared artifacts from Construction_Reference_Intelligence/shared/. This kernel does not define or modify shared artifacts.
