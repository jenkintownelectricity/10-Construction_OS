/**
 * Curb Flashing Geometry Template — 2D cross-section for equipment curb assemblies.
 * Origin: outside face of curb at deck plane (0,0).
 * X: horizontal into roof field. Y: vertical up.
 */

export interface Point2D { x: number; y: number; }
export interface AnnotationAnchor { id: string; point: Point2D; label: string; leader: Point2D; }
export interface DimensionAnchor { id: string; start: Point2D; end: Point2D; value: string; axis: 'x' | 'y'; }
export interface CurbGeometry { outline: Point2D[]; layerPolygons: Record<string, Point2D[]>; annotationAnchors: AnnotationAnchor[]; dimensionAnchors: DimensionAnchor[]; boundingBox: { minX: number; minY: number; maxX: number; maxY: number }; }
export interface AssemblyLayer { component_id: string; name: string; position: string; parameters?: Record<string, unknown>; }
export interface Assembly { components: AssemblyLayer[]; }

export function generateCurbGeometry(_assembly: Assembly): CurbGeometry {
  const fw = 500, dt = 150, ins = 100, mem = 8;
  const cW = 150, cH = 250, fH = 220, cant = 50, cfMm = 4, eqOff = 50;
  const memTop = ins + mem;
  const L: Record<string, Point2D[]> = {};

  L['deck'] = [{ x: -fw, y: -dt }, { x: 0, y: -dt }, { x: 0, y: 0 }, { x: -fw, y: 0 }];
  L['curb_framing'] = [{ x: 0, y: 0 }, { x: cW, y: 0 }, { x: cW, y: cH }, { x: 0, y: cH }];
  L['insulation'] = [{ x: -fw, y: 0 }, { x: 0, y: 0 }, { x: 0, y: ins }, { x: -fw, y: ins }];
  L['membrane'] = [{ x: -fw, y: ins }, { x: cant, y: ins }, { x: cant, y: memTop }, { x: -fw, y: memTop }];
  L['cant_strip'] = [{ x: 0, y: 0 }, { x: cant, y: 0 }, { x: cant, y: ins }, { x: 0, y: ins }];
  L['base_flashing'] = [
    { x: cant - 4, y: memTop }, { x: cant, y: memTop },
    { x: cant, y: memTop + fH }, { x: cant - 4, y: memTop + fH },
  ];
  L['counter_flashing'] = [
    { x: cant - cfMm, y: memTop + fH - 20 }, { x: cant + 40, y: memTop + fH - 20 },
    { x: cant + 40, y: memTop + fH }, { x: cant - cfMm, y: memTop + fH },
  ];
  L['equipment_support'] = [
    { x: 0, y: cH }, { x: cW + eqOff, y: cH },
    { x: cW + eqOff, y: cH + 25 }, { x: 0, y: cH + 25 },
  ];

  const outline: Point2D[] = [
    { x: -fw, y: -dt }, { x: cW, y: -dt }, { x: cW, y: cH + 25 },
    { x: 0, y: cH + 25 }, { x: 0, y: 0 }, { x: -fw, y: 0 },
  ];
  const annotationAnchors: AnnotationAnchor[] = [
    { id: 'ann_flash', point: { x: cant, y: memTop + fH / 2 }, label: 'Min 200mm base flashing', leader: { x: -200, y: memTop + fH / 2 } },
    { id: 'ann_cflash', point: { x: cant + 20, y: memTop + fH }, label: 'Counter-flashing w/ reglet', leader: { x: -150, y: memTop + fH + 20 } },
    { id: 'ann_cant', point: { x: cant / 2, y: ins / 2 }, label: '45° cant strip', leader: { x: -150, y: 20 } },
    { id: 'ann_curb', point: { x: cW / 2, y: cH / 2 }, label: `${cH}mm min curb height`, leader: { x: 350, y: cH / 2 } },
  ];
  const dimensionAnchors: DimensionAnchor[] = [
    { id: 'dim_curb', start: { x: cW + 20, y: 0 }, end: { x: cW + 20, y: cH }, value: `${cH}mm`, axis: 'y' },
    { id: 'dim_flash', start: { x: -20, y: memTop }, end: { x: -20, y: memTop + fH }, value: `${fH}mm`, axis: 'y' },
    { id: 'dim_ins', start: { x: -fw + 20, y: 0 }, end: { x: -fw + 20, y: ins }, value: `${ins}mm`, axis: 'y' },
  ];
  return {
    outline, layerPolygons: L, annotationAnchors, dimensionAnchors,
    boundingBox: { minX: -fw, minY: -dt, maxX: cW + eqOff, maxY: cH + 25 },
  };
}
