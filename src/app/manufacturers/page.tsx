const MANUFACTURERS = [
  { name: "Sika Corporation", category: "Waterproofing & Sealants", details: 34, products: 18, status: "Active" },
  { name: "Carlisle SynTec", category: "Roofing Membranes", details: 28, products: 12, status: "Active" },
  { name: "Tremco", category: "Sealants & Coatings", details: 22, products: 15, status: "Active" },
  { name: "YKK AP", category: "Curtain Wall Systems", details: 19, products: 8, status: "Active" },
  { name: "Henry Company", category: "Building Envelope", details: 16, products: 11, status: "Active" },
  { name: "W.R. Grace", category: "Waterproofing", details: 14, products: 9, status: "Inactive" },
  { name: "Georgia-Pacific", category: "Sheathing & Barriers", details: 12, products: 7, status: "Active" },
  { name: "Firestone Building Products", category: "Roofing Systems", details: 21, products: 10, status: "Active" },
];

const DETAIL_LIBRARY = [
  { manufacturer: "Sika Corporation", detail: "SikaProof A+ Below-Grade Waterproofing", system: "Below Grade", type: "Installation Guide" },
  { manufacturer: "Sika Corporation", detail: "Sikaflex-15 LM Joint Sealant", system: "Sealants", type: "Technical Data" },
  { manufacturer: "Carlisle SynTec", detail: "Sure-Weld TPO Membrane", system: "Roofing", type: "Installation Guide" },
  { manufacturer: "Carlisle SynTec", detail: "Carlisle FleeceBACK Securement", system: "Roofing", type: "Detail Drawing" },
  { manufacturer: "YKK AP", detail: "YCW 750 OG Curtain Wall", system: "Fenestration", type: "Shop Drawing Reference" },
  { manufacturer: "Tremco", detail: "Spectrem 1 Silicone Sealant", system: "Sealants", type: "Technical Data" },
];

export default function ManufacturersPage() {
  return (
    <div className="max-w-7xl mx-auto py-8 px-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>Manufacturers</h1>
        <p className="text-sm text-brand-text-muted mt-1">Manufacturer detail library and product references</p>
      </div>

      {/* Manufacturer Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4 mb-8">
        {MANUFACTURERS.map((m) => (
          <div key={m.name} className="card">
            <div className="flex items-start justify-between mb-2">
              <h3 className="text-sm font-semibold">{m.name}</h3>
              <span className={`badge ${m.status === "Active" ? "badge-healthy" : "badge-unknown"}`}>{m.status}</span>
            </div>
            <div className="text-xs text-brand-text-muted mb-3">{m.category}</div>
            <div className="flex gap-4 text-xs">
              <div>
                <span className="font-bold" style={{ color: "var(--wl-primary, #1e3a5f)" }}>{m.details}</span>
                <span className="text-brand-text-muted ml-1">details</span>
              </div>
              <div>
                <span className="font-bold" style={{ color: "var(--wl-secondary, #2d5f8a)" }}>{m.products}</span>
                <span className="text-brand-text-muted ml-1">products</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Detail Library */}
      <div className="card">
        <h2 className="text-lg font-semibold mb-4">Detail Library</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                <th className="text-left py-2 pr-4 font-medium">Manufacturer</th>
                <th className="text-left py-2 pr-4 font-medium">Detail</th>
                <th className="text-left py-2 pr-4 font-medium">System</th>
                <th className="text-left py-2 font-medium">Type</th>
              </tr>
            </thead>
            <tbody className="text-brand-text-muted">
              {DETAIL_LIBRARY.map((d, i) => (
                <tr key={i} className="border-b last:border-0" style={{ borderColor: "var(--wl-border, #e2e8f0)" }}>
                  <td className="py-2 pr-4 text-brand-text font-medium">{d.manufacturer}</td>
                  <td className="py-2 pr-4">{d.detail}</td>
                  <td className="py-2 pr-4"><span className="badge badge-unknown">{d.system}</span></td>
                  <td className="py-2 text-xs">{d.type}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
