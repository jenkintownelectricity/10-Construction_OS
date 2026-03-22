/**
 * Assembly Builder — Bounded UI Vertical Slice
 * Governance: VKGL04R
 */

export { AssemblyBuilderPanel } from './AssemblyBuilderPanel';
export { validateAssemblyDraft, formStateToDraft } from './assemblyDraftValidator';
export { runPreviewTest, getCompilerIR } from './previewTestAdapter';
export { getSampleRoofingDraft, hydrateRoofingDraft } from './roofingSourceAdapter';
export { getSampleFireproofingDraft, hydrateFireproofingDraft } from './fireproofingSourceAdapter';
export { CONTROL_LAYERS, getControlLayer, CONTROL_LAYER_IDS } from './controlLayerData';
export { INTERFACE_ZONES, getInterfaceZone, INTERFACE_ZONE_IDS } from './interfaceZoneData';
export { TPO_ROOF_ASSEMBLY_EXAMPLE, FIRE_RATED_ASSEMBLY_EXAMPLE, ASSEMBLY_EXAMPLES } from './assemblyExamples';
export type {
  CanonicalAssemblyDraft,
  AssemblyDraftFormState,
  ValidationOutcome,
  PreviewTestResult,
  SourceLineage,
  FieldDiagnostic,
} from './types';
