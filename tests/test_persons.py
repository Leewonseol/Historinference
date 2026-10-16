"""Persons, aliases, homonym separation and unsupported attributes."""

from conftest import errors
from historinference import validate


def test_real_people_pass(tables):
    assert errors(validate.check_person_attributes(tables)) == []
    assert errors(validate.check_identity(tables)) == []


def test_no_birth_year_or_age_without_source(tables):
    for a in tables["person_attributes"]:
        assert a["attribute"] not in ("birth_year", "age", "birth_date")
        if a["attribute"] == "age_range":
            assert a["span_ids"]


def test_birth_year_injection_is_rejected(mutable):
    mutable["person_attributes"].append({"attr_id": "PA-X", "person_id": "CHOI-P03", "attribute": "birth_year", "value": "1750",
                                         "claim_status": "UNKNOWN", "time_scope": "NA", "derivation": "NA", "span_ids": "CH-S22", "note": ""})
    assert any("생년" in f.message for f in errors(validate.check_person_attributes(mutable)))


def test_unsourced_status_is_rejected(mutable):
    mutable["person_attributes"].append({"attr_id": "PA-Y", "person_id": "CHOI-P03", "attribute": "status_verified",
                                         "value": "왕족", "claim_status": "CONTESTED", "time_scope": "1786",
                                         "derivation": "DIRECT", "span_ids": "CH-S53", "note": ""})
    msgs = [f.message for f in errors(validate.check_person_attributes(mutable))]
    assert any("입증된 신분" in m for m in msgs)


def test_attribute_without_span_is_rejected(mutable):
    mutable["person_attributes"][0]["span_ids"] = ""
    assert errors(validate.check_person_attributes(mutable), "V03")


def test_lee_chamang_status_not_verified(tables):
    attrs = [a for a in tables["person_attributes"] if a["person_id"] == "CHOI-P03"]
    assert not any(a["attribute"] == "status_verified" for a in attrs)
    claimed = [a for a in attrs if a["attribute"] == "status_claimed"]
    assert claimed and claimed[0]["claim_status"] == "CONTESTED"


def test_homonyms_kept_distinct(tables):
    persons = {p["person_id"]: p for p in tables["persons"]}
    assert persons["CHOI-P05"]["name_hanja"] == "趙匡善"
    assert persons["CHOI-P06"]["name_hanja"] == "趙匡辰"
    seps = {s["sep_id"]: s for s in tables["identity_separations"]}
    assert seps["ID-01"]["decision"] == "DISTINCT"
    assert seps["ID-05"]["decision"].startswith("DISTINCT")  # 조재항 / 조재풍 no inferred kinship
    assert not any(r["rel_type"] == "KINSHIP" and {"CHO-P01", "CHO-P05"} <= {r["source_person"], r["target_person"]}
                   for r in tables["relations"])


def test_merging_distinct_people_is_detected(mutable):
    sep = next(s for s in mutable["identity_separations"] if s["sep_id"] == "ID-01")
    sep["person_b"] = sep["person_a"]
    assert any("병합" in f.message for f in errors(validate.check_identity(mutable)))


def test_alias_collision_is_detected(mutable):
    mutable["person_aliases"].append({"alias_id": "AL-X", "person_id": "CHOI-P05", "surface": "조광신", "script": "HANGUL",
                                      "alias_type": "NAME", "status": "X", "span_ids": "CH-S24"})
    assert any("동일 표기" in f.message for f in errors(validate.check_identity(mutable)))


def test_cross_case_person_reference_is_detected(mutable):
    ev = next(e for e in mutable["events"] if e["case_id"] == "YE")
    ev["actor_ids"] = "GUSUN-P01"
    assert any("다른 사건 인물" in f.message for f in errors(validate.check_identity(mutable)))


def test_king_is_case_scoped(tables):
    kings = [p for p in tables["persons"] if p["name_ko"] == "정조"]
    assert {p["person_id"] for p in kings} == {"CHOI-K", "CHO-K", "YE-K", "GUSUN-K"}


def test_gender_only_from_kinship_terms(tables):
    for a in tables["person_attributes"]:
        if a["attribute"] == "gender":
            assert a["derivation"] == "KINSHIP_TERM"
