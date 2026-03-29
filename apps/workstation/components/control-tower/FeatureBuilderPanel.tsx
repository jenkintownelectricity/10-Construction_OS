import { useSyncExternalStore } from "react";
import { useLens, subscribe, getSnapshot, selectFeature, getFeatureCatalog, getBuildFeedback, MIRROR_STATES, type LensType } from "../../lib/mirror";

const STATE_BADGE_COLORS: Record<string, string> = {
  [MIRROR_STATES.AVAILABLE]: "#334155",
  [MIRROR_STATES.SELECTED]: "#854d0e",
  [MIRROR_STATES.BUILDING]: "#9a3412",
  [MIRROR_STATES.READY]: "#1e40af",
  [MIRROR_STATES.ACTIVE]: "#166534",
};

function getLensLabel(feature: ReturnType<typeof getFeatureCatalog>[number], lens: LensType): string {
  if (lens === "investor") return feature.investor_label;
  if (lens === "engineering") return feature.engineering_label;
  if (lens === "admin") return feature.admin_label ?? feature.buyer_label;
  return feature.buyer_label;
}

export function FeatureBuilderPanel() {
  const { activeLens } = useLens();
  const storeState = useSyncExternalStore(subscribe, getSnapshot);
  const features = getFeatureCatalog();

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        gap: 6,
        padding: 12,
        background: "#0f172a",
        borderRadius: 8,
        border: "1px solid #1e293b",
        minWidth: 220,
      }}
    >
      <div
        style={{
          fontSize: 10,
          fontFamily: "monospace",
          color: "#64748b",
          textTransform: "uppercase",
          letterSpacing: 1,
          marginBottom: 4,
        }}
      >
        Feature Builder
      </div>

      {features
        .sort((a, b) => a.display_order - b.display_order)
        .map((feature) => {
          const featureState = storeState.featureStates[feature.feature_id];
          const mirrorState = featureState?.mirrorState ?? MIRROR_STATES.AVAILABLE;
          const isActive = mirrorState !== MIRROR_STATES.AVAILABLE;
          const feedback = getBuildFeedback(feature.feature_id);
          const label = getLensLabel(feature, activeLens);

          return (
            <div key={feature.feature_id}>
              <button
                onClick={() => selectFeature(feature.feature_id)}
                style={{
                  width: "100%",
                  padding: "6px 10px",
                  fontSize: 11,
                  fontFamily: "monospace",
                  color: isActive ? "#e2e8f0" : "#94a3b8",
                  background: isActive ? "#1e293b" : "transparent",
                  border: `1px solid ${isActive ? "#334155" : "#1e293b"}`,
                  borderRadius: 4,
                  cursor: "pointer",
                  textAlign: "left",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  transition: "all 150ms ease",
                }}
              >
                <span>{isActive ? "−" : "+"} {label}</span>
                <span
                  style={{
                    fontSize: 8,
                    padding: "1px 5px",
                    borderRadius: 3,
                    background: STATE_BADGE_COLORS[mirrorState] ?? "#334155",
                    color: "#e2e8f0",
                  }}
                >
                  {mirrorState}
                </span>
              </button>

              {/* Build feedback */}
              {feedback && (
                <div
                  style={{
                    fontSize: 9,
                    fontFamily: "monospace",
                    color: "#eab308",
                    padding: "2px 10px",
                    animation: "pulse 1s ease-in-out infinite",
                  }}
                >
                  {feedback}
                </div>
              )}
            </div>
          );
        })}
    </div>
  );
}
