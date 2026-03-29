import { useSyncExternalStore, type CSSProperties } from "react";
import { useLens, subscribe, getSnapshot, getFeatureCatalog, getCapabilityMap, MIRROR_STATES, LENS_TYPES } from "../../lib/mirror";

export function AdminMirror() {
  const { activeLens, session } = useLens();
  const storeState = useSyncExternalStore(subscribe, getSnapshot);
  const features = getFeatureCatalog();
  const capabilities = getCapabilityMap();

  // Role-gated: only render if session role is ADMIN and admin lens is active
  if (session.role !== "ADMIN" || activeLens !== LENS_TYPES.ADMIN) {
    return null;
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 12,
        padding: 16,
        background: "#0f172a",
        borderRadius: 8,
        border: "1px solid #854d0e",
      }}
    >
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <div
          style={{
            fontSize: 11,
            fontFamily: "monospace",
            color: "#eab308",
            textTransform: "uppercase",
            letterSpacing: 1,
            fontWeight: 700,
          }}
        >
          Admin Mirror
        </div>
        <span
          style={{
            fontSize: 8,
            fontFamily: "monospace",
            color: "#854d0e",
            padding: "2px 6px",
            background: "#422006",
            borderRadius: 3,
          }}
        >
          OVERSIGHT ONLY
        </span>
      </div>

      {/* Mirror Node States */}
      <div style={sectionStyle}>
        <div style={sectionHeaderStyle}>Mirror Node States</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          {features.map((f) => {
            const featureState = storeState.featureStates[f.feature_id];
            const mirrorState = featureState?.mirrorState ?? MIRROR_STATES.AVAILABLE;
            return (
              <div
                key={f.feature_id}
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  fontSize: 10,
                  fontFamily: "monospace",
                }}
              >
                <span style={{ color: "#94a3b8" }}>{f.mirror_node_id}</span>
                <span
                  style={{
                    color: mirrorState === MIRROR_STATES.ACTIVE ? "#22c55e" : mirrorState === MIRROR_STATES.AVAILABLE ? "#64748b" : "#eab308",
                    fontWeight: mirrorState === MIRROR_STATES.ACTIVE ? 700 : 400,
                  }}
                >
                  {mirrorState}
                </span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Capability Mapping */}
      <div style={sectionStyle}>
        <div style={sectionHeaderStyle}>Capability Mapping</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          {capabilities.map((cap) => (
            <div key={cap.capability_id} style={{ fontSize: 10, fontFamily: "monospace" }}>
              <div style={{ color: "#a855f7" }}>{cap.capability_id}</div>
              <div style={{ color: "#64748b", paddingLeft: 8 }}>
                module: {cap.module_class} | layer: {cap.layer}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Feature Registry Mapping */}
      <div style={sectionStyle}>
        <div style={sectionHeaderStyle}>Feature Registry Mapping</div>
        <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
          {features.map((f) => (
            <div key={f.feature_id} style={{ fontSize: 9, fontFamily: "monospace" }}>
              <span style={{ color: "#eab308" }}>{f.feature_id}</span>
              <span style={{ color: "#475569" }}> → </span>
              <span style={{ color: "#94a3b8" }}>{f.internal_capability_id}</span>
              <span style={{ color: "#475569" }}> → </span>
              <span style={{ color: "#64748b" }}>{f.mirror_node_id}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Governance notice */}
      <div
        style={{
          fontSize: 8,
          fontFamily: "monospace",
          color: "#854d0e",
          textAlign: "center",
          padding: "8px 0 0",
          borderTop: "1px solid #1e293b",
        }}
      >
        Admin Mirror provides inspection only. No birthing, kernel modification, registry mutation, or runtime mutation permitted.
      </div>
    </div>
  );
}

const sectionStyle: CSSProperties = {
  padding: "8px 10px",
  background: "#1e293b",
  borderRadius: 4,
  display: "flex",
  flexDirection: "column",
  gap: 6,
};

const sectionHeaderStyle: CSSProperties = {
  fontSize: 9,
  fontFamily: "monospace",
  color: "#64748b",
  textTransform: "uppercase",
  letterSpacing: 0.5,
};
