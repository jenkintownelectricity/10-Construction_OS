/**
 * Assembly Builder Panel — Bounded UI Vertical Slice
 *
 * Creates canonical assembly drafts from existing accessible data and
 * passes them into a preview/test compiler adapter.
 *
 * Surfaces:
 *   1. Assembly type selection
 *   2. Control-layer assignment selection
 *   3. Interface-zone selection
 *   4. Layer/component stack editing
 *   5. Canonical assembly draft generation
 *   6. Fail-closed validation with field-level diagnostics
 *   7. Source evidence / lineage display
 *   8. Preview/test output
 *
 * Governance: VKGL04R — Ring 1 Outcome 1: "Assembly Builder UI surface"
 */

import { useCallback, useState } from 'react';
import { tokens } from '../theme/tokens';
import { CONTROL_LAYERS } from './controlLayerData';
import { INTERFACE_ZONES } from './interfaceZoneData';
import { TPO_ROOF_ASSEMBLY_EXAMPLE, TPO_ROOF_LINEAGE, FIRE_RATED_ASSEMBLY_EXAMPLE, FIRE_RATED_LINEAGE } from './assemblyExamples';
import { getSampleRoofingDraft } from './roofingSourceAdapter';
import { getSampleFireproofingDraft, AVAILABLE_ISOVER_SEQUENCES } from './fireproofingSourceAdapter';
import { validateAssemblyDraft, formStateToDraft } from './assemblyDraftValidator';
import { runPreviewTest } from './previewTestAdapter';
import type {
  AssemblyDraftFormState,
  AssemblyType,
  ControlLayerId,
  InterfaceZoneId,
  AttachmentMethod,
  ContinuityStatus,
  ExposureFlag,
  ExposureClass,
  GeometryContext,
  WarrantyPosture,
  CanonicalAssemblyDraft,
  ValidationOutcome,
  PreviewTestResult,
  SourceLineage,
  AssemblyLayer,
} from './types';

// ─── Sub-tab type ───────────────────────────────────────────────────────

type BuilderTab = 'assembly' | 'layers' | 'validation' | 'preview' | 'source';

// ─── Empty form state ───────────────────────────────────────────────────

function emptyForm(): AssemblyDraftFormState {
  return {
    system_id: '',
    title: '',
    assembly_type: 'roof_assembly',
    status: 'draft',
    layers: [],
    control_layer_continuity: {},
    interface_zones: [],
    climate_context: { climate_zone: '', exposure_flags: [], exposure_class: 'moderate' },
    geometry_context: { geometry_contexts: [], notes: '' },
    tested_assembly_refs: [],
    standards_refs: [],
    warranty_posture: 'unknown',
    notes: '',
  };
}

function draftToForm(draft: CanonicalAssemblyDraft): AssemblyDraftFormState {
  return {
    system_id: draft.system_id,
    title: draft.title,
    assembly_type: draft.assembly_type,
    status: draft.status,
    layers: draft.layers ? [...draft.layers] : [],
    control_layer_continuity: draft.control_layer_continuity ? { ...draft.control_layer_continuity } : {},
    interface_zones: draft.interface_zones ? [...draft.interface_zones] : [],
    climate_context: {
      climate_zone: draft.climate_context?.climate_zone ?? '',
      exposure_flags: draft.climate_context?.exposure_flags ? [...draft.climate_context.exposure_flags] : [],
      exposure_class: draft.climate_context?.exposure_class ?? 'moderate',
    },
    geometry_context: {
      geometry_contexts: draft.geometry_context?.geometry_contexts ? [...draft.geometry_context.geometry_contexts] : [],
      notes: draft.geometry_context?.notes ?? '',
    },
    tested_assembly_refs: draft.tested_assembly_refs ? [...draft.tested_assembly_refs] : [],
    standards_refs: draft.standards_refs ? [...draft.standards_refs] : [],
    warranty_posture: draft.warranty_posture ?? 'unknown',
    notes: draft.notes ?? '',
  };
}

// ─── Shared styles ──────────────────────────────────────────────────────

const sectionStyle: React.CSSProperties = {
  marginBottom: tokens.space.lg,
  padding: tokens.space.md,
  background: tokens.color.bgBase,
  borderRadius: tokens.radius.md,
  border: `1px solid ${tokens.color.border}`,
};

const labelStyle: React.CSSProperties = {
  display: 'block',
  fontSize: tokens.font.sizeXs,
  color: tokens.color.fgMuted,
  marginBottom: tokens.space.xs,
  fontWeight: tokens.font.weightMedium,
  textTransform: 'uppercase' as const,
  letterSpacing: '0.04em',
};

const inputStyle: React.CSSProperties = {
  width: '100%',
  padding: `${tokens.space.sm} ${tokens.space.md}`,
  background: tokens.color.bgSurface,
  border: `1px solid ${tokens.color.border}`,
  borderRadius: tokens.radius.sm,
  color: tokens.color.fgPrimary,
  fontSize: tokens.font.sizeSm,
  fontFamily: tokens.font.family,
  outline: 'none',
  boxSizing: 'border-box' as const,
};

const selectStyle: React.CSSProperties = {
  ...inputStyle,
  cursor: 'pointer',
};

const btnPrimary: React.CSSProperties = {
  padding: `${tokens.space.sm} ${tokens.space.lg}`,
  background: tokens.color.accentPrimary,
  color: '#fff',
  border: 'none',
  borderRadius: tokens.radius.sm,
  cursor: 'pointer',
  fontSize: tokens.font.sizeSm,
  fontFamily: tokens.font.family,
  fontWeight: tokens.font.weightMedium,
};

const btnSecondary: React.CSSProperties = {
  ...btnPrimary,
  background: tokens.color.bgElevated,
  color: tokens.color.fgSecondary,
  border: `1px solid ${tokens.color.border}`,
};

const chipStyle = (active: boolean): React.CSSProperties => ({
  display: 'inline-block',
  padding: `${tokens.space.xs} ${tokens.space.sm}`,
  borderRadius: tokens.radius.sm,
  fontSize: tokens.font.sizeXs,
  fontFamily: tokens.font.family,
  cursor: 'pointer',
  border: `1px solid ${active ? tokens.color.accentPrimary : tokens.color.border}`,
  background: active ? tokens.color.accentMuted : tokens.color.bgSurface,
  color: active ? tokens.color.accentPrimary : tokens.color.fgSecondary,
  transition: `all ${tokens.transition.fast}`,
  marginRight: tokens.space.xs,
  marginBottom: tokens.space.xs,
});

// ─── Component ──────────────────────────────────────────────────────────

export function AssemblyBuilderPanel() {
  const [activeTab, setActiveTab] = useState<BuilderTab>('assembly');
  const [form, setForm] = useState<AssemblyDraftFormState>(emptyForm());
  const [validation, setValidation] = useState<ValidationOutcome | null>(null);
  const [previewResult, setPreviewResult] = useState<PreviewTestResult | null>(null);
  const [lineage, setLineage] = useState<SourceLineage | null>(null);
  const [selectedSource, setSelectedSource] = useState<'roofing' | 'fireproofing' | null>(null);

  // ─── Hydrate from source ─────────────────────────────────────────────

  const hydrateRoofing = useCallback(() => {
    const { draft, lineage: lin } = getSampleRoofingDraft();
    setForm(draftToForm(draft));
    setLineage(lin);
    setSelectedSource('roofing');
    setValidation(null);
    setPreviewResult(null);
  }, []);

  const hydrateFireproofing = useCallback(() => {
    const { draft, lineage: lin } = getSampleFireproofingDraft();
    setForm(draftToForm(draft));
    setLineage(lin);
    setSelectedSource('fireproofing');
    setValidation(null);
    setPreviewResult(null);
  }, []);

  const loadExample = useCallback(() => {
    setForm(draftToForm(TPO_ROOF_ASSEMBLY_EXAMPLE));
    setLineage(TPO_ROOF_LINEAGE);
    setSelectedSource('roofing');
    setValidation(null);
    setPreviewResult(null);
  }, []);

  const clearForm = useCallback(() => {
    setForm(emptyForm());
    setLineage(null);
    setSelectedSource(null);
    setValidation(null);
    setPreviewResult(null);
  }, []);

  // ─── Validate ────────────────────────────────────────────────────────

  const handleValidate = useCallback(() => {
    const draft = formStateToDraft(form);
    const result = validateAssemblyDraft(draft);
    setValidation(result);
    setActiveTab('validation');
  }, [form]);

  // ─── Preview/Test ────────────────────────────────────────────────────

  const handlePreview = useCallback(() => {
    const draft = formStateToDraft(form);
    const result = runPreviewTest(draft);
    setPreviewResult(result);
    setActiveTab('preview');
  }, [form]);

  // ─── Form updates ───────────────────────────────────────────────────

  const updateField = useCallback(<K extends keyof AssemblyDraftFormState>(key: K, value: AssemblyDraftFormState[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  }, []);

  const toggleInterfaceZone = useCallback((zoneId: InterfaceZoneId) => {
    setForm((prev) => ({
      ...prev,
      interface_zones: prev.interface_zones.includes(zoneId)
        ? prev.interface_zones.filter((z) => z !== zoneId)
        : [...prev.interface_zones, zoneId],
    }));
  }, []);

  const updateLayer = useCallback((index: number, updates: Partial<AssemblyLayer>) => {
    setForm((prev) => ({
      ...prev,
      layers: prev.layers.map((l, i) => (i === index ? { ...l, ...updates } : l)),
    }));
  }, []);

  const addLayer = useCallback(() => {
    setForm((prev) => {
      const nextPos = prev.layers.length + 1;
      return {
        ...prev,
        layers: [
          ...prev.layers,
          {
            layer_id: `LYR-${String(nextPos).padStart(3, '0')}`,
            position: nextPos,
            control_layer_id: 'bulk_water_control' as ControlLayerId,
            material_ref: '',
          },
        ],
      };
    });
  }, []);

  const removeLayer = useCallback((index: number) => {
    setForm((prev) => ({
      ...prev,
      layers: prev.layers
        .filter((_, i) => i !== index)
        .map((l, i) => ({ ...l, position: i + 1 })),
    }));
  }, []);

  const updateContinuity = useCallback((layerId: string, status: ContinuityStatus) => {
    setForm((prev) => ({
      ...prev,
      control_layer_continuity: { ...prev.control_layer_continuity, [layerId]: status },
    }));
  }, []);

  // ─── Tab bar ─────────────────────────────────────────────────────────

  const tabs: { key: BuilderTab; label: string }[] = [
    { key: 'assembly', label: 'Assembly' },
    { key: 'layers', label: 'Layers' },
    { key: 'validation', label: 'Validation' },
    { key: 'preview', label: 'Preview' },
    { key: 'source', label: 'Source' },
  ];

  const draft = formStateToDraft(form);
  const errorCount = validation?.diagnostics.filter((d) => d.severity === 'error').length ?? 0;

  return (
    <div style={{ height: '100%', display: 'flex', flexDirection: 'column', background: tokens.color.bgSurface, color: tokens.color.fgPrimary, fontFamily: tokens.font.family }}>
      {/* Header */}
      <div style={{
        padding: `${tokens.space.sm} ${tokens.space.md}`,
        background: tokens.color.bgElevated,
        borderBottom: `1px solid ${tokens.color.border}`,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        minHeight: '40px',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: tokens.space.sm }}>
          <span style={{
            fontSize: tokens.font.sizeMd,
            fontWeight: tokens.font.weightSemibold,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
          }}>
            ASSEMBLY BUILDER
          </span>
          <span style={{
            fontSize: tokens.font.sizeXs,
            color: tokens.color.draft,
            padding: '2px 8px',
            borderRadius: tokens.radius.sm,
            background: `${tokens.color.draft}15`,
          }}>
            draft
          </span>
        </div>
        <div style={{ display: 'flex', gap: tokens.space.sm }}>
          <button onClick={hydrateRoofing} style={btnSecondary}>Hydrate Roofing</button>
          <button onClick={hydrateFireproofing} style={btnSecondary}>Hydrate Fireproofing</button>
          <button onClick={loadExample} style={btnSecondary}>Load Example</button>
          <button onClick={clearForm} style={{ ...btnSecondary, color: tokens.color.error, borderColor: tokens.color.error }}>Clear</button>
        </div>
      </div>

      {/* Tab Bar */}
      <div style={{
        display: 'flex',
        gap: '1px',
        background: tokens.color.border,
      }}>
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            style={{
              flex: 1,
              padding: `${tokens.space.sm} ${tokens.space.sm}`,
              background: activeTab === tab.key ? tokens.color.bgActive : tokens.color.bgElevated,
              color: activeTab === tab.key ? tokens.color.fgPrimary : tokens.color.fgSecondary,
              border: 'none',
              cursor: 'pointer',
              fontSize: tokens.font.sizeSm,
              fontWeight: activeTab === tab.key ? tokens.font.weightSemibold : tokens.font.weightNormal,
              fontFamily: tokens.font.family,
              transition: `all ${tokens.transition.fast}`,
            }}
          >
            {tab.label}
            {tab.key === 'validation' && errorCount > 0 && (
              <span style={{
                marginLeft: tokens.space.xs,
                background: tokens.color.error,
                color: '#fff',
                padding: '1px 6px',
                borderRadius: '8px',
                fontSize: '0.7rem',
                fontWeight: tokens.font.weightBold,
              }}>
                {errorCount}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflow: 'auto', padding: tokens.space.md }}>

        {/* ─── ASSEMBLY TAB ──────────────────────────────────────────── */}
        {activeTab === 'assembly' && (
          <div>
            {/* System ID + Title */}
            <div style={sectionStyle}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: tokens.space.md }}>
                <div>
                  <label style={labelStyle}>System ID</label>
                  <input
                    style={inputStyle}
                    value={form.system_id}
                    onChange={(e) => updateField('system_id', e.target.value)}
                    placeholder="ASSY-ROOF-001"
                  />
                </div>
                <div>
                  <label style={labelStyle}>Title</label>
                  <input
                    style={inputStyle}
                    value={form.title}
                    onChange={(e) => updateField('title', e.target.value)}
                    placeholder="Assembly title"
                  />
                </div>
              </div>
            </div>

            {/* Assembly Type */}
            <div style={sectionStyle}>
              <label style={labelStyle}>Assembly Type</label>
              <select
                style={selectStyle}
                value={form.assembly_type}
                onChange={(e) => updateField('assembly_type', e.target.value as AssemblyType)}
              >
                <option value="roof_assembly">Roof Assembly</option>
                <option value="wall_assembly">Wall Assembly</option>
                <option value="below_grade_assembly">Below Grade Assembly</option>
                <option value="plaza_assembly">Plaza Assembly</option>
                <option value="vegetated_assembly">Vegetated Assembly</option>
                <option value="hybrid_assembly">Hybrid Assembly</option>
              </select>
            </div>

            {/* Interface Zones */}
            <div style={sectionStyle}>
              <label style={labelStyle}>Interface Zones</label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: tokens.space.xs }}>
                {INTERFACE_ZONES.map((zone) => (
                  <span
                    key={zone.id}
                    onClick={() => toggleInterfaceZone(zone.id)}
                    style={chipStyle(form.interface_zones.includes(zone.id))}
                    title={zone.description}
                  >
                    {zone.name}
                  </span>
                ))}
              </div>
            </div>

            {/* Control Layer Continuity */}
            <div style={sectionStyle}>
              <label style={labelStyle}>Control Layer Continuity</label>
              {CONTROL_LAYERS.map((cl) => {
                const value = form.control_layer_continuity[cl.id];
                if (!value && !form.layers.some((l) => l.control_layer_id === cl.id)) return null;
                return (
                  <div key={cl.id} style={{ display: 'flex', alignItems: 'center', gap: tokens.space.md, marginBottom: tokens.space.sm }}>
                    <span style={{ flex: 1, fontSize: tokens.font.sizeSm, color: tokens.color.fgSecondary }}>{cl.name}</span>
                    <select
                      style={{ ...selectStyle, width: '180px' }}
                      value={value ?? 'continuous'}
                      onChange={(e) => updateContinuity(cl.id, e.target.value as ContinuityStatus)}
                    >
                      <option value="continuous">Continuous</option>
                      <option value="interrupted">Interrupted</option>
                      <option value="terminated">Terminated</option>
                      <option value="transitioned">Transitioned</option>
                    </select>
                  </div>
                );
              })}
              {Object.keys(form.control_layer_continuity).length === 0 && form.layers.length === 0 && (
                <div style={{ fontSize: tokens.font.sizeSm, color: tokens.color.fgMuted }}>
                  Add layers to configure control layer continuity.
                </div>
              )}
            </div>

            {/* Climate + Geometry + Warranty */}
            <div style={sectionStyle}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: tokens.space.md }}>
                <div>
                  <label style={labelStyle}>Climate Zone</label>
                  <input
                    style={inputStyle}
                    value={form.climate_context.climate_zone}
                    onChange={(e) => updateField('climate_context', { ...form.climate_context, climate_zone: e.target.value })}
                    placeholder="5A"
                  />
                </div>
                <div>
                  <label style={labelStyle}>Exposure Class</label>
                  <select
                    style={selectStyle}
                    value={form.climate_context.exposure_class}
                    onChange={(e) => updateField('climate_context', { ...form.climate_context, exposure_class: e.target.value as ExposureClass })}
                  >
                    <option value="sheltered">Sheltered</option>
                    <option value="moderate">Moderate</option>
                    <option value="severe">Severe</option>
                    <option value="extreme">Extreme</option>
                  </select>
                </div>
                <div>
                  <label style={labelStyle}>Warranty Posture</label>
                  <select
                    style={selectStyle}
                    value={form.warranty_posture}
                    onChange={(e) => updateField('warranty_posture', e.target.value as WarrantyPosture)}
                  >
                    <option value="manufacturer_standard">Manufacturer Standard</option>
                    <option value="manufacturer_extended">Manufacturer Extended</option>
                    <option value="system_warranty">System Warranty</option>
                    <option value="no_dollar_limit">No Dollar Limit</option>
                    <option value="prorated">Prorated</option>
                    <option value="none">None</option>
                    <option value="unknown">Unknown</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Notes */}
            <div style={sectionStyle}>
              <label style={labelStyle}>Notes</label>
              <textarea
                style={{ ...inputStyle, minHeight: '60px', resize: 'vertical' }}
                value={form.notes}
                onChange={(e) => updateField('notes', e.target.value)}
                placeholder="Assembly notes..."
              />
            </div>

            {/* Action bar */}
            <div style={{ display: 'flex', gap: tokens.space.sm, marginTop: tokens.space.md }}>
              <button onClick={handleValidate} style={btnPrimary}>Validate Draft</button>
              <button onClick={handlePreview} style={btnPrimary}>Run Preview/Test</button>
            </div>
          </div>
        )}

        {/* ─── LAYERS TAB ────────────────────────────────────────────── */}
        {activeTab === 'layers' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: tokens.space.md }}>
              <span style={{ fontSize: tokens.font.sizeMd, fontWeight: tokens.font.weightSemibold }}>
                Layer Stack ({form.layers.length} layers)
              </span>
              <button onClick={addLayer} style={btnPrimary}>+ Add Layer</button>
            </div>

            {form.layers.length === 0 && (
              <div style={{
                padding: tokens.space.xl,
                textAlign: 'center',
                color: tokens.color.fgMuted,
                border: `1px dashed ${tokens.color.border}`,
                borderRadius: tokens.radius.md,
              }}>
                No layers defined. Add layers or hydrate from a source.
              </div>
            )}

            {form.layers.map((layer, i) => (
              <div key={layer.layer_id} style={{
                ...sectionStyle,
                borderLeft: `3px solid ${tokens.color.accentPrimary}`,
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: tokens.space.sm }}>
                  <span style={{ fontSize: tokens.font.sizeSm, fontWeight: tokens.font.weightSemibold, color: tokens.color.accentPrimary }}>
                    Position {layer.position} — {layer.layer_id}
                  </span>
                  <button
                    onClick={() => removeLayer(i)}
                    style={{ ...btnSecondary, color: tokens.color.error, borderColor: tokens.color.error, padding: `${tokens.space.xs} ${tokens.space.sm}` }}
                  >
                    Remove
                  </button>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: tokens.space.md }}>
                  <div>
                    <label style={labelStyle}>Control Layer</label>
                    <select
                      style={selectStyle}
                      value={layer.control_layer_id}
                      onChange={(e) => updateLayer(i, { control_layer_id: e.target.value as ControlLayerId })}
                    >
                      {CONTROL_LAYERS.map((cl) => (
                        <option key={cl.id} value={cl.id}>{cl.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label style={labelStyle}>Attachment Method</label>
                    <select
                      style={selectStyle}
                      value={layer.attachment_method ?? ''}
                      onChange={(e) => updateLayer(i, { attachment_method: (e.target.value || undefined) as AttachmentMethod | undefined })}
                    >
                      <option value="">— select —</option>
                      <option value="mechanically_attached">Mechanically Attached</option>
                      <option value="fully_adhered">Fully Adhered</option>
                      <option value="ballasted">Ballasted</option>
                      <option value="torch_applied">Torch Applied</option>
                      <option value="hot_mopped">Hot Mopped</option>
                      <option value="cold_applied">Cold Applied</option>
                      <option value="spray_applied">Spray Applied</option>
                      <option value="self_adhered">Self-Adhered</option>
                      <option value="loose_laid">Loose Laid</option>
                      <option value="standing_seam">Standing Seam</option>
                      <option value="lapped">Lapped</option>
                      <option value="welded">Welded</option>
                    </select>
                  </div>
                  <div>
                    <label style={labelStyle}>Material Ref</label>
                    <input
                      style={inputStyle}
                      value={layer.material_ref}
                      onChange={(e) => updateLayer(i, { material_ref: e.target.value })}
                      placeholder="MATL-XXX-001"
                    />
                  </div>
                  <div>
                    <label style={labelStyle}>Thickness</label>
                    <input
                      style={inputStyle}
                      value={layer.thickness ?? ''}
                      onChange={(e) => updateLayer(i, { thickness: e.target.value || undefined })}
                      placeholder="e.g. 60 mil, 3 inches"
                    />
                  </div>
                </div>
                {layer.notes && (
                  <div style={{ marginTop: tokens.space.sm, fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted, fontStyle: 'italic' }}>
                    {layer.notes}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}

        {/* ─── VALIDATION TAB ────────────────────────────────────────── */}
        {activeTab === 'validation' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: tokens.space.md }}>
              <span style={{ fontSize: tokens.font.sizeMd, fontWeight: tokens.font.weightSemibold }}>Validation Diagnostics</span>
              <button onClick={handleValidate} style={btnPrimary}>Re-validate</button>
            </div>

            {!validation && (
              <div style={{
                padding: tokens.space.xl,
                textAlign: 'center',
                color: tokens.color.fgMuted,
                border: `1px dashed ${tokens.color.border}`,
                borderRadius: tokens.radius.md,
              }}>
                No validation run yet. Click "Validate Draft" to check against Assembly Kernel schema.
              </div>
            )}

            {validation && (
              <>
                {/* Status badge */}
                <div style={{
                  display: 'inline-block',
                  padding: `${tokens.space.sm} ${tokens.space.lg}`,
                  borderRadius: tokens.radius.sm,
                  background: validation.valid ? `${tokens.color.success}20` : `${tokens.color.error}20`,
                  color: validation.valid ? tokens.color.success : tokens.color.error,
                  fontSize: tokens.font.sizeSm,
                  fontWeight: tokens.font.weightBold,
                  marginBottom: tokens.space.md,
                }}>
                  {validation.valid ? 'VALID — PASS' : 'INVALID — FAIL (CLOSED)'}
                </div>

                {/* Diagnostics list */}
                {validation.diagnostics.length > 0 && (
                  <div>
                    {validation.diagnostics.map((d, i) => (
                      <div key={i} style={{
                        padding: tokens.space.sm,
                        marginBottom: tokens.space.sm,
                        background: tokens.color.bgBase,
                        borderRadius: tokens.radius.sm,
                        borderLeft: `3px solid ${d.severity === 'error' ? tokens.color.error : tokens.color.warning}`,
                        fontSize: tokens.font.sizeSm,
                        lineHeight: tokens.font.lineNormal,
                      }}>
                        <div style={{ display: 'flex', gap: tokens.space.sm, alignItems: 'baseline' }}>
                          <span style={{
                            fontWeight: tokens.font.weightBold,
                            color: d.severity === 'error' ? tokens.color.error : tokens.color.warning,
                            textTransform: 'uppercase',
                            fontSize: tokens.font.sizeXs,
                          }}>
                            {d.severity}
                          </span>
                          <span style={{ fontFamily: tokens.font.familyMono, color: tokens.color.accentPrimary, fontSize: tokens.font.sizeXs }}>
                            {d.field}
                          </span>
                        </div>
                        <div style={{ color: tokens.color.fgPrimary, marginTop: tokens.space.xs }}>
                          {d.message}
                        </div>
                        <div style={{ color: tokens.color.fgMuted, fontSize: tokens.font.sizeXs, marginTop: tokens.space.xs }}>
                          Rule: {d.rule}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {validation.diagnostics.length === 0 && validation.valid && (
                  <div style={{ color: tokens.color.success, fontSize: tokens.font.sizeSm }}>
                    All schema checks passed. Draft is valid against Assembly Kernel schema.
                  </div>
                )}

                <div style={{ marginTop: tokens.space.md, fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                  Validated at: {new Date(validation.timestamp).toISOString()}
                </div>
              </>
            )}
          </div>
        )}

        {/* ─── PREVIEW TAB ───────────────────────────────────────────── */}
        {activeTab === 'preview' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: tokens.space.md }}>
              <span style={{ fontSize: tokens.font.sizeMd, fontWeight: tokens.font.weightSemibold }}>Preview / Test Output</span>
              <button onClick={handlePreview} style={btnPrimary}>Run Preview</button>
            </div>

            {!previewResult && (
              <div style={{
                padding: tokens.space.xl,
                textAlign: 'center',
                color: tokens.color.fgMuted,
                border: `1px dashed ${tokens.color.border}`,
                borderRadius: tokens.radius.md,
              }}>
                No preview run yet. Click "Run Preview/Test" to test compiler handoff.
              </div>
            )}

            {previewResult && (
              <>
                {/* Status */}
                <div style={{
                  display: 'inline-block',
                  padding: `${tokens.space.sm} ${tokens.space.lg}`,
                  borderRadius: tokens.radius.sm,
                  background: previewResult.status === 'pass' ? `${tokens.color.success}20` : `${tokens.color.error}20`,
                  color: previewResult.status === 'pass' ? tokens.color.success : tokens.color.error,
                  fontSize: tokens.font.sizeSm,
                  fontWeight: tokens.font.weightBold,
                  marginBottom: tokens.space.md,
                }}>
                  PREVIEW: {previewResult.status.toUpperCase()}
                </div>

                <div style={{ marginBottom: tokens.space.sm, fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                  Compiler Adapter: {previewResult.compilerAdapter} | Draft ID: {previewResult.draftId}
                </div>

                {/* Diagnostics */}
                {previewResult.diagnostics.map((d, i) => (
                  <div key={i} style={{
                    padding: tokens.space.sm,
                    marginBottom: tokens.space.sm,
                    background: tokens.color.bgBase,
                    borderRadius: tokens.radius.sm,
                    borderLeft: `3px solid ${previewResult.status === 'pass' ? tokens.color.success : tokens.color.error}`,
                    fontSize: tokens.font.sizeSm,
                    fontFamily: tokens.font.familyMono,
                    lineHeight: tokens.font.lineNormal,
                    color: tokens.color.fgSecondary,
                  }}>
                    {d}
                  </div>
                ))}

                {/* Canonical Payload */}
                {previewResult.payload && (
                  <div style={{ marginTop: tokens.space.lg }}>
                    <label style={labelStyle}>Canonical Assembly Draft (JSON)</label>
                    <pre style={{
                      background: tokens.color.bgBase,
                      padding: tokens.space.md,
                      borderRadius: tokens.radius.sm,
                      border: `1px solid ${tokens.color.border}`,
                      fontSize: tokens.font.sizeXs,
                      fontFamily: tokens.font.familyMono,
                      color: tokens.color.fgSecondary,
                      overflow: 'auto',
                      maxHeight: '400px',
                      lineHeight: tokens.font.lineNormal,
                    }}>
                      {JSON.stringify(previewResult.payload, null, 2)}
                    </pre>
                  </div>
                )}

                <div style={{ marginTop: tokens.space.md, fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                  Tested at: {new Date(previewResult.timestamp).toISOString()}
                </div>
              </>
            )}
          </div>
        )}

        {/* ─── SOURCE TAB ────────────────────────────────────────────── */}
        {activeTab === 'source' && (
          <div>
            <span style={{ fontSize: tokens.font.sizeMd, fontWeight: tokens.font.weightSemibold, display: 'block', marginBottom: tokens.space.md }}>
              Source Evidence / Lineage
            </span>

            {/* Lineage info */}
            {lineage && (
              <div style={sectionStyle}>
                <label style={labelStyle}>Active Source Lineage</label>
                <div style={{ display: 'grid', gridTemplateColumns: '120px 1fr', gap: tokens.space.sm, fontSize: tokens.font.sizeSm }}>
                  <span style={{ color: tokens.color.fgMuted }}>Adapter:</span>
                  <span style={{ fontFamily: tokens.font.familyMono }}>{lineage.sourceAdapter}</span>
                  <span style={{ color: tokens.color.fgMuted }}>Source File:</span>
                  <span style={{ fontFamily: tokens.font.familyMono }}>{lineage.sourceFile}</span>
                  <span style={{ color: tokens.color.fgMuted }}>Source ID:</span>
                  <span style={{ fontFamily: tokens.font.familyMono }}>{lineage.sourceId}</span>
                  <span style={{ color: tokens.color.fgMuted }}>Hydrated:</span>
                  <span style={{ fontFamily: tokens.font.familyMono }}>{new Date(lineage.hydratedAt).toISOString()}</span>
                </div>
              </div>
            )}

            {!lineage && (
              <div style={{
                padding: tokens.space.lg,
                textAlign: 'center',
                color: tokens.color.fgMuted,
                border: `1px dashed ${tokens.color.border}`,
                borderRadius: tokens.radius.md,
                marginBottom: tokens.space.md,
              }}>
                No source data loaded. Use "Hydrate Roofing" or "Hydrate Fireproofing" to load source data.
              </div>
            )}

            {/* Assembly Kernel Examples */}
            <div style={sectionStyle}>
              <label style={labelStyle}>Assembly Kernel Examples (Read-Only)</label>
              <div style={{ marginBottom: tokens.space.md }}>
                <div style={{
                  padding: tokens.space.sm,
                  background: tokens.color.bgSurface,
                  borderRadius: tokens.radius.sm,
                  marginBottom: tokens.space.sm,
                  borderLeft: `3px solid ${tokens.color.success}`,
                }}>
                  <div style={{ fontSize: tokens.font.sizeSm, fontWeight: tokens.font.weightMedium }}>{TPO_ROOF_ASSEMBLY_EXAMPLE.title}</div>
                  <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                    {TPO_ROOF_ASSEMBLY_EXAMPLE.system_id} | {TPO_ROOF_ASSEMBLY_EXAMPLE.assembly_type} | {TPO_ROOF_ASSEMBLY_EXAMPLE.layers?.length ?? 0} layers
                  </div>
                </div>
                <div style={{
                  padding: tokens.space.sm,
                  background: tokens.color.bgSurface,
                  borderRadius: tokens.radius.sm,
                  borderLeft: `3px solid ${tokens.color.warning}`,
                }}>
                  <div style={{ fontSize: tokens.font.sizeSm, fontWeight: tokens.font.weightMedium }}>{FIRE_RATED_ASSEMBLY_EXAMPLE.title}</div>
                  <div style={{ fontSize: tokens.font.sizeXs, color: tokens.color.fgMuted }}>
                    {FIRE_RATED_ASSEMBLY_EXAMPLE.record_id} | {FIRE_RATED_ASSEMBLY_EXAMPLE.test_type} | {FIRE_RATED_ASSEMBLY_EXAMPLE.result}
                  </div>
                </div>
              </div>
            </div>

            {/* ISOVER Sequences Available */}
            <div style={sectionStyle}>
              <label style={labelStyle}>ISOVER FireProtect Sequences (fire_proof_assistant — Read-Only)</label>
              {AVAILABLE_ISOVER_SEQUENCES.map((seq) => (
                <div key={seq.id} style={{
                  padding: tokens.space.sm,
                  background: tokens.color.bgSurface,
                  borderRadius: tokens.radius.sm,
                  marginBottom: tokens.space.xs,
                  fontSize: tokens.font.sizeXs,
                  fontFamily: tokens.font.familyMono,
                  color: tokens.color.fgSecondary,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}>
                  <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', flex: 1 }}>
                    {seq.data.rating} @ {seq.data.crit_temp} — {seq.data.thick_mm}mm — A/V {seq.data.max_av ?? 'N/A'}
                  </span>
                  <span style={{ color: tokens.color.fgMuted, marginLeft: tokens.space.sm, flexShrink: 0 }}>
                    {seq.data.system}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
