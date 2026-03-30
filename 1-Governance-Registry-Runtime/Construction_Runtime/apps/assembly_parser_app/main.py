"""Assembly Parser App v0.2.

Lightweight entry point that demonstrates the assembly pipeline
with DXF, SVG, and JSON outputs.
"""

import json
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.pipeline import run_assembly_pipeline


SAMPLE_INPUT = """
Assembly: Steel Beam Connection A1

Components:
- W12x26 Steel Beam
- L4x4x1/4 Angle Bracket
- 3/4" A325 Bolts (qty 4)
- Shim Plate 1/4"

Constraint: Clearance = 1/2" minimum at beam-to-column interface
Constraint: Spacing = 3" on center for bolt pattern
Interface: Beam flange to column flange via angle bracket
Tolerance: +/- 1/16" on all dimensions
"""


def main():
    """Run the assembly parser app with sample input."""
    print("=" * 60)
    print("Construction Runtime v0.2 — Assembly Parser App")
    print("=" * 60)

    raw_input = SAMPLE_INPUT
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, "r") as f:
            raw_input = f.read()
        print(f"Input source: {input_file}")
    else:
        print("Input source: built-in sample")

    print()
    report, outputs = run_assembly_pipeline(raw_input)

    print()
    print("-" * 60)
    print("RUNTIME REPORT")
    print("-" * 60)
    print(f"Input type:        {report.input_type}")
    print(f"Validation status: {report.validation_status}")
    print(f"Actions taken:     {', '.join(report.actions_taken)}")
    print(f"Outputs generated: {', '.join(report.outputs_generated)}")
    if report.warnings:
        print(f"Warnings:          {report.warnings}")
    if report.errors:
        print(f"Errors:            {report.errors}")

    if "deliverable" in outputs:
        deliverable = outputs["deliverable"]
        print()
        print("-" * 60)
        print("DELIVERABLE")
        print("-" * 60)
        print(f"ID:      {deliverable.deliverable_id}")
        print(f"Version: {deliverable.deliverable_version}")
        for fmt_name, fmt in deliverable.formats.items():
            print(f"Format [{fmt_name}]: status={fmt.status}, size={len(fmt.content)} chars")

        print()
        print("-" * 60)
        print("JSON PREVIEW")
        print("-" * 60)
        preview = deliverable.payload.get("preview", {})
        print(json.dumps(preview, indent=2))

    if "audit_log" in outputs:
        print()
        print("-" * 60)
        print(f"AUDIT LOG ({len(outputs['audit_log'])} events)")
        print("-" * 60)
        for event in outputs["audit_log"]:
            print(f"  [{event['event_type']}] {event['stage']}: {event['message']}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()
