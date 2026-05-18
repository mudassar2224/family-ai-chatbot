# ================================================================
# utils/aiml_engine.py
# AIML Chatbot Engine
#
# Responsibilities:
#   - Load AIML files using python-aiml (aiml library)
#   - Respond to greetings, small talk, and generic queries
#   - Return None for queries that should go to Prolog
# ================================================================

import os
from typing import Optional

try:
    import aiml
    AIML_AVAILABLE = True
except ImportError:
    AIML_AVAILABLE = False


class AIMLEngine:
    """
    Wrapper around the python-aiml library.

    Usage:
        engine = AIMLEngine("aiml_files/")
        response = engine.respond("hello")
        # "Hello! I am the Family Relationship Chatbot..."
    """

    def __init__(self, aiml_dir: str):
        """
        Initialize the AIML engine and load all .aiml files in the directory.

        Args:
            aiml_dir: Path to the folder containing .aiml files.
        """
        self.aiml_dir  = os.path.abspath(aiml_dir)
        self.is_loaded = False
        self.error     = None
        self._kernel   = None

        self._initialize()

    # ----------------------------------------------------------
    # PUBLIC API
    # ----------------------------------------------------------

    def respond(self, user_input: str) -> Optional[str]:
        """
        Get AIML response for the given input.

        Returns:
            Response string if AIML matched, or None if no match.
        """
        if not self.is_loaded or self._kernel is None:
            return None

        response = self._kernel.respond(user_input.strip())

        # python-aiml returns empty string when no pattern matches
        if not response or response.strip() == "":
            return None

        return response.strip()

    def status(self) -> str:
        """Return a human-readable engine status string."""
        if not AIML_AVAILABLE:
            return "❌ python-aiml not installed. Run: pip install python-aiml"
        if not self.is_loaded:
            return f"❌ AIML engine failed to load: {self.error}"
        return f"✅ AIML engine loaded from: {self.aiml_dir}"

    # ----------------------------------------------------------
    # PRIVATE HELPERS
    # ----------------------------------------------------------

    def _initialize(self):
        """Load all AIML files from the specified directory."""
        if not AIML_AVAILABLE:
            self.error = "python-aiml is not installed. Install it with: pip install python-aiml"
            return

        if not os.path.isdir(self.aiml_dir):
            self.error = f"AIML directory not found: {self.aiml_dir}"
            return

        # Find all .aiml files
        aiml_files = [
            f for f in os.listdir(self.aiml_dir)
            if f.endswith(".aiml")
        ]

        if not aiml_files:
            self.error = f"No .aiml files found in: {self.aiml_dir}"
            return

        try:
            self._kernel = aiml.Kernel()
            self._kernel.setTextEncoding("utf-8")

            for filename in aiml_files:
                filepath = os.path.join(self.aiml_dir, filename)
                self._kernel.learn(filepath)

            self.is_loaded = True

        except Exception as e:
            self.error    = str(e)
            self.is_loaded = False
