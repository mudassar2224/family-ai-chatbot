# ================================================================
# utils/query_handler.py
# Natural Language Query Handler
#
# Responsibilities:
#   - Normalize raw user text
#   - Detect which relation is being asked about
#   - Extract the target person's name
#   - Build the appropriate Prolog query string
# ================================================================

import re
from typing import Optional, Tuple


# ----------------------------------------------------------------
# SUPPORTED RELATIONS
# Maps every keyword/phrase a user might type to the canonical
# Prolog predicate name that lives in family.pl
# ----------------------------------------------------------------
RELATION_MAP = {
    # Western basic
    "father"          : "father",
    "mother"          : "mother",
    "son"             : "son",
    "daughter"        : "daughter",
    "brother"         : "brother",
    "sister"          : "sister",

    # Extended western
    "uncle"           : "uncle",
    "aunt"            : "aunt",
    "cousin"          : "cousin",
    "nephew"          : "nephew",
    "niece"           : "niece",

    # Grandparents (western)
    "grandfather"     : "grandfather",
    "grandmother"     : "grandmother",
    "grandparent"     : "grandparent",
    "grand father"    : "grandfather",
    "grand mother"    : "grandmother",

    # Eastern relations (Urdu/cultural)
    "chacha"          : "chacha",       # father's brother
    "phoophi"         : "phoophi",      # father's sister
    "phupho"          : "phoophi",      # alternate spelling
    "maamu"           : "maamu",        # mother's brother
    "mama"            : "maamu",        # alternate spelling
    "khala"           : "khala",        # mother's sister

    # Eastern grandparents
    "dada"            : "dada",         # paternal grandfather
    "dadi"            : "dadi",         # paternal grandmother
    "nana"            : "nana",         # maternal grandfather
    "nani"            : "nani",         # maternal grandmother

    # In-laws
    "father in law"   : "father_in_law",
    "father-in-law"   : "father_in_law",
    "sasur"           : "father_in_law",
    "mother in law"   : "mother_in_law",
    "mother-in-law"   : "mother_in_law",
    "saas"            : "mother_in_law",
    "brother in law"  : "brother_in_law",
    "brother-in-law"  : "brother_in_law",
    "sister in law"   : "sister_in_law",
    "sister-in-law"   : "sister_in_law",

    # Lineage
    "ancestor"        : "ancestor",
    "descendant"      : "descendant",
    "descendents"     : "descendant",
}

# ----------------------------------------------------------------
# NOISE WORDS
# These words are stripped from the query before processing so
# they do not interfere with name/relation detection.
# ----------------------------------------------------------------
NOISE_WORDS = {
    "who", "is", "the", "of", "a", "an", "me", "tell",
    "please", "can", "you", "what", "are", "find", "show",
    "get", "give", "know", "i", "want", "to", "do",
    "could", "would", "my", "their", "his", "her",
    "let", "help", "explain", "describe", "about",
    "asking", "ask", "question", "wondering",
}

# Known family members (lowercase) for name extraction
KNOWN_NAMES = {
    "ali", "asad", "shakeel", "zain", "usman", "hamza",
    "alia", "shakeela", "zaini", "laiba", "sana", "nadia",
}


class QueryHandler:
    """
    Parses natural language family relationship queries.

    Usage:
        qh = QueryHandler()
        result = qh.parse("who is father of ali")
        # result = {"relation": "father", "person": "ali", "prolog_query": "father(X, ali)"}
    """

    def __init__(self):
        # Sort relation keys by length (longest first) so multi-word
        # relations like "father in law" are matched before "father"
        self._sorted_relations = sorted(
            RELATION_MAP.keys(), key=len, reverse=True
        )

    # ----------------------------------------------------------
    # PUBLIC API
    # ----------------------------------------------------------

    def parse(self, raw_text: str) -> dict:
        """
        Main entry point.  Accepts any natural language query and
        returns a structured result dictionary.

        Returns:
            {
                "is_relation_query": bool,
                "relation"         : str | None,
                "prolog_relation"  : str | None,
                "person"           : str | None,
                "prolog_query"     : str | None,
                "error"            : str | None,
            }
        """
        text = self._normalize(raw_text)

        # Step 1 — Detect relation
        relation_key, prolog_rel = self._detect_relation(text)
        if relation_key is None:
            return {
                "is_relation_query": False,
                "relation"         : None,
                "prolog_relation"  : None,
                "person"           : None,
                "prolog_query"     : None,
                "error"            : None,
            }

        # Step 2 — Extract person name
        person = self._extract_person(text, relation_key)
        if person is None:
            return {
                "is_relation_query": True,
                "relation"         : relation_key,
                "prolog_relation"  : prolog_rel,
                "person"           : None,
                "prolog_query"     : None,
                "error"            : "I found the relation but could not identify the person's name. Please include a name from the family tree.",
            }

        # Step 3 — Build Prolog query
        prolog_query = self._build_prolog_query(prolog_rel, person)

        return {
            "is_relation_query": True,
            "relation"         : relation_key,
            "prolog_relation"  : prolog_rel,
            "person"           : person,
            "prolog_query"     : prolog_query,
            "error"            : None,
        }

    def get_all_relations(self) -> list:
        """Return sorted list of all supported relation names."""
        return sorted(set(RELATION_MAP.values()))

    def get_known_names(self) -> list:
        """Return sorted list of all known family member names."""
        return sorted(KNOWN_NAMES)

    # ----------------------------------------------------------
    # PRIVATE HELPERS
    # ----------------------------------------------------------

    def _normalize(self, text: str) -> str:
        """
        Lowercase, strip punctuation, collapse whitespace.
        Preserve hyphens so 'father-in-law' stays intact before
        the relation detector converts it.
        """
        text = text.lower().strip()
        # Replace common punctuation (but keep hyphens for compound relations)
        text = re.sub(r"[?!.,;:\"\'()]", " ", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def _detect_relation(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Scan the normalized text for the longest matching relation key.
        Returns (relation_key, prolog_predicate) or (None, None).
        """
        for key in self._sorted_relations:
            # Build a word-boundary aware pattern
            pattern = r"\b" + re.escape(key) + r"\b"
            if re.search(pattern, text):
                return key, RELATION_MAP[key]
        return None, None

    def _extract_person(self, text: str, relation_key: str) -> Optional[str]:
        """
        Extract the target person's name from the query.

        Strategy (in order):
          1. Look for "of <name>" pattern after removing the relation.
          2. Look for any known family name in the remaining tokens.
        """
        # Remove the relation phrase from the text
        clean = re.sub(r"\b" + re.escape(relation_key) + r"\b", "", text).strip()

        # Strategy 1: "of <word>" pattern
        match = re.search(r"\bof\s+([a-z]+)\b", clean)
        if match:
            candidate = match.group(1)
            if candidate not in NOISE_WORDS:
                # Accept even unknown names (Prolog will handle it)
                return candidate

        # Strategy 2: Any remaining word that is a known family member
        tokens = clean.split()
        for token in tokens:
            if token in KNOWN_NAMES:
                return token

        # Strategy 3: Last non-noise word
        meaningful = [t for t in tokens if t not in NOISE_WORDS and len(t) > 1]
        if meaningful:
            return meaningful[-1]

        return None

    def _build_prolog_query(self, prolog_relation: str, person: str) -> str:
        """
        Build the Prolog query string.
        Pattern: relation(X, person)  — finds who has `relation` with `person`.
        E.g.: father(X, ali)  →  "Who is the father of ali?"
        """
        return f"{prolog_relation}(X, {person})"

    def format_answer(self, relation_key: str, person: str, results: list) -> str:
        """
        Format the Prolog results into a human-readable answer.

        Args:
            relation_key : e.g. "father"
            person       : e.g. "ali"
            results      : list of strings from Prolog, e.g. ["shakeel"]

        Returns:
            Human-readable string answer.
        """
        person_cap    = person.capitalize()
        relation_nice = relation_key.replace("_", "-").title()

        if not results:
            return (
                f"❌ I could not find any **{relation_nice}** for "
                f"**{person_cap}** in the family knowledge base.\n\n"
                f"Please check the name spelling or try a different relation."
            )

        if len(results) == 1:
            answer = results[0].capitalize()
            return (
                f"✅ The **{relation_nice}** of **{person_cap}** is **{answer}**."
            )

        # Multiple results
        formatted = ", ".join(r.capitalize() for r in results)
        return (
            f"✅ The **{relation_nice}** of **{person_cap}** "
            f"{'are' if len(results) > 1 else 'is'}: **{formatted}**."
        )
