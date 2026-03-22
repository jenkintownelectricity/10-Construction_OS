/**
 * Building Roof Map — Atlas Spatial Surface Level 1
 *
 * First-class Atlas building roof map surface. Renders roof assembly
 * objects from static data as clickable rectangles on an SVG canvas.
 *
 * Click behavior: performs exactly the existing object-selection behavior:
 *   projectToSourceContext(obj)
 *   generationStore.setSourceContext(...)
 *   activeObjectStore.setActiveObject(...)
 *   eventBus.emit('object.selected', ...)
 *   onNavigate('tools')
 *
 * No auto-generation. No drag/drop. No zoom/pan. No GIS. No persistence.
 *
 * Geometry transform: existing assembly coordinates are scaled by a
 * deterministic fixed factor (1.4x) to fill the 600x400 viewBox.
 *
 * Governance: VKGL04R — Ring 3 TOUCH-ALLOWED
 */

import { useState } from 'react';
import {
  ROOF_ASSEMBLY_OBJECTS,
  BUILDINGS,
  LEVELS,
  projectToSourceContext,
  type RoofAssemblyObject,
} from './roofAssemblyObjects';
import { generationStore } from '../stores/generationStore';
import { activeObjectStore } from '../stores/activeObjectStore';
import { eventBus } from '../events/EventBus';
import type { AtlasRoute } from './types';

// ─── Deterministic fixed UI transform ────────────────────────────────

const SCALE = 1.4;
const OFFSET_X = 10;
const OFFSET_Y = 10;

function tx(v: number): number {
  return Math.round(v * SCALE + OFFSET_X);
}
function ty(v: number): number {
  return Math.round(v * SCALE + OFFSET_Y);
}
function ts(v: number): number {
  return Math.round(v * SCALE);
}

// ─── Area colors by manufacturer ─────────────────────────────────────

const AREA_COLORS: Record<string, string> = {
  'Carlisle SynTec': '#3b82f6',
  'GAF': '#22c55e',
  'Johns Manville': '#a855f7',
  'Henry Company': '#f59e0b',
};

// ─── Props ───────────────────────────────────────────────────────────

interface BuildingRoofMapProps {
  onNavigate: (route: AtlasRoute) => void;
}

// ─── Component ───────────────────────────────────────────────────────

export function BuildingRoofMap({ onNavigate }: BuildingRoofMapProps) {
  const [selectedObjectId, setSelectedObjectId] = useState<string | null>(null);
  const [hoveredObjectId, setHoveredObjectId] = useState<string | null>(null);

  const building = BUILDINGS[0];
  const level = LEVELS[0];

  const handleAreaClick = (obj: RoofAssemblyObject) => {
    const sourceContext = projectToSourceContext(obj);
    if (!sourceContext) return;

    setSelectedObjectId(obj.objectId);

    // Exact same behavior as existing mini-map and Shop Drawings selection
    generationStore.setSourceContext(sourceContext);

    activeObjectStore.setActiveObject(
      { id: obj.objectId, type: 'document', name: obj.areaName },
      'explorer',
      'canonical',
    );

    eventBus.emit('object.selected', {
      object: { id: obj.objectId, type: 'document', name: obj.areaName },
      source: 'explorer',
      basis: 'canonical',
    });

    onNavigate('tools');
  };

  return (
    <div data-testid="building-roof-map">
      {/* Map header */}
      <div style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '12px',
      }}>
        <div>
          <div style={{
            fontSize: '16px',
            fontWeight: 700,
            color: '#1a1a2e',
          }}>
            {building.name}
          </div>
          <div style={{
            fontSize: '12px',
            color: '#64748b',
          }}>
            {level.name} — {ROOF_ASSEMBLY_OBJECTS.length} roof assemblies
          </div>
        </div>

        {/* Legend */}
        <div style={{ display: 'flex', gap: '14px' }}>
          {Object.entries(AREA_COLORS).map(([mfr, color]) => (
            <div key={mfr} style={{ display: 'flex', alignItems: 'center', gap: '5px' }}>
              <span style={{
                width: '10px',
                height: '10px',
                borderRadius: '3px',
                background: color,
                display: 'inline-block',
              }} />
              <span style={{ fontSize: '11px', color: '#64748b' }}>{mfr}</span>
            </div>
          ))}
        </div>
      </div>

      {/* SVG Canvas */}
      <svg
        data-testid="building-roof-map-canvas"
        viewBox="0 0 600 400"
        width="100%"
        style={{
          background: '#f8fafc',
          borderRadius: '8px',
          border: '1px solid #e2e8f0',
          display: 'block',
        }}
      >
        {/* Building boundary */}
        <rect
          data-testid="building-boundary"
          x={tx(5)}
          y={ty(15)}
          width={ts(390)}
          height={ts(260)}
          fill="none"
          stroke="#94a3b8"
          strokeWidth="1.5"
          strokeDasharray="6 3"
          rx="4"
        />
        {/* Building label */}
        <text
          x={tx(5) + 8}
          y={ty(15) + 14}
          fill="#94a3b8"
          fontSize="10"
          fontFamily="system-ui, -apple-system, sans-serif"
          fontWeight={600}
        >
          {building.name} — {level.name}
        </text>

        {/* Roof assembly areas */}
        {ROOF_ASSEMBLY_OBJECTS.map((obj) => {
          const color = AREA_COLORS[obj.manufacturer] ?? '#94a3b8';
          const isSelected = obj.objectId === selectedObjectId;
          const isHovered = obj.objectId === hoveredObjectId;
          const highlight = isSelected || isHovered;

          return (
            <g key={obj.objectId}>
              <rect
                data-testid={`atlas-roof-area-${obj.objectId}`}
                x={tx(obj.geometry.x)}
                y={ty(obj.geometry.y)}
                width={ts(obj.geometry.width)}
                height={ts(obj.geometry.height)}
                fill={`${color}${isSelected ? '30' : isHovered ? '20' : '12'}`}
                stroke={highlight ? '#1a1a2e' : color}
                strokeWidth={highlight ? 2 : 1}
                rx="4"
                style={{ cursor: 'pointer', transition: 'fill 0.1s, stroke 0.1s' }}
                onClick={() => handleAreaClick(obj)}
                onMouseEnter={() => setHoveredObjectId(obj.objectId)}
                onMouseLeave={() => setHoveredObjectId(null)}
              />
              {/* Area label */}
              <text
                x={tx(obj.geometry.x) + ts(obj.geometry.width) / 2}
                y={ty(obj.geometry.y) + ts(obj.geometry.height) / 2 - 7}
                textAnchor="middle"
                fill={highlight ? '#1a1a2e' : '#475569'}
                fontSize="12"
                fontWeight={highlight ? 700 : 500}
                fontFamily="system-ui, -apple-system, sans-serif"
                style={{ pointerEvents: 'none' }}
              >
                {obj.label}
              </text>
              {/* Manufacturer sub-label */}
              <text
                x={tx(obj.geometry.x) + ts(obj.geometry.width) / 2}
                y={ty(obj.geometry.y) + ts(obj.geometry.height) / 2 + 9}
                textAnchor="middle"
                fill="#94a3b8"
                fontSize="9"
                fontFamily="system-ui, -apple-system, sans-serif"
                style={{ pointerEvents: 'none' }}
              >
                {obj.manufacturer} | {obj.spec}
              </text>
            </g>
          );
        })}
      </svg>
    </div>
  );
}
