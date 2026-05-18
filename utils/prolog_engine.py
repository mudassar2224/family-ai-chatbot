# ================================================================
# utils/prolog_engine.py
# Prolog Reasoning Engine
#
# FIX: pyswip raises SwiPrologNotFoundError (NOT ImportError) when
#      SWI-Prolog binary is missing. We catch Exception broadly at
#      import time so the app does not crash on Streamlit Cloud.
#      The packages.txt file handles the real fix (apt install).
# ================================================================

import os
from typing import List, Optional

# ------------------------------------------------------------------
# SAFE IMPORT — pyswip raises SwiPrologNotFoundError at import time
# (not ImportError) when SWI-Prolog binary is not on the system.
# Catching broad Exception here prevents the whole app from crashing.
# ------------------------------------------------------------------
PYSWIP_AVAILABLE = False
_Prolog_class     = None

try:
    from pyswip import Prolog as _Prolog_class
    PYSWIP_AVAILABLE = True
except Exception:
    # SWI-Prolog binary not found OR pyswip not installed.
    # packages.txt will install swi-prolog on Streamlit Cloud.
    PYSWIP_AVAILABLE = False


class PrologEngine:
    """
    Wrapper around pyswip to interact with the Prolog knowledge base.

    Usage:
        engine = PrologEngine("family.pl")
        if engine.is_loaded:
            results = engine.query("father(X, ali)")
            # ['shakeel']
    """

    def __init__(self, pl_file_path: str):
        self.pl_file_path = os.path.abspath(pl_file_path)
        self.is_loaded    = False
        self.error        = None
        self._prolog      = None
        self._initialize()

    # ----------------------------------------------------------
    # PUBLIC API
    # ----------------------------------------------------------

    def query(self, query_string: str) -> List[str]:
        """
        Execute a Prolog query and return all bindings for variable X.
        Returns [] if Prolog unavailable or query fails.
        """
        if not self.is_loaded or self._prolog is None:
            return []

        results = []
        try:
            for solution in self._prolog.query(query_string):
                if "X" in solution:
                    results.append(str(solution["X"]))
        except Exception as e:
            self.error = f"Query error: {e}"
            return []

        # Deduplicate preserving order
        seen, unique = set(), []
        for r in results:
            if r not in seen:
                seen.add(r)
                unique.append(r)
        return unique

    def query_bool(self, query_string: str) -> bool:
        """Execute a boolean Prolog query (no variables)."""
        if not self.is_loaded or self._prolog is None:
            return False
        try:
            return len(list(self._prolog.query(query_string))) > 0
        except Exception:
            return False

    def get_all_members(self) -> dict:
        """Return all male/female members from the knowledge base."""
        return {
            "males"  : self.query("male(X)"),
            "females": self.query("female(X)"),
        }

    def status(self) -> str:
        if not PYSWIP_AVAILABLE:
            return (
                "❌ SWI-Prolog not found. "
                "Make sure packages.txt contains 'swi-prolog' "
                "and redeploy on Streamlit Cloud."
            )
        if not self.is_loaded:
            return f"❌ Knowledge base failed to load: {self.error}"
        return f"✅ Prolog engine loaded: {self.pl_file_path}"

    # ----------------------------------------------------------
    # PRIVATE
    # ----------------------------------------------------------

    def _initialize(self):
        if not PYSWIP_AVAILABLE:
            self.error = (
                "SWI-Prolog binary not found. "
                "On Streamlit Cloud, add 'swi-prolog' to packages.txt."
            )
            return

        if not os.path.exists(self.pl_file_path):
            self.error = f"Knowledge base file not found: {self.pl_file_path}"
            return

        try:
            self._prolog = _Prolog_class()
            safe_path    = self.pl_file_path.replace("\\", "/")
            self._prolog.consult(safe_path)
            self.is_loaded = True
        except Exception as e:
            self.error     = str(e)
            self.is_loaded = False
