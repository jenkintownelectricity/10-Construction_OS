import Link from "next/link";

const QUICK_LINKS = [
  { href: "/atlas", label: "Atlas", desc: "Detail canvas and reference graph" },
  { href: "/projects", label: "Projects", desc: "Active project tracking" },
  { href: "/observations", label: "Observations", desc: "Field observation feed" },
  { href: "/settings/ai", label: "AI Settings", desc: "Configure AI providers" },
];

const RECENT_PROJECTS = [
  { name: "Heritage Plaza Renovation", status: "Active", conditions: 24, observations: 156 },
  { name: "Waterfront Tower Phase 2", status: "Active", conditions: 18, observations: 89 },
  { name: "Metro Station Canopy", status: "In Review", conditions: 12, observations: 47 },
  { name: "Industrial Park Building C", status: "Planning", conditions: 8, observations: 23 },
];

const RECENT_OBSERVATIONS = [
  { detail: "Flashing at parapet intersection", severity: "High", project: "Heritage Plaza", time: "2 hours ago" },
  { detail: "Sealant joint at curtain wall", severity: "Medium", project: "Waterfront Tower", time: "4 hours ago" },
  { detail: "Roof membrane termination", severity: "Low", project: "Metro Station", time: "6 hours ago" },
  { detail: "Window head flashing continuity", severity: "High", project: "Heritage Plaza", time: "8 hours ago" },
];

const METRICS = [
  { label: "Active Projects", value: "12" },
  { label: "Open Conditions", value: "87" },
  { label: "Observations (7d)", value: "234" },
  { label: "Detail Families", value: "156" },
];

export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>
          Dashboard
        </h1>
        <p className="text-sm text-brand-text-muted mt-1">
          Construction intelligence overview
        </p>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {METRICS.map((m) => (
          <div key={m.label} className="card text-center">
            <div className="text-3xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>{m.value}</div>
            <div className="text-xs text-brand-text-muted mt-1">{m.label}</div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Projects */}
        <div className="lg:col-span-2 card">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold">Recent Projects</h2>
            <Link href="/projects" className="text-xs font-medium hover:underline" style={{ color: "var(--wl-secondary, #2d5f8a)" }}>
              View All
            </Link>
          </div>
          <div className="space-y-3">
            {RECENT_PROJECTS.map((p) => (
              <div key={p.name} className="flex items-center justify-between py-2 border-b last:border-0" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                <div>
                  <div className="text-sm font-medium">{p.name}</div>
                  <div className="text-xs text-brand-text-muted">{p.conditions} conditions &middot; {p.observations} observations</div>
                </div>
                <span className={`badge ${p.status === "Active" ? "badge-healthy" : p.status === "In Review" ? "badge-degraded" : "badge-unknown"}`}>
                  {p.status}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Quick Links */}
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">Quick Links</h2>
          {QUICK_LINKS.map((link) => (
            <Link key={link.href} href={link.href} className="card block hover:shadow-md transition-shadow">
              <div className="text-sm font-semibold">{link.label}</div>
              <div className="text-xs text-brand-text-muted mt-0.5">{link.desc}</div>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Observations */}
      <div className="mt-6 card">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Recent Observations</h2>
          <Link href="/observations" className="text-xs font-medium hover:underline" style={{ color: "var(--wl-secondary, #2d5f8a)" }}>
            View All
          </Link>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                <th className="text-left py-2 pr-4 font-medium">Detail</th>
                <th className="text-left py-2 pr-4 font-medium">Severity</th>
                <th className="text-left py-2 pr-4 font-medium">Project</th>
                <th className="text-left py-2 font-medium">Time</th>
              </tr>
            </thead>
            <tbody className="text-brand-text-muted">
              {RECENT_OBSERVATIONS.map((obs, i) => (
                <tr key={i} className="border-b last:border-0" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                  <td className="py-2 pr-4 text-brand-text font-medium">{obs.detail}</td>
                  <td className="py-2 pr-4">
                    <span className={`badge ${obs.severity === "High" ? "badge-unavailable" : obs.severity === "Medium" ? "badge-degraded" : "badge-healthy"}`}>
                      {obs.severity}
                    </span>
                  </td>
                  <td className="py-2 pr-4">{obs.project}</td>
                  <td className="py-2 text-xs">{obs.time}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
