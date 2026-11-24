#!/usr/bin/env python3
"""Check plumb's C4 model against the architecture-boundaries rules.

Usage:
  check-boundaries.py [DIR ...]

DIR is a directory of LikeC4 sources — by default every feature directory under
loam-docs/features/ that holds a delta.likec4 (the archive excluded). The model is
exported with the LikeC4 CLI: `likec4` on PATH, or the path in LIKEC4_BIN.

Exit status: 0 when every relationship keeps the rules, 1 when one does not, 2 when
the model could not be read.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SYSTEM = "svc_plumb"
CONTRACT_EDGE = f"{SYSTEM}.intake.http"
OUTBOUND_ADAPTERS = ("Client",)            # suffix of a component that calls another context
OWN_ADAPTERS = ("repo", "providers")      # the store adapter, the model-provider adapter
INTAKE_ADAPTER = f"{SYSTEM}.intake.dispatcher"
MODEL_PROVIDER_ADAPTER = f"{SYSTEM}.gateway.providers"
MODEL_PORT = f"{SYSTEM}.gateway.port"


def likec4_command():
    explicit = os.environ.get("LIKEC4_BIN")
    if explicit:
        return [explicit]
    found = shutil.which("likec4")
    if found:
        return [found]
    sys.exit("check-boundaries: LikeC4 CLI not found — put `likec4` on PATH or set LIKEC4_BIN")


def export(directory):
    out = Path(tempfile.mkdtemp(prefix="plumb-c4-")) / "model.json"
    run = subprocess.run(
        likec4_command() + ["export", "json", "--skip-layout", "-o", str(out), str(directory)],
        capture_output=True, text=True,
    )
    if run.returncode != 0 or not out.exists():
        print(run.stdout[-2000:], run.stderr[-2000:], sep="\n", file=sys.stderr)
        sys.exit(f"check-boundaries: LikeC4 could not export {directory}")
    return json.loads(out.read_text())


def context_of(fqn, elements):
    """The bounded context an element belongs to, or None for an element outside plumb."""
    parts = fqn.split(".")
    if parts[0] != SYSTEM or len(parts) < 2:
        return None
    ctx = ".".join(parts[:2])
    return ctx if elements.get(ctx, {}).get("kind") == "container" else None


def leaf(fqn):
    return fqn.rsplit(".", 1)[-1]


def is_outbound_adapter(fqn):
    return fqn == INTAKE_ADAPTER or leaf(fqn).endswith(OUTBOUND_ADAPTERS)


def check(model):
    elements = model["elements"]
    violations = []
    graph = {}

    for rel in model["relations"].values():
        src, dst = rel["source"]["model"], rel["target"]["model"]
        where = f"{src} -> {dst} ({rel.get('title') or 'untitled'})"
        src_ctx, dst_ctx = context_of(src, elements), context_of(dst, elements)
        dst_kind = elements.get(dst, {}).get("kind")

        # Rule 1 — a store is touched only by its own context's repo.
        if dst_kind == "database" and not (src_ctx == dst_ctx and leaf(src) == "repo"):
            violations.append(f"rule 1 (ownership): only the owning context's repo may touch a store — {where}")

        # Rule 4 — the model provider is reached only through the gateway's provider adapters.
        if src_ctx and dst_ctx is None and src != MODEL_PROVIDER_ADAPTER:
            violations.append(f"rule 4 (model gateway): only {MODEL_PROVIDER_ADAPTER} leaves plumb — {where}")
        if dst == MODEL_PORT and leaf(src) != "modelClient":
            violations.append(f"rule 4 (model gateway): the model port is called only by a modelClient — {where}")

        # Rule 2 — external actors enter at the contract edge only.
        if src_ctx is None and dst_ctx and dst != CONTRACT_EDGE:
            violations.append(f"rule 2 (one way in): external callers enter only at {CONTRACT_EDGE} — {where}")

        if src_ctx and dst_ctx and src_ctx != dst_ctx:
            graph.setdefault(src_ctx, set()).add(dst_ctx)
            # Rule 2 — another context is entered only at its port.
            if leaf(dst) != "port":
                violations.append(f"rule 2 (one way in): enter {dst_ctx} only at its port — {where}")
            # Rule 3 — a context is left only through its adapter for the dependency.
            if not is_outbound_adapter(src):
                violations.append(f"rule 3 (one way out): leave {src_ctx} only through its client — {where}")

    # Rule 5 — context dependencies form a directed acyclic graph.
    state, stack = {}, []

    def visit(node):
        state[node] = "open"
        stack.append(node)
        for nxt in sorted(graph.get(node, ())):
            if state.get(nxt) == "open":
                cycle = stack[stack.index(nxt):] + [nxt]
                violations.append("rule 5 (direction): dependency cycle " + " -> ".join(leaf(c) for c in cycle))
            elif nxt not in state:
                visit(nxt)
        stack.pop()
        state[node] = "done"

    for node in sorted(graph):
        if node not in state:
            visit(node)

    return violations, graph


def feature_dirs(root):
    features = root / "loam-docs" / "features"
    return sorted(p.parent for p in features.glob("*/delta.likec4") if p.parent.parent.name != "archive")


def main(argv):
    root = Path(__file__).resolve().parents[4]
    dirs = [Path(a) for a in argv] or feature_dirs(root)
    if not dirs:
        sys.exit("check-boundaries: no feature directory with a delta.likec4 under loam-docs/features/")
    failed = False
    for directory in dirs:
        model = export(directory)
        violations, graph = check(model)
        contexts = sorted({c for c in graph} | {c for deps in graph.values() for c in deps})
        print(f"{directory}: {len(contexts)} contexts, {len(model['relations'])} relationships")
        for ctx in contexts:
            deps = ", ".join(leaf(d) for d in sorted(graph.get(ctx, ()))) or "—"
            print(f"  {leaf(ctx):<10} → {deps}")
        if violations:
            failed = True
            print(f"  ✗ {len(violations)} violation(s):")
            for v in violations:
                print(f"    - {v}")
        else:
            print("  ✓ every relationship keeps the boundary rules")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
