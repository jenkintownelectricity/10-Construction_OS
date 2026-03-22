/**
 * Construction Atlas — Shop Drawings Page
 *
 * Submittal tracking and review. Left list + right detail.
 * Status workflow, review comments, revision history.
 */

import { useState } from 'react';
import { DEFAULT_BRANDING } from '../../../lib/branding/branding-types';
import { generationStore } from '../../stores/generationStore';
import { activeObjectStore } from '../../stores/activeObjectStore';
import { eventBus } from '../../events/EventBus';
import type { AtlasRoute } from '../types';

const c = DEFAULT_BRANDING.colors;

const cardStyle: React.CSSProperties = {
  background: '#ffffff',
  border: `1px solid ${c.border}`,
  borderRadius: '8px',
  padding: '20px',
};

const STATUS_COLORS: Record<string, { bg: string; fg: string }> = {
  'In Review': { bg: '#dbeafe', fg: '#1e40af' },
  Approved: { bg: '#dcfce7', fg: '#166534' },
  Submitted: { bg: '#f1f5f9', fg: '#475569' },
  Rejected: { bg: '#fecaca', fg: '#991b1b' },
  Revised: { bg: '#e0e7ff', fg: '#3730a3' },
};

interface Submittal {
  id: string;
  title: string;
  spec: string;
  manufacturer: string;
  rev: string;
  status: string;
  project: string;
  pages: number;
  size: string;
  submitted: string;
  reviewer: string;
}

const SUBMITTALS: Submittal[] = [
  { id: 'SD-001', title: 'Curtain Wall System \u2014 South Elevation', spec: '08 44 13', manufacturer: 'YKK AP', rev: 'Rev 2', status: 'In Review', project: 'Waterfront Tower Phase 2', pages: 24, size: '12.4 MB', submitted: '2026-03-10', reviewer: 'Michael Torres' },
  { id: 'SD-002', title: 'Roof Membrane Assembly \u2014 Full Plan', spec: '07 52 16', manufacturer: 'Carlisle SynTec', rev: 'Rev 3', status: 'Approved', project: 'Heritage Plaza', pages: 18, size: '8.2 MB', submitted: '2026-03-08', reviewer: 'Michael Torres' },
  { id: 'SD-003', title: 'Metal Panel Layout \u2014 Building C West', spec: '07 42 43', manufacturer: 'ATAS International', rev: 'Rev 1', status: 'Submitted', project: 'Industrial Park', pages: 12, size: '6.1 MB', submitted: '2026-03-12', reviewer: '' },
  { id: 'SD-004', title: 'Window Assemblies \u2014 Type A through E', spec: '08 51 13', manufacturer: 'Marvin Windows', rev: 'Rev 1', status: 'Rejected', project: 'Heritage Plaza', pages: 32, size: '15.3 MB', submitted: '2026-03-05', reviewer: 'Michael Torres' },
  { id: 'SD-005', title: 'Expansion Joint Covers \u2014 All Locations', spec: '07 95 13', manufacturer: 'Inpro Corporation', rev: 'Rev 2', status: 'Revised', project: 'Metro Station', pages: 8, size: '4.1 MB', submitted: '2026-03-09', reviewer: 'Rachel Kim' },
  { id: 'SD-006', title: 'Below-Grade Waterproofing \u2014 Foundation Walls', spec: '07 11 13', manufacturer: 'Sika Corporation', rev: 'Rev 1', status: 'Approved', project: 'Airport Terminal', pages: 14, size: '7.6 MB', submitted: '2026-03-06', reviewer: 'James Park' },
];

const WORKFLOW_STEPS = ['Submitted', 'In Review', 'Approved', 'Rejected'];

interface ShopDrawingsPageProps {
  onNavigate: (route: AtlasRoute) => void;
}

export function ShopDrawingsPage({ onNavigate }: ShopDrawingsPageProps) {
  const [selectedId, setSelectedId] = useState('SD-001');
  const [statusFilter, setStatusFilter] = useState<string | null>(null);

  const selected = SUBMITTALS.find((s) => s.id === selectedId) ?? SUBMITTALS[0];
  const filtered = statusFilter ? SUBMITTALS.filter((s) => s.status === statusFilter) : SUBMITTALS;

  const filterTabs = [
    { label: `All (${SUBMITTALS.length})`, value: null },
    { label: `Submitted (${SUBMITTALS.filter((s) => s.status === 'Submitted').length})`, value: 'Submitted' },
    { label: `In Review (${SUBMITTALS.filter((s) => s.status === 'In Review').length})`, value: 'In Review' },
    { label: `Approved (${SUBMITTALS.filter((s) => s.status === 'Approved').length})`, value: 'Approved' },
    { label: `Rejected (${SUBMITTALS.filter((s) => s.status === 'Rejected').length})`, value: 'Rejected' },
    { label: `Revised (${SUBMITTALS.filter((s) => s.status === 'Revised').length})`, value: 'Revised' },
  ];

  return (
    <div style={{ display: 'flex', gap: '0', height: 'calc(100vh - 40px)' }}>
      {/* Left: List */}
      <div style={{ width: '340px', flexShrink: 0, borderRight: `1px solid ${c.border}`, overflowY: 'auto', paddingRight: '16px' }}>
        <h1 style={{ fontSize: '24px', fontWeight: 700, color: c.text, margin: '0 0 4px' }}>Shop Drawings</h1>
        <p style={{ color: c.textMuted, margin: '0 0 16px', fontSize: '13px' }}>Submittal tracking and review</p>

        <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '16px' }}>
          {filterTabs.map((tab) => {
            const isActive = statusFilter === tab.value;
            return (
              <button
                key={tab.label}
                onClick={() => setStatusFilter(tab.value)}
                style={{
                  padding: '4px 10px', borderRadius: '12px', fontSize: '11px', fontWeight: 600,
                  background: isActive ? c.secondary : 'transparent',
                  color: isActive ? '#fff' : c.textMuted,
                  border: isActive ? 'none' : `1px solid ${c.border}`,
                  cursor: 'pointer',
                }}
              >
                {tab.label}
              </button>
            );
          })}
        </div>

        {filtered.map((s) => {
          const sc = STATUS_COLORS[s.status] ?? STATUS_COLORS.Submitted;
          const isSelected = s.id === selectedId;
          return (
            <button
              key={s.id}
              onClick={() => setSelectedId(s.id)}
              style={{
                display: 'block', width: '100%', textAlign: 'left',
                padding: '12px', marginBottom: '4px', borderRadius: '6px',
                background: isSelected ? c.surfaceAlt : 'transparent',
                border: isSelected ? `1px solid ${c.border}` : '1px solid transparent',
                cursor: 'pointer',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '12px', color: c.textMuted, fontFamily: 'monospace' }}>{s.id}</span>
                <span style={{ padding: '2px 8px', borderRadius: '10px', fontSize: '10px', fontWeight: 600, background: sc.bg, color: sc.fg }}>
                  {s.status}
                </span>
              </div>
              <div style={{ fontWeight: 500, color: c.text, fontSize: '13px', marginTop: '4px' }}>{s.title}</div>
              <div style={{ fontSize: '11px', color: c.textMuted, marginTop: '2px' }}>{s.spec} \u2014 {s.manufacturer} \u00B7 {s.rev}</div>
            </button>
          );
        })}
      </div>

      {/* Right: Detail */}
      <div style={{ flex: 1, overflowY: 'auto', paddingLeft: '24px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '4px' }}>
              <span style={{ fontSize: '13px', color: c.textMuted, fontFamily: 'monospace' }}>{selected.id}</span>
              <span style={{
                padding: '2px 10px', borderRadius: '10px', fontSize: '11px', fontWeight: 600,
                ...(STATUS_COLORS[selected.status] ? { background: STATUS_COLORS[selected.status].bg, color: STATUS_COLORS[selected.status].fg } : {}),
              }}>
                {selected.status}
              </span>
            </div>
            <h2 style={{ fontSize: '22px', fontWeight: 700, color: c.text, margin: '0 0 4px' }}>{selected.title}</h2>
            <div style={{ color: c.textMuted, fontSize: '13px' }}>{selected.spec} \u2014 {selected.manufacturer}</div>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <button
              onClick={() => {
                // Set source context for the generation loop
                generationStore.setSourceContext({
                  submittalId: selected.id,
                  submittalTitle: selected.title,
                  manufacturer: selected.manufacturer,
                  spec: selected.spec,
                  project: selected.project,
                });
                // Set active object so Workstation panels can pick up context
                activeObjectStore.setActiveObject(
                  { id: selected.id, type: 'document', name: selected.title },
                  'explorer',
                  'canonical',
                );
                // Emit object.selected for Truth Echo propagation
                eventBus.emit('object.selected', {
                  object: { id: selected.id, type: 'document', name: selected.title },
                  source: 'explorer',
                  basis: 'canonical',
                });
                onNavigate('tools');
              }}
              style={{
                padding: '8px 16px', borderRadius: '6px', background: c.primary, color: '#fff',
                border: 'none', fontWeight: 600, fontSize: '13px', cursor: 'pointer',
              }}
            >
              Launch Workstation
            </button>
            <button
              onClick={() => onNavigate('viewer')}
              style={{
                padding: '8px 16px', borderRadius: '6px', background: 'transparent', color: c.primary,
                border: `1px solid ${c.primary}`, fontWeight: 600, fontSize: '13px', cursor: 'pointer',
              }}
            >
              Open in Viewer
            </button>
          </div>
        </div>

        {/* Metadata grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr 1fr', gap: '12px', marginBottom: '24px' }}>
          {[
            { label: 'MANUFACTURER', value: selected.manufacturer },
            { label: 'PROJECT', value: selected.project },
            { label: 'REVISION', value: selected.rev },
            { label: 'PAGES', value: `${selected.pages} pages` },
            { label: 'SUBMITTED', value: selected.submitted },
            { label: 'REVIEWED', value: selected.reviewer ? 'Pending' : '\u2014' },
            { label: 'REVIEWER', value: selected.reviewer || '\u2014' },
            { label: 'FILE SIZE', value: selected.size },
          ].map((field) => (
            <div key={field.label} style={{ ...cardStyle, padding: '12px' }}>
              <div style={{ fontSize: '10px', fontWeight: 600, color: c.textMuted, letterSpacing: '0.5px', marginBottom: '4px' }}>{field.label}</div>
              <div style={{ fontSize: '14px', fontWeight: 500, color: c.text }}>{field.value}</div>
            </div>
          ))}
        </div>

        {/* Status Workflow */}
        <div style={{ ...cardStyle, marginBottom: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, color: c.text, margin: '0 0 12px' }}>Status Workflow</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            {WORKFLOW_STEPS.map((step, i) => {
              const isCurrent = step === selected.status;
              const isPast = WORKFLOW_STEPS.indexOf(selected.status) > i;
              return (
                <div key={step} style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{
                    padding: '4px 12px', borderRadius: '14px', fontSize: '12px', fontWeight: 600,
                    background: isCurrent ? c.secondary : isPast ? '#dcfce7' : c.surfaceAlt,
                    color: isCurrent ? '#fff' : isPast ? '#166534' : c.textMuted,
                  }}>
                    {step}
                  </span>
                  {i < WORKFLOW_STEPS.length - 1 && <span style={{ color: c.textMuted }}>{'\u203A'}</span>}
                </div>
              );
            })}
          </div>
        </div>

        {/* Review Comments */}
        <div style={{ ...cardStyle, marginBottom: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, color: c.text, margin: '0 0 12px' }}>Review Comments (2)</h3>
          {[
            { author: 'Michael Torres', date: '2026-03-12', sheet: 'Sheet 8, Detail 3A', comment: 'Stack joint detail at level 5 needs clarification \u2014 show sealant backup and weep path' },
            { author: 'Michael Torres', date: '2026-03-12', sheet: 'Sheet 12', comment: 'Verify anchor spacing at wind load zone 3 matches structural calc' },
          ].map((cmt, i) => (
            <div key={i} style={{ padding: '12px 0', borderBottom: i < 1 ? `1px solid ${c.border}` : 'none' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '4px' }}>
                <span style={{ fontWeight: 600, fontSize: '13px', color: c.text }}>{cmt.author}</span>
                <span style={{ fontSize: '12px', color: c.textMuted }}>{cmt.date}</span>
              </div>
              <div style={{ fontSize: '12px', color: c.textMuted, fontFamily: 'monospace', marginBottom: '6px' }}>{cmt.sheet}</div>
              <div style={{ fontSize: '13px', color: c.text }}>{cmt.comment}</div>
            </div>
          ))}
        </div>

        {/* Revision History */}
        <div style={{ ...cardStyle, marginBottom: '24px' }}>
          <h3 style={{ fontSize: '16px', fontWeight: 600, color: c.text, margin: '0 0 12px' }}>Revision History</h3>
          {[
            { num: 1, date: '2026-02-20', desc: 'Initial submission' },
            { num: 2, date: '2026-03-10', desc: 'Updated anchor spacing per structural review' },
          ].map((rev) => (
            <div key={rev.num} style={{ display: 'flex', gap: '12px', marginBottom: '12px' }}>
              <div style={{
                width: '24px', height: '24px', borderRadius: '50%', background: c.secondary,
                color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '11px', fontWeight: 700, flexShrink: 0,
              }}>
                {rev.num}
              </div>
              <div>
                <div style={{ fontSize: '12px', color: c.textMuted }}>{rev.date}</div>
                <div style={{ fontSize: '13px', color: c.text }}>{rev.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
