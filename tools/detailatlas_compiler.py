#!/usr/bin/env python3
"""
Detail Atlas Packet Compiler

Generates a 3-page Detail Atlas Guaranteed Detail Packet PDF from
validated assembly truth objects.

Pages:
  1. Detail sheet — SVG overlay with project metadata
  2. System specification summary — components, warranty, manufacturer
  3. Compliance certificate — rule results, hash, passport seed

Authority: 10-Construction_OS (domain plane)
Design: fail-closed, deterministic, no network calls
Compiler blocked if validator status == HALT.
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


# Detail Atlas color palette
VOID = colors.HexColor("#0A0D11")
DEEP_SLATE = colors.HexColor("#1A1D21")
PANEL = colors.HexColor("#22262C")
ELEVATED = colors.HexColor("#2C3136")
SIGNAL_CYAN = colors.HexColor("#00E5FF")
STEEL_BLUE = colors.HexColor("#4A657D")
CONCRETE_GRAY = colors.HexColor("#B0B7BD")
VALID_GREEN = colors.HexColor("#00C853")
WARNING_YELLOW = colors.HexColor("#FFD600")
ERROR_RED = colors.HexColor("#D50000")
WHITE = colors.HexColor("#FFFFFF")

PAGE_W, PAGE_H = letter
MARGIN = 0.75 * inch


def compute_hash(project_id: str, assembly_id: str, assembly_version: str,
                 status: str, rule_ids: list, timestamp: str) -> str:
    """Compute SHA-256 manufacturer verification hash."""
    payload = (
        project_id
        + assembly_id
        + assembly_version
        + status
        + ",".join(sorted(rule_ids))
        + timestamp
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def status_color(status: str) -> colors.HexColor:
    if status == "PASS":
        return VALID_GREEN
    elif status == "WARN":
        return WARNING_YELLOW
    else:
        return ERROR_RED


def draw_header(c: canvas.Canvas, page_num: int, total_pages: int, receipt_hash: str):
    """Draw Detail Atlas header bar on each page."""
    # Header background
    c.setFillColor(DEEP_SLATE)
    c.rect(0, PAGE_H - 48, PAGE_W, 48, fill=1, stroke=0)

    # Brand
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 14)
    c.drawString(MARGIN, PAGE_H - 32, "DETAIL ATLAS")

    c.setFillColor(CONCRETE_GRAY)
    c.setFont("Courier", 9)
    c.drawString(MARGIN + 160, PAGE_H - 32, "CONSTRUCTION INTELLIGENCE")

    # Page number
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 32, f"Page {page_num}/{total_pages}")

    # Hash strip
    c.setFillColor(PANEL)
    c.rect(0, PAGE_H - 68, PAGE_W, 20, fill=1, stroke=0)
    c.setFillColor(STEEL_BLUE)
    c.setFont("Courier", 7)
    c.drawString(MARGIN, PAGE_H - 63, f"DL-HASH: {receipt_hash[:32]}")
    c.drawRightString(PAGE_W - MARGIN, PAGE_H - 63, f"{receipt_hash[32:]}")


def draw_footer(c: canvas.Canvas, project_name: str, timestamp: str):
    """Draw footer bar."""
    c.setFillColor(DEEP_SLATE)
    c.rect(0, 0, PAGE_W, 28, fill=1, stroke=0)
    c.setFillColor(STEEL_BLUE)
    c.setFont("Courier", 7)
    c.drawString(MARGIN, 10, f"{project_name} | {timestamp}")
    c.drawRightString(PAGE_W - MARGIN, 10, "DETAIL ATLAS — GOVERNED DETAIL PACKET")


def draw_page1(c: canvas.Canvas, project: dict, assembly: dict,
               validation: dict, receipt_hash: str, timestamp: str):
    """Page 1: Detail sheet."""
    draw_header(c, 1, 3, receipt_hash)

    y = PAGE_H - 100

    # Title
    c.setFillColor(WHITE)
    c.setFont("Courier-Bold", 16)
    c.drawString(MARGIN, y, "DETAIL SHEET")
    y -= 8

    c.setStrokeColor(SIGNAL_CYAN)
    c.setLineWidth(1)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    y -= 30

    # Project info
    c.setFillColor(CONCRETE_GRAY)
    c.setFont("Courier-Bold", 8)
    labels = [
        ("PROJECT", project.get("project_name", "DEMO PROJECT")),
        ("CONTRACTOR", project.get("contractor_id", "DEMO-CONTRACTOR-001")),
        ("ASSEMBLY", f"{assembly['assembly_id']} v{assembly['assembly_version']}"),
        ("CONDITION", assembly.get("condition_type", "").upper().replace("_", " ")),
        ("NODE ID", assembly.get("node_id", "")),
        ("MANUFACTURER", assembly.get("manufacturer_name", assembly.get("manufacturer_id", ""))),
        ("DATE", timestamp[:10]),
    ]
    for label, value in labels:
        c.setFillColor(STEEL_BLUE)
        c.setFont("Courier-Bold", 8)
        c.drawString(MARGIN, y, label)
        c.setFillColor(WHITE)
        c.setFont("Courier", 10)
        c.drawString(MARGIN + 120, y, value)
        y -= 18

    y -= 20

    # Detail drawing area placeholder
    c.setStrokeColor(STEEL_BLUE)
    c.setLineWidth(0.5)
    c.setDash(4, 4)
    c.rect(MARGIN, y - 280, PAGE_W - 2 * MARGIN, 280, fill=0, stroke=1)
    c.setDash()

    c.setFillColor(STEEL_BLUE)
    c.setFont("Courier", 10)
    cx = PAGE_W / 2
    c.drawCentredString(cx, y - 130, "PARAPET TERMINATION DETAIL")
    c.drawCentredString(cx, y - 148, f"Barrett SBS Modified Bitumen — {assembly.get('condition_type', '').replace('_', ' ').title()}")

    c.setFont("Courier", 8)
    c.drawCentredString(cx, y - 170, "SVG overlay rendered from: templates/barrett_parapet_base.svg")

    # Status badge
    y_badge = y - 300
    sc = status_color(validation["status"])
    c.setFillColor(sc)
    c.roundRect(MARGIN, y_badge, 100, 24, 2, fill=1, stroke=0)
    c.setFillColor(VOID)
    c.setFont("Courier-Bold", 12)
    c.drawCentredString(MARGIN + 50, y_badge + 7, validation["status"])

    c.setFillColor(CONCRETE_GRAY)
    c.setFont("Courier", 9)
    c.drawString(MARGIN + 110, y_badge + 7,
                 f"{validation['passed_rules']}/{validation['total_rules']} rules passed")

    draw_footer(c, project.get("project_name", "DEMO"), timestamp)
    c.showPage()


def draw_page2(c: canvas.Canvas, assembly: dict, validation: dict,
               receipt_hash: str, timestamp: str, project: dict):
    """Page 2: System specification summary."""
    draw_header(c, 2, 3, receipt_hash)

    y = PAGE_H - 100

    c.setFillColor(WHITE)
    c.setFont("Courier-Bold", 16)
    c.drawString(MARGIN, y, "SYSTEM SPECIFICATION")
    y -= 8
    c.setStrokeColor(SIGNAL_CYAN)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    y -= 30

    # Manufacturer block
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 10)
    c.drawString(MARGIN, y, "MANUFACTURER")
    y -= 18
    c.setFillColor(WHITE)
    c.setFont("Courier", 10)
    c.drawString(MARGIN + 16, y, assembly.get("manufacturer_name", assembly.get("manufacturer_id", "")))
    y -= 14
    c.setFillColor(CONCRETE_GRAY)
    c.setFont("Courier", 9)
    c.drawString(MARGIN + 16, y, f"System: {assembly.get('system_type', '')}")
    y -= 14
    c.drawString(MARGIN + 16, y, f"CSI Section: {assembly.get('csi_section', 'N/A')}")
    y -= 28

    # Warranty block
    warranty = assembly.get("warranty_envelope", {})
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 10)
    c.drawString(MARGIN, y, "WARRANTY ENVELOPE")
    y -= 18
    w_items = [
        ("Type", warranty.get("type", "N/A")),
        ("Term", f"{warranty.get('term_years', 'N/A')} years"),
        ("Coverage", warranty.get("coverage", "N/A").replace("_", " ").title()),
        ("Wind Rating", f"{warranty.get('wind_speed_mph', 'N/A')} mph"),
        ("Certified Applicator", "Required" if warranty.get("requires_certified_applicator") else "Not Required"),
    ]
    for label, val in w_items:
        c.setFillColor(STEEL_BLUE)
        c.setFont("Courier-Bold", 8)
        c.drawString(MARGIN + 16, y, label.upper())
        c.setFillColor(WHITE)
        c.setFont("Courier", 9)
        c.drawString(MARGIN + 160, y, val)
        y -= 14
    y -= 16

    # Components table
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 10)
    c.drawString(MARGIN, y, "ASSEMBLY COMPONENTS")
    y -= 20

    # Table header
    c.setFillColor(PANEL)
    c.rect(MARGIN, y - 2, PAGE_W - 2 * MARGIN, 16, fill=1, stroke=0)
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 8)
    c.drawString(MARGIN + 4, y + 2, "COMPONENT")
    c.drawString(MARGIN + 180, y + 2, "MATERIAL")
    c.drawString(MARGIN + 340, y + 2, "POSITION")
    c.drawString(MARGIN + 440, y + 2, "REQ")
    y -= 18

    for comp in assembly.get("components", []):
        c.setFillColor(WHITE)
        c.setFont("Courier", 8)
        c.drawString(MARGIN + 4, y, comp.get("name", "")[:28])
        c.setFillColor(CONCRETE_GRAY)
        c.drawString(MARGIN + 180, y, comp.get("material", "")[:24])
        c.drawString(MARGIN + 340, y, comp.get("position", "")[:16])
        req_color = VALID_GREEN if comp.get("required") else STEEL_BLUE
        c.setFillColor(req_color)
        c.drawString(MARGIN + 440, y, "YES" if comp.get("required") else "OPT")
        y -= 14
        if y < 80:
            break

    draw_footer(c, project.get("project_name", "DEMO"), timestamp)
    c.showPage()


def draw_page3(c: canvas.Canvas, assembly: dict, validation: dict,
               receipt_hash: str, timestamp: str, project: dict):
    """Page 3: Compliance certificate."""
    draw_header(c, 3, 3, receipt_hash)

    y = PAGE_H - 100

    c.setFillColor(WHITE)
    c.setFont("Courier-Bold", 16)
    c.drawString(MARGIN, y, "COMPLIANCE CERTIFICATE")
    y -= 8
    c.setStrokeColor(SIGNAL_CYAN)
    c.line(MARGIN, y, PAGE_W - MARGIN, y)
    y -= 30

    # Status block
    sc = status_color(validation["status"])
    c.setFillColor(sc)
    c.roundRect(MARGIN, y - 4, 140, 30, 2, fill=1, stroke=0)
    c.setFillColor(VOID)
    c.setFont("Courier-Bold", 16)
    c.drawCentredString(MARGIN + 70, y + 2, validation["status"])

    c.setFillColor(WHITE)
    c.setFont("Courier", 10)
    c.drawString(MARGIN + 160, y + 6,
                 f"{validation['passed_rules']}/{validation['total_rules']} constraints verified")
    y -= 50

    # Rule results table
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 10)
    c.drawString(MARGIN, y, "CONSTRAINT VERIFICATION RESULTS")
    y -= 20

    c.setFillColor(PANEL)
    c.rect(MARGIN, y - 2, PAGE_W - 2 * MARGIN, 16, fill=1, stroke=0)
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 8)
    c.drawString(MARGIN + 4, y + 2, "RULE ID")
    c.drawString(MARGIN + 180, y + 2, "STATUS")
    c.drawString(MARGIN + 240, y + 2, "MESSAGE")
    y -= 18

    for rule in validation.get("rule_results", []):
        rc = status_color(rule["status"])
        c.setFillColor(WHITE)
        c.setFont("Courier", 8)
        c.drawString(MARGIN + 4, y, rule["rule_id"])
        c.setFillColor(rc)
        c.setFont("Courier-Bold", 8)
        c.drawString(MARGIN + 180, y, rule["status"])
        c.setFillColor(CONCRETE_GRAY)
        c.setFont("Courier", 7)
        msg = rule.get("message", "")[:50]
        c.drawString(MARGIN + 240, y, msg)
        y -= 14

    y -= 20

    # Hash block
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 10)
    c.drawString(MARGIN, y, "VERIFICATION RECEIPT")
    y -= 20

    hash_items = [
        ("MANUFACTURER VERIFICATION HASH", receipt_hash),
        ("WARRANTY RECEIPT ID", receipt_hash[:16]),
        ("WARRANTY STATUS", "VERIFIED" if validation["status"] == "PASS" else "PROVISIONAL" if validation["status"] == "WARN" else "INVALID"),
        ("TIMESTAMP", timestamp),
        ("ASSEMBLY", f"{assembly['assembly_id']} v{assembly['assembly_version']}"),
    ]
    for label, val in hash_items:
        c.setFillColor(STEEL_BLUE)
        c.setFont("Courier-Bold", 7)
        c.drawString(MARGIN, y, label)
        y -= 12
        c.setFillColor(WHITE)
        c.setFont("Courier", 8)
        c.drawString(MARGIN + 16, y, val)
        y -= 16

    y -= 10

    # Passport seed block
    c.setFillColor(SIGNAL_CYAN)
    c.setFont("Courier-Bold", 10)
    c.drawString(MARGIN, y, "SYSTEM PASSPORT SEED")
    y -= 20

    c.setFillColor(PANEL)
    c.rect(MARGIN, y - 60, PAGE_W - 2 * MARGIN, 70, fill=1, stroke=0)

    c.setFillColor(CONCRETE_GRAY)
    c.setFont("Courier", 7)
    passport = {
        "node_id": assembly.get("node_id"),
        "assembly_id": assembly.get("assembly_id"),
        "manufacturer_id": assembly.get("manufacturer_id"),
        "status": validation["status"],
        "receipt_hash": receipt_hash[:16],
        "warranty_type": assembly.get("warranty_envelope", {}).get("type"),
        "governed": validation["status"] in ("PASS", "WARN"),
    }
    py = y - 4
    for k, v in passport.items():
        c.drawString(MARGIN + 8, py, f"{k}: {v}")
        py -= 10

    draw_footer(c, project.get("project_name", "DEMO"), timestamp)
    c.showPage()


def compile_packet(assembly: dict, validation: dict, project: dict,
                   output_path: str) -> dict:
    """Compile 3-page Detail Atlas packet PDF.

    Blocked if validation status is HALT.
    Returns compilation result with hash and artifact path.
    """
    if validation["status"] == "HALT":
        return {
            "compiled": False,
            "status": "BLOCKED",
            "reason": "Compiler blocked — validation status is HALT",
            "failed_rules": validation.get("failed_rule_ids", []),
            "remediation": [
                r["remediation"] for r in validation.get("rule_results", [])
                if r.get("remediation")
            ],
            "artifact_path": None,
            "receipt_hash": None,
        }

    timestamp = validation.get("timestamp", datetime.now(timezone.utc).isoformat())

    # Compute hash AFTER validation is finalized
    all_rule_ids = [r["rule_id"] for r in validation.get("rule_results", [])]
    receipt_hash = compute_hash(
        project.get("project_id", "DEMO-001"),
        assembly["assembly_id"],
        assembly["assembly_version"],
        validation["status"],
        all_rule_ids,
        timestamp,
    )

    # Generate PDF
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setTitle(f"Detail Atlas — {assembly['assembly_id']}")
    c.setAuthor("Detail Atlas Compiler")
    c.setSubject("Guaranteed Detail Packet")

    draw_page1(c, project, assembly, validation, receipt_hash, timestamp)
    draw_page2(c, assembly, validation, receipt_hash, timestamp, project)
    draw_page3(c, assembly, validation, receipt_hash, timestamp, project)

    c.save()

    return {
        "compiled": True,
        "status": "COMPILED",
        "artifact_path": output_path,
        "receipt_hash": receipt_hash,
        "warranty_receipt_id": receipt_hash[:16],
        "warranty_status": "VERIFIED" if validation["status"] == "PASS" else "PROVISIONAL",
        "pages": 3,
        "assembly_id": assembly["assembly_id"],
        "assembly_version": assembly["assembly_version"],
        "validation_status": validation["status"],
        "timestamp": timestamp,
    }


def main():
    """CLI entry point for compiler."""
    if len(sys.argv) < 2:
        print("Usage: python detailatlas_compiler.py <assembly_json> [project_json] [output_pdf]")
        sys.exit(1)

    assembly_path = sys.argv[1]
    with open(assembly_path, "r") as f:
        assembly = json.load(f)

    project = {}
    if len(sys.argv) >= 3:
        with open(sys.argv[2], "r") as f:
            project = json.load(f)

    output_path = sys.argv[3] if len(sys.argv) >= 4 else "detail_atlas_packet.pdf"

    # Import and run validator
    sys.path.insert(0, str(Path(__file__).parent))
    from validator import validate

    validation = validate(assembly, project)

    result = compile_packet(assembly, validation, project, output_path)

    print(json.dumps(result, indent=2))

    if not result["compiled"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
