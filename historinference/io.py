"""Small CSV / hashing helpers (stdlib only)."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "research"
CURATED = ROOT / "data" / "curated"
NORMALIZED = ROOT / "data" / "normalized"
RAW_INDEX = ROOT / "data" / "raw_index"
AUDIT = ROOT / "data" / "audit"
MODELS = ROOT / "models"
OUTPUTS = ROOT / "outputs"
DOCS = ROOT / "docs"
CONFIG = ROOT / "config"

MULTI_SEP = "|"
NA = "NA"


def read_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [dict(row) for row in csv.DictReader(fh)]


def write_csv(path: Path, rows: list[dict], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="raise", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({k: _cell(row.get(k, "")) for k in fieldnames})


def _cell(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (list, tuple, set)):
        return MULTI_SEP.join(str(v) for v in value)
    return str(value)


def split(value: str | None) -> list[str]:
    """Split a multi-valued cell; empty and NA give an empty list."""
    if value is None:
        return []
    value = value.strip()
    if not value or value == NA:
        return []
    return [part.strip() for part in value.split(MULTI_SEP) if part.strip()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2, sort_keys=False)
        fh.write("\n")


def rel(path: Path) -> str:
    return str(path.resolve().relative_to(ROOT))
