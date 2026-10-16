import copy
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from historinference import constraints, normalize  # noqa: E402


@pytest.fixture(scope="session")
def tables():
    """Normalized tables rebuilt from data/curated + research/ (in memory)."""
    return normalize.build_tables()


@pytest.fixture()
def mutable(tables):
    """Deep copy for defect-injection tests."""
    return copy.deepcopy(tables)


@pytest.fixture(scope="session")
def edges(tables):
    return constraints.build_partial_order(tables)


def errors(findings, check=None):
    return [f for f in findings if f.severity == "ERROR" and (check is None or f.check == check)]
