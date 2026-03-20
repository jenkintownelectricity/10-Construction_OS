const ARTIFACTS = [
  { id: "ART-001", name: "Heritage Plaza — Parapet Details", type: "PDF", format: "pdf", size: "2.4 MB", project: "Heritage Plaza Renovation", created: "2026-03-15", pages: 12, status: "Final" },
  { id: "ART-002", name: "Waterfront Tower — Curtain Wall Shop Drawings", type: "DXF", format: "dxf", size: "8.1 MB", project: "Waterfront Tower Phase 2", created: "2026-03-12", pages: null, status: "In Review" },
  { id: "ART-003", name: "Metro Station — Roof Plan", type: "SVG", format: "svg", size: "1.2 MB", project: "Metro Station Canopy", created: "2026-03-10", pages: null, status: "Final" },
  { id: "ART-004", name: "Heritage Plaza — Window Schedule", type: "PDF", format: "pdf", size: "890 KB", project: "Heritage Plaza Renovation", created: "2026-03-08", pages: 4, status: "Final" },
  { id: "ART-005", name: "Airport Terminal — Foundation Details", type: "DXF", format: "dxf", size: "5.6 MB", project: "Airport Terminal B Extension", created: "2026-03-05", pages: null, status: "Draft" },
  { id: "ART-006", name: "Library Wing — Masonry Elevations", type: "SVG", format: "svg", size: "3.2 MB", project: "Civic Center Library Wing", created: "2026-03-03", pages: null, status: "Final" },
  { id: "ART-007", name: "Industrial Park — Metal Panel Layout", type: "PDF", format: "pdf", size: "1.8 MB", project: "Industrial Park Building C", created: "2026-02-28", pages: 8, status: "In Review" },
  { id: "ART-008", name: "Heritage Plaza — Waterproofing Plan", type: "PDF", format: "pdf", size: "3.1 MB", project: "Heritage Plaza Renovation", created: "2026-02-25", pages: 6, status: "Final" },
];

function FormatBadge({ format }: { format: string }) {
  const colors: Record<string, string> = {
    pdf: "#dc2626",
    dxf: "#2563eb",
    svg: "#059669",
  };
  return (
    <span
      className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold text-white uppercase"
      style={{ backgroundColor: colors[format] ?? "#6b7280" }}
    >
      {format}
    </span>
  );
}

export default function ArtifactsPage() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>Artifacts</h1>
          <p className="text-sm text-brand-text-muted mt-1">Construction documents, drawings, and reference materials</p>
        </div>
        <div className="flex gap-3 text-xs">
          <span className="badge badge-unknown">{ARTIFACTS.filter((a) => a.format === "pdf").length} PDF</span>
          <span className="badge badge-unknown">{ARTIFACTS.filter((a) => a.format === "dxf").length} DXF</span>
          <span className="badge badge-unknown">{ARTIFACTS.filter((a) => a.format === "svg").length} SVG</span>
        </div>
      </div>

      {/* Artifact Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
        {ARTIFACTS.map((a) => (
          <div key={a.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between mb-2">
              <FormatBadge format={a.format} />
              <span className={`badge ${a.status === "Final" ? "badge-healthy" : a.status === "In Review" ? "badge-degraded" : "badge-unknown"}`}>
                {a.status}
              </span>
            </div>
            <h3 className="text-sm font-semibold mt-2 mb-1">{a.name}</h3>
            <div className="text-xs text-brand-text-muted mb-3">
              {a.project}
            </div>
            <div className="flex items-center justify-between text-xs text-brand-text-muted border-t pt-2" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
              <div className="flex gap-3">
                <span>{a.size}</span>
                {a.pages && <span>{a.pages} pages</span>}
              </div>
              <span>{a.created}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
