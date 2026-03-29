import { LensProvider, type SessionContext } from "../../lib/mirror";
import { ControlTowerTopBar } from "./ControlTowerTopBar";
import { FeatureBuilderPanel } from "./FeatureBuilderPanel";
import { MirrorGraph } from "../system-map/MirrorGraph";
import { PricingValuePanel } from "./PricingValuePanel";
import { MirrorAssistantPanel } from "./MirrorAssistantPanel";
import { AdminMirror } from "./AdminMirror";

interface MirrorBuilderProps {
  session: SessionContext;
}

/**
 * Multi-Lens Mirror Builder — root layout component.
 *
 * Composes the Control Tower surface:
 * - Top Bar with lens toggle (right-aligned)
 * - Feature Builder panel (left rail)
 * - Mirror Graph viewport (center)
 * - Pricing / Value panel (right rail)
 * - Assistant panel (right rail, below pricing)
 * - Admin Mirror (below graph, role-gated)
 *
 * All lenses derive from one underlying platform configuration model.
 * Lens switching alters presentation only — never mutates features,
 * topology, or platform configuration state.
 */
export function MirrorBuilder({ session }: MirrorBuilderProps) {
  return (
    <LensProvider session={session}>
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          height: "100%",
          background: "#0a0a12",
          color: "#e2e8f0",
          fontFamily: "monospace",
        }}
      >
        {/* Top Bar with Lens Toggle */}
        <ControlTowerTopBar />

        {/* Main content area */}
        <div
          style={{
            display: "flex",
            flex: 1,
            overflow: "hidden",
          }}
        >
          {/* Left rail: Feature Builder */}
          <div
            style={{
              width: 260,
              minWidth: 220,
              overflow: "auto",
              borderRight: "1px solid #1e293b",
              padding: 8,
            }}
          >
            <FeatureBuilderPanel />
          </div>

          {/* Center: Mirror Graph viewport */}
          <div
            style={{
              flex: 1,
              overflow: "auto",
              padding: 12,
              display: "flex",
              flexDirection: "column",
              gap: 12,
            }}
          >
            <MirrorGraph />

            {/* Admin Mirror appears below graph when active */}
            <AdminMirror />
          </div>

          {/* Right rail: Pricing / Value + Assistant */}
          <div
            style={{
              width: 280,
              minWidth: 240,
              overflow: "auto",
              borderLeft: "1px solid #1e293b",
              padding: 8,
              display: "flex",
              flexDirection: "column",
              gap: 8,
            }}
          >
            <PricingValuePanel />
            <MirrorAssistantPanel />
          </div>
        </div>
      </div>
    </LensProvider>
  );
}
