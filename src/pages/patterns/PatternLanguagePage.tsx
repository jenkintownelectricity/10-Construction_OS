/**
 * Construction OS — Pattern Language Page
 * Wave C1 — Deterministic pattern data. No cross-repo load.
 */

import { useState } from 'react';
import { tokens } from '../../ui/theme/tokens';
import { MOCK_PATTERNS, type MockPattern } from '../../mock/primitives/mockPatterns';

const t = tokens;

const categoryColors: Record<string, string> = {
  Assembly: t.color.accentPrimary,
  Performance: t.color.success,
  'Water Management': '#06b6d4',
  Moisture: t.color.compare,
  Detail: t.color.warning,
};

export function PatternLanguagePage() {
  const [selectedPattern, setSelectedPattern] = useState<MockPattern | null>(null);

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Pattern Language</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Construction pattern intelligence — Alexander Engine reference
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '280px 1fr 300px', gap: '16px' }}>
        {/* Pattern List */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '12px',
          }}
        >
          <h3 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: '0 0 12px 0', padding: '0 4px' }}>Pattern List</h3>
          {MOCK_PATTERNS.map((pat) => {
            const isSelected = selectedPattern?.id === pat.id;
            return (
              <button
                key={pat.id}
                onClick={() => setSelectedPattern(pat)}
                style={{
                  display: 'block',
                  width: '100%',
                  padding: '10px 10px',
                  marginBottom: '4px',
                  border: 'none',
                  borderRadius: t.radius.sm,
                  cursor: 'pointer',
                  background: isSelected ? t.color.accentMuted : 'transparent',
                  textAlign: 'left',
                  fontFamily: t.font.family,
                }}
              >
                <div style={{ fontSize: t.font.sizeXs, color: isSelected ? '#fff' : t.color.fgPrimary, fontWeight: Number(t.font.weightMedium) }}>
                  {pat.name}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginTop: '4px' }}>
                  <span
                    style={{
                      fontSize: '10px',
                      padding: '1px 6px',
                      borderRadius: '8px',
                      background: (categoryColors[pat.category] || t.color.fgMuted) + '22',
                      color: categoryColors[pat.category] || t.color.fgMuted,
                    }}
                  >
                    {pat.category}
                  </span>
                  <span style={{ fontSize: '10px', color: t.color.fgMuted }}>
                    {(pat.confidence * 100).toFixed(0)}%
                  </span>
                </div>
              </button>
            );
          })}
        </div>

        {/* Pattern Graph */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '16px',
          }}
        >
          <h3 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: '0 0 12px 0' }}>Pattern Graph</h3>
          <svg
            width="100%"
            height="460"
            viewBox="0 0 600 460"
            style={{ display: 'block' }}
          >
            {/* Edges */}
            {MOCK_PATTERNS.flatMap((pat) =>
              pat.relatedPatterns.map((relId) => {
                const target = MOCK_PATTERNS.find((p) => p.id === relId);
                if (!target) return null;
                return (
                  <line
                    key={`${pat.id}-${relId}`}
                    x1={pat.x}
                    y1={pat.y}
                    x2={target.x}
                    y2={target.y}
                    stroke={t.color.border}
                    strokeWidth={1.5}
                    strokeOpacity={0.5}
                  />
                );
              })
            )}
            {/* Nodes */}
            {MOCK_PATTERNS.map((pat) => {
              const isSelected = selectedPattern?.id === pat.id;
              const color = categoryColors[pat.category] || t.color.fgMuted;
              return (
                <g
                  key={pat.id}
                  onClick={() => setSelectedPattern(pat)}
                  style={{ cursor: 'pointer' }}
                >
                  <circle
                    cx={pat.x}
                    cy={pat.y}
                    r={isSelected ? 22 : 18}
                    fill={t.color.bgElevated}
                    stroke={isSelected ? color : t.color.border}
                    strokeWidth={isSelected ? 2.5 : 1.5}
                  />
                  <circle cx={pat.x} cy={pat.y} r={5} fill={color} />
                  <text
                    x={pat.x}
                    y={pat.y + 30}
                    textAnchor="middle"
                    fill={t.color.fgSecondary}
                    fontSize="10"
                    fontFamily={t.font.family}
                  >
                    {pat.name.length > 22 ? pat.name.substring(0, 20) + '\u2026' : pat.name}
                  </text>
                </g>
              );
            })}
          </svg>
        </div>

        {/* Pattern Detail */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '16px',
          }}
        >
          <h3 style={{ fontSize: t.font.sizeSm, fontWeight: Number(t.font.weightSemibold), margin: '0 0 12px 0' }}>Pattern Detail</h3>
          {selectedPattern ? (
            <div style={{ fontSize: t.font.sizeXs }}>
              <div style={{ fontWeight: Number(t.font.weightSemibold), color: t.color.fgPrimary, marginBottom: '8px', fontSize: t.font.sizeSm }}>
                {selectedPattern.name}
              </div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
                <span
                  style={{
                    padding: '2px 8px',
                    borderRadius: '10px',
                    background: (categoryColors[selectedPattern.category] || t.color.fgMuted) + '22',
                    color: categoryColors[selectedPattern.category] || t.color.fgMuted,
                    fontSize: '11px',
                  }}
                >
                  {selectedPattern.category}
                </span>
                <span style={{ color: t.color.fgMuted }}>Confidence: {(selectedPattern.confidence * 100).toFixed(0)}%</span>
              </div>
              <p style={{ color: t.color.fgSecondary, lineHeight: t.font.lineNormal, marginBottom: '16px' }}>
                {selectedPattern.description}
              </p>
              <div style={{ color: t.color.fgMuted, fontWeight: Number(t.font.weightMedium), marginBottom: '6px' }}>Related Patterns</div>
              {selectedPattern.relatedPatterns.map((relId) => {
                const rel = MOCK_PATTERNS.find((p) => p.id === relId);
                return rel ? (
                  <div
                    key={relId}
                    onClick={() => setSelectedPattern(rel)}
                    style={{
                      padding: '6px 8px',
                      marginBottom: '4px',
                      background: t.color.bgElevated,
                      borderRadius: t.radius.sm,
                      cursor: 'pointer',
                      color: t.color.fgSecondary,
                    }}
                  >
                    {rel.name}
                  </div>
                ) : null;
              })}
            </div>
          ) : (
            <p style={{ color: t.color.fgMuted, fontSize: t.font.sizeXs }}>Select a pattern to view details</p>
          )}
        </div>
      </div>
    </div>
  );
}
