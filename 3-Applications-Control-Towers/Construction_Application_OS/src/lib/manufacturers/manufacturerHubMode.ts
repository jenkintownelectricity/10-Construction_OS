/**
 * Manufacturer Hub — Mode Management
 * Wave 1 UI Surface
 *
 * Manages the dual-surface operational mode for the Manufacturer Hub.
 * WORK mode = light office surface for submittal/admin/review.
 * SYSTEM mode = dark visualization surface for system reasoning.
 *
 * This is NOT a simple theme toggle. It changes the cognitive posture
 * of the entire workspace surface.
 */

import type { ManufacturerHubMode } from './manufacturerHubTypes';

/** Default mode on hub entry */
export const DEFAULT_HUB_MODE: ManufacturerHubMode = 'work';

/** Mode display labels — explicitly WORK | SYSTEM, never Light | Dark */
export const MODE_LABELS: Record<ManufacturerHubMode, string> = {
  work: 'WORK',
  system: 'SYSTEM',
};

/** Mode descriptions for UI tooltips */
export const MODE_DESCRIPTIONS: Record<ManufacturerHubMode, string> = {
  work: 'Office surface — submittal review, admin, document work',
  system: 'System surface — visualization, inspection, rule reasoning',
};

/** WORK mode surface tokens (light office surface) */
export const WORK_SURFACE = {
  bg: '#f8f9fb',
  bgPanel: '#ffffff',
  bgElevated: '#f0f2f5',
  bgHover: '#e8ebf0',
  fg: '#1a1d23',
  fgSecondary: '#4a5068',
  fgMuted: '#8b93a8',
  border: '#e0e4ec',
  borderActive: '#3b82f6',
  accent: '#3b82f6',
  accentMuted: '#dbeafe',
} as const;

/** SYSTEM mode surface tokens (dark control tower surface) */
export const SYSTEM_SURFACE = {
  bg: '#0c0f15',
  bgPanel: '#121620',
  bgElevated: '#181d2a',
  bgHover: '#1e2538',
  fg: '#e0e4ec',
  fgSecondary: '#8b93a8',
  fgMuted: '#555d73',
  border: '#1e2538',
  borderActive: '#3b82f6',
  accent: '#3b82f6',
  accentMuted: '#1e3a5f',
} as const;

/** Get surface tokens for a given mode */
export function getSurfaceTokens(mode: ManufacturerHubMode) {
  return mode === 'work' ? WORK_SURFACE : SYSTEM_SURFACE;
}
