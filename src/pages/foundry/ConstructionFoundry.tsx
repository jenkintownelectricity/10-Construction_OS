/**
 * Construction OS — Construction Foundry Shell
 * Wave C1 — Shell only. No minting behavior. Mint button disabled.
 */

import { useState } from 'react';
import { tokens } from '../../ui/theme/tokens';

const t = tokens;

const FOUNDRY_STEPS = [
  { id: 1, label: 'Intent Brief', description: 'Define the purpose and context of the new primitive.' },
  { id: 2, label: 'Primitive Type', description: 'Select the type of construction primitive to create.' },
  { id: 3, label: 'Governance Density', description: 'Set governance requirements and compliance level.' },
  { id: 4, label: 'Boundary Definition', description: 'Define scope boundaries and constraint parameters.' },
  { id: 5, label: 'Doctrine Preview', description: 'Preview governing doctrine rules that will apply.' },
  { id: 6, label: 'Contract Preview', description: 'Review the primitive contract and interface definition.' },
  { id: 7, label: 'Sentinel Preview', description: 'Preview sentinel validation rules and guards.' },
  { id: 8, label: 'Mint Primitive', description: 'Execute mint operation to register the primitive.' },
];

const PRIMITIVE_TYPES = [
  'Assembly',
  'Material',
  'Specification',
  'Chemistry',
  'Scope',
  'Pattern',
];

export function ConstructionFoundry() {
  const [activeStep, setActiveStep] = useState(1);
  const [selectedType, setSelectedType] = useState<string | null>(null);

  return (
    <div>
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: t.font.sizeXl, fontWeight: Number(t.font.weightBold), margin: 0 }}>Construction Foundry</h1>
        <p style={{ fontSize: t.font.sizeSm, color: t.color.fgSecondary, marginTop: '4px' }}>
          Primitive creation workflow — governed, validated, deterministic
        </p>
      </div>

      {/* Wave C1 Banner */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '10px',
          padding: '10px 16px',
          background: t.color.bgElevated,
          border: `1px solid ${t.color.warning}33`,
          borderRadius: t.radius.md,
          marginBottom: '24px',
          fontSize: t.font.sizeXs,
        }}
      >
        <span style={{ width: 8, height: 8, borderRadius: '50%', background: t.color.warning, display: 'inline-block' }} />
        <span style={{ color: t.color.warning, fontWeight: Number(t.font.weightSemibold) }}>Wave C1 — Shell Only</span>
        <span style={{ color: t.color.fgMuted }}>Minting operations are not connected in this wave. Visual workflow preview only.</span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '240px 1fr', gap: '16px' }}>
        {/* Steps sidebar */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '12px',
          }}
        >
          {FOUNDRY_STEPS.map((step) => {
            const isActive = activeStep === step.id;
            const isMint = step.id === 8;
            return (
              <button
                key={step.id}
                onClick={() => !isMint && setActiveStep(step.id)}
                disabled={isMint}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  width: '100%',
                  padding: '10px 12px',
                  marginBottom: '4px',
                  border: 'none',
                  borderRadius: t.radius.sm,
                  cursor: isMint ? 'not-allowed' : 'pointer',
                  background: isActive ? t.color.accentMuted : 'transparent',
                  color: isMint ? t.color.fgMuted : isActive ? '#ffffff' : t.color.fgSecondary,
                  fontSize: t.font.sizeXs,
                  fontWeight: isActive ? Number(t.font.weightSemibold) : Number(t.font.weightMedium),
                  fontFamily: t.font.family,
                  textAlign: 'left',
                  opacity: isMint ? 0.5 : 1,
                }}
              >
                <span
                  style={{
                    width: 22,
                    height: 22,
                    borderRadius: '50%',
                    background: isActive ? t.color.accentPrimary : t.color.bgElevated,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: '11px',
                    fontWeight: Number(t.font.weightBold),
                    flexShrink: 0,
                    color: isActive ? '#fff' : t.color.fgMuted,
                  }}
                >
                  {step.id}
                </span>
                <span>{step.label}</span>
              </button>
            );
          })}
        </div>

        {/* Step content */}
        <div
          style={{
            background: t.color.bgSurface,
            border: `1px solid ${t.color.border}`,
            borderRadius: t.radius.md,
            padding: '24px',
          }}
        >
          <h2 style={{ fontSize: t.font.sizeMd, fontWeight: Number(t.font.weightSemibold), margin: '0 0 8px 0' }}>
            Step {activeStep}: {FOUNDRY_STEPS[activeStep - 1].label}
          </h2>
          <p style={{ fontSize: t.font.sizeXs, color: t.color.fgSecondary, marginBottom: '20px' }}>
            {FOUNDRY_STEPS[activeStep - 1].description}
          </p>

          {/* Step 2: Primitive Type Selection */}
          {activeStep === 2 && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '10px' }}>
              {PRIMITIVE_TYPES.map((type) => (
                <button
                  key={type}
                  onClick={() => setSelectedType(type)}
                  style={{
                    padding: '16px',
                    background: selectedType === type ? t.color.accentMuted : t.color.bgElevated,
                    border: `1px solid ${selectedType === type ? t.color.accentPrimary : t.color.border}`,
                    borderRadius: t.radius.md,
                    cursor: 'pointer',
                    color: selectedType === type ? '#ffffff' : t.color.fgSecondary,
                    fontSize: t.font.sizeSm,
                    fontWeight: Number(t.font.weightMedium),
                    fontFamily: t.font.family,
                  }}
                >
                  {type}
                </button>
              ))}
            </div>
          )}

          {/* Default step content */}
          {activeStep !== 2 && activeStep !== 8 && (
            <div
              style={{
                padding: '40px',
                border: `1px dashed ${t.color.border}`,
                borderRadius: t.radius.md,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: t.color.fgMuted,
                fontSize: t.font.sizeXs,
              }}
            >
              Configuration panel — Wave C1 placeholder
            </div>
          )}

          {/* Mint button (always disabled) */}
          <div style={{ marginTop: '24px', display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
            {activeStep > 1 && (
              <button
                onClick={() => setActiveStep(activeStep - 1)}
                style={{
                  padding: '8px 20px',
                  background: t.color.bgElevated,
                  border: `1px solid ${t.color.border}`,
                  borderRadius: t.radius.md,
                  color: t.color.fgSecondary,
                  cursor: 'pointer',
                  fontSize: t.font.sizeXs,
                  fontFamily: t.font.family,
                }}
              >
                Back
              </button>
            )}
            {activeStep < 8 ? (
              <button
                onClick={() => setActiveStep(activeStep + 1)}
                style={{
                  padding: '8px 20px',
                  background: t.color.accentPrimary,
                  border: 'none',
                  borderRadius: t.radius.md,
                  color: '#ffffff',
                  cursor: 'pointer',
                  fontSize: t.font.sizeXs,
                  fontWeight: Number(t.font.weightSemibold),
                  fontFamily: t.font.family,
                }}
              >
                Next
              </button>
            ) : (
              <button
                disabled
                style={{
                  padding: '8px 20px',
                  background: t.color.bgElevated,
                  border: `1px solid ${t.color.border}`,
                  borderRadius: t.radius.md,
                  color: t.color.fgMuted,
                  cursor: 'not-allowed',
                  fontSize: t.font.sizeXs,
                  fontWeight: Number(t.font.weightSemibold),
                  fontFamily: t.font.family,
                  opacity: 0.5,
                }}
              >
                Mint Primitive (Disabled — Wave C1)
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
