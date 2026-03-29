/**
 * Birth Planner Page — Construction OS Control Tower
 * Absorbed from VTI control tower Birth Planner surface.
 *
 * GOVERNANCE NOTE: This is a planning and preview surface ONLY.
 * DomainFoundryOS remains the sole birthing authority.
 * This page does NOT execute births — it presents plans for review.
 */

import { ControlTowerPage, type PageMetric, type AssetItem } from '../../components/control-tower';

const metrics: PageMetric[] = [
  { label: 'Active Plans', value: '2', delta: 'In composition', trend: 'neutral' },
  { label: 'Approved', value: '1', delta: 'Ready for foundry', trend: 'up' },
  { label: 'Executed', value: '3', delta: 'Via DomainFoundryOS', trend: 'up' },
  { label: 'Pending Review', value: '1', delta: 'Awaiting approval', trend: 'neutral' },
];

const assets: AssetItem[] = [
  { id: 'BP-001', name: 'Construction Kernel v2', category: 'core', status: 'COMPLETE', detail: 'Seed-from-template birth' },
  { id: 'BP-002', name: 'Pattern Intelligence Layer', category: 'intelligence', status: 'COMPLETE', detail: 'Mirror growth birth' },
  { id: 'BP-003', name: 'Governance Extension Pack', category: 'governance', status: 'COMPLETE', detail: 'Surface-only birth' },
  { id: 'BP-004', name: 'Material DNA Substrate', category: 'core', status: 'PREVIEW', detail: 'Pending mirror composition' },
  { id: 'BP-005', name: 'Shop Drawing Engine v2', category: 'output', status: 'STAGED', detail: 'Upgrade plan staged' },
];

export function BirthPlannerPage() {
  return (
    <ControlTowerPage
      title="Birth Planner"
      subtitle="Governed composition and plan review — DomainFoundryOS executes all births"
      statusBadge="GOVERNED"
      metrics={metrics}
      tableLabel="Birth Plans"
      assets={assets}
      chartLabel="Birth Activity Timeline"
      seedNotice="Birth Planner provides plan composition and preview only. All birth execution is performed by DomainFoundryOS as the sole birthing authority. Plans shown reflect seed/staged data."
    />
  );
}
