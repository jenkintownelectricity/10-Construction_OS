/**
 * Shop Drawings Shell — Right Properties Panel
 *
 * Ported from OMNI-VIEW legacy layout (.rpanel). Three-tab right sidebar:
 * - Properties: Document props, Selection props, Text props, Measurement
 * - Taxonomy: SDIO rename engine with full revision/version options + rename history
 * - Toolbox: Redline tool grid (3-col) + Document ops + Count + Measurements
 *
 * Presentation shell only. No deprecated logic.
 * Taxonomy fields are display-ready but not wired to rename engine.
 * Redline tool grid mirrors OMNI-VIEW .tcgrid layout.
 */

import { useState } from 'react';
import { tokens } from '../theme/tokens';
import type { PropertiesPanelTab, DocumentProperties, ViewerTool } from './types';

// ─── Styles ────────────────────────────────────────────────────────────

const panelStyle: React.CSSProperties = {
  width: '280px',
  minWidth: '200px',
  background: tokens.color.bgSurface,
  borderLeft: `1px solid ${tokens.color.border}`,
  display: 'flex',
  flexDirection: 'column',
  flexShrink: 0,
  overflow: 'hidden',
};

const tabBarStyle: React.CSSProperties = {
  display: 'flex',
  borderBottom: `1px solid ${tokens.color.border}`,
  flexShrink: 0,
};

const sectionStyle: React.CSSProperties = {
  padding: '8px 10px',
  borderBottom: `1px solid ${tokens.color.border}`,
};

const sectionLabelStyle: React.CSSProperties = {
  fontSize: '9px',
  fontWeight: 700,
  letterSpacing: '1.2px',
  color: tokens.color.fgMuted,
  marginBottom: '4px',
  textTransform: 'uppercase',
};

const propRowStyle: React.CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  gap: '6px',
  padding: '3px 0',
};

const propLabelStyle: React.CSSProperties = {
  fontSize: '9px',
  color: tokens.color.fgMuted,
  minWidth: '55px',
  fontWeight: 600,
};

const propValueStyle: React.CSSProperties = {
  fontSize: '10px',
  color: tokens.color.fgSecondary,
  wordBreak: 'break-all',
};

const fieldRowStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: '3px',
  marginBottom: '6px',
};

const fieldLabelStyle: React.CSSProperties = {
  fontSize: '9px',
  color: tokens.color.fgMuted,
  letterSpacing: '0.5px',
  fontWeight: 700,
  textTransform: 'uppercase',
};

const fieldInputStyle: React.CSSProperties = {
  padding: '5px 8px',
  background: tokens.color.bgDeep,
  border: `1px solid ${tokens.color.border}`,
  borderRadius: '4px',
  color: tokens.color.fgPrimary,
  fontSize: '11px',
  outline: 'none',
  width: '100%',
  fontFamily: tokens.font.familyMono,
};

const docOpsBtnStyle: React.CSSProperties = {
  padding: '6px 10px',
  background: tokens.color.bgElevated,
  border: `1px solid ${tokens.color.border}`,
  borderRadius: '4px',
  color: tokens.color.fgSecondary,
  fontSize: '10px',
  cursor: 'pointer',
  display: 'flex',
  alignItems: 'center',
  gap: '6px',
  fontWeight: 600,
  width: '100%',
  textAlign: 'left',
};

// ─── Redline tool grid data (matches OMNI-VIEW .tcgrid) ───────────────

const REDLINE_TOOLS: { id: ViewerTool; label: string; icon: string }[] = [
  { id: 'cursor', label: 'Cursor', icon: '\u2197' },
  { id: 'pen', label: 'Pen', icon: '\u270E' },
  { id: 'highlighter', label: 'Highlight', icon: '\u{1F58D}' },
  { id: 'text', label: 'Text', icon: 'T' },
  { id: 'arrow', label: 'Arrow', icon: '\u2192' },
  { id: 'rect', label: 'Rect', icon: '\u25A1' },
  { id: 'cloud', label: 'Cloud', icon: '\u2601' },
  { id: 'callout', label: 'Callout', icon: '\u{1F4AC}' },
  { id: 'dimension', label: 'Dimension', icon: '\u21A4' },
  { id: 'count', label: 'Count', icon: '#' },
  { id: 'stamp', label: 'Stamp', icon: '\u{1F4F7}' },
  { id: 'eraser', label: 'Eraser', icon: '\u2716' },
];

// ─── Component ────────────────────────────────────────────────────────

interface PropertiesPanelProps {
  documentProps: DocumentProperties | null;
  activeTool?: ViewerTool;
  onToolSelect?: (tool: ViewerTool) => void;
}

export function PropertiesPanel({ documentProps, activeTool, onToolSelect }: PropertiesPanelProps) {
  const [activeTab, setActiveTab] = useState<PropertiesPanelTab>('properties');

  const tabs: { key: PropertiesPanelTab; label: string }[] = [
    { key: 'properties', label: 'Properties' },
    { key: 'taxonomy', label: 'Taxonomy' },
    { key: 'toolbox', label: 'Toolbox' },
  ];

  return (
    <div style={panelStyle}>
      {/* Tab bar — matches OMNI-VIEW .rtabs */}
      <div style={tabBarStyle}>
        {tabs.map((tab) => {
          const isActive = activeTab === tab.key;
          return (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              style={{
                flex: 1,
                padding: '7px 4px',
                textAlign: 'center',
                fontSize: '9px',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.8px',
                color: isActive ? tokens.color.accentPrimary : tokens.color.fgMuted,
                cursor: 'pointer',
                borderBottom: `2px solid ${isActive ? tokens.color.accentPrimary : 'transparent'}`,
                background: 'transparent',
                borderTop: 'none',
                borderLeft: 'none',
                borderRight: 'none',
                transition: '0.15s',
              }}
            >
              {tab.label}
            </button>
          );
        })}
      </div>

      {/* Tab content */}
      <div style={{ flex: 1, overflowY: 'auto' }}>

        {/* ═══ PROPERTIES TAB ═══ */}
        {activeTab === 'properties' && (
          <div>
            {/* Document Properties — matches OMNI-VIEW #propDoc */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Document Properties</div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>File</label>
                <span style={propValueStyle}>{documentProps?.fileName ?? 'None'}</span>
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Pages</label>
                <span style={propValueStyle}>{documentProps?.pageCount ?? '\u2014'}</span>
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Size</label>
                <span style={propValueStyle}>{documentProps?.fileSize ?? '\u2014'}</span>
              </div>
            </div>

            {/* Selection Properties — matches OMNI-VIEW #propSel */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Selection Properties</div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Type</label>
                <span style={{ ...propValueStyle, color: tokens.color.accentPrimary }}>{'\u2014'}</span>
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Fill</label>
                <input type="color" defaultValue="#e74c3c" style={{ width: '28px', height: '22px', padding: 0, border: `1px solid ${tokens.color.border}`, cursor: 'pointer', background: 'transparent' }} />
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Stroke</label>
                <input type="color" defaultValue="#e74c3c" style={{ width: '28px', height: '22px', padding: 0, border: `1px solid ${tokens.color.border}`, cursor: 'pointer', background: 'transparent' }} />
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Opacity</label>
                <input type="range" min="0" max="1" step="0.05" defaultValue="1" style={{ flex: 1 }} />
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Width</label>
                <input type="number" defaultValue="2" min="0.5" max="20" step="0.5" style={{ ...fieldInputStyle, width: '60px' }} />
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Style</label>
                <select defaultValue="solid" style={{ ...fieldInputStyle, flex: 1 }}>
                  <option value="solid">Solid</option>
                  <option value="dash">Dashed</option>
                  <option value="dot">Dotted</option>
                </select>
              </div>
            </div>

            {/* Text Properties — matches OMNI-VIEW #propText */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Text Properties</div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Font</label>
                <select defaultValue="Arial" style={{ ...fieldInputStyle, flex: 1 }}>
                  <option>Arial</option>
                  <option>Helvetica</option>
                  <option>Times New Roman</option>
                  <option>Courier New</option>
                  <option>Georgia</option>
                </select>
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Size</label>
                <input type="number" defaultValue="16" min="6" max="200" style={{ ...fieldInputStyle, width: '60px' }} />
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Color</label>
                <input type="color" defaultValue="#e74c3c" style={{ width: '28px', height: '22px', padding: 0, border: `1px solid ${tokens.color.border}`, cursor: 'pointer', background: 'transparent' }} />
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Bold</label>
                <input type="checkbox" style={{ width: 'auto' }} />
              </div>
            </div>

            {/* Measurement — matches OMNI-VIEW #propMeas */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Measurement</div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Scale</label>
                <span style={propValueStyle}>Not calibrated</span>
              </div>
              <div style={propRowStyle}>
                <label style={propLabelStyle}>Unit</label>
                <span style={propValueStyle}>{'\u2014'}</span>
              </div>
            </div>
          </div>
        )}

        {/* ═══ TAXONOMY TAB ═══ */}
        {activeTab === 'taxonomy' && (
          <div>
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>SDIO Rename Engine</div>
              <div style={fieldRowStyle}>
                <label style={fieldLabelStyle}>Document Class (XXX)</label>
                <select style={fieldInputStyle}>
                  <option value="">{'\u2014'}</option>
                  <option value="500">500 — Full Shop Set (PDF)</option>
                  <option value="501">501 — Shop Dwg (PDF)</option>
                  <option value="502">502 — Shop Dwg (DWG)</option>
                  <option value="503">503 — As-Builts</option>
                  <option value="103">103 — Spec Sections (Div 7)</option>
                  <option value="200">200 — Full Project Set</option>
                  <option value="210">210 — Full Arch Set</option>
                  <option value="220">220 — Full Civil Set</option>
                </select>
              </div>
              <div style={fieldRowStyle}>
                <label style={fieldLabelStyle}>Revision</label>
                <select style={fieldInputStyle}>
                  <option value="">{'\u2014'}</option>
                  <option value="R00">R00 — Initial</option>
                  <option value="R01">R01</option>
                  <option value="R02">R02</option>
                  <option value="R03">R03</option>
                  <option value="R04">R04</option>
                  <option value="R05">R05</option>
                  <option value="RA">RA</option>
                  <option value="RB">RB</option>
                  <option value="RC">RC</option>
                  <option value="RD">RD</option>
                </select>
              </div>
              <div style={fieldRowStyle}>
                <label style={fieldLabelStyle}>Version</label>
                <select style={fieldInputStyle}>
                  <option value="">{'\u2014'}</option>
                  <option value="V01">V01</option>
                  <option value="V02">V02</option>
                  <option value="V03">V03</option>
                  <option value="DRAFT">DRAFT</option>
                  <option value="FINAL">FINAL</option>
                  <option value="IFC">IFC — For Construction</option>
                  <option value="IFR">IFR — For Review</option>
                  <option value="IFB">IFB — For Bid</option>
                  <option value="RECORD">RECORD — As-Built</option>
                </select>
              </div>
              <div style={fieldRowStyle}>
                <label style={fieldLabelStyle}>CSI Spec (6-digit)</label>
                <input type="text" placeholder="e.g. 072726" maxLength={6} style={fieldInputStyle} />
              </div>
              <div style={fieldRowStyle}>
                <label style={fieldLabelStyle}>Date (DDMMYY)</label>
                <input type="text" placeholder="DDMMYY" maxLength={6} style={fieldInputStyle} />
              </div>
              <div style={fieldRowStyle}>
                <label style={fieldLabelStyle}>Client Job# (AAAYYJJ)</label>
                <input type="text" placeholder="e.g. PAT2602" maxLength={10} style={fieldInputStyle} />
              </div>
              <div style={fieldRowStyle}>
                <label style={fieldLabelStyle}>User Notes</label>
                <input type="text" placeholder="e.g. StumpNeck-Assembly" maxLength={80} style={fieldInputStyle} />
              </div>
            </div>

            {/* Predicted filename box — matches OMNI-VIEW .pvbox */}
            <div style={{
              margin: '0 10px 8px',
              padding: '10px',
              background: tokens.color.bgDeep,
              border: `1px solid ${tokens.color.border}`,
              borderRadius: '6px',
            }}>
              <div style={{
                fontSize: '8px',
                fontWeight: 700,
                color: tokens.color.accentPrimary,
                letterSpacing: '1.5px',
                marginBottom: '4px',
              }}>
                PREDICTED FILENAME
              </div>
              <div style={{
                fontSize: '12px',
                fontWeight: 700,
                color: tokens.color.fgPrimary,
                wordBreak: 'break-all',
                minHeight: '18px',
              }}>
                {'\u2014'}
              </div>
            </div>

            {/* Rename button — matches OMNI-VIEW .btnren */}
            <button
              disabled
              style={{
                margin: '0 10px 8px',
                padding: '8px',
                background: tokens.color.accentPrimary,
                color: '#fff',
                border: 'none',
                borderRadius: '5px',
                cursor: 'default',
                fontSize: '11px',
                fontWeight: 700,
                letterSpacing: '1px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '6px',
                opacity: 0.35,
                width: 'calc(100% - 20px)',
              }}
            >
              RENAME FILE
            </button>

            {/* Rename History — matches OMNI-VIEW #rHist */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Rename History</div>
              <div style={{
                maxHeight: '120px',
                overflowY: 'auto',
                fontSize: '10px',
                color: tokens.color.fgMuted,
              }}>
                No rename history
              </div>
            </div>
          </div>
        )}

        {/* ═══ TOOLBOX TAB ═══ */}
        {activeTab === 'toolbox' && (
          <div>
            {/* Redline Tools Grid — matches OMNI-VIEW .tcgrid */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Redline Tools</div>
              <div style={{
                display: 'grid',
                gridTemplateColumns: '1fr 1fr 1fr',
                gap: '3px',
              }}>
                {REDLINE_TOOLS.map((tool) => {
                  const isActive = activeTool === tool.id;
                  return (
                    <button
                      key={tool.id}
                      onClick={() => onToolSelect?.(tool.id)}
                      style={{
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '2px',
                        padding: '6px 2px',
                        background: isActive ? `${tokens.color.accentPrimary}12` : tokens.color.bgElevated,
                        border: `1px solid ${isActive ? `${tokens.color.accentPrimary}59` : tokens.color.border}`,
                        borderRadius: '4px',
                        cursor: 'pointer',
                        color: isActive ? tokens.color.accentPrimary : tokens.color.fgSecondary,
                        transition: 'all 0.12s',
                      }}
                      onMouseEnter={(e) => {
                        if (!isActive) {
                          e.currentTarget.style.background = tokens.color.bgHover;
                          e.currentTarget.style.color = tokens.color.fgPrimary;
                        }
                      }}
                      onMouseLeave={(e) => {
                        if (!isActive) {
                          e.currentTarget.style.background = tokens.color.bgElevated;
                          e.currentTarget.style.color = tokens.color.fgSecondary;
                        }
                      }}
                    >
                      <span style={{ fontSize: '18px' }}>{tool.icon}</span>
                      <span style={{ fontSize: '7px', letterSpacing: '0.3px', fontWeight: 600 }}>{tool.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* Document Ops — matches OMNI-VIEW .docops */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Document Ops</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '4px' }}>
                {[
                  { icon: '\u21BB', label: 'Rotate 90\u00B0 CW' },
                  { icon: '\u21BA', label: 'Rotate 90\u00B0 CCW' },
                  { icon: '\u2913', label: 'Extract Page' },
                  { icon: '\u2261', label: 'Flatten Markups' },
                  { icon: '\u{1F50D}', label: 'OCR Page' },
                  { icon: '\u{1F4D0}', label: 'Calibrate Scale' },
                  { icon: '\u{1F4CA}', label: 'Link Excel' },
                ].map((op) => (
                  <button
                    key={op.label}
                    style={docOpsBtnStyle}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = tokens.color.bgHover;
                      e.currentTarget.style.color = tokens.color.fgPrimary;
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = tokens.color.bgElevated;
                      e.currentTarget.style.color = tokens.color.fgSecondary;
                    }}
                  >
                    <span>{op.icon}</span>
                    {op.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Count — matches OMNI-VIEW count section */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Count</div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '20px', fontWeight: 800, color: '#f0a030' }}>0</span>
                <button
                  style={{
                    ...docOpsBtnStyle,
                    width: 'auto',
                    padding: '2px 8px',
                    fontSize: '10px',
                  }}
                  title="Reset Count"
                >
                  {'\u21BA'}
                </button>
              </div>
            </div>

            {/* Measurements — matches OMNI-VIEW #measList */}
            <div style={sectionStyle}>
              <div style={sectionLabelStyle}>Measurements</div>
              <div style={{ maxHeight: '100px', overflowY: 'auto', fontSize: '10px', color: tokens.color.fgMuted }}>
                None
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
