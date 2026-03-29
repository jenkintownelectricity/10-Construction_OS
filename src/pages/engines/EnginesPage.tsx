/**
 * Engines Page (Engine Registry) — Construction OS Control Tower
 * Absorbed from VTI control tower Engines surface.
 * Displays registered execution engines, load status, and trend data.
 */

import { ControlTowerPage, type PageMetric, type AssetItem } from '../../components/control-tower';

const metrics: PageMetric[] = [
  { label: 'Engines Loaded', value: '5', delta: '+2 since deploy', trend: 'up' },
  { label: 'Executions Today', value: '34', delta: '+12 vs yesterday', trend: 'up' },
  { label: 'Success Rate', value: '97%', delta: '+1%', trend: 'up' },
  { label: 'Queue Depth', value: '0', delta: 'Clear', trend: 'neutral' },
];

const assets: AssetItem[] = [
  { id: 'ENG-001', name: 'Compatibility Engine', category: 'intelligence', status: 'ACTIVE', detail: 'Material constraint resolution' },
  { id: 'ENG-002', name: 'Atlas Engine', category: 'spatial', status: 'ACTIVE', detail: 'Spatial topology reasoning' },
  { id: 'ENG-003', name: 'Detail Generator', category: 'output', status: 'ACTIVE', detail: 'Construction detail production' },
  { id: 'ENG-004', name: 'Shop Drawing Engine', category: 'output', status: 'ACTIVE', detail: 'Fabrication document output' },
  { id: 'ENG-005', name: 'Governance Audit Engine', category: 'governance', status: 'ACTIVE', detail: 'Deterministic audit resolution' },
];

export function EnginesPage() {
  return (
    <ControlTowerPage
      title="Engines"
      subtitle="Execution engine registry — loaded engines, execution metrics, and trends"
      statusBadge="ACTIVE"
      metrics={metrics}
      tableLabel="Engine Registry"
      assets={assets}
      chartLabel="Engine Execution Trend"
      seedNotice="Engine registry displays seed data aligned with the feature catalog. Execution metrics reflect staged demonstration values."
    />
  );
}
