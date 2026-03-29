import { useSyncExternalStore } from "react";
import { useLens, subscribe, getSnapshot, getFeatureCatalog, getCapability, MIRROR_STATES } from "../../lib/mirror";

const PRICING_VALUES: Record<string, number> = {
  "pricing-compatibility-standard": 2400,
  "pricing-atlas-standard": 3200,
  "pricing-governance-pro": 4800,
  "pricing-intelligence-pack": 5600,
  "pricing-detail-standard": 1800,
  "pricing-signal-standard": 1200,
  "pricing-shop-drawing-pro": 3600,
  "pricing-worker-fleet-standard": 2000,
};

function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", minimumFractionDigits: 0 }).format(amount);
}

export function PricingValuePanel() {
  const { activeLens } = useLens();
  const storeState = useSyncExternalStore(subscribe, getSnapshot);
  const features = getFeatureCatalog();

  const activeFeatures = features.filter(
    (f) => storeState.featureStates[f.feature_id]?.mirrorState !== MIRROR_STATES.AVAILABLE
  );

  const totalCost = activeFeatures.reduce((sum, f) => sum + (PRICING_VALUES[f.pricing_key] ?? 0), 0);

  // BUYER LENS: pricing panel
  if (activeLens === "buyer") {
    return (
      <div style={panelStyle}>
        <div style={headerStyle}>Estimated Platform Cost</div>
        {activeFeatures.length === 0 ? (
          <div style={emptyStyle}>Select features to see pricing</div>
        ) : (
          <>
            {activeFeatures.map((f) => (
              <div key={f.feature_id} style={rowStyle}>
                <span style={{ color: "#cbd5e1", fontSize: 11 }}>{f.buyer_label}</span>
                <span style={{ color: "#22c55e", fontSize: 11, fontFamily: "monospace" }}>
                  {formatCurrency(PRICING_VALUES[f.pricing_key] ?? 0)}
                </span>
              </div>
            ))}
            <div style={{ ...rowStyle, borderTop: "1px solid #334155", paddingTop: 8, marginTop: 4 }}>
              <span style={{ color: "#e2e8f0", fontSize: 12, fontWeight: 700 }}>Configured Platform Total</span>
              <span style={{ color: "#22c55e", fontSize: 13, fontWeight: 700, fontFamily: "monospace" }}>
                {formatCurrency(totalCost)}
              </span>
            </div>
          </>
        )}
      </div>
    );
  }

  // INVESTOR LENS: platform value panel
  if (activeLens === "investor") {
    const layers = new Set(activeFeatures.map((f) => getCapability(f.internal_capability_id)?.investor_layer).filter(Boolean));
    return (
      <div style={panelStyle}>
        <div style={headerStyle}>Platform Value Stack</div>
        <div style={sectionStyle}>
          <div style={labelStyle}>Licensing Tier</div>
          <div style={{ color: "#3b82f6", fontSize: 12, fontFamily: "monospace" }}>
            {activeFeatures.length >= 6 ? "Enterprise" : activeFeatures.length >= 3 ? "Professional" : "Starter"}
          </div>
        </div>
        <div style={sectionStyle}>
          <div style={labelStyle}>Deployment Class</div>
          <div style={{ color: "#3b82f6", fontSize: 12, fontFamily: "monospace" }}>
            {activeFeatures.length >= 5 ? "Full Platform" : activeFeatures.length >= 2 ? "Modular" : "Single Module"}
          </div>
        </div>
        <div style={sectionStyle}>
          <div style={labelStyle}>Capability Stack</div>
          {[...layers].map((layer) => (
            <div key={layer} style={{ color: "#94a3b8", fontSize: 10, fontFamily: "monospace", paddingLeft: 8 }}>
              {layer}
            </div>
          ))}
          {layers.size === 0 && <div style={emptyStyle}>No capabilities selected</div>}
        </div>
      </div>
    );
  }

  // ENGINEERING LENS: capability composition
  if (activeLens === "engineering") {
    return (
      <div style={panelStyle}>
        <div style={headerStyle}>Capability Composition</div>
        {activeFeatures.length === 0 ? (
          <div style={emptyStyle}>No features selected</div>
        ) : (
          activeFeatures.map((f) => {
            const cap = getCapability(f.internal_capability_id);
            return (
              <div key={f.feature_id} style={sectionStyle}>
                <div style={{ color: "#a855f7", fontSize: 11, fontFamily: "monospace" }}>{cap?.module_class ?? "Unknown"}</div>
                <div style={{ color: "#64748b", fontSize: 9, fontFamily: "monospace" }}>contract: {cap?.contract_class ?? "N/A"}</div>
                {cap?.dependencies && cap.dependencies.length > 0 && (
                  <div style={{ color: "#475569", fontSize: 9, fontFamily: "monospace" }}>
                    deps: {cap.dependencies.join(", ")}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    );
  }

  // ADMIN LENS: pricing linkage inspection
  return (
    <div style={panelStyle}>
      <div style={headerStyle}>Pricing Linkage Inspection</div>
      {features.map((f) => {
        const featureState = storeState.featureStates[f.feature_id];
        return (
          <div key={f.feature_id} style={{ ...rowStyle, flexDirection: "column", alignItems: "flex-start", gap: 2 }}>
            <div style={{ color: "#eab308", fontSize: 10, fontFamily: "monospace" }}>{f.feature_id}</div>
            <div style={{ color: "#64748b", fontSize: 9, fontFamily: "monospace" }}>
              pricing_key: {f.pricing_key} | value: {formatCurrency(PRICING_VALUES[f.pricing_key] ?? 0)} | state: {featureState?.mirrorState ?? "N/A"}
            </div>
          </div>
        );
      })}
    </div>
  );
}

const panelStyle: React.CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 8,
  padding: 12,
  background: "#0f172a",
  borderRadius: 8,
  border: "1px solid #1e293b",
  minWidth: 240,
};

const headerStyle: React.CSSProperties = {
  fontSize: 10,
  fontFamily: "monospace",
  color: "#64748b",
  textTransform: "uppercase",
  letterSpacing: 1,
  marginBottom: 4,
};

const rowStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: "3px 0",
};

const sectionStyle: React.CSSProperties = {
  padding: "6px 8px",
  background: "#1e293b",
  borderRadius: 4,
};

const labelStyle: React.CSSProperties = {
  fontSize: 9,
  color: "#64748b",
  fontFamily: "monospace",
  marginBottom: 2,
};

const emptyStyle: React.CSSProperties = {
  color: "#475569",
  fontSize: 10,
  fontFamily: "monospace",
  fontStyle: "italic",
};
