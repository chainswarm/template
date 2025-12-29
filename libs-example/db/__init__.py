"""
Database utilities and base patterns.

This module provides generic database patterns that can be adapted
for specific database implementations (PostgreSQL, ClickHouse, etc.).
"""
from libs.db.base import BaseRepository
from libs.db.utils import sanitize_identifier, build_insert_query

__all__ = [
    "BaseRepository",
    "sanitize_identifier",
    "build_insert_query",
]
