"""Lunar date strings with partial precision.

Dates are kept in the calendar of the source (almost always LUNAR). We never
convert to the solar calendar here: conversion would need an external table
that is not stored in this repository, so solar dates stay NOT_COMPUTED.

A value such as ``1785`` or ``1786-11`` denotes a whole year / month; its lower
bound is the first day and its upper bound the last day of that span.
"""

from __future__ import annotations

import re

_DATE = re.compile(r"^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$")


def parse_bounds(value: str | None) -> tuple[tuple[int, int, int], tuple[int, int, int]] | None:
    """Return ((y,m,d) lower, (y,m,d) upper) or None when unknown/unparseable."""
    if not value:
        return None
    m = _DATE.match(value.strip())
    if not m:
        return None
    year = int(m.group(1))
    month = int(m.group(2)) if m.group(2) else None
    day = int(m.group(3)) if m.group(3) else None
    if month is None:
        return (year, 1, 1), (year, 12, 30)
    if day is None:
        return (year, month, 1), (year, month, 30)
    return (year, month, day), (year, month, day)


def is_parseable(value: str | None) -> bool:
    return parse_bounds(value) is not None


def lower(value: str | None):
    b = parse_bounds(value)
    return b[0] if b else None


def upper(value: str | None):
    b = parse_bounds(value)
    return b[1] if b else None


def interval(start: str | None, end: str | None):
    """Interval (lo, hi) for an event recorded with start/end strings."""
    lo = lower(start)
    hi = upper(end) if end else upper(start)
    if lo is None and hi is None:
        return None
    return lo, hi


def strictly_before(a, b) -> bool:
    """True when interval a ends before interval b starts (definite order)."""
    if a is None or b is None or a[1] is None or b[0] is None:
        return False
    return a[1] < b[0]


def year_of(value: str | None) -> int | None:
    b = parse_bounds(value)
    return b[0][0] if b else None
