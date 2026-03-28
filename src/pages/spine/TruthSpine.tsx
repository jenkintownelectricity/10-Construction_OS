/**
 * Construction OS — Truth Spine Page
 * Wave C1 — Static architecture graph with deterministic positions.
 * No force-directed layout. No dynamic mutation.
 */

import { useState } from 'react';
import { tokens } from '../../ui/theme/tokens';
import { TRUTH_SPINE_NODES, TRUTH_SPINE_EDGES, type TruthSpineNode } from '../../mock/primitives/mockTruthSpine';

const t = tokens;

const nodeTypeColors: Record<string, string> = {
  KERNEL: t.color.accentPrimary,
  RUNTIME: t.color.success,
  REGISTRY: t.color.warning,
  ENGINE: t.color.compare,
  ATLAS: '#06b6d4',
};

const statusIndicator: Record<string, string> = {
  ACTIVE: t.color.success,
  IDLE: t.color.warning,
  OFFLINE: t.color.fgMuted,
};

export function TruthSpine() {
  const [selectedNode, setSelectedNode] = useState<TruthSpineNode | null>(null);

  const svgWidth = 800;
  const svgHeight = 560;

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Truth Spine</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Construction OS architecture graph — static topology, deterministic layout
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 320px', gap: '16px' }}>
        {/* Graph */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '16px',
            overflow: 'auto',
          }}
        >
          <svg
            width={svgWidth}
            height={svgHeight}
            viewBox={`0 0 ${svgWidth} ${svgHeight}`}
            style={{ display: 'block', margin: '0 auto' }}
          >
            {/* Edges */}
            {TRUTH_SPINE_EDGES.map((edge) => {
              const src = TRUTH_SPINE_NODES.find((n) => n.id === edge.source);
              const tgt = TRUTH_SPINE_NODES.find((n) => n.id === edge.target);
              if (!src || !tgt) return null;
              return (
                <line
                  key={edge.id}
                  x1={src.x}
                  y1={src.y}
                  x2={tgt.x}
                  y2={tgt.y}
                  stroke={t.color.border}
                  strokeWidth={1.5}
                  strokeOpacity={0.6}
                />
              );
            })}
            {/* Nodes */}
            {TRUTH_SPINE_NODES.map((node) => {
              const isSelected = selectedNode?.id === node.id;
              const color = nodeTypeColors[node.type] || t.color.fgMuted;
              return (
                <g
                  key={node.id}
                  onClick={() => setSelectedNode(node)}
                  style={{ cursor: 'pointer' }}
                >
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={isSelected ? 26 : 22}
                    fill={t.color.bgElevated}
                    stroke={isSelected ? color : t.color.border}
                    strokeWidth={isSelected ? 2.5 : 1.5}
                  />
                  <circle
                    cx={node.x}
                    cy={node.y}
                    r={6}
                    fill={color}
                  />
                  <text
                    x={node.x}
                    y={node.y + 36}
                    textAnchor="middle"
                    fill={t.color.fgSecondary}
                    fontSize="11"
                    fontFamily={t.font.family}
                  >
                    {node.name}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Side panel */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Legend */}
          <div
            style={{
              background: t.color.bgSurface,
              border: `1px solid ${t.color.border}`,
              borderRadius: t.radius.md,
              padding: '16px',
            }}
          >
            <h3 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: '0 0 12px 0' }}>Legend</h3>
            {Object.entries(nodeTypeColors).map(([type, color]) => (
              <div key={type} style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '6px' }}>
                <span style={{ width: 10, height: 10, borderRadius: '50%', background: color, display: 'inline-block' }} />
                <span style={{ fontSize: t.font.sizeXs, color: t.color.fgSecondary }}>{type}</span>
              </div>
            ))}
          </div>

          {/* Selected node details */}
          <div
            style={{
              background: t.color.bgSurface,
              border: `1px solid ${t.color.border}`,
              borderRadius: t.radius.md,
              padding: '16px',
              flex: 1,
            }}
          >
            <h3 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: '0 0 12px 0' }}>Node Details</h3>
            {selectedNode ? (
              <div style={{ fontSize: t.font.sizeXs }}>
                <div style={{ marginBottom: '8px' }}>
                  <span style={{ color: t.color.fgMuted }}>Name: </span>
                  <span style={{ color: t.color.fgPrimary, fontWeight: Number(t.font.weightMedium) }}>{selectedNode.name}</span>
                </div>
                <div style={{ marginBottom: '8px' }}>
                  <span style={{ color: t.color.fgMuted }}>Type: </span>
                  <span style={{ color: nodeTypeColors[selectedNode.type] }}>{selectedNode.type}</span>
                </div>
                <div style={{ marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ color: t.color.fgMuted }}>Status: </span>
                  <span style={{ width: 6, height: 6, borderRadius: '50%', background: statusIndicator[selectedNode.status], display: 'inline-block' }} />
                  <span style={{ color: statusIndicator[selectedNode.status] }}>{selectedNode.status}</span>
                </div>
                <div style={{ marginTop: '12px', color: t.color.fgSecondary, lineHeight: t.font.lineNormal }}>
                  {selectedNode.description}
                </div>
                {/* Relationships */}
                <div style={{ marginTop: '16px' }}>
                  <div style={{ color: t.color.fgMuted, marginBottom: '6px', fontWeight: Number(t.font.weightMedium) }}>Relationships</div>
                  {TRUTH_SPINE_EDGES.filter((e) => e.source === selectedNode.id || e.target === selectedNode.id).map((edge) => {
                    const other = edge.source === selectedNode.id
                      ? TRUTH_SPINE_NODES.find((n) => n.id === edge.target)?.name
                      : TRUTH_SPINE_NODES.find((n) => n.id === edge.source)?.name;
                    const direction = edge.source === selectedNode.id ? '\u2192' : '\u2190';
                    return (
                      <div key={edge.id} style={{ padding: '3px 0', color: t.color.fgSecondary }}>
                        {direction} {edge.relationship} {other}
                      </div>
                    );
                  })}
                </div>
              </div>
            ) : (
              <p style={{ color: t.color.fgMuted, fontSize: t.font.sizeXs }}>Select a node to view details</p>
            )}
          </div>
        </div>
      </div>

      {/* Relationship Summary */}
      <div
        style={{
          marginTop: '16px',
          background: t.color.bgSurface,
          border: `1px solid ${t.color.border}`,
          borderRadius: t.radius.md,
          padding: '16px',
        }}
      >
        <h3 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: '0 0 12px 0' }}>Relationship Summary</h3>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '8px', fontSize: t.font.sizeXs }}>
          {TRUTH_SPINE_EDGES.map((edge) => {
            const src = TRUTH_SPINE_NODES.find((n) => n.id === edge.source)?.name;
            const tgt = TRUTH_SPINE_NODES.find((n) => n.id === edge.target)?.name;
            return (
              <div
                key={edge.id}
                style={{
                  padding: '6px 10px',
                  background: t.color.bgElevated,
                  borderRadius: t.radius.sm,
                  color: t.color.fgSecondary,
                }}
              >
                <span style={{ color: t.color.fgPrimary }}>{src}</span>
                {' '}\u2192 <span style={{ color: t.color.accentPrimary }}>{edge.relationship}</span>{' '}
                \u2192 <span style={{ color: t.color.fgPrimary }}>{tgt}</span>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
