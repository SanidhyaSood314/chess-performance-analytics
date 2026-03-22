# services/analysis_cache.py

"""
Simple in-memory cache for analyzed games.

Maps PGN hash → analysis result.
"""

import hashlib
from typing import Dict, Any


class AnalysisCache:

    def __init__(self):
        self.cache: Dict[str, Any] = {}

    def _hash_pgn(self, pgn_string: str) -> str:
        """
        Generate stable hash for a PGN string.
        """
        return hashlib.md5(pgn_string.encode()).hexdigest()

    def get(self, pgn_string: str):

        key = self._hash_pgn(pgn_string)

        return self.cache.get(key)

    def set(self, pgn_string: str, analysis):

        key = self._hash_pgn(pgn_string)

        self.cache[key] = analysis


# global cache instance
analysis_cache = AnalysisCache()