"""
Ingest package initializer for primary fetcher.

Expose primary fetcher functions for easy import:
from src.ingest import primary_fetcher

"""
from .primary_fetcher import (
    fetch_latest,
    fetch_round,
    validate_payload,
    compute_checksum,
    IngestError,
    NetworkError,
    HTTPError,
    JSONError,
    ValidationError,
)

__all__ = [
    "fetch_latest",
    "fetch_round",
    "validate_payload",
    "compute_checksum",
    "IngestError",
    "NetworkError",
    "HTTPError",
    "JSONError",
    "ValidationError",
]
