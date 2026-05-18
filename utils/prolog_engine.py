# ================================================================
# utils/prolog_engine.py
# FIXES applied:
#   1. Catch Exception (not just ImportError) for SwiPrologNotFoundError
#   2. safe_val() converts bytes/Atom objects to plain Python str
#      → fixes "TypeError: a bytes-like object is required" on Python 3.12
# ================================================================

import os
from typing import List

# ------------------------------------------------------------------
# SAFE IMPORT
# pyswip raises SwiPrologNotFoundError (a custom Exception, NOT
# ImportError) when the SWI-Prolog binary is missing on the system.
# Catching broad Exception keeps the app alive until packages.txt
# installs swi-prolog on Streamlit Cloud.
# ------------------------------------------------------------------
PYSWIP_AVAILABLE = False
_Prolog          = None

try:
    from pyswip import Prolog as _Prolog
    PYSWIP_AVAILABLE = True
except Exception:
    PYSWIP_AVAILABLE = False


def _safe_val(val) -> str:
    """
    Convert any pyswip result to a clean Python string.

    pyswip 0.3.x may return:
      - str       (older versions)
      - bytes     (newer versions on Linux/Python 3.12)
      - Atom      (pyswip wrapper object with a .chars attribute)
    All cases are handled here to avoid TypeError downstream.
    """
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    if hasattr(val, "chars"):           # pyswip Atom object
        return str(val.chars)
    if hasattr(val, "value"):           # pyswip Term object
        return str(val.value)
    return str(val)


class PrologEngine:
    """
    Wrapper around pyswip for the family.pl knowledge base.

    Usage
    -----
    engine = PrologEngine("family.pl")
    if engine.is_loaded:
        print(engine.query("father(X, ali)"))   # ['shakeel']
    """

    def __init__(self, pl_file_path: str):
        self.pl_file_path = os.path.abspath(pl_file_path)
        self.is_loaded    = False
        self.error        = None
        self._prolog      = None
        self._initialize()

    # ── Public API ─────────────────────────────────────────────

    def query(self, query_string: str) -> List[str]:
        """
        Run a Prolog query and return all bindings for variable X.
        Always returns a list of plain Python strings.
        """
        if not self.is_loaded or self._prolog is None:
            return []

        results = []
        try:
            for solution in self._prolog.query(query_string):
                if "X" in solution:
                    results.append(_safe_val(solution["X"]))
        except Exception as e:
            self.error = f"Query error: {e}"
            return []

        # Remove duplicates while preserving order
        seen, unique = set(), []
        for r in results:
            if r not in seen:
                seen.add(r)
                unique.append(r)
        return unique

    def query_bool(self, query_string: str) -> bool:
        """Boolean Prolog query — returns True if any solution exists."""
        if not self.is_loaded or self._prolog is None:
            return False
        try:
            return len(list(self._prolog.query(query_string))) > 0
        except Exception:
            return False

    def get_all_members(self) -> dict:
        return {
            "males"  : self.query("male(X)"),
            "females": self.query("female(X)"),
        }

    def status(self) -> str:
        if not PYSWIP_AVAILABLE:
            return (
                "❌ SWI-Prolog not found on this system. "
                "Add 'swi-prolog' to packages.txt for Streamlit Cloud."
            )
        if not self.is_loaded:
            return f"❌ Knowledge base failed to load: {self.error}"
        return f"✅ Prolog engine loaded: {self.pl_file_path}"

    # ── Private ────────────────────────────────────────────────

    def _initialize(self):
        if not PYSWIP_AVAILABLE:
            self.error = (
                "SWI-Prolog binary not found. "
                "Add 'swi-prolog' to packages.txt on Streamlit Cloud."
            )
            return

        if not os.path.exists(self.pl_file_path):
            self.error = f"Knowledge base file not found: {self.pl_file_path}"
            return

        try:
            self._prolog = _Prolog()
            safe_path    = self.pl_file_path.replace("\\", "/")
            self._prolog.consult(safe_path)
            self.is_loaded = True
        except Exception as e:
            self.error     = str(e)
            self.is_loaded = False
