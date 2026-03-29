/**
 * Kernels Page (Kernel Vault) — Construction OS Control Tower
 * Absorbed from VTI control tower Kernel Vault surface.
 * Displays minted kernel assets with class, purity, and governance density.
 */

import { ControlTowerPage, type PageMetric, type AssetItem } from '../../components/control-tower';

const metrics: PageMetric[] = [
  { label: 'Total Kernels', value: '6', delta: '+1 this pass', trend: 'up' },
  { label: 'Minted Assets', value: '5', delta: 'Verified', trend: 'neutral' },
  { label: 'Avg Purity', value: '94%', delta: '+2%', trend: 'up' },
  { label: 'Locked', value: '1', delta: 'Immutable', trend: 'neutral' },
];

const assets: AssetItem[] = [
  { id: 'KRN-001', name: 'Construction Kernel', category: 'core', status: 'ACTIVE', detail: 'v1.0 — Purity: 98% — Density: 4' },
  { id: 'KRN-002', name: 'Assembly Kernel', category: 'core', status: 'ACTIVE', detail: 'v1.0 — Purity: 96% — Density: 3' },
  { id: 'KRN-003', name: 'Governance Kernel', category: 'governance', status: 'STABLE', detail: 'v1.0 — Purity: 99% — Density: 5' },
  { id: 'KRN-004', name: 'Spatial Kernel', category: 'spatial', status: 'ACTIVE', detail: 'v1.0 — Purity: 92% — Density: 3' },
  { id: 'KRN-005', name: 'Intelligence Kernel', category: 'intelligence', status: 'EXPERIMENTAL', detail: 'v0.9 — Purity: 87% — Density: 2' },
  { id: 'KRN-006', name: 'Foundation Kernel', category: 'core', status: 'STABLE', detail: 'v1.0 — Purity: 99% — Locked' },
];

export function KernelsPage() {
  return (
    <ControlTowerPage
      title="Kernel Vault"
      subtitle="Minted kernel assets — class, purity grade, and governance density"
      statusBadge="STABLE"
      metrics={metrics}
      tableLabel="Vault Registry"
      assets={assets}
      chartLabel="Mint History"
      seedNotice="Kernel Vault displays seed data representing the platform's minted kernel assets. Vault entries reflect staged classification."
    />
  );
}
