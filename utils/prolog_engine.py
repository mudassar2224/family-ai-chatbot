# ================================================================
# utils/prolog_engine.py
# Prolog Reasoning Engine
#
# Responsibilities:
#   - Load the family.pl knowledge base using pyswip
#   - Execute dynamic queries against the knowledge base
#   - Return clean Python lists of results
#   - Handle errors gracefully
# ================================================================

import os
from typing import List, Optional

try:
    from pyswip import Prolog
    PYSWIP_AVAILABLE = True
except ImportError:
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
        """
        Initialize the Prolog engine and load the knowledge base.

        Args:
            pl_file_path: Absolute or relative path to the .pl file.
        """
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
        Execute a Prolog query and return all results for variable X.

        Args:
            query_string: Prolog query, e.g. "father(X, ali)"

        Returns:
            List of string results.  Empty list if none found.
            None if Prolog is not loaded.
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

        # Remove duplicates while preserving order
        seen   = set()
        unique = []
        for r in results:
            if r not in seen:
                seen.add(r)
                unique.append(r)

        return unique

    def query_bool(self, query_string: str) -> bool:
        """
        Execute a Prolog query that returns true/false (no variables).

        Args:
            query_string: e.g. "male(ali)"

        Returns:
            True if the query succeeds, False otherwise.
        """
        if not self.is_loaded or self._prolog is None:
            return False
        try:
            results = list(self._prolog.query(query_string))
            return len(results) > 0
        except Exception:
            return False

    def get_all_members(self) -> dict:
        """
        Return all male and female family members from the knowledge base.

        Returns:
            {"males": [...], "females": [...]}
        """
        males   = self.query("male(X)")
        females = self.query("female(X)")
        return {"males": males, "females": females}

    def status(self) -> str:
        """Return a human-readable engine status string."""
        if not PYSWIP_AVAILABLE:
            return "❌ pyswip library not installed. Run: pip install pyswip"
        if not self.is_loaded:
            return f"❌ Prolog knowledge base failed to load: {self.error}"
        return f"✅ Prolog engine loaded: {self.pl_file_path}"

    # ----------------------------------------------------------
    # PRIVATE HELPERS
    # ----------------------------------------------------------

    def _initialize(self):
        """Load the Prolog knowledge base file."""
        if not PYSWIP_AVAILABLE:
            self.error = "pyswip is not installed. Install it with: pip install pyswip"
            return

        if not os.path.exists(self.pl_file_path):
            self.error = f"Knowledge base file not found: {self.pl_file_path}"
            return

        try:
            self._prolog = Prolog()
            # Use forward slashes for cross-platform compatibility
            safe_path = self.pl_file_path.replace("\\", "/")
            self._prolog.consult(safe_path)
            self.is_loaded = True
        except Exception as e:
            self.error    = str(e)
            self.is_loaded = False
