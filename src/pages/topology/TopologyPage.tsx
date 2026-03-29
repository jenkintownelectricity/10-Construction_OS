/**
 * Topology Page — Construction OS Control Tower
 * Absorbed from VTI control tower topology surface.
 * Shows system graph architecture with nodes, edges, and relationship visualization.
 */

import { ControlTowerPage, type PageMetric, type AssetItem } from '../../components/control-tower';

const metrics: PageMetric[] = [
  { label: 'System Nodes', value: '14', delta: '+2 this session', trend: 'up' },
  { label: 'Active Nodes', value: '11', delta: 'Stable', trend: 'neutral' },
  { label: 'Governed Edges', value: '22', delta: '+4 this pass', trend: 'up' },
  { label: 'Total Contracts', value: '38', delta: '+6 linked', trend: 'up' },
];

const assets: AssetItem[] = [
  { id: 'TN-001', name: 'Construction Kernel', category: 'core', status: 'ACTIVE', detail: 'Primary kernel node' },
  { id: 'TN-002', name: 'Construction Runtime', category: 'execution', status: 'ACTIVE', detail: 'Execution engine' },
  { id: 'TN-003', name: 'Construction Atlas', category: 'spatial', status: 'ACTIVE', detail: 'Spatial context layer' },
  { id: 'TN-004', name: 'Cognitive Bus', category: 'intelligence', status: 'ACTIVE', detail: 'Event routing substrate' },
  { id: 'TN-005', name: 'Construction Registry', category: 'registry', status: 'ACTIVE', detail: 'Append-only ledger' },
  { id: 'TN-006', name: 'Governance Sentinel', category: 'governance', status: 'ACTIVE', detail: 'Boundary enforcement' },
  { id: 'TN-007', name: 'Pattern System', category: 'intelligence', status: 'ACTIVE', detail: 'Pattern recognition layer' },
  { id: 'TN-008', name: 'Worker Fleet', category: 'execution', status: 'ACTIVE', detail: 'Distributed execution pool' },
  { id: 'TN-009', name: 'DNA Layer', category: 'core', status: 'STAGED', detail: 'Material encoding substrate' },
  { id: 'TN-010', name: 'Application Surface', category: 'output', status: 'ACTIVE', detail: 'Primary user interface' },
];

export function TopologyPage() {
  return (
    <ControlTowerPage
      title="Topology"
      subtitle="System architecture graph — node and edge relationships across the platform"
      statusBadge="ACTIVE"
      metrics={metrics}
      tableLabel="Topology Nodes"
      assets={assets}
      chartLabel="Edge Activity Trend"
      seedNotice="Topology data sourced from Construction_OS_Registry reference vocabulary. Graph visualization staged for interactive SVG integration."
    />
  );
}
