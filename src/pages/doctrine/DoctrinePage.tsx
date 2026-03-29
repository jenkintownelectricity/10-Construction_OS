/**
 * Doctrine Page (Doctrine Library) — Construction OS Control Tower
 * Absorbed from VTI control tower Doctrine surface.
 * Displays platform doctrine documents, kernel doctrine, and mirror doctrine.
 */

import { ControlTowerPage, type PageMetric, type AssetItem } from '../../components/control-tower';

const metrics: PageMetric[] = [
  { label: 'Active Docs', value: '12', delta: 'Stable', trend: 'neutral' },
  { label: 'Kernel Doctrine', value: '4', delta: '+1 this pass', trend: 'up' },
  { label: 'Mirror Doctrine', value: '2', delta: 'Stable', trend: 'neutral' },
  { label: 'Platform Doctrine', value: '6', delta: 'Canonical', trend: 'neutral' },
];

const assets: AssetItem[] = [
  { id: 'DC-001', name: 'Birthing Singularity', category: 'governance', status: 'STABLE', detail: 'DomainFoundryOS sole birth authority' },
  { id: 'DC-002', name: 'Fail-Closed Semantics', category: 'governance', status: 'STABLE', detail: 'Ambiguous state rejected, not swallowed' },
  { id: 'DC-003', name: 'Truth Echo Propagation', category: 'core', status: 'STABLE', detail: 'Active object propagation doctrine' },
  { id: 'DC-004', name: 'Adapter Seam Boundary', category: 'core', status: 'STABLE', detail: 'UI never invents truth' },
  { id: 'DC-005', name: 'No Panel-to-Panel Calls', category: 'core', status: 'STABLE', detail: 'All communication via event bus' },
  { id: 'DC-006', name: 'Source Basis Visibility', category: 'governance', status: 'STABLE', detail: 'Data labeled canonical/derived/draft/mock' },
  { id: 'DC-007', name: 'Mirror State Enum', category: 'core', status: 'STABLE', detail: 'AVAILABLE/SELECTED/BUILDING/READY/ACTIVE' },
  { id: 'DC-008', name: 'Lens Presentation Purity', category: 'core', status: 'STABLE', detail: 'Lens switching alters presentation only' },
];

export function DoctrinePage() {
  return (
    <ControlTowerPage
      title="Doctrine Library"
      subtitle="Platform architecture doctrine — canonical rules and design principles"
      statusBadge="STABLE"
      metrics={metrics}
      tableLabel="Doctrine Documents"
      assets={assets}
      chartLabel="Governance Health"
      seedNotice="Doctrine library presents canonical platform rules. These are reference-only — doctrine authority originates from DomainFoundryOS and VTI governance."
    />
  );
}
