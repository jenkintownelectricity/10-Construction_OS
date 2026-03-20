# Mirror Blueprint Notes: GCP Shop Drawing Mirror

> Working notes for the blueprint visualization of this mirror within the
> Construction OS architecture diagrams. These notes guide the rendering of
> this mirror in system maps, dependency graphs, and architectural overviews.

## Visual Identity

- **Mirror ID:** `gcp_shopdrawing`
- **Display Name:** GCP Shop Drawing
- **Color Code:** `#2E7D32` (construction green)
- **Secondary Color:** `#81C784` (light green, for staged elements)
- **Icon:** Drafting compass overlay on document
- **Badge:** `L0.6` (current kernel level)
- **Border Style:** Solid (active mirror; dashed would indicate dormant)

---

## Blueprint Placement

### In the Full System Map

This mirror sits in the **External Integration Layer**, one level outside the
Construction OS kernel core. It is positioned in the "Trade Partner Mirrors"
cluster, alongside other mirrors like `procore_rfi`, `bluebeam_markup`, etc.

```
+--------------------------------------------------+
|              Construction OS Kernel               |
|  +--------------------------------------------+  |
|  |            Core Primitives                  |  |
|  +--------------------------------------------+  |
|  +--------------------------------------------+  |
|  |         Schema Registry (L0)               |  |
|  +--------------------------------------------+  |
+--------------------------------------------------+
          |              |              |
          v              v              v
   +-----------+  +-----------+  +-----------+
   |  Mirror:  |  |  Mirror:  |  |  Mirror:  |
   |   GCP     |  |  Procore  |  |  Bluebeam |
   |  ShopDraw |  |   RFI     |  |  Markup   |
   +-----------+  +-----------+  +-----------+
          |              |              |
          v              v              v
   (Source Systems / External APIs)
```

### Relative Positioning
- **Above:** Kernel core (this mirror hangs below the kernel)
- **Left neighbors:** Other trade partner mirrors
- **Below:** The GCP source system (external, outside trust boundary)
- **Trust boundary line:** Drawn between the mirror and the source system

---

## Internal Structure Visualization

### Slice Ring Diagram

The mirror's internal structure is best visualized as a ring diagram with the
mirror core at the center and slices arranged in concentric rings by activation
status.

```
                    STAGED RING (outer)
         +----------------------------------+
         |  governance  registry  receipt   |
         |  artifact_gen  exec_orch         |
         |  review  delivery  standards     |
         |  spec_ingestion  submittal       |
         |   +-------------------------+    |
         |   |     ACTIVE RING         |    |
         |   |  detail_norm  rules     |    |
         |   |  validation  manifest   |    |
         |   |  lineage                |    |
         |   |   +----------------+   |    |
         |   |   | MIRROR CORE    |   |    |
         |   |   | sync engine    |   |    |
         |   |   | trust boundary |   |    |
         |   |   | contracts      |   |    |
         |   |   +----------------+   |    |
         |   +-------------------------+    |
         +----------------------------------+
```

- **Active slices:** Rendered in solid fill with the primary color
- **Staged slices:** Rendered in outline only with the secondary color
- **Mirror core:** Rendered with a darker shade and a lock icon (trust boundary)

### Dependency Flow Arrows

Within the ring diagram, show dependency arrows between slices:

- `detail_normalization` --> `rules_engine` (normalization feeds rules)
- `rules_engine` --> `validation` (rules feed validation)
- `validation` --> `artifact_manifest` (validated artifacts enter manifest)
- `artifact_manifest` --> `lineage` (manifested artifacts get lineage tracking)
- `lineage` --> `detail_normalization` (lineage informs re-normalization — weak link, dashed arrow)

---

## Connection Visualization

### Upstream Connection (to Kernel)

- **Line style:** Thick solid line
- **Color:** Kernel primary color
- **Label:** "schema-mediated reflection"
- **Direction:** Bidirectional (kernel provides contracts; mirror provides reflections)
- **Annotations:**
  - Show the contract count on the line (e.g., "45 contracts")
  - Show the last sync timestamp

### Downstream Connection (to Source System)

- **Line style:** Thin dashed line
- **Color:** Red-orange (indicating external/untrusted)
- **Label:** "API observation only"
- **Direction:** One-way (mirror observes; never writes back)
- **Annotations:**
  - Show the trust boundary crossing with a shield icon
  - Show the observation frequency (daily/weekly)
  - Explicitly label "NO DATA REPLICATION" near the line

### Cross-Mirror Connections

- **Line style:** Dotted line
- **Color:** Gray
- **Label:** Specific shared schema or reflection name
- **Current cross-mirror links:**
  - None active yet
  - Planned: `detail_normalization` schema sharing with `procore_rfi` mirror

---

## State Indicators for Blueprint

### Mirror Health Badge

Render a small status indicator in the top-right corner of the mirror box:

| State | Color | Icon | Meaning |
|---|---|---|---|
| `HEALTHY` | Green | Checkmark | All syncs passing, no drift |
| `DRIFTING` | Yellow | Warning triangle | Drift detected, within tolerance |
| `DEGRADED` | Orange | Exclamation | Sync failures or contract violations |
| `HALTED` | Red | Stop sign | Sync halted, manual intervention needed |
| `DETACHING` | Purple | Scissors | Breakaway in progress |

### Slice Status Indicators

Each slice in the ring diagram should show its own status:

| Status | Visual Treatment |
|---|---|
| `ACTIVE` | Solid fill, full opacity |
| `STAGED` | Outline only, 40% opacity |
| `PROMOTING` | Pulsing border animation (in interactive views) |
| `STALE` | Hatched fill pattern |
| `FROZEN` | Blue tint overlay with snowflake icon |

---

## Blueprint Annotations

### Key Metrics to Display

When the blueprint supports detail-on-hover or expanded views, show these metrics:

- **Slice count:** 5 active / 10 staged / 15 total
- **Reflection count:** Total reflections across all active slices
- **Contract pass rate:** Percentage of contracts passing
- **Last sync:** Timestamp of most recent successful sync
- **Drift score:** Current aggregate drift score
- **Parity score:** Current parity measurement vs. source system
- **Transfer readiness:** Percentage of slices at FULL_HANDOFF_READY

### Narrative Annotations

For presentation-mode blueprints, include these callout boxes:

1. **"Schema-mediated, not replicated"** — Near the source system connection,
   emphasizing the mirror philosophy.
2. **"Non-destructive breakaway guaranteed"** — Near the trust boundary line,
   emphasizing the safety model.
3. **"2 promotion candidates approaching readiness"** — Near the kernel connection,
   showing value flowing upward.

---

## Animation Notes (Interactive Blueprints)

For interactive or animated blueprint views:

1. **Sync pulse:** When a sync occurs, animate a pulse traveling from the source
   system through the trust boundary into the mirror, then up to the kernel.
2. **Drift warning:** When drift is detected, the affected slice should glow yellow
   with a slow pulse.
3. **Promotion flow:** When a reflection is promoted, animate it lifting from the
   mirror ring into the kernel core, leaving a reference link behind.
4. **Breakaway animation:** If a breakaway is triggered, animate the downstream
   connection line being cut (scissors animation) while the mirror remains intact.

---

## Version History

| Date | Change | Author |
|---|---|---|
| 2026-03-20 | Initial blueprint notes created | Mirror Architecture Team |

---

## Open Questions for Blueprint Design

- [ ] Should staged slices be visible by default or hidden behind a toggle?
- [ ] How to represent the 90-day backward-compatibility shim after promotion?
- [ ] Should cross-mirror connections be shown even when only planned (not active)?
- [ ] What level of metric detail is appropriate for the default (non-expanded) view?
- [ ] Should the blueprint show historical state (e.g., previous sync results) or only current?
