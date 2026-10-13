"""Guardia de recursos: memoria del proceso, tiempo total y trabajadores.

La corrida larga anterior se cortó porque el sistema se quedó sin memoria.
Ahora el laboratorio mide su propio uso y, al pasar el límite, guarda el
checkpoint y se detiene ordenadamente (se reanuda con --resume).
"""

import os
import sys
import time


def process_rss_mb():
    """Memoria residente del proceso en MB (Windows / Linux), o None."""
    try:
        if sys.platform == "win32":
            import ctypes
            from ctypes import wintypes

            class PMC(ctypes.Structure):
                _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                            ("PeakWorkingSetSize", ctypes.c_size_t),
                            ("WorkingSetSize", ctypes.c_size_t),
                            ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                            ("QuotaPagedPoolUsage", ctypes.c_size_t),
                            ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                            ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                            ("PagefileUsage", ctypes.c_size_t),
                            ("PeakPagefileUsage", ctypes.c_size_t)]
            c = PMC()
            c.cb = ctypes.sizeof(PMC)
            k32 = ctypes.windll.kernel32
            # Firmas explícitas: sin restype el handle de 64 bits se truncaba
            # y la llamada fallaba en silencio (la guardia quedaba ciega).
            k32.GetCurrentProcess.restype = wintypes.HANDLE
            fn = ctypes.windll.psapi.GetProcessMemoryInfo
            fn.argtypes = [wintypes.HANDLE, ctypes.POINTER(PMC), wintypes.DWORD]
            fn.restype = wintypes.BOOL
            if fn(k32.GetCurrentProcess(), ctypes.byref(c), c.cb):
                return c.WorkingSetSize / 2**20
            return None
        with open("/proc/self/statm") as f:
            return int(f.read().split()[1]) * os.sysconf("SC_PAGE_SIZE") / 2**20
    except Exception:  # noqa: BLE001
        return None


def safe_workers(requested=None, reserve=1):
    n = os.cpu_count() or 2
    return max(1, min(requested or n, n - reserve))


class ResourceGuard:
    def __init__(self, max_rss_mb=1500.0, max_seconds=None, rss_fn=process_rss_mb,
                 clock=time.monotonic):
        self.max_rss_mb, self.max_seconds = max_rss_mb, max_seconds
        self.rss_fn, self.clock = rss_fn, clock
        self.start = clock()
        self.peak_rss = 0.0

    def check(self):
        """-> (ok, motivo). No lanza: el que llama decide cortar y guardar."""
        rss = self.rss_fn()
        if rss is not None:
            self.peak_rss = max(self.peak_rss, rss)
            if rss > self.max_rss_mb:
                return False, f"memoria {rss:.0f} MB > límite {self.max_rss_mb:.0f} MB"
        if self.max_seconds is not None and self.clock() - self.start > self.max_seconds:
            return False, f"tiempo > {self.max_seconds:.0f}s"
        return True, "ok"
