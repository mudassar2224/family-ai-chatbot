# ================================================================
# utils/aiml_engine.py
# FIX: Ensure respond() always returns a plain Python str (never
#      bytes), preventing "TypeError: a bytes-like object is
#      required" when the response is used in string operations.
# ================================================================

import os
from typing import Optional

try:
    import aiml
    AIML_AVAILABLE = True
except ImportError:
    AIML_AVAILABLE = False


def _safe_str(val) -> str:
    """Convert bytes or any value to a clean Python string."""
    if isinstance(val, bytes):
        return val.decode("utf-8", errors="replace")
    return str(val) if val is not None else ""


class AIMLEngine:
    """
    Wrapper around python-aiml.

    Usage
    -----
    engine = AIMLEngine("aiml_files/")
    response = engine.respond("hello")
    """

    def __init__(self, aiml_dir: str):
        self.aiml_dir  = os.path.abspath(aiml_dir)
        self.is_loaded = False
        self.error     = None
        self._kernel   = None
        self._initialize()

    # ── Public API ─────────────────────────────────────────────

    def respond(self, user_input: str) -> Optional[str]:
        """
        Return AIML response for user_input, or None if no match.
        Always returns a plain Python str (never bytes).
        """
        if not self.is_loaded or self._kernel is None:
            return None

        try:
            raw = self._kernel.respond(_safe_str(user_input).strip())
        except Exception:
            return None

        response = _safe_str(raw).strip()
        return response if response else None

    def status(self) -> str:
        if not AIML_AVAILABLE:
            return "❌ python-aiml not installed. Run: pip install python-aiml"
        if not self.is_loaded:
            return f"❌ AIML engine failed to load: {self.error}"
        return f"✅ AIML engine loaded from: {self.aiml_dir}"

    # ── Private ────────────────────────────────────────────────

    def _initialize(self):
        if not AIML_AVAILABLE:
            self.error = "python-aiml not installed."
            return

        if not os.path.isdir(self.aiml_dir):
            self.error = f"AIML directory not found: {self.aiml_dir}"
            return

        aiml_files = [f for f in os.listdir(self.aiml_dir) if f.endswith(".aiml")]
        if not aiml_files:
            self.error = f"No .aiml files found in: {self.aiml_dir}"
            return

        try:
            self._kernel = aiml.Kernel()
            self._kernel.setTextEncoding("utf-8")
            for filename in aiml_files:
                self._kernel.learn(os.path.join(self.aiml_dir, filename))
            self.is_loaded = True
        except Exception as e:
            self.error     = str(e)
            self.is_loaded = False
