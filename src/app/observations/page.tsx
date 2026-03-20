const OBSERVATIONS = [
  { id: "OBS-0147", detail: "Flashing at parapet intersection", severity: "High", project: "Heritage Plaza Renovation", observer: "Sarah Chen", date: "2026-03-20", status: "Open", notes: "Membrane lap is only 2 inches at intersection. Code requires 4 inches minimum. Ponding water observed at low point." },
  { id: "OBS-0146", detail: "Sealant joint at curtain wall", severity: "Medium", project: "Waterfront Tower Phase 2", observer: "Michael Torres", date: "2026-03-20", status: "Open", notes: "Joint width exceeds manufacturer maximum. Sealant shows early signs of adhesion loss at south elevation." },
  { id: "OBS-0145", detail: "Roof membrane termination", severity: "Low", project: "Metro Station Canopy", observer: "Rachel Kim", date: "2026-03-19", status: "Resolved", notes: "Termination bar secured correctly. Minor aesthetic issue with exposed fastener heads." },
  { id: "OBS-0144", detail: "Window head flashing continuity", severity: "High", project: "Heritage Plaza Renovation", observer: "Sarah Chen", date: "2026-03-19", status: "Open", notes: "Head flashing discontinuous at mullion. No end dam installed at left jamb transition." },
  { id: "OBS-0143", detail: "Below-grade waterproofing overlap", severity: "Medium", project: "Airport Terminal B Extension", observer: "James Park", date: "2026-03-18", status: "In Review", notes: "Overlap meets minimum requirement but alignment is inconsistent. Protection board not yet installed." },
  { id: "OBS-0142", detail: "Expansion joint cover alignment", severity: "Low", project: "Civic Center Library Wing", observer: "Lisa Wang", date: "2026-03-18", status: "Resolved", notes: "Cover plate re-aligned after initial installation. Now meets tolerance requirements." },
  { id: "OBS-0141", detail: "Metal panel clip spacing", severity: "High", project: "Industrial Park Building C", observer: "David Olsen", date: "2026-03-17", status: "Open", notes: "Clip spacing at 24 inches o.c. exceeds 16 inch maximum specified for wind zone. Structural review needed." },
  { id: "OBS-0140", detail: "Masonry through-wall flashing", severity: "Medium", project: "Civic Center Library Wing", observer: "Lisa Wang", date: "2026-03-17", status: "Open", notes: "Through-wall flashing end dams missing at corner condition. Weep spacing at 32 inches exceeds 24 inch maximum." },
];

const SEVERITY_COUNTS = { High: 3, Medium: 3, Low: 2 };

export default function ObservationsPage() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-6">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>Observations</h1>
          <p className="text-sm text-brand-text-muted mt-1">Field observation feed and severity tracking</p>
        </div>
        <div className="flex gap-3">
          {(Object.entries(SEVERITY_COUNTS) as [string, number][]).map(([sev, count]) => (
            <div key={sev} className="text-center">
              <div className={`text-lg font-bold ${sev === "High" ? "text-brand-danger" : sev === "Medium" ? "text-brand-warning" : "text-brand-success"}`}>
                {count}
              </div>
              <div className="text-xs text-brand-text-muted">{sev}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Observation Cards */}
      <div className="space-y-4">
        {OBSERVATIONS.map((obs) => (
          <div key={obs.id} className="card">
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-center gap-3">
                <span className="text-xs font-mono text-brand-text-muted">{obs.id}</span>
                <h3 className="text-sm font-semibold">{obs.detail}</h3>
              </div>
              <div className="flex items-center gap-2">
                <span className={`badge ${obs.status === "Open" ? "badge-unavailable" : obs.status === "In Review" ? "badge-degraded" : "badge-healthy"}`}>
                  {obs.status}
                </span>
                <span className={`badge ${obs.severity === "High" ? "badge-unavailable" : obs.severity === "Medium" ? "badge-degraded" : "badge-healthy"}`}>
                  {obs.severity}
                </span>
              </div>
            </div>
            <div className="text-xs text-brand-text-muted mb-2">
              {obs.project} &middot; {obs.observer} &middot; {obs.date}
            </div>
            <p className="text-sm text-brand-text-muted leading-relaxed">{obs.notes}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
