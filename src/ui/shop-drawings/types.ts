/**
 * Shop Drawings Shell — Type definitions
 *
 * Presentation-shell types for the legacy OMNI-VIEW layout port.
 * No runtime, parser, or generation logic. No deprecated adapters.
 */

/** File entry in the left navigation tree */
export interface ShopDrawingFile {
  id: string;
  name: string;
  type: 'folder' | 'pdf' | 'dwg' | 'image' | 'document';
  children?: ShopDrawingFile[];
  /** Page count for PDFs */
  pageCount?: number;
  /** File size display string */
  size?: string;
}

/** Page thumbnail entry */
export interface PageThumbnail {
  pageNumber: number;
  label: string;
  isActive: boolean;
}

/** Right panel tab identifiers */
export type PropertiesPanelTab = 'properties' | 'taxonomy' | 'toolbox';

/** Viewer tool identifiers — presentation shell only, no behavior */
export type ViewerTool =
  | 'cursor' | 'pen' | 'highlighter' | 'text' | 'arrow'
  | 'rect' | 'polyline' | 'cloud' | 'callout' | 'dimension'
  | 'count' | 'stamp' | 'eraser'
  | 'snapshot' | 'redact' | 'fill' | 'format-painter';

/** Toolbar tool group */
export interface ToolGroup {
  label: string;
  tools: { id: ViewerTool; title: string; icon: string }[];
}

/** Document properties for the right panel */
export interface DocumentProperties {
  fileName: string;
  pageCount: number;
  fileSize: string;
}
