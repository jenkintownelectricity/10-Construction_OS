/**
 * Read-only hydration of Interface Zones from CRI shared artifacts.
 * Source: Construction_Reference_Intelligence/shared/interface_zones.json
 *
 * This data is consumed read-only. No CRI files are modified.
 * Governance: VKGL04R — Ring 3 NO-TOUCH on CRI.
 */

import type { InterfaceZoneDef, InterfaceZoneId } from './types';

/**
 * Canonical interface zone definitions from CRI shared/interface_zones.json.
 * Frozen snapshot — matches schema_version v1.
 */
export const INTERFACE_ZONES: readonly InterfaceZoneDef[] = [
  {
    id: 'roof_to_wall',
    name: 'Roof-to-Wall Transition',
    description: 'Interface where roofing system meets vertical wall assembly. Critical for water, air, and thermal continuity.',
  },
  {
    id: 'parapet_transition',
    name: 'Parapet Transition',
    description: 'Interface at parapet walls where roof membrane terminates and wall cladding begins.',
  },
  {
    id: 'penetration',
    name: 'Penetration',
    description: 'Any point where pipes, conduits, structural members, or equipment pass through the building enclosure.',
  },
  {
    id: 'fenestration_edge',
    name: 'Fenestration Edge',
    description: 'Perimeter interface around windows, doors, curtain wall frames, and glazing systems.',
  },
  {
    id: 'below_grade_transition',
    name: 'Below-Grade Transition',
    description: 'Interface where above-grade wall assembly transitions to below-grade waterproofing.',
  },
  {
    id: 'expansion_joint',
    name: 'Expansion Joint',
    description: 'Designed movement joint accommodating differential structural movement between building sections.',
  },
  {
    id: 'deck_to_wall',
    name: 'Deck-to-Wall Transition',
    description: 'Interface where horizontal deck or plaza assembly meets vertical wall.',
  },
  {
    id: 'roof_edge',
    name: 'Roof Edge',
    description: 'Perimeter edge condition including fascia, drip edge, gravel stop, or coping.',
  },
  {
    id: 'curb_transition',
    name: 'Curb Transition',
    description: 'Interface where roof membrane transitions up and over equipment curbs, skylights, or hatches.',
  },
  {
    id: 'drain_transition',
    name: 'Drain Transition',
    description: 'Interface at roof drains, scuppers, and overflow points where membrane connects to drainage hardware.',
  },
] as const;

/** Lookup by ID */
export function getInterfaceZone(id: InterfaceZoneId): InterfaceZoneDef | undefined {
  return INTERFACE_ZONES.find((iz) => iz.id === id);
}

/** All valid interface zone IDs */
export const INTERFACE_ZONE_IDS: readonly InterfaceZoneId[] = INTERFACE_ZONES.map((iz) => iz.id);
