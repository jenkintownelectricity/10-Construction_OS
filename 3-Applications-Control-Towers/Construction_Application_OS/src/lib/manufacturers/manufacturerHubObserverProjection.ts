/**
 * Manufacturer Hub — Observer-Derived Projection
 * Wave 1 UI Surface
 *
 * ============================================================
 * OBSERVER-DERIVED PROJECTION — NON-CANONICAL
 * ============================================================
 *
 * This file contains a LOCAL, OBSERVER-DERIVED projection of
 * manufacturer truth for Construction OS UI consumption ONLY.
 *
 * This data is NOT canonical truth. Canonical truth lives in:
 *   10-building-envelope-manufacturer-os (registry)
 *   00-ValidKernel-Registry (root registry)
 *
 * This projection is derived from currently seeded manufacturer
 * records. It must not invent unsupported manufacturer truth.
 *
 * Barrett: fully seeded — complete projection
 * Siplast: scaffold only — not yet seeded in registry
 *
 * No runtime engine claims. No certification execution.
 * No fabricated event history, timestamps, or prior transitions.
 * ============================================================
 */

import type { ManufacturerHubProjection } from './manufacturerHubTypes';

export const MANUFACTURER_HUB_PROJECTION: ManufacturerHubProjection = {
  manufacturers: [
    {
      id: 'barrett',
      name: 'Barrett Company',
      seedStatus: 'seeded',
      productsCount: 6,
      systemsCount: 2,
      certificationsCount: 2,
      description: 'Roofing and waterproofing manufacturer — fully seeded in registry',
    },
    {
      id: 'siplast',
      name: 'Siplast',
      seedStatus: 'scaffold',
      productsCount: 0,
      systemsCount: 0,
      certificationsCount: 0,
      description: 'Scaffold entry only — not yet seeded in manufacturer registry',
    },
  ],

  products: [
    {
      id: 'barrett-hyppocoat-100',
      manufacturerId: 'barrett',
      name: 'HyppoCoat 100',
      type: 'coating',
      role: 'base-membrane',
      description: 'Primary fluid-applied waterproofing membrane',
    },
    {
      id: 'barrett-hyppocoat-pc',
      manufacturerId: 'barrett',
      name: 'HyppoCoat PC',
      type: 'primer',
      role: 'primer-coat',
      description: 'Primer coat for substrate preparation',
    },
    {
      id: 'barrett-hyppocoat-bc',
      manufacturerId: 'barrett',
      name: 'HyppoCoat BC',
      type: 'coating',
      role: 'base-coat',
      description: 'Base coat application layer',
    },
    {
      id: 'barrett-hyppocoat-tc',
      manufacturerId: 'barrett',
      name: 'HyppoCoat TC',
      type: 'coating',
      role: 'top-coat',
      description: 'Top coat / wear surface layer',
    },
    {
      id: 'barrett-hyppocoat-gc',
      manufacturerId: 'barrett',
      name: 'HyppoCoat GC',
      type: 'coating',
      role: 'grout-coat',
      description: 'Grout coat for tile / paver integration',
    },
    {
      id: 'barrett-ram-quick-flash',
      manufacturerId: 'barrett',
      name: 'Ram Quick Flash PMMA Membrane',
      type: 'membrane',
      role: 'flashing-membrane',
      description: 'PMMA-based rapid-cure flashing membrane',
    },
  ],

  systems: [
    {
      id: 'barrett-hyppocoat-trafficable',
      manufacturerId: 'barrett',
      name: 'Barrett HyppoCoat Trafficable System',
      systemType: 'trafficable-waterproofing',
      description: 'Complete trafficable waterproofing system for plaza decks, balconies, and parking structures',
      productIds: [
        'barrett-hyppocoat-pc',
        'barrett-hyppocoat-bc',
        'barrett-hyppocoat-100',
        'barrett-hyppocoat-tc',
      ],
      certificationIds: ['barrett-trafficable-cert'],
      conditionIds: ['cond-plaza-deck', 'cond-balcony', 'cond-parking-deck'],
    },
    {
      id: 'barrett-pmma-flashing',
      manufacturerId: 'barrett',
      name: 'Barrett Ram Quick Flash PMMA Flashing System',
      systemType: 'pmma-flashing',
      description: 'PMMA-based rapid-cure flashing system for detail work at parapets, penetrations, and roof edges',
      productIds: ['barrett-ram-quick-flash'],
      certificationIds: ['barrett-pmma-flashing-cert'],
      conditionIds: ['cond-parapet', 'cond-penetration', 'cond-roof-edge'],
    },
  ],

  certifications: [
    {
      id: 'barrett-trafficable-cert',
      manufacturerId: 'barrett',
      systemId: 'barrett-hyppocoat-trafficable',
      name: 'Barrett Trafficable Certification',
      status: 'unverified',
      requirementSummary: 'System-level certification for trafficable waterproofing applications — observer-derived status, not engine-executed',
    },
    {
      id: 'barrett-pmma-flashing-cert',
      manufacturerId: 'barrett',
      systemId: 'barrett-pmma-flashing',
      name: 'Barrett PMMA Flashing Certification',
      status: 'unverified',
      requirementSummary: 'System-level certification for PMMA flashing applications — observer-derived status, not engine-executed',
    },
  ],

  rulesSummary: [
    {
      id: 'rule-primer-required',
      systemId: 'barrett-hyppocoat-trafficable',
      name: 'Primer Required',
      description: 'HyppoCoat PC primer coat must be applied before base coat',
      materialized: false,
    },
    {
      id: 'rule-topcoat-required',
      systemId: 'barrett-hyppocoat-trafficable',
      name: 'Topcoat Required',
      description: 'HyppoCoat TC top coat must be applied as final wear surface',
      materialized: false,
    },
    {
      id: 'rule-fleece-required',
      systemId: 'barrett-hyppocoat-trafficable',
      name: 'Fleece Required',
      description: 'Reinforcing fleece may be required depending on condition — rule file not yet materialized',
      materialized: false,
    },
    {
      id: 'rule-cure-before-overlay',
      systemId: 'barrett-hyppocoat-trafficable',
      name: 'Cure Before Overlay',
      description: 'Each coat must cure before the next layer is applied',
      materialized: false,
    },
  ],

  conditionsSummary: [
    { id: 'cond-plaza-deck', systemId: 'barrett-hyppocoat-trafficable', name: 'Plaza Deck', conditionType: 'application-condition' },
    { id: 'cond-balcony', systemId: 'barrett-hyppocoat-trafficable', name: 'Balcony', conditionType: 'application-condition' },
    { id: 'cond-parking-deck', systemId: 'barrett-hyppocoat-trafficable', name: 'Parking Deck', conditionType: 'application-condition' },
    { id: 'cond-parapet', systemId: 'barrett-pmma-flashing', name: 'Parapet', conditionType: 'detail-condition' },
    { id: 'cond-penetration', systemId: 'barrett-pmma-flashing', name: 'Penetration', conditionType: 'detail-condition' },
    { id: 'cond-roof-edge', systemId: 'barrett-pmma-flashing', name: 'Roof Edge', conditionType: 'detail-condition' },
  ],

  governanceStatus: {
    barrett: {
      certificationState: 'unverified',
      projectionState: 'active',
      truthDebt: [
        'Structured rule files not yet materialized',
        'Certification engine not yet connected',
        'Condition compatibility matrix not yet formalized',
      ],
      seedStatus: 'seeded',
    },
    siplast: {
      certificationState: 'unverified',
      projectionState: 'scaffold',
      truthDebt: [
        'Manufacturer not yet seeded in registry',
        'No products, systems, or certifications available',
      ],
      seedStatus: 'scaffold',
    },
  },

  actions: [
    { id: 'action-inspect-system', label: 'Inspect System', actionType: 'inspect', enabled: true },
    { id: 'action-view-products', label: 'View Products', actionType: 'navigate', enabled: true },
    { id: 'action-switch-system', label: 'Switch to System Mode', actionType: 'mode-switch', targetMode: 'system', enabled: true },
    { id: 'action-switch-work', label: 'Switch to Work Mode', actionType: 'mode-switch', targetMode: 'work', enabled: true },
    { id: 'action-prepare-conditions', label: 'Prepare Condition Mapping', actionType: 'future', enabled: false },
    { id: 'action-connect-cert-engine', label: 'Connect to Certification Engine', actionType: 'future', enabled: false },
  ],
};
