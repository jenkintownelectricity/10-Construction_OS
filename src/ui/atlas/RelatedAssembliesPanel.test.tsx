/**
 * Related Assemblies Panel — Tests
 *
 * Proves:
 *   - Panel renders with data-testid
 *   - Shows empty state when no assembly is selected
 *   - Shows related assemblies when assembly is selected
 *   - Related items display label, manufacturer, spec, relationship kind
 *   - Click on related item calls generationStore.setSourceContext
 *   - Click on related item calls activeObjectStore.setActiveObject
 *   - Click on related item calls eventBus.emit('object.selected')
 *   - Click on related item calls onNavigate('tools')
 *   - Click does NOT auto-generate
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { RelatedAssembliesPanel } from './RelatedAssembliesPanel';
import { generationStore } from '../stores/generationStore';
import { activeObjectStore } from '../stores/activeObjectStore';
import { eventBus } from '../events/EventBus';

beforeEach(() => {
  generationStore.clear();
  activeObjectStore.reset();
  eventBus.clear();
});

describe('RelatedAssembliesPanel — rendering', () => {
  it('renders panel with data-testid', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId={null} onNavigate={onNavigate} />);
    expect(screen.getByTestId('related-assemblies-panel')).toBeDefined();
  });

  it('shows empty state when no assembly is selected', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId={null} onNavigate={onNavigate} />);
    expect(screen.getByTestId('related-empty-state')).toBeDefined();
    expect(screen.getByText('Select a roof assembly to see related assemblies')).toBeDefined();
  });

  it('shows related assemblies for RA-001', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);
    // RA-001 is related to RA-002 (adjacent), RA-003 (down-slope), RA-004 (adjacent)
    expect(screen.getByTestId('related-item-RA-002')).toBeDefined();
    expect(screen.getByTestId('related-item-RA-003')).toBeDefined();
  });

  it('shows selected assembly header', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);
    expect(screen.getByText('Main Roof Area A')).toBeDefined();
  });

  it('shows relationship kind badge on related items', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);
    // Multiple "Adjacent" badges may exist; use getAllByText
    expect(screen.getAllByText('Adjacent').length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText('Down-Slope')).toBeDefined();
  });

  it('shows no related items for unknown assembly', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-NONEXISTENT" onNavigate={onNavigate} />);
    expect(screen.getByText('No related assemblies found')).toBeDefined();
  });
});

describe('RelatedAssembliesPanel — click behavior', () => {
  it('clicking related item sets sourceContext via generationStore', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);

    fireEvent.click(screen.getByTestId('related-item-RA-002'));

    const state = generationStore.getState();
    expect(state.sourceContext).not.toBeNull();
    expect(state.sourceContext!.submittalId).toBe('RA-002');
    expect(state.sourceContext!.manufacturer).toBe('GAF');
    expect(state.sourceContext!.spec).toBe('07 54 23');
  });

  it('clicking related item navigates to tools', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);

    fireEvent.click(screen.getByTestId('related-item-RA-002'));

    expect(onNavigate).toHaveBeenCalledWith('tools');
  });

  it('clicking related item sets activeObject', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);

    fireEvent.click(screen.getByTestId('related-item-RA-003'));

    const active = activeObjectStore.getState();
    expect(active.activeObject).toEqual({
      id: 'RA-003',
      type: 'document',
      name: 'Podium Level Roof — Plaza Deck',
    });
  });

  it('clicking related item emits object.selected event', async () => {
    const handler = vi.fn();
    eventBus.on('object.selected', handler);

    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-002" onNavigate={onNavigate} />);

    fireEvent.click(screen.getByTestId('related-item-RA-004'));

    await new Promise((r) => setTimeout(r, 20));
    expect(handler).toHaveBeenCalledWith(
      expect.objectContaining({
        object: { id: 'RA-004', type: 'document', name: 'Service Wing — Modified Bitumen' },
        source: 'explorer',
        basis: 'canonical',
      }),
    );
  });

  it('clicking related item does NOT auto-generate (requestState stays idle)', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);

    fireEvent.click(screen.getByTestId('related-item-RA-002'));

    expect(generationStore.getState().requestState.status).toBe('idle');
  });

  it('at least 2 related assembly selections set valid sourceContext', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-001" onNavigate={onNavigate} />);

    // Click RA-002
    generationStore.clear();
    fireEvent.click(screen.getByTestId('related-item-RA-002'));
    expect(generationStore.getState().sourceContext).not.toBeNull();
    expect(generationStore.getState().sourceContext!.submittalId).toBe('RA-002');

    // Click RA-003
    generationStore.clear();
    fireEvent.click(screen.getByTestId('related-item-RA-003'));
    expect(generationStore.getState().sourceContext).not.toBeNull();
    expect(generationStore.getState().sourceContext!.submittalId).toBe('RA-003');
  });
});

describe('RelatedAssembliesPanel — inverse relationship display', () => {
  it('shows Up-Slope when querying target of a down-slope edge (RA-003)', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-003" onNavigate={onNavigate} />);
    // GE-002: RA-001 → down-slope → RA-003; RA-003 should see RA-001 as Up-Slope
    // Multiple Up-Slope badges may exist; use getAllByText
    expect(screen.getAllByText('Up-Slope').length).toBeGreaterThanOrEqual(1);
  });

  it('shows Down-Slope when querying target of an up-slope edge (RA-004)', () => {
    const onNavigate = vi.fn();
    render(<RelatedAssembliesPanel selectedAssemblyId="RA-004" onNavigate={onNavigate} />);
    // GE-005: RA-003 → up-slope → RA-004; RA-004 should see RA-003 as Down-Slope
    expect(screen.getByText('Down-Slope')).toBeDefined();
  });
});
