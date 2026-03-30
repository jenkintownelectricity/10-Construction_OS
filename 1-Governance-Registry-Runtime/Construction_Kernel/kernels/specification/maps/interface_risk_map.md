# Interface Risk Map — Construction Specification Kernel

## Purpose

This map identifies specification gap risks at each interface zone. When specifications do not explicitly address transitions, the risk of building envelope failure increases.

## Interface Zone Risk Assessment

### roof_to_wall — Risk: CRITICAL

**Required specification coverage:**
- Membrane base flashing height and attachment
- Counter-flashing type and attachment
- Air barrier continuity through transition
- Insulation continuity (thermal bridging prevention)
- Drainage path at transition base

**Common gaps:** Air barrier termination detail unspecified, thermal continuity at transition not addressed, drainage path from wall to roof not defined.

### parapet_transition — Risk: HIGH

**Required specification coverage:**
- Membrane termination at parapet top or behind coping
- Coping attachment and joint treatment
- Through-wall flashing at parapet base
- Parapet cap slope for drainage

**Common gaps:** Coping expansion joint spacing not specified, through-wall flashing not coordinated with roofing.

### penetration — Risk: HIGH

**Required specification coverage:**
- Flashing method per penetration type (pipe, conduit, structural)
- Sealant compatibility with flashing and penetration materials
- Minimum flashing dimensions and overlaps
- Firestopping coordination at rated assemblies

**Common gaps:** Multiple penetration consolidation strategy missing, firestopping not coordinated with waterproofing.

### fenestration_edge — Risk: CRITICAL

**Required specification coverage:**
- Window/door frame-to-wall membrane integration
- Sill pan flashing requirements
- Head and jamb flashing sequencing
- Sealant joint design at perimeter

**Common gaps:** Sequencing of air barrier and window installation not defined, sill drainage path unspecified.

### below_grade_transition — Risk: HIGH

**Required specification coverage:**
- Transition from waterproofing to above-grade weather barrier
- Protection board termination detail
- Drainage board-to-foundation drain coordination
- Insect screen or termite shield coordination

**Common gaps:** Lap direction at grade line not specified, protection board above-grade exposure not addressed.

### expansion_joint — Risk: MEDIUM

**Required specification coverage:**
- Joint cover assembly type and movement capacity
- Membrane termination at joint edges
- Fire-rated joint treatment where required

**Common gaps:** Movement range not quantified, fire rating at expansion joint not addressed.

### roof_edge — Risk: HIGH

**Required specification coverage:**
- Edge metal type and securement
- Membrane termination at edge
- Fascia or gravel stop coordination
- Gutter integration (if applicable)

**Common gaps:** Wind uplift rating of edge assembly not specified, continuous cleat attachment not detailed.

### curb_transition — Risk: MEDIUM

**Required specification coverage:**
- Minimum curb height above finished roof
- Membrane wrap-up and termination method
- Counter-flashing or cap detail
- Equipment mounting coordination

**Common gaps:** Curb height for specific equipment not stated, membrane-to-curb adhesion method unspecified.

### drain_transition — Risk: MEDIUM

**Required specification coverage:**
- Drain flashing integration method
- Clamping ring requirements
- Membrane stripping-in procedure
- Overflow/secondary drain coordination

**Common gaps:** Drain manufacturer coordination with membrane manufacturer not specified.

## Risk Flagging Protocol

When a specification section serves a control layer at an interface zone but lacks explicit requirements for that zone, the kernel flags the gap with `ambiguity_flag: true` and documents the missing coverage.
