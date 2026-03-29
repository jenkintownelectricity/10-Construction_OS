import { useSyncExternalStore } from "react";
import { useLens, subscribe, getSnapshot, selectNode, computeMirrorNodes, computeMirrorEdges } from "../../lib/mirror";
import { MirrorNodeComponent } from "./MirrorNode";
import { MirrorEdgeComponent } from "./MirrorEdge";

const LAYER_LABELS: Record<string, { label: string; y: number }> = {
  "Application Layer": { label: "Application Layer", y: 45 },
  "Intelligence Layer": { label: "Intelligence Layer", y: 165 },
  "Infrastructure Layer": { label: "Infrastructure Layer", y: 285 },
};

export function MirrorGraph() {
  const { activeLens } = useLens();
  const storeState = useSyncExternalStore(subscribe, getSnapshot);

  const nodes = computeMirrorNodes(activeLens);
  const edges = computeMirrorEdges();

  const handleSelectNode = (nodeId: string) => {
    selectNode(storeState.selectedNodeId === nodeId ? null : nodeId);
  };

  return (
    <div
      style={{
        background: "#0c0c14",
        borderRadius: 8,
        border: "1px solid #1e293b",
        padding: 8,
        minHeight: 380,
        position: "relative",
      }}
    >
      {/* Lens indicator */}
      <div
        style={{
          position: "absolute",
          top: 8,
          left: 12,
          fontSize: 10,
          color: "#64748b",
          fontFamily: "monospace",
          textTransform: "uppercase",
          letterSpacing: 1,
        }}
      >
        {activeLens} lens
      </div>

      <svg viewBox="0 0 520 380" style={{ width: "100%", minHeight: 360 }}>
        {/* Grid lines */}
        {[80, 160, 240, 320].map((y) => (
          <line key={y} x1={0} y1={y} x2={520} y2={y} stroke="#1a1a2e" strokeWidth={0.5} />
        ))}

        {/* Layer labels (investor lens reorganizes visually) */}
        {activeLens === "investor" &&
          Object.values(LAYER_LABELS).map((layer) => (
            <text
              key={layer.label}
              x={10}
              y={layer.y}
              fill="#475569"
              fontSize={8}
              fontFamily="monospace"
              fontWeight="bold"
            >
              {layer.label}
            </text>
          ))}

        {/* Edges */}
        {edges.map((edge, i) => (
          <MirrorEdgeComponent key={i} edge={edge} nodes={nodes} />
        ))}

        {/* Nodes */}
        {nodes.map((node) => (
          <MirrorNodeComponent
            key={node.id}
            node={node}
            isSelected={storeState.selectedNodeId === node.id}
            onSelect={handleSelectNode}
          />
        ))}
      </svg>
    </div>
  );
}
