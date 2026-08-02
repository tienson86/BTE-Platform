"""Shared sys.path bootstrap for Runtime entrypoints.

Project root must be importable as ``runtime``, but putting the repo at
``sys.path[0]`` can shadow third-party packages if a same-named folder/file
exists. Preflight Dependency Resolver probes for that class of failure.
"""

from __future__ import annotations

import sys
from pathlib import Path


def project_root() -> Path:
    """Return the BTE repository root (parent of ``runtime/``)."""
    return Path(__file__).resolve().parents[1]


def ensure_project_root_on_sys_path() -> Path:
    """
    Ensure the repository root is on ``sys.path`` for ``import runtime``.

    Uses insert(0) so the local ``runtime`` package wins over any site
    package with the same name. Dependency preflight must detect shadowing
    of third-party import names (e.g. ``dateutil``) if they ever appear
    under the project root.
    """
    root = project_root()
    root_s = str(root)
    # Keep a single occurrence at the front.
    sys.path[:] = [p for p in sys.path if p != root_s]
    sys.path.insert(0, root_s)
    return root
