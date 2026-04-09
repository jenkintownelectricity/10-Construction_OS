/**
 * Roof Drain Geometry Template — 2D cross-section for roof drain assemblies.
 * Origin: drain centreline at finished membrane surface (0,0).
 * X: horizontal away from drain. Y: vertical up.
 */

export interface Point2D { x: number; y: number; }
export interface AnnotationAnchor { id: string; point: Point2D; label: string; leader: Point2D; }
export interface DimensionAnchor { id: string; start: Point2D; end: Point2D; value: string; axis: 'x' | 'y'; }
export interface DrainGeometry { outline: Point2D[]; layerPolygons: Record<string, Point2D[]>; annotationAnchors: AnnotationAnchor[]; dimensionAnchors: DimensionAnchor[]; boundingBox: { minX: number; minY: number; maxX: number; maxY: number }; }
export interface AssemblyLayer { component_id: string; name: string; position: string; parameters?: Record<string, unknown>; }
export interface Assembly { components: AssemblyLayer[]; }

export function generateDrainGeometry(_assembly: Assembly): DrainGeometry {
  const fw = 500, dt = 150, ins = 100, mem = 8;
  const sumpD = 50, sumpR = 125, bowlR = 75;
  const bodyR = 60, bodyD = 200, flangeH = 6, clampH = 10;
  const sumpY = ins - sumpD;
  const memTop = ins + mem;
  const L: Record<string, Point2D[]> = {};

  L['deck'] = [{ x: -fw, y: -dt }, { x: fw, y: -dt }, { x: fw, y: 0 }, { x: -fw, y: 0 }];
  L['insulation'] = [
    { x: -fw, y: 0 }, { x: -sumpR, y: 0 }, { x: -sumpR, y: sumpY },
    { x: -bowlR, y: sumpY }, { x: bowlR, y: sumpY }, { x: sumpR, y: sumpY },
    { x: sumpR, y: 0 }, { x: fw, y: 0 }, { x: fw, y: ins }, { x: -fw, y: ins },
  ];
  L['membrane'] = [
    { x: -fw, y: ins }, { x: -bowlR, y: sumpY }, { x: bowlR, y: sumpY },
    { x: fw, y: ins }, { x: fw, y: memTop }, { x: -fw, y: memTop },
  ];
  L['drain_flange'] = [
    { x: -bowlR, y: sumpY - flangeH }, { x: bowlR, y: sumpY - flangeH },
    { x: bowlR, y: sumpY }, { x: -bowlR, y: sumpY },
  ];
  L['drain_body'] = [
    { x: -bodyR, y: -dt - bodyD }, { x: bodyR, y: -dt - bodyD },
    { x: bodyR, y: sumpY - flangeH }, { x: -bodyR, y: sumpY - flangeH },
  ];
  L['clamping_ring'] = [
    { x: -bowlR, y: sumpY }, { x: bowlR, y: sumpY },
    { x: bowlR, y: sumpY + clampH }, { x: -bowlR, y: sumpY + clampH },
  ];

  const outline: Point2D[] = [
    { x: -fw, y: -dt }, { x: fw, y: -dt }, { x: fw, y: memTop }, { x: -fw, y: memTop },
  ];
  const annotationAnchors: AnnotationAnchor[] = [
    { id: 'ann_sump', point: { x: 0, y: sumpY }, label: 'Tapered insulation sump', leader: { x: -350, y: sumpY - 20 } },
    { id: 'ann_flange', point: { x: bowlR, y: sumpY - flangeH / 2 }, label: 'Cast iron drain flange', leader: { x: 300, y: sumpY } },
    { id: 'ann_clamp', point: { x: 0, y: sumpY + clampH }, label: 'Clamping ring — membrane sandwich', leader: { x: 280, y: ins } },
    { id: 'ann_slope', point: { x: -300, y: ins + 20 }, label: 'Min 1% slope to drain', leader: { x: -300, y: memTop + 15 } },
  ];
  const dimensionAnchors: DimensionAnchor[] = [
    { id: 'dim_sump', start: { x: fw + 20, y: sumpY }, end: { x: fw + 20, y: ins }, value: `${sumpD}mm sump`, axis: 'y' },
    { id: 'dim_ins', start: { x: -fw - 20, y: 0 }, end: { x: -fw - 20, y: ins }, value: `${ins}mm insul.`, axis: 'y' },
    { id: 'dim_bowl', start: { x: -bowlR, y: -20 }, end: { x: bowlR, y: -20 }, value: `${bowlR * 2}mm bowl`, axis: 'x' },
  ];
  return {
    outline, layerPolygons: L, annotationAnchors, dimensionAnchors,
    boundingBox: { minX: -fw, minY: -dt - bodyD, maxX: fw, maxY: memTop },
  };
}
