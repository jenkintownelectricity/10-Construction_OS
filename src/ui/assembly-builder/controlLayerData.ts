/**
 * Read-only hydration of Control Layers from CRI shared artifacts.
 * Source: Construction_Reference_Intelligence/shared/control_layers.json
 *
 * This data is consumed read-only. No CRI files are modified.
 * Governance: VKGL04R — Ring 3 NO-TOUCH on CRI.
 */

import type { ControlLayerDef, ControlLayerId } from './types';

/**
 * Canonical control layer definitions from CRI shared/control_layers.json.
 * Frozen snapshot — matches schema_version v1.
 */
export const CONTROL_LAYERS: readonly ControlLayerDef[] = [
  {
    id: 'bulk_water_control',
    name: 'Bulk Water Control',
    description: 'Primary barrier against liquid water ingress from rain, snowmelt, and standing water.',
  },
  {
    id: 'capillary_control',
    name: 'Capillary Control',
    description: 'Resistance to moisture migration through porous materials via capillary action.',
  },
  {
    id: 'air_control',
    name: 'Air Control',
    description: 'Continuous barrier limiting uncontrolled air movement through the building enclosure.',
  },
  {
    id: 'vapor_control',
    name: 'Vapor Control',
    description: 'Layer managing vapor diffusion to prevent interstitial condensation.',
  },
  {
    id: 'thermal_control',
    name: 'Thermal Control',
    description: 'Insulation layer managing heat flow through the building enclosure.',
  },
  {
    id: 'fire_smoke_control',
    name: 'Fire and Smoke Control',
    description: 'Barriers and rated assemblies limiting fire spread and smoke migration.',
  },
  {
    id: 'movement_control',
    name: 'Movement Control',
    description: 'Joints, fastening patterns, and details accommodating thermal, structural, and seismic movement.',
  },
  {
    id: 'weathering_surface',
    name: 'Weathering Surface',
    description: 'Outermost exposed layer that resists UV, wind, precipitation, and environmental degradation.',
  },
  {
    id: 'drainage_plane',
    name: 'Drainage Plane',
    description: 'Dedicated layer or surface directing incidental moisture downward and outward.',
  },
  {
    id: 'protection_layer',
    name: 'Protection Layer',
    description: 'Layer shielding underlying control layers from mechanical damage, backfill pressure, or traffic.',
  },
  {
    id: 'vegetation_support_layer',
    name: 'Vegetation Support Layer',
    description: 'Substrate and root-barrier system supporting vegetated roof or wall assemblies.',
  },
] as const;

/** Lookup by ID */
export function getControlLayer(id: ControlLayerId): ControlLayerDef | undefined {
  return CONTROL_LAYERS.find((cl) => cl.id === id);
}

/** All valid control layer IDs */
export const CONTROL_LAYER_IDS: readonly ControlLayerId[] = CONTROL_LAYERS.map((cl) => cl.id);
