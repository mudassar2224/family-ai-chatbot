# ================================================================
# utils/__init__.py
# Each engine is wrapped in its own try/except so one failing
# import (e.g. Prolog on cold start) does not crash the whole app.
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
