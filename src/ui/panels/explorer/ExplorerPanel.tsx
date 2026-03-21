/**
 * Construction OS — Explorer Panel
 *
 * Project hierarchy, search, filter, object/document/zone selection.
 * Emits: object.selected, zone.selected
 * Subscribes to: truth-echo.propagated, zone.selected, validation.updated
 * State owned: selectedNodeId, expandedNodes, searchQuery, filterState
 */

import { useCallback, useEffect, useState } from 'react';
import { PanelShell } from '../PanelShell';
import { eventBus } from '../../events/EventBus';
import { adapters } from '../../adapters';
import { useActiveObject } from '../../stores/useSyncExternalStore';
import { tokens } from '../../theme/tokens';
import type { ProjectNode } from '../../contracts/adapters';
import type { ActiveObjectIdentity } from '../../contracts/events';

export function ExplorerPanel() {
  const [tree, setTree] = useState<ProjectNode | null>(null);
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set(['proj-001', 'zone-001', 'zone-002', 'zone-003']));
  const [searchQuery, setSearchQuery] = useState('');
  const { activeObject } = useActiveObject();

  useEffect(() => {
    adapters.truth.getProjectTree().then((result) => {
      setTree(result.data);
    });
  }, []);

  const handleSelect = useCallback((node: ProjectNode) => {
    const object: ActiveObjectIdentity = {
      id: node.id,
      name: node.name,
      type: node.type as ActiveObjectIdentity['type'],
    };

    if (node.type === 'zone') {
      eventBus.emit('zone.selected', {
        zoneId: node.id,
        zoneName: node.name,
        source: 'explorer',
        containedObjects: node.children?.map((c) => c.id),
      });
    } else {
      eventBus.emit('object.selected', {
        object,
        source: 'explorer',
        basis: 'mock',
      });
    }
  }, []);

  const toggleExpand = useCallback((nodeId: string) => {
    setExpandedNodes((prev) => {
      const next = new Set(prev);
      if (next.has(nodeId)) next.delete(nodeId);
      else next.add(nodeId);
      return next;
    });
  }, []);

  const renderNode = (node: ProjectNode, depth: number = 0): React.ReactNode => {
    const isActive = activeObject?.id === node.id;
    const isExpanded = expandedNodes.has(node.id);
    const hasChildren = node.children && node.children.length > 0;
    const matchesSearch = !searchQuery || node.name.toLowerCase().includes(searchQuery.toLowerCase());

    if (!matchesSearch && !hasChildren) return null;

    const typeIcon: Record<string, string> = {
      project: '\u25C6',
      zone: '\u25A0',
      folder: '\u25B7',
      document: '\u25A1',
      assembly: '\u25B2',
      element: '\u25CF',
      specification: '\u25C7',
    };

    return (
      <div key={node.id}>
        <div
          onClick={() => {
            if (hasChildren) toggleExpand(node.id);
            handleSelect(node);
          }}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: tokens.space.xs,
            padding: `3px ${tokens.space.sm}`,
            paddingLeft: `${depth * 16 + 8}px`,
            cursor: 'pointer',
            background: isActive ? tokens.color.bgActive : 'transparent',
            borderLeft: isActive ? `2px solid ${tokens.color.echoActive}` : '2px solid transparent',
            color: isActive ? tokens.color.fgPrimary : tokens.color.fgSecondary,
            fontSize: tokens.font.sizeSm,
            transition: `background ${tokens.transition.fast}`,
            userSelect: 'none',
          }}
          onMouseEnter={(e) => {
            if (!isActive) e.currentTarget.style.background = tokens.color.bgHover;
          }}
          onMouseLeave={(e) => {
            if (!isActive) e.currentTarget.style.background = 'transparent';
          }}
        >
          {hasChildren && (
            <span style={{ fontSize: '8px', color: tokens.color.fgMuted, width: '10px' }}>
              {isExpanded ? '\u25BC' : '\u25B6'}
            </span>
          )}
          {!hasChildren && <span style={{ width: '10px' }} />}
          <span style={{ color: isActive ? tokens.color.echoActive : tokens.color.fgMuted, fontSize: '10px' }}>
            {typeIcon[node.type] ?? '\u25CB'}
          </span>
          <span style={{ fontWeight: isActive ? tokens.font.weightSemibold : tokens.font.weightNormal }}>
            {node.name}
          </span>
          <span style={{ color: tokens.color.fgMuted, fontFamily: tokens.font.familyMono, fontSize: tokens.font.sizeXs, marginLeft: 'auto' }}>
            {node.type}
          </span>
        </div>
        {hasChildren && isExpanded && node.children!.map((child) => renderNode(child, depth + 1))}
      </div>
    );
  };

  return (
    <PanelShell panelId="explorer" title="Explorer" isMock={adapters.truth.isMock}>
      {/* Search */}
      <div style={{ marginBottom: tokens.space.md }}>
        <input
          type="text"
          placeholder="Search objects..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            width: '100%',
            padding: `${tokens.space.xs} ${tokens.space.sm}`,
            background: tokens.color.bgBase,
            border: `1px solid ${tokens.color.border}`,
            borderRadius: tokens.radius.sm,
            color: tokens.color.fgPrimary,
            fontSize: tokens.font.sizeSm,
            outline: 'none',
          }}
        />
      </div>

      {/* Tree */}
      <div style={{ margin: `-${tokens.space.md}`, marginTop: 0 }}>
        {tree ? renderNode(tree) : (
          <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeSm, padding: tokens.space.md }}>
            Loading project tree...
          </div>
        )}
      </div>
    </PanelShell>
  );
}
