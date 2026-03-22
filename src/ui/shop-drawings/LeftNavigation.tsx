/**
 * Shop Drawings Shell — Left Navigation Panel
 *
 * Ported from OMNI-VIEW legacy layout. File explorer sidebar with:
 * - Filter/search input
 * - Hierarchical file tree
 * - Selection state with accent border
 * - Workspace label
 *
 * Presentation shell only. Wired to existing event bus for object selection.
 */

import { useCallback, useState } from 'react';
import { tokens } from '../theme/tokens';
import { eventBus } from '../events/EventBus';
import type { ShopDrawingFile } from './types';
import type { ActiveObjectIdentity } from '../contracts/events';

// ─── Sample file tree (presentation shell) ────────────────────────────

const SAMPLE_TREE: ShopDrawingFile[] = [
  {
    id: 'folder-specs',
    name: 'Specifications',
    type: 'folder',
    children: [
      { id: 'spec-072100', name: '072100 - Thermal Insulation.pdf', type: 'pdf', pageCount: 12, size: '2.4 MB' },
      { id: 'spec-072726', name: '072726 - Fluid-Applied Membrane.pdf', type: 'pdf', pageCount: 8, size: '1.8 MB' },
      { id: 'spec-075216', name: '075216 - SBS Modified Bitumen.pdf', type: 'pdf', pageCount: 15, size: '3.1 MB' },
    ],
  },
  {
    id: 'folder-drawings',
    name: 'Shop Drawings',
    type: 'folder',
    children: [
      { id: 'sd-001', name: 'SD-A101 Roof Plan.pdf', type: 'pdf', pageCount: 1, size: '4.2 MB' },
      { id: 'sd-002', name: 'SD-A102 Roof Details.pdf', type: 'pdf', pageCount: 3, size: '6.8 MB' },
      { id: 'sd-003', name: 'SD-A103 Wall Section.pdf', type: 'pdf', pageCount: 2, size: '5.1 MB' },
      { id: 'sd-004', name: 'SD-A104 Assembly Detail.dwg', type: 'dwg', size: '1.2 MB' },
    ],
  },
  {
    id: 'folder-submittals',
    name: 'Submittals',
    type: 'folder',
    children: [
      { id: 'sub-001', name: 'TPO Membrane Submittal.pdf', type: 'pdf', pageCount: 24, size: '8.9 MB' },
      { id: 'sub-002', name: 'Insulation Product Data.pdf', type: 'pdf', pageCount: 6, size: '2.1 MB' },
    ],
  },
];

// ─── Styles ────────────────────────────────────────────────────────────

const panelStyle: React.CSSProperties = {
  width: '240px',
  minWidth: '180px',
  background: tokens.color.bgSurface,
  borderRight: `1px solid ${tokens.color.border}`,
  display: 'flex',
  flexDirection: 'column',
  flexShrink: 0,
};

const headerStyle: React.CSSProperties = {
  height: '32px',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '0 10px',
  background: tokens.color.bgElevated,
  borderBottom: `1px solid ${tokens.color.border}`,
  flexShrink: 0,
};

const headerLabelStyle: React.CSSProperties = {
  fontSize: '9px',
  fontWeight: 700,
  letterSpacing: '1.5px',
  color: tokens.color.fgMuted,
  textTransform: 'uppercase',
};

const filterStyle: React.CSSProperties = {
  margin: '6px 8px',
  padding: '5px 8px',
  background: tokens.color.bgDeep,
  border: `1px solid ${tokens.color.border}`,
  borderRadius: '4px',
  color: tokens.color.fgPrimary,
  fontSize: '11px',
  outline: 'none',
  width: 'calc(100% - 16px)',
  fontFamily: tokens.font.familyMono,
};

// ─── File type icons (Unicode, matching OMNI-VIEW style) ──────────────

const FILE_ICONS: Record<string, string> = {
  folder: '\u{1F4C1}',
  pdf: '\u{1F4C4}',
  dwg: '\u{1F4D0}',
  image: '\u{1F5BC}',
  document: '\u{1F4C3}',
};

// ─── Component ────────────────────────────────────────────────────────

interface LeftNavigationProps {
  onFileSelect?: (file: ShopDrawingFile) => void;
  selectedFileId?: string | null;
}

export function LeftNavigation({ onFileSelect, selectedFileId }: LeftNavigationProps) {
  const [filter, setFilter] = useState('');
  const [expandedFolders, setExpandedFolders] = useState<Set<string>>(
    new Set(['folder-specs', 'folder-drawings', 'folder-submittals'])
  );

  const toggleFolder = useCallback((folderId: string) => {
    setExpandedFolders((prev) => {
      const next = new Set(prev);
      if (next.has(folderId)) next.delete(folderId);
      else next.add(folderId);
      return next;
    });
  }, []);

  const handleSelect = useCallback((file: ShopDrawingFile) => {
    if (file.type === 'folder') {
      toggleFolder(file.id);
      return;
    }

    // Emit on the existing event bus
    const object: ActiveObjectIdentity = {
      id: file.id,
      name: file.name,
      type: 'document',
    };
    eventBus.emit('object.selected', {
      object,
      source: 'explorer',
      basis: 'canonical',
    });

    onFileSelect?.(file);
  }, [onFileSelect, toggleFolder]);

  const renderFile = (file: ShopDrawingFile, depth: number = 0) => {
    const matchesFilter = !filter || file.name.toLowerCase().includes(filter.toLowerCase());
    const hasChildren = file.children && file.children.length > 0;

    if (!matchesFilter && !hasChildren) return null;

    const isSelected = selectedFileId === file.id;
    const isExpanded = expandedFolders.has(file.id);

    return (
      <div key={file.id}>
        <button
          onClick={() => handleSelect(file)}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '6px',
            padding: '4px 10px',
            paddingLeft: `${depth * 14 + 10}px`,
            cursor: 'pointer',
            borderLeft: isSelected ? `2px solid ${tokens.color.accentPrimary}` : '2px solid transparent',
            borderTop: 'none',
            borderRight: 'none',
            borderBottom: 'none',
            background: isSelected ? `${tokens.color.accentPrimary}12` : 'transparent',
            color: isSelected ? tokens.color.fgPrimary : tokens.color.fgSecondary,
            fontSize: '11px',
            textAlign: 'left',
            width: '100%',
            transition: 'background 0.08s',
            fontFamily: tokens.font.familyMono,
          }}
          onMouseEnter={(e) => {
            if (!isSelected) e.currentTarget.style.background = tokens.color.bgHover;
          }}
          onMouseLeave={(e) => {
            if (!isSelected) e.currentTarget.style.background = 'transparent';
          }}
        >
          {hasChildren && (
            <span style={{ fontSize: '8px', color: tokens.color.fgMuted, width: '8px', flexShrink: 0 }}>
              {isExpanded ? '\u25BC' : '\u25B6'}
            </span>
          )}
          <span style={{ fontSize: '14px', flexShrink: 0 }}>{FILE_ICONS[file.type] ?? FILE_ICONS.document}</span>
          <span style={{
            overflow: 'hidden',
            textOverflow: 'ellipsis',
            whiteSpace: 'nowrap',
            flex: 1,
          }}>
            {file.name}
          </span>
        </button>
        {hasChildren && isExpanded && file.children!.map((child) => renderFile(child, depth + 1))}
      </div>
    );
  };

  return (
    <div style={panelStyle}>
      <div style={headerStyle}>
        <span style={headerLabelStyle}>EXPLORER</span>
      </div>
      <input
        type="text"
        placeholder="Filter files..."
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
        style={filterStyle}
      />
      <div style={{ flex: 1, overflowY: 'auto', padding: '2px 0' }}>
        {SAMPLE_TREE.map((file) => renderFile(file))}
      </div>
      {/* Workspace label — matches OMNI-VIEW #wlabel */}
      {selectedFileId && (
        <div style={{
          padding: '6px 10px',
          borderTop: `1px solid ${tokens.color.border}`,
          fontSize: '9px',
          color: tokens.color.accentPrimary,
          fontWeight: 700,
          flexShrink: 0,
        }}>
          WORKSPACE ACTIVE
        </div>
      )}
    </div>
  );
}
