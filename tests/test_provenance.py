"""Step 0/1: source inventory, provenance integrity, offline rule, checksums."""

import re
from pathlib import Path

from conftest import ROOT, errors
from historinference import validate
from historinference.io import read_csv, sha256_file


def test_register_and_local_documents_are_inventoried(tables):
    official = [s for s in tables["sources"] if s["is_local_carrier"] == "0"]
    local = [s for s in tables["sources"] if s["is_local_carrier"] == "1"]
    assert len(official) == len(read_csv(ROOT / "research" / "source_register.csv")) == 22
    assert len(local) == 12
    for s in local:
        assert (ROOT / s["local_path"]).exists(), s["local_path"]


def test_no_official_source_is_promoted_to_retrieved_text(tables):
    for s in tables["sources"]:
        if s["is_local_carrier"] == "0":
            assert s["offline_text_status"] == "UNAVAILABLE_SOURCE_TEXT"
            assert s["retrieval_status"] == "NOT_RETRIEVED"
            assert s["evidence_grade"] == "X"


def test_no_span_claims_verbatim_original(tables):
    assert all(s["offline_primary_verbatim"] == "NO" for s in tables["source_spans"])
    assert not any(s["evidence_grade"] == "A" for s in tables["source_spans"])


def test_source_integrity_passes_on_real_data(tables):
    assert errors(validate.check_source_integrity(tables)) == []


def test_only_approved_domains(tables):
    for s in tables["sources"]:
        if s["is_local_carrier"] == "0":
            assert s["domain_policy"] in ("APPROVED_OFFICIAL_PRIMARY", "APPROVED_INSTITUTIONAL_HOLDING"), s["source_id"]


def test_forbidden_redistribution_is_detected(mutable):
    mutable["sources"].append({**mutable["sources"][0], "source_id": "BAD-1", "url": "https://zh.wikisource.org/wiki/x",
                               "url_domain": "zh.wikisource.org"})
    assert any("비승인" in f.message for f in errors(validate.check_source_integrity(mutable)))


def test_dangling_span_reference_is_detected(mutable):
    mutable["mechanism_codes"][0]["span_ids"] = "NO-SUCH-SPAN"
    assert errors(validate.check_source_integrity(mutable), "V01")


def test_link_promoted_to_text_is_detected(mutable):
    s = next(x for x in mutable["sources"] if x["is_local_carrier"] == "0")
    s["offline_text_status"] = "FULL_TEXT"
    assert any("원문 확보" in f.message for f in errors(validate.check_source_integrity(mutable)))


def test_gusun_crosswalk_matches_register(tables):
    assert {x["register_source_id"] for x in tables["source_crosswalk"]} == {f"GS-00{i}" for i in range(1, 9)}
    assert all(x["match_basis"] == "IDENTICAL_URL" for x in tables["source_crosswalk"])


def test_imported_files_unchanged_checksums():
    pinned = read_csv(ROOT / "data" / "raw_index" / "imported_checksums.csv")
    assert len(pinned) == 7
    actual = {r["path"]: sha256_file(ROOT / r["path"]) for r in pinned}
    assert errors(validate.check_checksums({}, pinned, actual)) == []


def test_checksum_change_is_detected():
    pinned = read_csv(ROOT / "data" / "raw_index" / "imported_checksums.csv")
    actual = {r["path"]: r["sha256"] for r in pinned}
    actual[pinned[1]["path"]] = "0" * 64
    assert errors(validate.check_checksums({}, pinned, actual), "V12")


def test_gusun_import_preserves_counts(tables):
    props = [s for s in tables["source_spans"] if s["carrier_id"] == "LOC-GUSUN-05"]
    facts = [s for s in tables["source_spans"] if s["carrier_id"] == "LOC-GUSUN-01"]
    assert len(props) == 156 and len(facts) == 50
    assert len([c for c in tables["claims"] if c["claim_id"].startswith("GS-CL-")]) == 50


def test_package_has_no_network_code():
    pkg = ROOT / "historinference"
    pattern = re.compile(r"^\s*(import|from)\s+(requests|urllib\.request|http\.client|socket|httpx|aiohttp)\b", re.M)
    for path in pkg.glob("*.py"):
        assert not pattern.search(path.read_text(encoding="utf-8")), path.name


def test_pages_copy_points_to_local_data():
    from historinference.reports import pages_index_html
    html = pages_index_html((ROOT / "index.html").read_text(encoding="utf-8"))
    assert '<script src="dashboard_data.js"></script>' in html
    assert "outputs/dashboard_data.js\"></script>" not in html
