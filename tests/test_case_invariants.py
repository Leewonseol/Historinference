"""Interpretive guard-rails for the four cases (CLAUDE.md step 3)."""

from conftest import errors
from historinference import validate


def test_invariants_pass(tables):
    assert errors(validate.check_case_invariants(tables)) == []
    assert errors(validate.check_case_separation(tables)) == []
    assert errors(validate.check_layers(tables)) == []


def test_choi_1787_conclusion_is_contested_by_1789(tables):
    claims = {c["claim_id"]: c for c in tables["claims"]}
    assert claims["CL-CH-04"]["claim_status"] == "CONTESTED"
    assert "1789" in claims["CL-CH-04"]["truth_status"]
    dec = {d["decision_id"]: d for d in tables["decisions"]}
    assert dec["DC-CH-08"]["decision_type"] == "PENALTY_APPROVAL"  # not acquittal, not execution


def test_choi_1787_conclusion_promoted_is_detected(mutable):
    c = next(x for x in mutable["claims"] if x["claim_id"] == "CL-CH-04")
    c["claim_status"] = "OFFICIAL_JUDGMENT"
    assert errors(validate.check_case_invariants(mutable), "V11")


def test_cho_accuser_is_not_coded_as_killer(tables):
    outcome = next(o for o in tables["case_outcomes"] if o["case_id"] == "CHO")
    assert outcome["historical_culprit_status"].startswith("UNKNOWN")
    rels = [r for r in tables["relations"] if r["source_person"] == "CHO-P03" and r["target_person"] == "CHO-P02"]
    assert all(r["rel_type"] == "KINSHIP" for r in rels)
    collusion = next(r for r in tables["relations"] if r["rel_id"] == "RL-CHO-07")
    assert collusion["claim_status"] == "UNKNOWN"


def test_ye_counts_preserved_separately(tables):
    counts = [c for c in tables["claims"] if c["conflict_group"] == "CG-YE-COUNT"]
    assert {c["claim_id"] for c in counts} == {"CL-YE-03", "CL-YE-04"}
    assert "31" in counts[0]["proposition"] or "31" in counts[1]["proposition"]
    assert all(c["contradicts"] for c in counts)


def test_ye_count_merge_is_detected(mutable):
    mutable["claims"] = [c for c in mutable["claims"] if c["claim_id"] != "CL-YE-04"]
    c = next(x for x in mutable["claims"] if x["claim_id"] == "CL-YE-03")
    c["proposition"] = "사망자는 31명 또는 25명(평균 28명)"
    msgs = [f.message for f in errors(validate.check_case_invariants(mutable))]
    assert any("31" in m for m in msgs)


def test_ye_1801_event_is_not_fused(mutable):
    mutable["events"].append({**mutable["events"][0], "event_id": "EV-YE-99", "case_id": "YE", "date_start": "1801", "date_end": "1801",
                              "actor_ids": "YE-P01", "target_ids": "NA", "span_ids": "YE-S09"})
    assert any("1801" in f.message for f in errors(validate.check_case_separation(mutable)))


def test_gusun_death_causation_unresolved(tables):
    outcome = next(o for o in tables["case_outcomes"] if o["case_id"] == "GUSUN")
    assert outcome["historical_culprit_status"] == "UNRESOLVED_DIRECT_CAUSATION"
    death = next(e for e in tables["events"] if e["event_id"] == "EV-GS-09")
    assert "인과" in death["note"] and death["actor_ids"] == "NA"


def test_no_deliberate_collusion_coded(tables):
    assert not any(c["fault_type"] == "DELIBERATE_COLLUSION" for c in tables["mechanism_codes"])


def test_deliberate_collusion_injection_is_detected(mutable):
    row = next(c for c in mutable["mechanism_codes"] if c["code"] == "E05" and c["value"] == "1")
    row["fault_type"] = "DELIBERATE_COLLUSION"
    assert errors(validate.check_case_invariants(mutable), "V11")


def test_same_date_cases_do_not_share_people_or_spans(tables):
    ye_people = {p for e in tables["events"] if e["case_id"] == "YE" for p in (e["actor_ids"] + "|" + e["target_ids"]).split("|")}
    assert not any(p.startswith("GUSUN-") for p in ye_people)
    ye_spans = {s for e in tables["events"] if e["case_id"] == "YE" for s in e["span_ids"].split("|")}
    assert not any(s.startswith("GS-") for s in ye_spans)


def test_hypothesis_in_observed_layer_is_detected(mutable):
    ev = next(e for e in mutable["events"] if e["layer"] == "OBSERVED_ACT")
    ev["claim_status"] = "HYPOTHESIS"
    assert any("관측 층" in f.message for f in errors(validate.check_layers(mutable)))


def test_hypotheses_only_from_in_source_doubts(tables):
    atts = {a["att_id"]: a for a in tables["attestations"]}
    for c in tables["claims"]:
        if c["claim_status"] == "HYPOTHESIS":
            assert atts[c["att_id"]]["att_mode"] == "ROYAL_DOUBT"


def test_out_of_scope_case_rows_are_detected(mutable):
    mutable["claims"].append({**mutable["claims"][0], "claim_id": "CL-X", "case_id": "YE1801_HWANG"})
    assert errors(validate.check_case_separation(mutable), "V10")
