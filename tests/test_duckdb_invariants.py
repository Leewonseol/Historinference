"""SQL cross-check of key invariants with DuckDB (local Python/DuckDB run; not Oracle)."""

import pytest

from historinference.io import write_csv

duckdb = pytest.importorskip("duckdb")


@pytest.fixture(scope="module")
def con(tables, tmp_path_factory):
    d = tmp_path_factory.mktemp("normalized")
    c = duckdb.connect()
    for name in ("mechanism_codes", "claims", "persons", "source_spans", "decisions", "events"):
        path = d / f"{name}.csv"
        write_csv(path, tables[name])
        c.execute(f"CREATE TABLE {name} AS SELECT * FROM read_csv('{path.as_posix()}', header=true, all_varchar=true)")
    yield c
    c.close()


def test_no_binary_code_without_span(con):
    n = con.execute("SELECT count(*) FROM mechanism_codes WHERE value IN ('1','0') AND coalesce(span_ids,'') = ''").fetchone()[0]
    assert n == 0


def test_every_code_span_exists(con):
    q = """
    WITH s AS (SELECT code_row_id, unnest(string_split(span_ids, '|')) AS sp FROM mechanism_codes WHERE coalesce(span_ids,'') <> '')
    SELECT count(*) FROM s LEFT JOIN source_spans ss ON ss.span_id = s.sp WHERE ss.span_id IS NULL
    """
    assert con.execute(q).fetchone()[0] == 0


def test_person_ids_unique(con):
    assert con.execute("SELECT count(*) - count(DISTINCT person_id) FROM persons").fetchone()[0] == 0


def test_ye_two_count_claims(con):
    assert con.execute("SELECT count(*) FROM claims WHERE conflict_group = 'CG-YE-COUNT'").fetchone()[0] == 2


def test_no_executed_orders(con):
    assert con.execute("SELECT count(*) FROM decisions WHERE execution_status = 'EXECUTED'").fetchone()[0] == 0


def test_no_hypothesis_in_observed_layer(con):
    q = "SELECT count(*) FROM events WHERE layer = 'OBSERVED_ACT' AND claim_status IN ('HYPOTHESIS','UNKNOWN')"
    assert con.execute(q).fetchone()[0] == 0
