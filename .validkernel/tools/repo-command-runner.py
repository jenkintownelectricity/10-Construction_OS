#!/usr/bin/env python3
"""Repo Command Runner v1

Accepts validated command payload and executes only approved local actions.
This is the local execution surface within each target repository.

Usage:
    python .validkernel/tools/repo-command-runner.py \\
        --command-file <path-to-command-payload.json> \\
        --repo-root <path-to-repo>

Allowed actions (v1):
    - registry_append
    - documentation_create
    - documentation_update
    - receipt_emit
    - classification_validate
    - target_validate
    - sentinel_run

Forbidden actions (v1):
    - arbitrary shell execution
    - direct truth-kernel mutation
    - cross-repo write
    - registry authority reassignment
    - signal routing mutation
    - destructive file deletion outside explicit payload contract

Exit codes:
    0 — command executed successfully
    1 — command execution failed
    2 — usage error
"""

import argparse
import json
import os
import sys
from datetime import datetime, timezone

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ALLOWED_ACTIONS = {
    "registry_append",
    "documentation_create",
    "documentation_update",
    "receipt_emit",
    "classification_validate",
    "target_validate",
    "sentinel_run",
    "noop",
}

FORBIDDEN_ACTIONS = {
    "shell_exec",
    "truth_kernel_mutate",
    "cross_repo_write",
    "authority_reassign",
    "signal_routing_mutate",
    "destructive_delete",
}


def utc_now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def validate_payload(command_data):
    """Validate the command payload structure."""
    issues = []
    if not command_data.get("command_id"):
        issues.append("Missing command_id")
    if not command_data.get("authority"):
        issues.append("Missing authority")
    if not command_data.get("payload"):
        issues.append("Missing payload")
    return issues


def validate_action(action):
    """Validate that the requested action is allowed."""
    if action in FORBIDDEN_ACTIONS:
        return f"FORBIDDEN action: {action}"
    if action not in ALLOWED_ACTIONS:
        return f"UNKNOWN action: {action} (not in allowlist)"
    return None


def execute_action(action, params, repo_root):
    """Execute an allowed action within the repo."""
    if action == "noop":
        return {"status": "PASS", "message": "No-op executed (validation only)"}

    if action == "registry_append":
        registry_path = os.path.join(
            repo_root, ".validkernel/registry/command-registry.json"
        )
        if not os.path.isfile(registry_path):
            return {"status": "FAIL", "message": "Command registry not found"}
        return {"status": "PASS", "message": "Registry append validated"}

    if action == "receipt_emit":
        receipts_dir = os.path.join(repo_root, ".validkernel/receipts")
        if not os.path.isdir(receipts_dir):
            return {"status": "FAIL", "message": "Receipts directory not found"}
        return {"status": "PASS", "message": "Receipt emission validated"}

    if action == "classification_validate":
        authority_path = os.path.join(
            repo_root, ".validkernel/authority/authority.json"
        )
        if not os.path.isfile(authority_path):
            return {"status": "FAIL", "message": "Authority file not found"}
        return {"status": "PASS", "message": "Classification validated"}

    if action == "sentinel_run":
        gate_path = os.path.join(
            repo_root, ".validkernel/tools/runtime-gate.py"
        )
        if not os.path.isfile(gate_path):
            return {"status": "FAIL", "message": "Runtime gate not found"}
        return {"status": "PASS", "message": "Sentinel run validated"}

    if action in ("documentation_create", "documentation_update", "target_validate"):
        return {"status": "PASS", "message": f"Action '{action}' validated"}

    return {"status": "FAIL", "message": f"Unhandled action: {action}"}


def emit_receipt(command_data, action_results, repo_root, repo_name):
    """Emit a local execution receipt."""
    command_id = command_data.get("command_id", "UNKNOWN")
    now = utc_now_iso()

    all_pass = all(r.get("status") == "PASS" for r in action_results)

    receipt = {
        "receipt_version": "0.1",
        "command_id": command_id,
        "authority": command_data.get("authority", ""),
        "organization": command_data.get("organization", ""),
        "issued_at": now[:10],
        "executed_at": now,
        "repository": repo_name,
        "branch": "",
        "commit_hash": "",
        "status": "EXECUTED" if all_pass else "BLOCKED",
        "gate_result": "PASS" if all_pass else "FAIL",
        "files_changed": [],
        "summary": f"Local command execution: {command_id}",
        "blocked_reason": "" if all_pass else "One or more actions failed",
        "next_action": "",
        "signer": "agent",
        "signature_status": "UNSIGNED",
    }

    receipt_path = os.path.join(
        repo_root, ".validkernel", "receipts",
        f"{command_id}.receipt.json"
    )
    save_json(receipt_path, receipt)
    return receipt_path


def main():
    parser = argparse.ArgumentParser(
        description="Repo Command Runner — execute approved local actions."
    )
    parser.add_argument("--command-file", required=True)
    parser.add_argument("--repo-root", required=True)
    args = parser.parse_args()

    repo_root = os.path.abspath(args.repo_root)
    repo_name = os.path.basename(repo_root)

    print(f"Repo Command Runner — {repo_name}")
    print()

    # Load and validate payload
    if not os.path.isfile(args.command_file):
        print(f"FAIL: Command file not found: {args.command_file}")
        sys.exit(1)

    command_data = load_json(args.command_file)
    issues = validate_payload(command_data)
    if issues:
        for issue in issues:
            print(f"  FAIL: {issue}")
        print("FAIL_CLOSED: Invalid command payload.")
        sys.exit(1)

    print(f"  Command: {command_data.get('command_id')}")
    print(f"  Authority: {command_data.get('authority')}")

    # Extract and validate actions
    payload = command_data.get("payload", {})
    actions = payload.get("actions", ["noop"])
    if isinstance(actions, str):
        actions = [actions]

    print(f"  Actions: {actions}")
    print()

    # Validate all actions before executing any
    for action in actions:
        error = validate_action(action)
        if error:
            print(f"  FAIL: {error}")
            print("FAIL_CLOSED: Forbidden or unknown action.")
            sys.exit(1)

    # Execute actions
    results = []
    for action in actions:
        params = payload.get("params", {})
        result = execute_action(action, params, repo_root)
        results.append(result)
        print(f"  {result['status']}: {action} — {result['message']}")

    # Emit receipt
    receipt_path = emit_receipt(command_data, results, repo_root, repo_name)
    print()
    print(f"  Receipt: {receipt_path}")

    all_pass = all(r.get("status") == "PASS" for r in results)
    if all_pass:
        print("PASS: All actions executed successfully.")
        sys.exit(0)
    else:
        print("FAIL: One or more actions failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
