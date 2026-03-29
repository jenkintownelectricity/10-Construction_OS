import { useSyncExternalStore } from "react";
import { useLens, subscribe, getSnapshot, getFeatureCatalog, getCapability, type LensType, type FeatureCatalogEntry } from "../../lib/mirror";

function getAssistantMessage(feature: FeatureCatalogEntry, lens: LensType): string {
  if (lens === "buyer") return feature.buyer_summary;
  if (lens === "investor") return feature.investor_summary;
  if (lens === "engineering") return feature.engineering_summary;
  if (lens === "admin") return feature.admin_summary ?? "No admin summary available.";
  return feature.buyer_summary;
}

function getAssistantPrefix(lens: LensType): string {
  if (lens === "buyer") return "This feature";
  if (lens === "investor") return "Strategic value";
  if (lens === "engineering") return "Capability mapping";
  if (lens === "admin") return "Registry inspection";
  return "";
}

export function MirrorAssistantPanel() {
  const { activeLens } = useLens();
  const storeState = useSyncExternalStore(subscribe, getSnapshot);
  const features = getFeatureCatalog();

  const selectedNode = storeState.selectedNodeId;
  const selectedFeature = selectedNode
    ? features.find((f) => f.mirror_node_id === selectedNode)
    : null;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 8,
        padding: 12,
        background: "#0f172a",
        borderRadius: 8,
        border: "1px solid #1e293b",
        minHeight: 120,
      }}
    >
      <div
        style={{
          fontSize: 10,
          fontFamily: "monospace",
          color: "#64748b",
          textTransform: "uppercase",
          letterSpacing: 1,
          display: "flex",
          justifyContent: "space-between",
        }}
      >
        <span>Assistant</span>
        <span style={{ color: "#475569" }}>{activeLens} lens</span>
      </div>

      {!selectedFeature ? (
        <div
          style={{
            color: "#475569",
            fontSize: 11,
            fontFamily: "monospace",
            fontStyle: "italic",
            padding: "16px 0",
          }}
        >
          Select a node in the Mirror Graph to inspect.
        </div>
      ) : (
        <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
          {/* Feature name in active lens */}
          <div style={{ color: "#e2e8f0", fontSize: 12, fontWeight: 600, fontFamily: "monospace" }}>
            {activeLens === "buyer" && selectedFeature.buyer_label}
            {activeLens === "investor" && selectedFeature.investor_label}
            {activeLens === "engineering" && selectedFeature.engineering_label}
            {activeLens === "admin" && (selectedFeature.admin_label ?? selectedFeature.buyer_label)}
          </div>

          {/* Lens-specific prefix */}
          <div style={{ color: "#64748b", fontSize: 9, fontFamily: "monospace", textTransform: "uppercase" }}>
            {getAssistantPrefix(activeLens)}
          </div>

          {/* Lens-adaptive explanation */}
          <div
            style={{
              color: "#94a3b8",
              fontSize: 11,
              fontFamily: "monospace",
              lineHeight: 1.5,
              padding: "6px 8px",
              background: "#1e293b",
              borderRadius: 4,
            }}
          >
            {getAssistantMessage(selectedFeature, activeLens)}
          </div>

          {/* Engineering lens: show capability details */}
          {activeLens === "engineering" && (
            <div style={{ padding: "4px 8px" }}>
              {(() => {
                const cap = getCapability(selectedFeature.internal_capability_id);
                if (!cap) return null;
                return (
                  <div style={{ display: "flex", flexDirection: "column", gap: 3 }}>
                    <div style={{ color: "#a855f7", fontSize: 9, fontFamily: "monospace" }}>
                      module: {cap.module_class}
                    </div>
                    <div style={{ color: "#64748b", fontSize: 9, fontFamily: "monospace" }}>
                      contract: {cap.contract_class}
                    </div>
                    {cap.dependencies.length > 0 && (
                      <div style={{ color: "#475569", fontSize: 9, fontFamily: "monospace" }}>
                        dependencies: {cap.dependencies.join(", ")}
                      </div>
                    )}
                  </div>
                );
              })()}
            </div>
          )}

          {/* Admin lens: show registry mapping */}
          {activeLens === "admin" && (
            <div
              style={{
                padding: "4px 8px",
                background: "#1e293b",
                borderRadius: 4,
                display: "flex",
                flexDirection: "column",
                gap: 2,
              }}
            >
              <div style={{ color: "#eab308", fontSize: 9, fontFamily: "monospace" }}>
                feature_id: {selectedFeature.feature_id}
              </div>
              <div style={{ color: "#eab308", fontSize: 9, fontFamily: "monospace" }}>
                capability_id: {selectedFeature.internal_capability_id}
              </div>
              <div style={{ color: "#eab308", fontSize: 9, fontFamily: "monospace" }}>
                mirror_node_id: {selectedFeature.mirror_node_id}
              </div>
              <div style={{ color: "#eab308", fontSize: 9, fontFamily: "monospace" }}>
                pricing_key: {selectedFeature.pricing_key}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
