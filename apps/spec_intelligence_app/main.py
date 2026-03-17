"""Spec Intelligence App.

Lightweight entry point that demonstrates the spec intelligence pipeline.
"""

import json
import sys
import os

# Ensure project root is on path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from runtime.pipeline import run_spec_pipeline


SAMPLE_INPUT = """
Section 07 92 00 - Joint Sealants

1.1 Summary
This section includes joint sealant materials and installation for
exterior and interior applications.

1.2 Related Sections
Section 07 91 00 - Preformed Joint Seals

2.1 Products
Manufacturer: Dow Corning
Product: 795 Silicone Building Sealant
Basis of Design: Dow Corning 795

2.2 Requirements
The sealant shall comply with ASTM C920, Type S, Grade NS, Class 25.
Joint width must be minimum 1/4" and maximum 1".
Surface preparation shall be performed per manufacturer recommendations.
Primer is required on all porous substrates.

3.1 Execution
All joints must be clean, dry, and free of contaminants before application.
Backer rod is mandatory for joints deeper than 1/2".
Model No: 795-SBS
"""


def main():
    """Run the spec intelligence app with sample input."""
    print("=" * 60)
    print("Construction Runtime — Spec Intelligence App")
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
    report, outputs = run_spec_pipeline(raw_input)

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

    if "intelligence" in outputs:
        print()
        print("-" * 60)
        print("SPEC INTELLIGENCE")
        print("-" * 60)
        print(json.dumps(outputs["intelligence"], indent=2))

    print()
    print("Done.")


if __name__ == "__main__":
    main()
