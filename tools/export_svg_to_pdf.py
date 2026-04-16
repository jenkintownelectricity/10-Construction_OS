#!/usr/bin/env python3
"""
export_svg_to_pdf.py — Barrett PMMA / Fireproofing SVG-to-PDF Packet Compiler

Converts PRINT_STANDARD SVG detail sheets into a combined PDF packet.
Uses svglib + reportlab for conversion.

Usage:
    python3 tools/export_svg_to_pdf.py --input output/barrett_pmma_packet/print/ \
                                        --output output/barrett_pmma_packet/client/Barrett_PMMA_Detail_Packet_v1.pdf

    python3 tools/export_svg_to_pdf.py --input output/fireproofing_packet/print/ \
                                        --output output/fireproofing_packet/client/Fireproofing_Starter_Packet_v1.pdf

Requirements:
    pip install svglib reportlab cairosvg
"""

import argparse
import os
import sys
from pathlib import Path

def convert_with_cairosvg(svg_files, output_pdf):
    """Convert SVGs to PDF using cairosvg (higher fidelity)."""
    import cairosvg
    from io import BytesIO

    pdf_pages = []
    for svg_path in svg_files:
        print(f"  Converting: {os.path.basename(svg_path)}")
        pdf_bytes = cairosvg.svg2pdf(url=str(svg_path))
        pdf_pages.append(pdf_bytes)

    if not pdf_pages:
        print("ERROR: No SVG files converted.")
        return False

    # If only one page, write directly
    if len(pdf_pages) == 1:
        with open(output_pdf, 'wb') as f:
            f.write(pdf_pages[0])
        return True

    # For multiple pages, try PyPDF merger
    try:
        from reportlab.lib.pagesizes import TABLOID, landscape
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader

        # Write individual PDFs then merge
        temp_dir = Path(output_pdf).parent / "_temp_pages"
        temp_dir.mkdir(exist_ok=True)
        temp_files = []

        for i, pdf_bytes in enumerate(pdf_pages):
            temp_path = temp_dir / f"page_{i:02d}.pdf"
            with open(temp_path, 'wb') as f:
                f.write(pdf_bytes)
            temp_files.append(str(temp_path))

        # Use simple concatenation via reportlab
        merge_pdfs(temp_files, output_pdf)

        # Cleanup
        for tf in temp_files:
            os.remove(tf)
        temp_dir.rmdir()
        return True

    except Exception as e:
        print(f"  Multi-page merge failed ({e}), writing first page only")
        with open(output_pdf, 'wb') as f:
            f.write(pdf_pages[0])
        # Also write individual PDFs
        for i, pdf_bytes in enumerate(pdf_pages):
            individual = output_pdf.replace('.pdf', f'_page_{i+1:02d}.pdf')
            with open(individual, 'wb') as f:
                f.write(pdf_bytes)
        return True


def merge_pdfs(pdf_files, output_path):
    """Merge multiple PDF files into one."""
    try:
        # Try PyPDF2 first
        from PyPDF2 import PdfMerger
        merger = PdfMerger()
        for pdf_file in pdf_files:
            merger.append(pdf_file)
        merger.write(output_path)
        merger.close()
    except ImportError:
        try:
            # Fallback: use reportlab to read and combine
            from reportlab.lib.pagesizes import TABLOID, landscape
            from reportlab.pdfgen import canvas as pdf_canvas
            import subprocess

            # Use ghostscript if available
            gs_cmd = ['gs', '-dBATCH', '-dNOPAUSE', '-q', '-sDEVICE=pdfwrite',
                      f'-sOutputFile={output_path}'] + pdf_files
            result = subprocess.run(gs_cmd, capture_output=True)
            if result.returncode != 0:
                raise Exception("Ghostscript not available")
        except Exception:
            # Last resort: just copy first file and write individuals
            import shutil
            shutil.copy(pdf_files[0], output_path)
            print(f"  Warning: Could not merge PDFs. Individual page PDFs written.")
            for i, pf in enumerate(pdf_files):
                dest = output_path.replace('.pdf', f'_page_{i+1:02d}.pdf')
                shutil.copy(pf, dest)


def convert_with_svglib(svg_files, output_pdf):
    """Convert SVGs to PDF using svglib + reportlab."""
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    from reportlab.lib.pagesizes import TABLOID, landscape
    from reportlab.pdfgen import canvas

    page_width, page_height = landscape(TABLOID)  # 17x11 inches
    c = canvas.Canvas(output_pdf, pagesize=landscape(TABLOID))

    for i, svg_path in enumerate(svg_files):
        print(f"  Converting: {os.path.basename(svg_path)}")
        try:
            drawing = svg2rlg(str(svg_path))
            if drawing is None:
                print(f"    WARNING: Could not parse {svg_path}, skipping")
                continue

            # Scale to fit page with margins
            margin = 36  # 0.5 inch margins
            available_w = page_width - 2 * margin
            available_h = page_height - 2 * margin
            scale_x = available_w / drawing.width
            scale_y = available_h / drawing.height
            scale = min(scale_x, scale_y)

            drawing.width *= scale
            drawing.height *= scale
            drawing.scale(scale, scale)

            renderPDF.draw(drawing, c, margin, margin)
            c.showPage()
        except Exception as e:
            print(f"    ERROR converting {svg_path}: {e}")
            continue

    c.save()
    return True


def main():
    parser = argparse.ArgumentParser(description='Convert SVG detail sheets to PDF packet')
    parser.add_argument('--input', '-i', required=True, help='Directory containing SVG files')
    parser.add_argument('--output', '-o', required=True, help='Output PDF file path')
    parser.add_argument('--engine', '-e', default='cairosvg', choices=['cairosvg', 'svglib'],
                        help='Conversion engine (default: cairosvg)')
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_path = Path(args.output)

    if not input_dir.is_dir():
        print(f"ERROR: Input directory not found: {input_dir}")
        sys.exit(1)

    # Find SVG files, sorted by name
    svg_files = sorted(input_dir.glob('*.svg'))
    if not svg_files:
        print(f"ERROR: No SVG files found in {input_dir}")
        sys.exit(1)

    print(f"Found {len(svg_files)} SVG files in {input_dir}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if args.engine == 'cairosvg':
        success = convert_with_cairosvg(svg_files, str(output_path))
    else:
        success = convert_with_svglib(svg_files, str(output_path))

    if success and output_path.exists():
        size_kb = output_path.stat().st_size / 1024
        print(f"\nSUCCESS: PDF written to {output_path} ({size_kb:.1f} KB)")
    else:
        print(f"\nFAILED: Could not generate PDF")
        sys.exit(1)


if __name__ == '__main__':
    main()
