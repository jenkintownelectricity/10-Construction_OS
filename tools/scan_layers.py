import json
from pathlib import Path
from collections import defaultdict

INPUT_DIR = Path("source/barrett/json")

layer_counts = defaultdict(int)
files_using_layer = defaultdict(set)

for file in INPUT_DIR.rglob("*.json"):

    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    for e in data.get("entities", []):
        layer = e.get("layer", "UNKNOWN")

        layer_counts[layer] += 1
        files_using_layer[layer].add(file.name)

print("\n===== BARRETT LAYER INVENTORY =====\n")

for layer, count in sorted(layer_counts.items(), key=lambda x: -x[1]):

    print(f"{layer}")
    print(f"  entities: {count}")
    print(f"  files: {len(files_using_layer[layer])}")
    print()