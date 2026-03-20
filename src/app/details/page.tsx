const DETAIL_FAMILIES = [
  { family: "Parapet Assemblies", count: 6, system: "Roof Edge", desc: "Cap flashing, coping, membrane termination at parapet walls" },
  { family: "Window Flashings", count: 8, system: "Fenestration", desc: "Head, sill, and jamb flashing for window openings" },
  { family: "Foundation Waterproofing", count: 4, system: "Below Grade", desc: "Membrane systems, drainage board, and protection layers" },
  { family: "Curtain Wall Interfaces", count: 7, system: "Fenestration", desc: "Sill pans, stack joints, and mullion transitions" },
  { family: "Roof Terminations", count: 5, system: "Roofing", desc: "Edge details, penetrations, and membrane terminations" },
  { family: "Expansion Joints", count: 4, system: "Structural", desc: "Cover plates, sealant joints, and bellows assemblies" },
  { family: "Masonry Interfaces", count: 6, system: "Masonry", desc: "Through-wall flashings, weep systems, shelf angles" },
  { family: "Metal Panel Systems", count: 5, system: "Cladding", desc: "Panel clips, joints, and weather barrier integration" },
];

const VARIANTS = [
  { name: "Standard Parapet — TPO", id: "PW-001-A", status: "Verified" },
  { name: "Standard Parapet — EPDM", id: "PW-001-B", status: "Verified" },
  { name: "High Parapet — TPO", id: "PW-002-A", status: "Draft" },
  { name: "Coped Parapet — Metal", id: "PW-003-A", status: "Verified" },
  { name: "Parapet with Gutter", id: "PW-004-A", status: "In Review" },
  { name: "Parapet Expansion Joint", id: "PW-005-A", status: "Draft" },
];

export default function DetailsPage() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>Details</h1>
        <p className="text-sm text-brand-text-muted mt-1">Detail families and variant catalog</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Detail Families */}
        <div className="lg:col-span-2">
          <h2 className="text-lg font-semibold mb-4">Detail Families</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {DETAIL_FAMILIES.map((d) => (
              <div key={d.family} className="card">
                <div className="flex items-start justify-between mb-2">
                  <h3 className="text-sm font-semibold">{d.family}</h3>
                  <span className="text-xs font-mono px-2 py-0.5 rounded" style={{ backgroundColor: "var(--wl-surface-alt, #f1f5f9)" }}>
                    {d.count} variants
                  </span>
                </div>
                <div className="text-xs text-brand-text-muted mb-2">{d.desc}</div>
                <span className="badge badge-unknown">{d.system}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Variant Overview */}
        <div className="card h-fit">
          <h2 className="text-lg font-semibold mb-4">Parapet Variants</h2>
          <div className="space-y-2">
            {VARIANTS.map((v) => (
              <div key={v.id} className="flex items-center justify-between py-2 border-b last:border-0" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                <div>
                  <div className="text-sm font-medium">{v.name}</div>
                  <div className="text-xs font-mono text-brand-text-muted">{v.id}</div>
                </div>
                <span className={`badge ${v.status === "Verified" ? "badge-healthy" : v.status === "In Review" ? "badge-degraded" : "badge-unknown"}`}>
                  {v.status}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
