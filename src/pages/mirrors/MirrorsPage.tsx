/**
 * Mirrors Page (Mirror Registry) — Construction OS Control Tower
 * Absorbed from VTI control tower Mirrors surface.
 * Displays mirror registry, activity, and classification state.
 * Complements the Multi-Lens Mirror Builder which handles configuration.
 */

import { ControlTowerPage, type PageMetric, type AssetItem } from '../../components/control-tower';

const metrics: PageMetric[] = [
  { label: 'Active Mirrors', value: '3', delta: '+1 this week', trend: 'up' },
  { label: 'Pending Review', value: '2', delta: 'Awaiting classification', trend: 'neutral' },
  { label: 'Configured', value: '8', delta: 'Via Mirror Builder', trend: 'up' },
  { label: 'Blocked', value: '0', delta: 'Clear', trend: 'neutral' },
];

const assets: AssetItem[] = [
  { id: 'MR-001', name: 'Platform Mirror', category: 'core', status: 'ACTIVE', detail: 'Primary platform configuration mirror' },
  { id: 'MR-002', name: 'Governance Mirror', category: 'governance', status: 'ACTIVE', detail: 'Governance overlay mirror' },
  { id: 'MR-003', name: 'Intelligence Mirror', category: 'intelligence', status: 'ACTIVE', detail: 'AI/reasoning capability mirror' },
  { id: 'MR-004', name: 'Spatial Mirror', category: 'spatial', status: 'PENDING', detail: 'Assembly topology mirror' },
  { id: 'MR-005', name: 'Output Mirror', category: 'output', status: 'PENDING', detail: 'Document generation mirror' },
];

export function MirrorsPage() {
  return (
    <ControlTowerPage
      title="Mirrors"
      subtitle="Mirror registry and activity — complements the Multi-Lens Mirror Builder"
      statusBadge="ACTIVE"
      metrics={metrics}
      tableLabel="Mirror Registry"
      assets={assets}
      chartLabel="Mirror Activity Trend"
      seedNotice="Mirror registry shows seed classification data. Use the Mirror Builder (Core nav group) for live multi-lens feature configuration."
    />
  );
}
