const DETAIL_FAMILIES = [
  { id: "DF-001", name: "Parapet Wall Assembly", variants: 6, system: "Roof Edge", readiness: "Ready" },
  { id: "DF-002", name: "Window Head Flashing", variants: 4, system: "Fenestration", readiness: "Ready" },
  { id: "DF-003", name: "Foundation Waterproofing", variants: 3, system: "Below Grade", readiness: "In Progress" },
  { id: "DF-004", name: "Curtain Wall Sill", variants: 5, system: "Fenestration", readiness: "Ready" },
  { id: "DF-005", name: "Roof Membrane Termination", variants: 4, system: "Roofing", readiness: "Review" },
  { id: "DF-006", name: "Expansion Joint Cover", variants: 3, system: "Structural", readiness: "Ready" },
];

const RELATED_DETAILS = [
  { from: "Parapet Wall Assembly", to: "Roof Membrane Termination", relation: "terminates_at" },
  { from: "Window Head Flashing", to: "Curtain Wall Sill", relation: "integrates_with" },
  { from: "Foundation Waterproofing", to: "Expansion Joint Cover", relation: "transitions_to" },
  { from: "Parapet Wall Assembly", to: "Expansion Joint Cover", relation: "intersects" },
];

const INSTALL_SEQUENCE = [
  { step: 1, detail: "Foundation Waterproofing", action: "Apply membrane below grade" },
  { step: 2, detail: "Expansion Joint Cover", action: "Install joint sealant and cover" },
  { step: 3, detail: "Curtain Wall Sill", action: "Set sill flashing with weeps" },
  { step: 4, detail: "Window Head Flashing", action: "Install head flashing over frame" },
  { step: 5, detail: "Roof Membrane Termination", action: "Terminate membrane at edge" },
  { step: 6, detail: "Parapet Wall Assembly", action: "Complete cap flashing and coping" },
];

export default function AtlasPage() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>Atlas</h1>
        <p className="text-sm text-brand-text-muted mt-1">Detail canvas, relationships, and installation sequences</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Detail Canvas */}
        <div className="lg:col-span-2 card">
          <h2 className="text-lg font-semibold mb-4">Detail Families</h2>
          <div className="space-y-2">
            {DETAIL_FAMILIES.map((d) => (
              <div key={d.id} className="flex items-center justify-between py-2.5 px-3 rounded-lg border" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                <div className="flex items-center gap-3">
                  <span className="text-xs font-mono text-brand-text-muted w-16">{d.id}</span>
                  <div>
                    <div className="text-sm font-medium">{d.name}</div>
                    <div className="text-xs text-brand-text-muted">{d.system} &middot; {d.variants} variants</div>
                  </div>
                </div>
                <span className={`badge ${d.readiness === "Ready" ? "badge-healthy" : d.readiness === "In Progress" ? "badge-degraded" : "badge-unknown"}`}>
                  {d.readiness}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Reference Graph Preview */}
        <div className="space-y-6">
          <div className="card">
            <h2 className="text-lg font-semibold mb-3">Related Details</h2>
            <div className="space-y-2">
              {RELATED_DETAILS.map((r, i) => (
                <div key={i} className="text-xs py-2 border-b last:border-0" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                  <div className="font-medium text-brand-text">{r.from}</div>
                  <div className="text-brand-text-muted my-0.5">
                    <span className="inline-block px-1.5 py-0.5 rounded text-[10px] font-mono" style={{ backgroundColor: "var(--wl-surface-alt, #f1f5f9)" }}>
                      {r.relation}
                    </span>
                  </div>
                  <div className="font-medium text-brand-text">{r.to}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h2 className="text-lg font-semibold mb-3">Install Sequence</h2>
            <div className="space-y-2">
              {INSTALL_SEQUENCE.map((s) => (
                <div key={s.step} className="flex gap-3 text-xs py-1.5">
                  <div className="w-5 h-5 rounded-full flex items-center justify-center text-white font-bold text-[10px] shrink-0" style={{ backgroundColor: "var(--wl-primary, #1e3a5f)" }}>
                    {s.step}
                  </div>
                  <div>
                    <div className="font-medium text-brand-text">{s.detail}</div>
                    <div className="text-brand-text-muted">{s.action}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
