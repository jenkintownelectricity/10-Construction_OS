/**
 * Building Roof Map — Tests
 *
 * Proves:
 *   - Map renders with data-testid
 *   - SVG canvas renders with viewBox "0 0 600 400"
 *   - Building boundary is rendered
 *   - All 4 roof assembly areas are rendered
 *   - Click on area calls generationStore.setSourceContext with projected context
 *   - Click on area calls activeObjectStore.setActiveObject
 *   - Click on area calls eventBus.emit('object.selected')
 *   - Click on area calls onNavigate('tools')
 *   - Click does NOT auto-generate
 *   - Building name and level name are displayed
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { BuildingRoofMap } from './BuildingRoofMap';
import { ROOF_ASSEMBLY_OBJECTS, BUILDINGS, LEVELS } from './roofAssemblyObjects';
import { generationStore } from '../stores/generationStore';
import { activeObjectStore } from '../stores/activeObjectStore';
import { eventBus } from '../events/EventBus';

beforeEach(() => {
  generationStore.clear();
  activeObjectStore.reset();
  eventBus.clear();
});

describe('BuildingRoofMap — rendering', () => {
  it('renders map with data-testid', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);
    expect(screen.getByTestId('building-roof-map')).toBeDefined();
  });

  it('renders SVG canvas with viewBox 0 0 600 400', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);
    const canvas = screen.getByTestId('building-roof-map-canvas');
    expect(canvas.getAttribute('viewBox')).toBe('0 0 600 400');
  });

  it('renders building boundary', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);
    expect(screen.getByTestId('building-boundary')).toBeDefined();
  });

  it('renders all 4 roof assembly areas', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);
    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      expect(screen.getByTestId(`atlas-roof-area-${obj.objectId}`)).toBeDefined();
    }
  });

  it('displays building name', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);
    expect(screen.getByText(BUILDINGS[0].name)).toBeDefined();
  });

  it('displays level name and assembly count', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);
    expect(screen.getByText(`${LEVELS[0].name} — ${ROOF_ASSEMBLY_OBJECTS.length} roof assemblies`)).toBeDefined();
  });
});

describe('BuildingRoofMap — click behavior', () => {
  it('clicking area sets sourceContext via generationStore', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);

    const obj = ROOF_ASSEMBLY_OBJECTS[0];
    fireEvent.click(screen.getByTestId(`atlas-roof-area-${obj.objectId}`));

    const state = generationStore.getState();
    expect(state.sourceContext).toEqual({
      submittalId: obj.objectId,
      title: obj.areaName,
      manufacturer: obj.manufacturer,
      spec: obj.spec,
      project: obj.project,
    });
  });

  it('clicking area navigates to tools', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);

    const obj = ROOF_ASSEMBLY_OBJECTS[1];
    fireEvent.click(screen.getByTestId(`atlas-roof-area-${obj.objectId}`));

    expect(onNavigate).toHaveBeenCalledWith('tools');
  });

  it('clicking area sets activeObject', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);

    const obj = ROOF_ASSEMBLY_OBJECTS[0];
    fireEvent.click(screen.getByTestId(`atlas-roof-area-${obj.objectId}`));

    const active = activeObjectStore.getState();
    expect(active.activeObject).toEqual({
      id: obj.objectId,
      type: 'document',
      name: obj.areaName,
    });
  });

  it('clicking area emits object.selected event', async () => {
    const handler = vi.fn();
    eventBus.on('object.selected', handler);

    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);

    const obj = ROOF_ASSEMBLY_OBJECTS[2];
    fireEvent.click(screen.getByTestId(`atlas-roof-area-${obj.objectId}`));

    await new Promise((r) => setTimeout(r, 20));
    expect(handler).toHaveBeenCalledWith(
      expect.objectContaining({
        object: { id: obj.objectId, type: 'document', name: obj.areaName },
        source: 'explorer',
        basis: 'canonical',
      }),
    );
  });

  it('clicking area does NOT auto-generate (requestState stays idle)', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);

    const obj = ROOF_ASSEMBLY_OBJECTS[0];
    fireEvent.click(screen.getByTestId(`atlas-roof-area-${obj.objectId}`));

    expect(generationStore.getState().requestState.status).toBe('idle');
  });

  it('all 4 roof areas are clickable and project valid sourceContext', () => {
    const onNavigate = vi.fn();
    render(<BuildingRoofMap onNavigate={onNavigate} />);

    for (const obj of ROOF_ASSEMBLY_OBJECTS) {
      generationStore.clear();
      fireEvent.click(screen.getByTestId(`atlas-roof-area-${obj.objectId}`));

      const state = generationStore.getState();
      expect(state.sourceContext).not.toBeNull();
      expect(state.sourceContext!.submittalId).toBe(obj.objectId);
    }
    expect(onNavigate).toHaveBeenCalledTimes(ROOF_ASSEMBLY_OBJECTS.length);
  });
});
