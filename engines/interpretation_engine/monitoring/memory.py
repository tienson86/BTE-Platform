"""Process memory sampler for Pack 03 monitoring.

Best-effort RSS sampling without external dependencies (no psutil/Redis).
"""

from __future__ import annotations

import logging
import sys
from datetime import datetime, timezone

from engines.interpretation_engine.monitoring.models import MemorySample

logger = logging.getLogger(__name__)


def _utc_now() -> str:
    """Return UTC ISO-8601 timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sample_memory_bytes() -> int:
    """Return best-effort current process memory usage in bytes.

    Tries Unix ``resource`` first, then Windows process counters.
    Returns ``0`` when unavailable.
    """
    try:
        import resource

        usage = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        # Linux reports KB; macOS reports bytes.
        if sys.platform == "darwin":
            return max(usage, 0)
        return max(usage * 1024, 0)
    except Exception:
        logger.debug("memory_sample_resource_unavailable", exc_info=True)

    if sys.platform == "win32":
        try:
            return _windows_working_set_bytes()
        except Exception:
            logger.debug("memory_sample_windows_unavailable", exc_info=True)

    return 0


def _windows_working_set_bytes() -> int:
    """Return Windows process working set size via ctypes."""
    import ctypes
    from ctypes import wintypes

    class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
        _fields_ = [
            ("cb", wintypes.DWORD),
            ("PageFaultCount", wintypes.DWORD),
            ("PeakWorkingSetSize", ctypes.c_size_t),
            ("WorkingSetSize", ctypes.c_size_t),
            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPagedPoolUsage", ctypes.c_size_t),
            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
            ("PagefileUsage", ctypes.c_size_t),
            ("PeakPagefileUsage", ctypes.c_size_t),
        ]

    psapi = ctypes.WinDLL("psapi")
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    get_current_process = kernel32.GetCurrentProcess
    get_current_process.restype = wintypes.HANDLE
    get_process_memory_info = psapi.GetProcessMemoryInfo
    get_process_memory_info.argtypes = [
        wintypes.HANDLE,
        ctypes.POINTER(PROCESS_MEMORY_COUNTERS),
        wintypes.DWORD,
    ]
    get_process_memory_info.restype = wintypes.BOOL

    counters = PROCESS_MEMORY_COUNTERS()
    counters.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
    ok = get_process_memory_info(
        get_current_process(),
        ctypes.byref(counters),
        counters.cb,
    )
    if not ok:
        return 0
    return int(counters.WorkingSetSize)


def sample_memory(*, source: str = "process") -> MemorySample:
    """Build a MemorySample for the current process."""
    return MemorySample(
        bytes_used=sample_memory_bytes(),
        timestamp=_utc_now(),
        source=source,
    )
