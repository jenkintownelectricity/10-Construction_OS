import type { MirrorEdge as MirrorEdgeType, MirrorNode } from "../../lib/mirror";

interface MirrorEdgeProps {
  edge: MirrorEdgeType;
  nodes: MirrorNode[];
}

export function MirrorEdgeComponent({ edge, nodes }: MirrorEdgeProps) {
  const fromNode = nodes.find((n) => n.id === edge.from);
  const toNode = nodes.find((n) => n.id === edge.to);
  if (!fromNode || !toNode) return null;

  const isDependency = edge.relationship === "dependency";

  return (
    <line
      x1={fromNode.x}
      y1={fromNode.y}
      x2={toNode.x}
      y2={toNode.y}
      stroke={isDependency ? "#334155" : "#1e293b"}
      strokeWidth={isDependency ? 1.5 : 1}
      strokeDasharray={isDependency ? undefined : "4 2"}
      opacity={0.6}
    />
  );
}
