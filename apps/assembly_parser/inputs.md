# Assembly Parser Inputs

## Primary Input
- Raw manufacturer assembly letter text (plain text)

## Input Contract
- Must conform to `contracts/assembly_input.schema.json` (v0.2) after parsing
- Required fields: name, components[], constraints[], source_text

## Input Sources
- File upload (text file)
- Direct text input
- API submission
