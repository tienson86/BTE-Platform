"""Minimal import probe — no Runtime dependency code.

Usage:
    python runtime/debug_import.py
"""

from __future__ import annotations

import os
import pprint
import sys


def main() -> int:
    """Print interpreter context and try importing dateutil + pandas."""
    print("=== debug_import ===")
    print("sys.executable:", sys.executable)
    print("sys.version:", sys.version.replace("\n", " "))
    print("cwd:", os.getcwd())
    print("PYTHONPATH:", os.environ.get("PYTHONPATH"))
    print("VIRTUAL_ENV:", os.environ.get("VIRTUAL_ENV"))
    print("sys.path:")
    pprint.pp(sys.path)
    print("sys.meta_path:")
    pprint.pp([type(x).__name__ for x in sys.meta_path])

    status = 0
    for name in ("dateutil", "pandas"):
        try:
            mod = __import__(name)
            print(f"import {name}: OK file={getattr(mod, '__file__', None)}")
        except Exception as exc:
            status = 1
            print(f"import {name}: FAIL {type(exc).__name__}: {exc}")
    return status


if __name__ == "__main__":
    raise SystemExit(main())
