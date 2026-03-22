/**
 * SVG Detail View — Tests
 *
 * Proves:
 *   - Renders SVG content into DOM
 *   - Displays detail ID, artifact type, filename labels
 *   - SVG canvas uses white background (CADless_drawings pattern)
 *   - No generation logic, no truth ownership
 *
 * Governance: VKGL04R — Ring 2 gate proof
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { SvgDetailView } from './SvgDetailView';

const TEST_SVG = '<svg viewBox="0 0 1080 720"><rect x="10" y="10" width="100" height="50" fill="#3498db"/></svg>';

describe('SvgDetailView', () => {
  it('renders SVG content into the canvas', () => {
    render(
      <SvgDetailView
        svgContent={TEST_SVG}
        detailId="DRAFT-ROOF-SD-002"
        artifactType="roofing_detail"
        filename="DRAFT-ROOF-SD-002.dxf"
      />,
    );
    const canvas = screen.getByTestId('svg-detail-canvas');
    expect(canvas.innerHTML).toContain('<svg');
    expect(canvas.innerHTML).toContain('viewBox="0 0 1080 720"');
    expect(canvas.innerHTML).toContain('fill="#3498db"');
  });

  it('displays detail ID label', () => {
    render(
      <SvgDetailView
        svgContent={TEST_SVG}
        detailId="DRAFT-ROOF-SD-002"
        artifactType="roofing_detail"
        filename="DRAFT-ROOF-SD-002.dxf"
      />,
    );
    expect(screen.getByText('DRAFT-ROOF-SD-002')).toBeDefined();
  });

  it('displays artifact type label', () => {
    render(
      <SvgDetailView
        svgContent={TEST_SVG}
        detailId="DRAFT-ROOF-SD-002"
        artifactType="roofing_detail"
        filename="DRAFT-ROOF-SD-002.dxf"
      />,
    );
    expect(screen.getByText('roofing_detail')).toBeDefined();
  });

  it('displays filename label', () => {
    render(
      <SvgDetailView
        svgContent={TEST_SVG}
        detailId="DRAFT-ROOF-SD-002"
        artifactType="roofing_detail"
        filename="DRAFT-ROOF-SD-002.dxf"
      />,
    );
    expect(screen.getByText('DRAFT-ROOF-SD-002.dxf')).toBeDefined();
  });

  it('has svg-detail-view test ID on root', () => {
    render(
      <SvgDetailView
        svgContent={TEST_SVG}
        detailId="DRAFT-ROOF-SD-002"
        artifactType="roofing_detail"
        filename="DRAFT-ROOF-SD-002.dxf"
      />,
    );
    expect(screen.getByTestId('svg-detail-view')).toBeDefined();
  });

  it('canvas has white background for SVG display (CADless_drawings pattern)', () => {
    render(
      <SvgDetailView
        svgContent={TEST_SVG}
        detailId="D"
        artifactType="t"
        filename="f"
      />,
    );
    const canvas = screen.getByTestId('svg-detail-canvas');
    // jsdom normalizes #ffffff to rgb(255, 255, 255)
    expect(canvas.style.background).toMatch(/^(#ffffff|rgb\(255,\s*255,\s*255\))$/);
  });
});
