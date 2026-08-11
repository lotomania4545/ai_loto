#!/usr/bin/env python3
"""
Primary fetcher for Loto6 from tank1159jhs/jp-lottery-api

Provides:
- fetch_latest() -> dict with raw JSON and metadata
- fetch_round(round:int) -> dict with raw JSON and metadata
- validate_payload(payload:dict) -> (normalized_dict) or raises ValidationError
- compute_checksum(raw_payload: dict) -> hex sha256 string
Exceptions:
- NetworkError, HTTPError, JSONError, ValidationError, IngestError
Uses only Python standard library.
"""
from typing import Any, Dict
import urllib.request
import urllib.error
import json
import hashlib
from datetime import datetime
import re

RAW_BASE = "https://raw.githubusercontent.com/tank1159jhs/jp-lottery-api/main/data/loto6"
LATEST_URL = f"{RAW_BASE}/latest.json"

# Exceptions
class IngestError(Exception):
    pass

class NetworkError(IngestError):
    pass

class HTTPError(IngestError):
    def __init__(self, status_code:int, message:str):
        super().__init__(f"HTTP {status_code}: {message}")
        self.status_code = status_code

class JSONError(IngestError):
    pass

class ValidationError(IngestError):
    pass

# HTTP helpers
def _http_get(url: str, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-loto-collector/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", None) or resp.getcode()
            if status is None or int(status) >= 400:
                raise HTTPError(int(status) if status is not None else -1, f"Bad status for {url}")
            data = resp.read()
            return data
    except urllib.error.HTTPError as e:
        raise HTTPError(e.code, f"{e.reason} ({url})") from e
    except urllib.error.URLError as e:
        raise NetworkError(f"Network error fetching {url}: {e}") from e
    except Exception as e:
        raise NetworkError(f"Unexpected network error fetching {url}: {e}") from e

def _parse_json_bytes(b: bytes, url: str) -> Any:
    try:
        text = b.decode("utf-8")
    except Exception as e:
        raise JSONError(f"Failed to decode response from {url}: {e}") from e
    try:
        return json.loads(text)
    except Exception as e:
        raise JSONError(f"Failed to parse JSON from {url}: {e}") from e

# Public fetch functions
def fetch_latest() -> Dict[str, Any]:
    """
    Fetch latest.json from PRIMARY.
    Returns: dict with keys: payload (parsed JSON), raw (bytes), url, retrieved_at (ISO), checksum
    Raises NetworkError/HTTPError/JSONError
    """
    url = LATEST_URL
    raw = _http_get(url)
    payload = _parse_json_bytes(raw, url)
    checksum = compute_checksum_from_bytes(raw)
    return {
        "payload": payload,
        "raw": raw,
        "url": url,
        "checksum": checksum,
        "retrieved_at": datetime.utcnow().isoformat() + "Z",
    }

def fetch_round(round_no: int) -> Dict[str, Any]:
    """
    Fetch per-round JSON data for given round number.
    """
    if not isinstance(round_no, int):
        raise ValidationError("round_no must be int")
    url = f"{RAW_BASE}/{round_no}.json"
    raw = _http_get(url)
    payload = _parse_json_bytes(raw, url)
    checksum = compute_checksum_from_bytes(raw)
    return {
        "payload": payload,
        "raw": raw,
        "url": url,
        "checksum": checksum,
        "retrieved_at": datetime.utcnow().isoformat() + "Z",
    }

# Checksum helpers
def compute_checksum_from_bytes(raw_bytes: bytes) -> str:
    h = hashlib.sha256()
    h.update(raw_bytes)
    return h.hexdigest()

def compute_checksum(raw_payload: Dict[str, Any]) -> str:
    """
    Stable JSON serialization and SHA256 hex digest.
    """
    # ensure stable ordering, no extra spaces, UTF-8 bytes
    s = json.dumps(raw_payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

# Validation & normalization
DATE_PATTERNS = ("%Y-%m-%d", "%Y/%m/%d")

def _normalize_date(date_str: str) -> str:
    if not isinstance(date_str, str):
        raise ValidationError("date must be string")
    for fmt in DATE_PATTERNS:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%Y-%m-%d")
        except Exception:
            continue
    # Do not guess ambiguous formats
    raise ValidationError("date format not recognized; expected YYYY-MM-DD or YYYY/MM/DD")

def validate_payload(raw_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate the payload structure and contents per requirements.
    Returns normalized dict:
    {
        "draw_no": int,
        "draw_date": "YYYY-MM-DD",
        "numbers": [int x6 ascending],
        "bonus": int,
        "source": "tank1159jhs/jp-lottery-api",
        "source_url": "...",
        "raw_payload": { ... }
    }
    Raises ValidationError on schema issues.
    """
    if not isinstance(raw_payload, dict):
        raise ValidationError("payload must be a JSON object")

    # type
    t = raw_payload.get("type")
    if t != "loto6":
        raise ValidationError(f'payload type must be "loto6" (got {t})')

    # round
    if "round" not in raw_payload:
        raise ValidationError("missing 'round'")
    try:
        draw_no = int(raw_payload["round"])
    except Exception:
        raise ValidationError("'round' must be integer")

    # date
    if "date" not in raw_payload:
        raise ValidationError("missing 'date'")
    draw_date = _normalize_date(raw_payload["date"])

    # numbers
    nums = raw_payload.get("numbers")
    if not isinstance(nums, list) or len(nums) != 6:
        raise ValidationError("'numbers' must be a list of 6 integers")
    normalized_nums = []
    for n in nums:
        if not isinstance(n, int):
            raise ValidationError("each number must be integer")
        if not (1 <= n <= 43):
            raise ValidationError("each number must be in range 1..43")
        normalized_nums.append(n)
    if len(set(normalized_nums)) != 6:
        raise ValidationError("numbers must not contain duplicates")
    normalized_nums_sorted = sorted(normalized_nums)

    # bonus
    if "bonus" not in raw_payload:
        raise ValidationError("missing 'bonus'")
    try:
        bonus = int(raw_payload["bonus"])
    except Exception:
        raise ValidationError("bonus must be integer")
    if not (1 <= bonus <= 43):
        raise ValidationError("bonus must be in range 1..43")
    if bonus in normalized_nums_sorted:
        raise ValidationError("bonus must not duplicate main numbers")

    normalized = {
        "draw_no": draw_no,
        "draw_date": draw_date,
        "numbers": normalized_nums_sorted,
        "bonus": bonus,
        "source": "tank1159jhs/jp-lottery-api",
        # source_url to be filled by caller (fetch functions return url)
        "source_url": None,
        "raw_payload": raw_payload,
    }
    return normalized
