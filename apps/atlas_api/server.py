"""Atlas API Server — FastAPI endpoints for graph navigation and artifact rendering.

Serves:
  GET  /api/graph          — full graph data for Atlas UI
  GET  /api/graph/nodes    — nodes filtered by type
  GET  /api/graph/node/:id — single node with connected data
  POST /api/render         — trigger rendering for a detail
  GET  /api/artifacts      — list stored artifacts
  GET  /api/artifacts/:id  — download artifact file
  POST /api/pipeline       — run full condition->render pipeline
  GET  /health             — health check

All data is read-only relative to kernel. Runtime generates artifacts only.
"""

import os
import json
import uuid
from typing import Any
from pathlib import Path

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

# Runtime imports
from runtime.condition_graph.condition_graph_builder import ConditionGraphBuilder
from runtime.detail_resolver.detail_resolution_engine import resolve_details
from runtime.detail_variants.variant_generator import (
    generate_variant,
    DETAIL_CONDITION_MAP,
    CONDITION_PARAMETERS,
    CANONICAL_DETAIL_FAMILIES,
)
from runtime.installation_sequence.sequence_engine import generate_sequence
from runtime.artifact_renderer.renderer_pipeline import render_artifacts
from runtime.artifact_renderer.artifact_contract import RenderManifest
from runtime.artifact_renderer.pipeline_integration import (
    build_detail_dna,
    run_full_render_pipeline,
    store_artifact,
)

ARTIFACTS_DIR = os.environ.get("ARTIFACTS_DIR", "artifacts")
PORT = int(os.environ.get("ATLAS_API_PORT", "8100"))


def build_graph_data() -> dict[str, Any]:
    """Build the full graph data from runtime state.

    Scans artifacts dir and builds graph from resolved details.
    """
    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    edge_counter = 0

    # Load pipeline result if available
    result_path = os.path.join(ARTIFACTS_DIR, "pipeline_result.json")
    pipeline_result = None
    if os.path.isfile(result_path):
        with open(result_path) as f:
            pipeline_result = json.load(f)

    if pipeline_result:
        # Build condition nodes from resolved details
        for item in pipeline_result.get("resolved_details", []):
            cond_ref = item.get("condition_ref", "")
            canonical_id = item.get("canonical_detail_id", "")
            condition = DETAIL_CONDITION_MAP.get(canonical_id, "")

            # Condition node
            if cond_ref:
                nodes.append({
                    "id": cond_ref,
                    "type": "condition",
                    "label": f"{condition} Condition",
                    "data": {
                        "condition_id": cond_ref,
                        "condition_type": condition,
                        "severity": "major",
                        "status": "resolved",
                        "detail_refs": [canonical_id],
                    },
                })

            # Detail node
            detail_node_id = f"detail-{canonical_id}"
            seq_data = None
            for seq in pipeline_result.get("sequences", []):
                if seq.get("detail_ref") == canonical_id:
                    seq_data = seq
                    break

            # Find SVG artifact for preview
            svg_preview = ""
            for art in pipeline_result.get("stored_artifacts", []):
                if art.get("source_detail_id") == canonical_id and art.get("format") == "SVG":
                    svg_path = art.get("filepath", "")
                    if os.path.isfile(svg_path):
                        with open(svg_path) as f:
                            svg_preview = f.read()
                    break

            # Find variants
            variants = []
            for v in pipeline_result.get("variants", []):
                if v.get("canonical_detail_id") == canonical_id:
                    variants.append({
                        "variant_id": v.get("variant_id", ""),
                        "parameters": v.get("parameters", {}),
                        "description": f"Variant of {canonical_id}",
                    })

            # Installation sequence
            install_seq = []
            if seq_data and seq_data.get("steps"):
                install_seq = [s.get("action", "") for s in seq_data["steps"]]

            nodes.append({
                "id": detail_node_id,
                "type": "detail",
                "label": canonical_id.replace("-", " ").title()[:50],
                "data": {
                    "detail_id": canonical_id,
                    "display_name": canonical_id.replace("-", " ").title(),
                    "assembly_family": condition.lower() if condition else "",
                    "tags": [t.lower() for t in canonical_id.split("-") if len(t) > 2],
                    "variants": variants,
                    "installation_sequence": install_seq,
                    "svg_preview": svg_preview,
                },
            })

            # Assembly node
            asm_node_id = f"asm-{condition.lower()}"
            if not any(n["id"] == asm_node_id for n in nodes):
                nodes.append({
                    "id": asm_node_id,
                    "type": "assembly",
                    "label": f"{condition.title()} Assembly",
                    "data": {
                        "assembly_id": asm_node_id,
                        "assembly_name": f"{condition.title()} Assembly System",
                        "system": "roofing",
                        "class": condition.lower(),
                        "components": [],
                    },
                })

            # Edges: condition -> detail -> assembly
            if cond_ref:
                edge_counter += 1
                edges.append({
                    "id": f"e{edge_counter}",
                    "source": cond_ref,
                    "target": detail_node_id,
                    "type": "resolves_to",
                    "label": "resolves",
                })

            edge_counter += 1
            edges.append({
                "id": f"e{edge_counter}",
                "source": detail_node_id,
                "target": asm_node_id,
                "type": "belongs_to",
                "label": "assembly",
            })

            # Artifact nodes + edges
            for art in pipeline_result.get("stored_artifacts", []):
                if art.get("source_detail_id") == canonical_id:
                    art_node_id = f"art-{art['artifact_id']}"
                    nodes.append({
                        "id": art_node_id,
                        "type": "artifact",
                        "label": f"{canonical_id[:30]} {art['format']}",
                        "data": {
                            "artifact_id": art["artifact_id"],
                            "format": art["format"],
                            "content_hash": art.get("content_hash", ""),
                            "source_detail_id": canonical_id,
                            "source_manifest_id": "",
                            "renderer_id": art.get("renderer_id", ""),
                            "download_url": f"/api/artifacts/{art['filename']}",
                            "filename": art["filename"],
                            "file_size": art.get("file_size", 0),
                        },
                    })
                    edge_counter += 1
                    edges.append({
                        "id": f"e{edge_counter}",
                        "source": detail_node_id,
                        "target": art_node_id,
                        "type": "produces",
                        "label": art["format"],
                    })

    return {"nodes": nodes, "edges": edges}


class AtlasAPIHandler(BaseHTTPRequestHandler):
    """HTTP request handler for Atlas API."""

    def _send_json(self, data: Any, status: int = 200) -> None:
        body = json.dumps(data, indent=2, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, filepath: str, content_type: str) -> None:
        if not os.path.isfile(filepath):
            self._send_json({"error": "File not found"}, 404)
            return
        with open(filepath, "rb") as f:
            content = f.read()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Disposition", f"attachment; filename={os.path.basename(filepath)}")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/health":
            self._send_json({"status": "ok", "service": "atlas-api", "wave": "18+19"})

        elif path == "/api/graph":
            graph = build_graph_data()
            self._send_json(graph)

        elif path == "/api/graph/nodes":
            graph = build_graph_data()
            node_type = params.get("type", [None])[0]
            nodes = graph["nodes"]
            if node_type:
                nodes = [n for n in nodes if n["type"] == node_type]
            self._send_json({"nodes": nodes})

        elif path.startswith("/api/graph/node/"):
            node_id = path[len("/api/graph/node/"):]
            graph = build_graph_data()
            node = next((n for n in graph["nodes"] if n["id"] == node_id), None)
            if node:
                connected = [
                    e for e in graph["edges"]
                    if e["source"] == node_id or e["target"] == node_id
                ]
                self._send_json({"node": node, "edges": connected})
            else:
                self._send_json({"error": "Node not found"}, 404)

        elif path == "/api/artifacts":
            artifacts = []
            if os.path.isdir(ARTIFACTS_DIR):
                for fname in sorted(os.listdir(ARTIFACTS_DIR)):
                    if fname.endswith((".dxf", ".svg", ".pdf")):
                        fpath = os.path.join(ARTIFACTS_DIR, fname)
                        artifacts.append({
                            "filename": fname,
                            "format": fname.rsplit(".", 1)[-1].upper(),
                            "file_size": os.path.getsize(fpath),
                            "download_url": f"/api/artifacts/{fname}",
                        })
            self._send_json({"artifacts": artifacts})

        elif path.startswith("/api/artifacts/"):
            filename = path[len("/api/artifacts/"):]
            filepath = os.path.join(ARTIFACTS_DIR, filename)
            content_types = {
                ".dxf": "application/dxf",
                ".svg": "image/svg+xml",
                ".pdf": "application/pdf",
            }
            ext = os.path.splitext(filename)[1]
            self._send_file(filepath, content_types.get(ext, "application/octet-stream"))

        elif path == "/api/details":
            details = []
            for detail_id in sorted(CANONICAL_DETAIL_FAMILIES):
                condition = DETAIL_CONDITION_MAP.get(detail_id, "")
                details.append({
                    "detail_id": detail_id,
                    "condition": condition,
                    "display_name": detail_id.replace("-", " ").title(),
                    "allowed_params": CONDITION_PARAMETERS.get(condition, []),
                })
            self._send_json({"details": details})

        else:
            self._send_json({"error": "Not found", "path": path}, 404)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length > 0 else {}

        if path == "/api/render":
            detail_id = body.get("detail_id", "")
            if not detail_id:
                self._send_json({"error": "detail_id required"}, 400)
                return

            formats = body.get("formats", ["DXF", "SVG", "PDF"])
            variant_params = body.get("variant_params", {})

            detail_dna = build_detail_dna(detail_id)
            manifest = RenderManifest(
                manifest_id=f"MAN-{uuid.uuid4().hex[:8]}",
                detail_id=detail_id,
                instruction_set_id=f"IS-{detail_id}",
                requested_formats=formats,
                metadata={"display_name": detail_dna["display_name"]},
            )

            result = render_artifacts(manifest, detail_dna, variant_params or None)

            stored = []
            if result.success:
                os.makedirs(ARTIFACTS_DIR, exist_ok=True)
                for artifact in result.artifacts:
                    stored.append(store_artifact(artifact, ARTIFACTS_DIR))

            self._send_json({
                "success": result.success,
                "artifacts": stored,
                "errors": result.errors,
                "lineage": result.lineage,
            })

        elif path == "/api/pipeline":
            # Build condition graph from request body
            nodes_spec = body.get("nodes", [])
            edges_spec = body.get("edges", [])
            material = body.get("material_context")
            formats = body.get("formats", ["DXF", "SVG", "PDF"])

            if not nodes_spec:
                # Default: build a sample condition graph
                builder = ConditionGraphBuilder("project-demo", ["demo-input"])
                builder.add_node("N1", "PARAPET", "North Parapet", material_context="EPDM")
                builder.add_node("N2", "PIPE_PENETRATION", "Vent Pipe A", material_context="EPDM")
                builder.add_node("N3", "DRAIN", "Roof Drain 1", material_context="TPO")
                builder.add_node("N4", "ROOF_FIELD", "Main Roof Area")
                builder.add_edge("N4", "N3", "drains_to")
                builder.add_edge("N2", "N4", "penetrates")
                condition_graph = builder.build()
            else:
                builder = ConditionGraphBuilder(
                    body.get("graph_id", f"graph-{uuid.uuid4().hex[:6]}"),
                )
                for n in nodes_spec:
                    builder.add_node(
                        n["node_id"], n["condition_type"], n.get("label", ""),
                        material_context=n.get("material_context"),
                    )
                for e in edges_spec:
                    builder.add_edge(e["source"], e["target"], e["edge_type"])
                condition_graph = builder.build()

            result = run_full_render_pipeline(
                condition_graph,
                material_context=material,
                output_dir=ARTIFACTS_DIR,
                requested_formats=formats,
            )

            self._send_json(result)

        else:
            self._send_json({"error": "Not found"}, 404)

    def log_message(self, format, *args):
        """Quiet logging."""
        pass


def main():
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    server = HTTPServer(("0.0.0.0", PORT), AtlasAPIHandler)
    print(f"Atlas API server running on http://localhost:{PORT}")
    print(f"  GET  /health")
    print(f"  GET  /api/graph")
    print(f"  GET  /api/artifacts")
    print(f"  GET  /api/details")
    print(f"  POST /api/render")
    print(f"  POST /api/pipeline")
    print(f"Artifacts dir: {os.path.abspath(ARTIFACTS_DIR)}")
    server.serve_forever()


if __name__ == "__main__":
    main()
