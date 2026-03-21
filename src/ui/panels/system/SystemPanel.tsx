/**
 * Construction OS — System Panel
 *
 * Validation summary, alerts, mailbox/proposals, tasks, activity/log, system intelligence.
 * Emits: validation.requested, task.created, proposal.created
 * Subscribes to: truth-echo.propagated, validation.updated, proposal.created, task.created, truth-echo.failed
 * State owned: activeTab, validationSummary, tasks, proposals, alerts
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { eventBus } from '../../events/EventBus';
import { useActiveObject } from '../../stores/useSyncExternalStore';
import { tokens } from '../../theme/tokens';
import type { ValidationUpdatedPayload, TruthEchoFailedPayload, TaskCreatedPayload, ProposalCreatedPayload } from '../../contracts/events';

type SystemTab = 'validation' | 'tasks' | 'proposals' | 'activity';

interface Alert {
  id: string;
  type: 'info' | 'warning' | 'error';
  message: string;
  timestamp: number;
}

export function SystemPanel() {
  const { activeObject } = useActiveObject();
  const [activeTab, setActiveTab] = useState<SystemTab>('validation');
  const [validations, setValidations] = useState<ValidationUpdatedPayload[]>([]);
  const [tasks, setTasks] = useState<TaskCreatedPayload[]>([]);
  const [proposals, setProposals] = useState<ProposalCreatedPayload[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [activityLog, setActivityLog] = useState<Array<{ event: string; time: number; detail: string }>>([]);

  // Subscribe to events
  useEffect(() => {
    const unsubs = [
      eventBus.on('validation.updated', (payload) => {
        setValidations((prev) => [payload, ...prev.slice(0, 49)]);
        setActivityLog((prev) => [{ event: 'validation.updated', time: Date.now(), detail: `${payload.objectId}: ${payload.status}` }, ...prev.slice(0, 99)]);
      }),
      eventBus.on('task.created', (payload) => {
        setTasks((prev) => [payload, ...prev]);
        setActivityLog((prev) => [{ event: 'task.created', time: Date.now(), detail: payload.title }, ...prev.slice(0, 99)]);
      }),
      eventBus.on('proposal.created', (payload) => {
        setProposals((prev) => [payload, ...prev]);
        setActivityLog((prev) => [{ event: 'proposal.created', time: Date.now(), detail: payload.title }, ...prev.slice(0, 99)]);
      }),
      eventBus.on('truth-echo.failed', (payload) => {
        setAlerts((prev) => [{
          id: `alert-${Date.now()}`,
          type: 'error',
          message: `Truth Echo Failed: ${payload.reason} — ${payload.details}`,
          timestamp: payload.timestamp,
        }, ...prev.slice(0, 49)]);
        setActivityLog((prev) => [{ event: 'truth-echo.failed', time: Date.now(), detail: payload.details }, ...prev.slice(0, 99)]);
      }),
      eventBus.on('truth-echo.propagated', (payload) => {
        setActivityLog((prev) => [{ event: 'truth-echo.propagated', time: Date.now(), detail: `${payload.object.name} from ${payload.originPanel} → ${payload.subscribedPanels.join(', ')}` }, ...prev.slice(0, 99)]);
      }),
    ];
    return () => unsubs.forEach((u) => u());
  }, []);

  const handleCreateTask = useCallback(() => {
    if (!activeObject) return;
    eventBus.emit('task.created', {
      taskId: `task-${Date.now()}`,
      objectId: activeObject.id,
      title: `Review ${activeObject.name}`,
      source: 'system',
    });
  }, [activeObject]);

  const tabs: { key: SystemTab; label: string; count?: number }[] = [
    { key: 'validation', label: 'Validation', count: validations.length },
    { key: 'tasks', label: 'Tasks', count: tasks.length },
    { key: 'proposals', label: 'Proposals', count: proposals.length },
    { key: 'activity', label: 'Activity', count: activityLog.length },
  ];

  return (
    <PanelShell panelId="system" title="System" isMock>
      {/* Tab Bar */}
      <div style={{ display: 'flex', gap: '1px', marginBottom: tokens.space.md, background: tokens.color.border, borderRadius: tokens.radius.sm, overflow: 'hidden' }}>
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              flex: 1,
              padding: `${tokens.space.xs} ${tokens.space.sm}`,
              background: activeTab === tab.key ? tokens.color.bgActive : tokens.color.bgElevated,
              color: activeTab === tab.key ? tokens.color.fgPrimary : tokens.color.fgSecondary,
              border: 'none',
              cursor: 'pointer',
              fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.family,
              fontWeight: activeTab === tab.key ? tokens.font.weightSemibold : tokens.font.weightNormal,
            }}
          >
            {tab.label}
            {tab.count !== undefined && tab.count > 0 && (
              <span style={{ marginLeft: '4px', opacity: 0.6 }}>({tab.count})</span>
            )}
          </button>
        ))}
      </div>

      {/* Alerts */}
      {alerts.length > 0 && (
        <div style={{ marginBottom: tokens.space.md }}>
          {alerts.slice(0, 3).map((alert) => (
            <div key={alert.id} style={{
              padding: tokens.space.sm,
              marginBottom: tokens.space.xs,
              background: `${tokens.color[alert.type]}10`,
              borderLeft: `3px solid ${tokens.color[alert.type]}`,
              borderRadius: tokens.radius.sm,
              fontSize: tokens.font.sizeXs,
              color: tokens.color[alert.type],
            }}>
              {alert.message}
            </div>
          ))}
        </div>
      )}

      {/* Tab Content */}
      {activeTab === 'validation' && (
        <div>
          {validations.length === 0 ? (
            <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>No validation events yet.</div>
          ) : (
            validations.map((v, i) => (
              <div key={i} style={{
                padding: tokens.space.sm,
                marginBottom: tokens.space.xs,
                background: tokens.color.bgBase,
                borderRadius: tokens.radius.sm,
                borderLeft: `3px solid ${v.status === 'passed' ? tokens.color.success : v.status === 'failed' ? tokens.color.error : tokens.color.warning}`,
                fontSize: tokens.font.sizeXs,
              }}>
                <span style={{ fontWeight: tokens.font.weightMedium }}>{v.objectId}</span> — {v.status.toUpperCase()}
                {v.issues.length > 0 && <span style={{ color: tokens.color.fgMuted }}> ({v.issues.length} issues)</span>}
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'tasks' && (
        <div>
          {activeObject && (
            <button onClick={handleCreateTask} style={{
              padding: `${tokens.space.xs} ${tokens.space.md}`,
              marginBottom: tokens.space.md,
              background: tokens.color.bgElevated,
              color: tokens.color.fgSecondary,
              border: `1px solid ${tokens.color.border}`,
              borderRadius: tokens.radius.sm,
              cursor: 'pointer',
              fontSize: tokens.font.sizeXs,
              fontFamily: tokens.font.family,
            }}>
              + Create Task for {activeObject.name}
            </button>
          )}
          {tasks.length === 0 ? (
            <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>No tasks yet.</div>
          ) : (
            tasks.map((t, i) => (
              <div key={i} style={{
                padding: tokens.space.sm,
                marginBottom: tokens.space.xs,
                background: tokens.color.bgBase,
                borderRadius: tokens.radius.sm,
                fontSize: tokens.font.sizeXs,
              }}>
                <span style={{ fontWeight: tokens.font.weightMedium }}>{t.title}</span>
                <span style={{ color: tokens.color.fgMuted, marginLeft: tokens.space.sm }}>{t.objectId}</span>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'proposals' && (
        <div>
          {proposals.length === 0 ? (
            <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>No proposals yet.</div>
          ) : (
            proposals.map((p, i) => (
              <div key={i} style={{
                padding: tokens.space.sm,
                marginBottom: tokens.space.xs,
                background: tokens.color.bgBase,
                borderRadius: tokens.radius.sm,
                fontSize: tokens.font.sizeXs,
              }}>
                <span style={{ fontWeight: tokens.font.weightMedium }}>{p.title}</span>
                <div style={{ color: tokens.color.fgMuted, marginTop: '2px' }}>{p.description}</div>
              </div>
            ))
          )}
        </div>
      )}

      {activeTab === 'activity' && (
        <div>
          {activityLog.length === 0 ? (
            <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm }}>No activity yet.</div>
          ) : (
            activityLog.map((entry, i) => (
              <div key={i} style={{
                padding: `${tokens.space.xs} ${tokens.space.sm}`,
                marginBottom: '1px',
                background: i % 2 === 0 ? tokens.color.bgBase : 'transparent',
                fontSize: tokens.font.sizeXs,
                fontFamily: tokens.font.familyMono,
                display: 'flex',
                gap: tokens.space.sm,
              }}>
                <span style={{ color: tokens.color.fgMuted, flexShrink: 0 }}>
                  {new Date(entry.time).toLocaleTimeString()}
                </span>
                <span style={{ color: tokens.color.accentPrimary, flexShrink: 0 }}>
                  {entry.event}
                </span>
                <span style={{ color: tokens.color.fgSecondary, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {entry.detail}
                </span>
              </div>
            ))
          )}
        </div>
      )}
    </PanelShell>
  );
}
