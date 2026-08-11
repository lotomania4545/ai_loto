"""
Minimal package wrapper for src.db.

Provides a convenience run() that calls init_db.
"""
from .init_db import init_db


def run(db_path: str = "data/loto6.db"):
    """Convenience wrapper to initialize DB programmatically."""
    return init_db(db_path)
