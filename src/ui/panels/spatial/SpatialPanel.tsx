/**
 * Construction OS — Spatial Panel
 *
 * Atlas / plan / zone / location shell.
 * Selected object spatial context. Map/plan adapter seam.
 * Emits: object.selected, zone.selected
 * Subscribes to: truth-echo.propagated, object.selected, zone.selected
 * State owned: viewportState, activeZoneId, selectedSpatialObject, layerVisibility
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { eventBus } from '../../events/EventBus';
import { adapters } from '../../adapters';
import { useActiveObject } from '../../stores/useSyncExternalStore';
import { tokens } from '../../theme/tokens';
import type { SpatialObject, SpatialZone } from '../../contracts/adapters';

export function SpatialPanel() {
  const { activeObject } = useActiveObject();
  const [zones, setZones] = useState<readonly SpatialZone[]>([]);
  const [spatialObjects, setSpatialObjects] = useState<readonly SpatialObject[]>([]);
  const [activeZoneId, setActiveZoneId] = useState<string | null>(null);
  const [layers, setLayers] = useState<Record<string, boolean>>({ structural: true, envelope: true, mep: true });

  // Load zones on mount
  useEffect(() => {
    adapters.spatial.getZones().then((result) => setZones(result.data));
    adapters.spatial.getSpatialObjects().then((result) => setSpatialObjects(result.data));
  }, []);

  // Highlight active object's spatial context
  useEffect(() => {
    if (!activeObject) return;
    adapters.spatial.getObjectSpatialContext(activeObject.id).then((result) => {
      if (result.data?.zone) {
        setActiveZoneId(result.data.zone.id);
      }
    });
  }, [activeObject?.id]);

  const handleSelectSpatialObject = useCallback((obj: SpatialObject) => {
    eventBus.emit('object.selected', {
      object: {
        id: obj.objectId,
        name: obj.label,
        type: 'element',
      },
      source: 'spatial',
      basis: 'mock',
    });
  }, []);

  const handleSelectZone = useCallback((zone: SpatialZone) => {
    setActiveZoneId(zone.id);
    eventBus.emit('zone.selected', {
      zoneId: zone.id,
      zoneName: zone.name,
      source: 'spatial',
      containedObjects: [...zone.objects],
    });
  }, []);

  const toggleLayer = useCallback((layer: string) => {
    setLayers((prev) => ({ ...prev, [layer]: !prev[layer] }));
  }, []);

  // Plan viewport dimensions
  const viewWidth = 720;
  const viewHeight = 520;

  const filteredObjects = spatialObjects.filter((obj) => !obj.layer || layers[obj.layer]);

  return (
    <PanelShell panelId="spatial" title="Spatial" isMock={adapters.spatial.isMock}>
      {/* Layer Controls */}
      <div style={{ display: 'flex', gap: tokens.space.sm, marginBottom: tokens.space.md, flexWrap: 'wrap' }}>
        {Object.entries(layers).map(([layer, visible]) => (
          <button
            key={layer}
            onClick={() => toggleLayer(layer)}
            style={{
              padding: `${tokens.space.sm} ${tokens.space.sm}`,
              background: visible ? tokens.color.bgActive : tokens.color.bgElevated,
              color: visible ? tokens.color.fgPrimary : tokens.color.fgMuted,
              border: `1px solid ${visible ? tokens.color.borderActive : tokens.color.border}`,
              borderRadius: tokens.radius.sm,
              cursor: 'pointer',
              fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.family,
              textTransform: 'capitalize',
              lineHeight: tokens.font.lineTight,
            }}
          >
            {layer}
          </button>
        ))}
      </div>

      {/* Spatial Plan View — SVG-based plan rendering */}
      <div
        style={{
          position: 'relative',
          background: tokens.color.bgDeep,
          borderRadius: tokens.radius.md,
          border: `1px solid ${tokens.color.border}`,
          overflow: 'hidden',
        }}
      >
        <svg
          viewBox={`0 0 ${viewWidth} ${viewHeight}`}
          style={{ width: '100%', height: 'auto', display: 'block' }}
        >
          {/* Grid */}
          <defs>
            <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
              <path d="M 50 0 L 0 0 0 50" fill="none" stroke={tokens.color.borderSubtle} strokeWidth="0.5" />
            </pattern>
          </defs>
          <rect width={viewWidth} height={viewHeight} fill="url(#grid)" />

          {/* Zones */}
          {zones.map((zone) => (
            <g key={zone.id} onClick={() => handleSelectZone(zone)} style={{ cursor: 'pointer' }}>
              <rect
                x={zone.bounds.x}
                y={zone.bounds.y}
                width={zone.bounds.width}
                height={zone.bounds.height}
                fill={activeZoneId === zone.id ? tokens.color.echoTrace : 'rgba(255,255,255,0.02)'}
                stroke={activeZoneId === zone.id ? tokens.color.echoActive : tokens.color.border}
                strokeWidth={activeZoneId === zone.id ? 2 : 1}
                strokeDasharray={activeZoneId === zone.id ? 'none' : '4 2'}
                rx={4}
              />
              <text
                x={zone.bounds.x + 8}
                y={zone.bounds.y + 16}
                fill={tokens.color.fgMuted}
                fontSize="10"
                fontFamily={tokens.font.family}
              >
                {zone.name}
              </text>
            </g>
          ))}

          {/* Spatial Objects */}
          {filteredObjects.map((obj) => {
            const isActive = activeObject?.id === obj.objectId;
            return (
              <g
                key={obj.id}
                onClick={() => handleSelectSpatialObject(obj)}
                style={{ cursor: 'pointer' }}
              >
                <rect
                  x={obj.x}
                  y={obj.y}
                  width={obj.width}
                  height={obj.height}
                  fill={isActive ? tokens.color.echoPulse : 'rgba(59,130,246,0.08)'}
                  stroke={isActive ? tokens.color.echoActive : tokens.color.accentMuted}
                  strokeWidth={isActive ? 2 : 1}
                  rx={3}
                />
                <text
                  x={obj.x + obj.width / 2}
                  y={obj.y + obj.height / 2 + 3}
                  textAnchor="middle"
                  fill={isActive ? tokens.color.fgPrimary : tokens.color.fgSecondary}
                  fontSize="9"
                  fontFamily={tokens.font.familyMono}
                >
                  {obj.label}
                </text>
              </g>
            );
          })}
        </svg>
      </div>

      {/* Zone List */}
      <div style={{ marginTop: tokens.space.md }}>
        <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, marginBottom: tokens.space.sm, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Zones
        </div>
        {zones.map((zone) => (
          <div
            key={zone.id}
            onClick={() => handleSelectZone(zone)}
            style={{
              padding: `${tokens.space.sm} ${tokens.space.sm}`,
              background: activeZoneId === zone.id ? tokens.color.bgActive : 'transparent',
              borderLeft: activeZoneId === zone.id ? `2px solid ${tokens.color.echoActive}` : '2px solid transparent',
              cursor: 'pointer',
              fontSize: tokens.font.sizeSm,
              color: activeZoneId === zone.id ? tokens.color.fgPrimary : tokens.color.fgSecondary,
              lineHeight: tokens.font.lineNormal,
            }}
          >
            {zone.name}
            <span style={{ color: tokens.color.fgMuted, marginLeft: tokens.space.sm, fontSize: tokens.font.sizeXs }}>
              {zone.objects.length} objects
            </span>
          </div>
        ))}
      </div>
    </PanelShell>
  );
}
