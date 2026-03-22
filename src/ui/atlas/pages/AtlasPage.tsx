/**
 * Construction Atlas — Atlas Page
 *
 * Building roof map surface + interactive reference graph.
 * Atlas spatial surface Level 1: clickable roof assembly map
 * that launches the governed roofing generation loop.
 *
 * Governance: VKGL04R — Ring 3 TOUCH-ALLOWED
 */

import { useState } from 'react';
import { DEFAULT_BRANDING } from '../../../lib/branding/branding-types';
import { BuildingRoofMap } from '../BuildingRoofMap';
import type { AtlasRoute } from '../types';

const c = DEFAULT_BRANDING.colors;

const cardStyle: React.CSSProperties = {
  background: '#ffffff',
  border: `1px solid ${c.border}`,
  borderRadius: '8px',
  padding: '20px',
};

const NODE_COLORS = { ready: '#16a34a', inProgress: '#f59e0b', review: '#6366f1' };

interface GraphNode {
  id: string;
  label: string;
  status: 'ready' | 'inProgress' | 'review';
  x: number;
  y: number;
}

const NODES: GraphNode[] = [
  { id: 'DF-001', label: 'Parapet Wall Assembly', status: 'ready', x: 350, y: 40 },
  { id: 'DF-005', label: 'Roof Membrane Termination', status: 'review', x: 550, y: 120 },
  { id: 'DF-002', label: 'Window Head Flashing', status: 'ready', x: 220, y: 160 },
  { id: 'DF-004', label: 'Curtain Wall Sill', status: 'ready', x: 370, y: 200 },
  { id: 'DF-003', label: 'Foundation Waterproofing', status: 'inProgress', x: 180, y: 300 },
  { id: 'DF-006', label: 'Expansion Joint Cover', status: 'ready', x: 500, y: 280 },
  { id: 'DF-007', label: 'Masonry Through-Wall', status: 'ready', x: 300, y: 350 },
  { id: 'DF-008', label: 'Metal Panel Clip', status: 'inProgress', x: 550, y: 350 },
];

const INSTALL_SEQUENCE = [
  { num: 1, label: 'Foundation Waterproofing', desc: 'Apply membrane below grade' },
  { num: 2, label: 'Masonry Through-Wall', desc: 'Install through-wall flashing' },
  { num: 3, label: 'Expansion Joint Cover', desc: 'Install joint sealant and cover' },
  { num: 4, label: 'Curtain Wall Sill', desc: 'Set sill flashing with weeps' },
  { num: 5, label: 'Window Head Flashing', desc: 'Install head flashing over frame' },
  { num: 6, label: 'Metal Panel Clip', desc: 'Mount panel clips to structure' },
  { num: 7, label: 'Roof Membrane Termination', desc: 'Terminate membrane at edge' },
  { num: 8, label: 'Parapet Wall Assembly', desc: 'Complete cap flashing and coping' },
];

interface AtlasPageProps {
  onNavigate?: (route: AtlasRoute) => void;
}

export function AtlasPage({ onNavigate }: AtlasPageProps = {}) {
  const [selectedNode, setSelectedNode] = useState<string | null>(null);

  const handleNavigate = onNavigate ?? (() => {});

  return (
    <div>
      <h1 style={{ fontSize: '24px', fontWeight: 700, color: c.text, margin: 0 }}>Atlas</h1>
      <p style={{ color: c.textMuted, margin: '4px 0 24px', fontSize: '14px' }}>Building roof map, detail graph, and installation sequences</p>

      {/* Building Roof Map Surface */}
      <div style={{ ...cardStyle, marginBottom: '24px' }}>
        <BuildingRoofMap onNavigate={handleNavigate} />
      </div>

      <div style={{ display: 'flex', gap: '24px' }}>
        {/* Graph */}
        <div style={{ ...cardStyle, flex: 2 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
            <h2 style={{ fontSize: '16px', fontWeight: 600, color: c.text, margin: 0 }}>Reference Graph</h2>
            <div style={{ display: 'flex', gap: '16px', fontSize: '12px' }}>
              {[
                { color: NODE_COLORS.ready, label: 'Ready' },
                { color: NODE_COLORS.inProgress, label: 'In Progress' },
                { color: NODE_COLORS.review, label: 'Review' },
              ].map((legend) => (
                <div key={legend.label} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: legend.color, display: 'inline-block' }} />
                  <span style={{ color: c.textMuted }}>{legend.label}</span>
                </div>
              ))}
            </div>
          </div>

          <div style={{ position: 'relative', height: '420px', background: c.surface, borderRadius: '6px', overflow: 'hidden' }}>
            {/* SVG edges */}
            <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
              <line x1="380" y1="70" x2="580" y2="140" stroke={c.border} strokeWidth="1.5" strokeDasharray="4" />
              <line x1="250" y1="180" x2="370" y2="220" stroke={c.border} strokeWidth="1.5" strokeDasharray="4" />
              <line x1="400" y1="220" x2="520" y2="300" stroke={c.border} strokeWidth="1.5" strokeDasharray="4" />
              <line x1="210" y1="320" x2="300" y2="370" stroke={c.border} strokeWidth="1.5" strokeDasharray="4" />
              <line x1="530" y1="300" x2="580" y2="370" stroke={c.border} strokeWidth="1.5" strokeDasharray="4" />
              <line x1="250" y1="180" x2="370" y2="70" stroke={c.border} strokeWidth="1.5" strokeDasharray="4" />
            </svg>

            {/* Nodes */}
            {NODES.map((node) => {
              const isSelected = selectedNode === node.id;
              return (
                <button
                  key={node.id}
                  onClick={() => setSelectedNode(node.id)}
                  style={{
                    position: 'absolute',
                    left: `${node.x}px`,
                    top: `${node.y}px`,
                    transform: 'translate(-50%, -50%)',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    gap: '4px',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                  }}
                >
                  <div style={{
                    width: isSelected ? '36px' : '30px',
                    height: isSelected ? '36px' : '30px',
                    borderRadius: '50%',
                    background: NODE_COLORS[node.status],
                    boxShadow: isSelected ? `0 0 0 3px ${NODE_COLORS[node.status]}40` : 'none',
                    transition: 'all 0.15s',
                  }} />
                  <span style={{ fontSize: '11px', fontWeight: 500, color: c.text, whiteSpace: 'nowrap' }}>{node.label}</span>
                  <span style={{ fontSize: '9px', color: c.textMuted }}>{node.id}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right sidebar */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {/* Selected node info */}
          <div style={cardStyle}>
            {selectedNode ? (
              <div>
                <div style={{ fontWeight: 600, color: c.text, marginBottom: '8px' }}>
                  {NODES.find((n) => n.id === selectedNode)?.label}
                </div>
                <div style={{ fontSize: '12px', color: c.textMuted }}>
                  {selectedNode}
                </div>
              </div>
            ) : (
              <div style={{ color: c.textMuted, textAlign: 'center', fontSize: '13px' }}>
                Click a node in the graph to see details
              </div>
            )}
          </div>

          {/* Install Sequence */}
          <div style={cardStyle}>
            <h3 style={{ fontSize: '16px', fontWeight: 600, color: c.text, margin: '0 0 16px' }}>Install Sequence</h3>
            {INSTALL_SEQUENCE.map((step) => (
              <div key={step.num} style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
                <div style={{
                  width: '24px', height: '24px', borderRadius: '50%', background: c.secondary,
                  color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: '11px', fontWeight: 700, flexShrink: 0,
                }}>
                  {step.num}
                </div>
                <div>
                  <div style={{ fontWeight: 600, fontSize: '13px', color: c.text }}>{step.label}</div>
                  <div style={{ fontSize: '12px', color: c.textMuted }}>{step.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
