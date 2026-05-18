# ================================================================
# utils/__init__.py
# FIX: Import each engine individually inside try/except so one
#      failing engine (e.g. Prolog on first deploy) does not crash
#      the entire application at startup.
# ================================================================

from .query_handler import QueryHandler

try:
    from .prolog_engine import PrologEngine
except Exception:
    PrologEngine = None  # type: ignore

try:
    from .aiml_engine import AIMLEngine
except Exception:
    AIMLEngine = None  # type: ignore

__all__ = ["QueryHandler", "PrologEngine", "AIMLEngine"]
