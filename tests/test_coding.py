"""Step 2: codebook discipline — no 1/0 without evidence, NA preserved."""

from conftest import errors
from historinference import validate


def test_real_codes_pass(tables):
    assert errors(validate.check_coding_evidence(tables)) == []


def test_unit_level_coding_not_case_level(tables):
    unit_types = {c["unit_type"] for c in tables["mechanism_codes"]}
    assert {"EVENT", "PERSON", "CLAIM", "RELATION", "EPISODE", "DECISION"} <= unit_types
    # far more than one row per case
    for case in ("CHOI", "CHO", "YE", "GUSUN"):
        assert sum(1 for c in tables["mechanism_codes"] if c["case_id"] == case) >= 10


def test_na_is_used_for_unknowns(tables):
    na = [c for c in tables["mechanism_codes"] if c["value"] == "NA"]
    assert len(na) >= 20
    # E04 bribery in CHOI must stay NA while sources only report it as a claim
    e04 = [c for c in tables["mechanism_codes"] if c["case_id"] == "CHOI" and c["code"] == "E04"]
    assert e04 and all(c["value"] == "NA" for c in e04)


def test_zero_codes_cite_explicit_absence(tables):
    zeros = [c for c in tables["mechanism_codes"] if c["value"] == "0"]
    assert zeros, "explicit-absence codes should exist (e.g. royal finding that 김명신 was not beaten)"
    for c in zeros:
        assert c["span_ids"] and "부재 판단" in c["rationale"]


def test_one_without_evidence_is_rejected(mutable):
    mutable["mechanism_codes"][0]["span_ids"] = ""
    assert any("증거 없는" in f.message for f in errors(validate.check_coding_evidence(mutable)))


def test_zero_without_absence_rationale_is_rejected(mutable):
    row = next(c for c in mutable["mechanism_codes"] if c["value"] == "1")
    row["value"] = "0"
    assert any("부재" in f.message for f in errors(validate.check_coding_evidence(mutable)))


def test_hypothesis_status_cannot_carry_one(mutable):
    row = next(c for c in mutable["mechanism_codes"] if c["value"] == "1")
    row["claim_status"] = "HYPOTHESIS"
    assert errors(validate.check_coding_evidence(mutable), "V02")


def test_unknown_code_is_rejected(mutable):
    mutable["mechanism_codes"][0]["code"] = "E99"
    assert any("코드북" in f.message for f in errors(validate.check_coding_evidence(mutable)))


def test_cross_case_evidence_is_rejected(mutable):
    row = next(c for c in mutable["mechanism_codes"] if c["case_id"] == "YE" and c["value"] == "1")
    row["span_ids"] = "GS-F-CF046"
    assert any("다른 사건" in f.message for f in errors(validate.check_coding_evidence(mutable)))


def test_link_only_evidence_cannot_support_coding(mutable):
    mutable["source_spans"].append({"span_id": "TMP-CONTEXT", "case_id": "CHOI", "source_id": "CH-001", "carrier_id": "LOC-GUSUN-02",
                                    "evidence_grade": "CONTEXT", "offline_primary_verbatim": "NO"})
    row = next(c for c in mutable["mechanism_codes"] if c["case_id"] == "CHOI" and c["value"] == "1")
    row["span_ids"] = "TMP-CONTEXT"
    assert any("등급" in f.message for f in errors(validate.check_coding_evidence(mutable)))


def test_relation_types_have_source_time_status(tables):
    assert errors(validate.check_layers(tables)) == []
    required = {"KINSHIP", "MARRIAGE", "PATRONAGE", "BRIBERY", "COMMAND", "TESTIMONY_INFLUENCE", "INFORMATION_TRANSFER"}
    assert required <= {r["rel_type"] for r in tables["relations"]}


def test_relation_missing_time_is_rejected(mutable):
    mutable["relations"][0]["time_scope"] = ""
    assert any("시점" in f.message for f in errors(validate.check_layers(mutable)))


def test_contemporary_vs_historical_culprit_separated(tables):
    for o in tables["case_outcomes"]:
        assert o["culprit_contemporary_judgment"]
        assert not o["historical_culprit_status"].startswith("CONFIRMED")
