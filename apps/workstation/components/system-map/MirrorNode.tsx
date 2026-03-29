import { MIRROR_STATES, type MirrorNode as MirrorNodeType } from "../../lib/mirror";

const STATE_COLORS: Record<string, string> = {
  [MIRROR_STATES.AVAILABLE]: "#64748b",
  [MIRROR_STATES.SELECTED]: "#eab308",
  [MIRROR_STATES.BUILDING]: "#f97316",
  [MIRROR_STATES.READY]: "#3b82f6",
  [MIRROR_STATES.ACTIVE]: "#22c55e",
};

const STATE_OPACITY: Record<string, number> = {
  [MIRROR_STATES.AVAILABLE]: 0.5,
  [MIRROR_STATES.SELECTED]: 0.75,
  [MIRROR_STATES.BUILDING]: 0.85,
  [MIRROR_STATES.READY]: 0.9,
  [MIRROR_STATES.ACTIVE]: 1.0,
};

interface MirrorNodeProps {
  node: MirrorNodeType;
  isSelected: boolean;
  onSelect: (nodeId: string) => void;
}

export function MirrorNodeComponent({ node, isSelected, onSelect }: MirrorNodeProps) {
  const color = STATE_COLORS[node.state] ?? "#64748b";
  const opacity = STATE_OPACITY[node.state] ?? 0.5;
  const radius = node.state === MIRROR_STATES.ACTIVE ? 24 : 20;

  return (
    <g
      onClick={() => onSelect(node.id)}
      style={{ cursor: "pointer" }}
      role="button"
      aria-label={`Mirror node: ${node.label}`}
    >
      {/* Selection ring */}
      {isSelected && (
        <circle cx={node.x} cy={node.y} r={radius + 6} fill="none" stroke="#ffffff" strokeWidth={2} opacity={0.6} />
      )}

      {/* Build pulse animation */}
      {(node.state === MIRROR_STATES.BUILDING || node.state === MIRROR_STATES.SELECTED) && (
        <circle cx={node.x} cy={node.y} r={radius + 10} fill="none" stroke={color} strokeWidth={1} opacity={0.3}>
          <animate attributeName="r" from={String(radius + 4)} to={String(radius + 16)} dur="1.2s" repeatCount="indefinite" />
          <animate attributeName="opacity" from="0.4" to="0" dur="1.2s" repeatCount="indefinite" />
        </circle>
      )}

      {/* Node circle */}
      <circle cx={node.x} cy={node.y} r={radius} fill={color} opacity={opacity} stroke={isSelected ? "#ffffff" : "none"} strokeWidth={isSelected ? 2 : 0} />

      {/* Node label */}
      <text
        x={node.x}
        y={node.y + radius + 14}
        textAnchor="middle"
        fill="#e2e8f0"
        fontSize={9}
        fontFamily="monospace"
      >
        {node.label.length > 28 ? node.label.slice(0, 26) + "…" : node.label}
      </text>

      {/* State indicator */}
      <text
        x={node.x}
        y={node.y + 3}
        textAnchor="middle"
        fill="#0f172a"
        fontSize={7}
        fontWeight="bold"
        fontFamily="monospace"
      >
        {node.state === MIRROR_STATES.ACTIVE ? "✓" : node.state === MIRROR_STATES.BUILDING ? "…" : ""}
      </text>
    </g>
  );
}
