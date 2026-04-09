/**
 * Parapet Geometry Template
 * Generates 2D cross-section coordinates for parapet termination assemblies.
 * Origin: inside corner of deck-to-wall transition (0, 0).
 * X: horizontal (positive = toward roof field). Y: vertical (positive = up).
 */

export interface Point2D { x: number; y: number; }
export interface AnnotationAnchor { id: string; point: Point2D; label: string; leader: Point2D; }
export interface DimensionAnchor { id: string; start: Point2D; end: Point2D; value: string; axis: 'x' | 'y'; }

export interface ParapetGeometry {
  outline: Point2D[];
  layerPolygons: Record<string, Point2D[]>;
  annotationAnchors: AnnotationAnchor[];
  dimensionAnchors: DimensionAnchor[];
  boundingBox: { minX: number; minY: number; maxX: number; maxY: number };
}

export interface AssemblyLayer {
  component_id: string;
  name: string;
  position: string;
  parameters?: Record<string, unknown>;
}

export interface Assembly { components: AssemblyLayer[]; }

function getParam(layer: AssemblyLayer, key: string, fallback: number): number {
  const p = layer.parameters ?? {};
  const v = p[key];
  return typeof v === 'number' ? v : fallback;
}

export function generateParapetGeometry(assembly: Assembly): ParapetGeometry {
  const insulationMm = 100;
  const membraneThicknessMm = 8;
  const flashingHeightMm = 220;
  const parapetHeightMm = 400;
  const parapetThicknessMm = 200;
  const cantSizeMm = 50;
  const fieldWidthMm = 600;
  const deckThicknessMm = 150;

  const layers: Record<string, Point2D[]> = {};

  layers['deck'] = [
    { x: -fieldWidthMm, y: -deckThicknessMm },
    { x: 0, y: -deckThicknessMm },
    { x: 0, y: 0 },
    { x: -fieldWidthMm, y: 0 },
  ];

  layers['insulation'] = [
    { x: -fieldWidthMm, y: 0 },
    { x: 0, y: 0 },
    { x: 0, y: insulationMm },
    { x: -fieldWidthMm, y: insulationMm },
  ];

  const memTop = insulationMm + membraneThicknessMm;
  layers['membrane'] = [
    { x: -fieldWidthMm, y: insulationMm },
    { x: cantSizeMm, y: insulationMm },
    { x: cantSizeMm, y: memTop },
    { x: -fieldWidthMm, y: memTop },
  ];

  layers['cant_strip'] = [
    { x: 0, y: 0 }, { x: cantSizeMm, y: 0 },
    { x: cantSizeMm, y: insulationMm }, { x: 0, y: insulationMm },
  ];

  layers['flashing'] = [
    { x: cantSizeMm - 4, y: memTop },
    { x: cantSizeMm, y: memTop },
    { x: cantSizeMm, y: memTop + flashingHeightMm },
    { x: cantSizeMm - 4, y: memTop + flashingHeightMm },
  ];

  layers['parapet_wall'] = [
    { x: 0, y: 0 }, { x: parapetThicknessMm, y: 0 },
    { x: parapetThicknessMm, y: parapetHeightMm }, { x: 0, y: parapetHeightMm },
  ];

  const outline: Point2D[] = [
    { x: -fieldWidthMm, y: -deckThicknessMm },
    { x: parapetThicknessMm, y: -deckThicknessMm },
    { x: parapetThicknessMm, y: parapetHeightMm },
    { x: 0, y: parapetHeightMm },
    { x: 0, y: 0 },
    { x: -fieldWidthMm, y: 0 },
  ];

  const annotationAnchors: AnnotationAnchor[] = [
    { id: 'ann_flashing_height', point: { x: cantSizeMm, y: memTop + flashingHeightMm / 2 }, label: 'Min 200mm flashing height', leader: { x: 300, y: memTop + flashingHeightMm / 2 } },
    { id: 'ann_cant_strip', point: { x: cantSizeMm / 2, y: insulationMm / 2 }, label: '45° cant strip', leader: { x: 200, y: 30 } },
    { id: 'ann_termination_bar', point: { x: cantSizeMm, y: memTop + flashingHeightMm }, label: 'Termination bar + sealant', leader: { x: 300, y: memTop + flashingHeightMm + 20 } },
    { id: 'ann_membrane', point: { x: -fieldWidthMm / 2, y: (insulationMm + memTop) / 2 }, label: 'SBS cap sheet', leader: { x: -fieldWidthMm / 2, y: memTop + 40 } },
  ];

  const dimensionAnchors: DimensionAnchor[] = [
    { id: 'dim_flashing_height', start: { x: cantSizeMm + 20, y: memTop }, end: { x: cantSizeMm + 20, y: memTop + flashingHeightMm }, value: '220mm', axis: 'y' },
    { id: 'dim_insulation', start: { x: -fieldWidthMm + 20, y: 0 }, end: { x: -fieldWidthMm + 20, y: insulationMm }, value: '100mm', axis: 'y' },
    { id: 'dim_cant', start: { x: 0, y: insulationMm + 20 }, end: { x: cantSizeMm, y: insulationMm + 20 }, value: '50mm', axis: 'x' },
  ];

  return {
    outline, layerPolygons: layers, annotationAnchors, dimensionAnchors,
    boundingBox: { minX: -fieldWidthMm, minY: -deckThicknessMm, maxX: parapetThicknessMm, maxY: parapetHeightMm },
  };
}
