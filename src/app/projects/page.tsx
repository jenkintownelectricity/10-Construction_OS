const PROJECTS = [
  { id: "PRJ-001", name: "Heritage Plaza Renovation", status: "Active", owner: "Sarah Chen", conditions: 24, observations: 156, systems: ["Roofing", "Fenestration", "Below Grade"], startDate: "2025-08-15" },
  { id: "PRJ-002", name: "Waterfront Tower Phase 2", status: "Active", owner: "Michael Torres", conditions: 18, observations: 89, systems: ["Curtain Wall", "Roofing", "Structural"], startDate: "2025-11-01" },
  { id: "PRJ-003", name: "Metro Station Canopy", status: "In Review", owner: "Rachel Kim", conditions: 12, observations: 47, systems: ["Roofing", "Structural", "Waterproofing"], startDate: "2026-01-10" },
  { id: "PRJ-004", name: "Industrial Park Building C", status: "Planning", owner: "David Olsen", conditions: 8, observations: 23, systems: ["Metal Panel", "Roofing"], startDate: "2026-03-01" },
  { id: "PRJ-005", name: "Civic Center Library Wing", status: "Active", owner: "Lisa Wang", conditions: 31, observations: 198, systems: ["Masonry", "Roofing", "Fenestration", "Waterproofing"], startDate: "2025-06-20" },
  { id: "PRJ-006", name: "Airport Terminal B Extension", status: "Active", owner: "James Park", conditions: 42, observations: 267, systems: ["Curtain Wall", "Roofing", "Expansion Joints", "Below Grade"], startDate: "2025-04-01" },
];

export default function ProjectsPage() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>Projects</h1>
          <p className="text-sm text-brand-text-muted mt-1">Active construction projects and condition tracking</p>
        </div>
        <div className="text-sm text-brand-text-muted">{PROJECTS.length} projects</div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
        {PROJECTS.map((p) => (
          <div key={p.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-3">
              <div>
                <span className="text-xs font-mono text-brand-text-muted">{p.id}</span>
                <h3 className="text-base font-semibold mt-0.5">{p.name}</h3>
              </div>
              <span className={`badge ${p.status === "Active" ? "badge-healthy" : p.status === "In Review" ? "badge-degraded" : "badge-unknown"}`}>
                {p.status}
              </span>
            </div>
            <div className="text-xs text-brand-text-muted mb-3">
              Owner: {p.owner} &middot; Started {p.startDate}
            </div>
            <div className="flex gap-4 mb-3 text-xs">
              <div>
                <div className="text-lg font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>{p.conditions}</div>
                <div className="text-brand-text-muted">Conditions</div>
              </div>
              <div>
                <div className="text-lg font-bold" style={{ color: "var(--wl-secondary, #2d5f8a)" }}>{p.observations}</div>
                <div className="text-brand-text-muted">Observations</div>
              </div>
            </div>
            <div className="flex flex-wrap gap-1.5">
              {p.systems.map((s) => (
                <span key={s} className="px-2 py-0.5 rounded text-[10px] font-medium" style={{ backgroundColor: "var(--wl-surface-alt, #f1f5f9)", color: "var(--wl-text-muted, #64748b)" }}>
                  {s}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
